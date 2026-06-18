# AI Incident Assistant - Deep Dive Questions & Answers

---

# 1. Why did you build this project?

### Answer

Modern production environments generate thousands of alerts daily.

Engineers often spend significant time gathering information from logs, metrics, deployment history, and incident records before identifying a root cause.

The goal of AI Incident Assistant was to automate the investigation workflow by:

* Classifying incidents
* Planning investigations
* Executing relevant tools
* Collecting evidence
* Generating actionable recommendations

This allows engineers to focus on resolution instead of information gathering.

---

# 2. Why did you choose an Agent Workflow instead of a single prompt?

### Answer

A single prompt lacks structured reasoning and tool access.

I wanted the system to mimic how an SRE investigates incidents.

Instead of:

```text
Alert
↓
LLM
↓
Answer
```

I implemented:

```text
Alert
↓
Classification
↓
Tool Planning
↓
Tool Execution
↓
Evidence Collection
↓
LLM Analysis
↓
Response
```

Benefits:

* Better explainability
* More deterministic behavior
* Easier debugging
* Easier future integrations

---

# 3. Why not use LangGraph?

### Answer

Initially I intentionally implemented the workflow manually.

This helped me understand:

* State transitions
* Tool orchestration
* Agent execution flow

The current workflow is simple enough that LangGraph would add unnecessary complexity.

Future versions could migrate to LangGraph for:

* Conditional routing
* Multi-agent workflows
* Human-in-the-loop approval

---

# 4. How does incident classification work?

### Answer

The agent first categorizes incidents into:

* startup_failure
* latency
* cpu
* memory
* unknown

Classification is currently rule-based.

Example:

```text
CrashLoopBackOff
↓
startup_failure
```

```text
ServiceDegradation
↓
latency
```

The classification determines which investigation tools are executed.

---

# 5. How are tools selected?

### Answer

Each incident category maps to a predefined investigation plan.

Example:

Latency:

```text
get_service_metrics
get_recent_deployments
get_service_health
```

Startup Failure:

```text
get_pod_logs
get_deployment_status
get_recent_incidents
```

This prevents unnecessary tool execution and reduces context size.

---

# 5A. How does the agent decide which tools to execute?

### Answer

The tool selection process is deterministic and happens in two stages:

```text
Incoming Alert
        ↓
Incident Classification
        ↓
Investigation Plan Selection
        ↓
Tool Execution
```

Example:

Input:

```json
{
  "service_name": "search-service",
  "alert_type": "ServiceDegradation",
  "message": "P95 latency increased from 150ms to 2.5s"
}
```

Classification:

```text
latency
```

Investigation plan:

```python
[
    "get_service_metrics",
    "get_recent_deployments",
    "get_service_health"
]
```

The selected tools are then executed through the Tool Registry.

This design ensures:

* Consistent investigations
* Predictable behavior
* Lower token usage
* Reduced hallucinations

---

# 5B. Why not let the LLM choose the tools dynamically?

### Answer

I intentionally chose deterministic tool planning instead of LLM-driven tool selection.

Current architecture:

```text
Classification
        ↓
Predefined Tool Plan
        ↓
Tool Execution
```

Instead of:

```text
Alert
        ↓
LLM decides tools
        ↓
Tool Execution
```

Reasons:

1. More predictable
2. Easier debugging
3. Easier evaluation
4. Lower latency
5. Lower cost

For a small set of incident types, deterministic routing is sufficient.

If the number of tools grows significantly, I would consider:

* OpenAI Function Calling
* OpenAI Agents SDK
* LangGraph
* Google ADK

for dynamic tool selection.

---

# 5C. How is the input to each tool determined?

### Answer

The input comes directly from the incoming alert payload.

Example alert:

```json
{
  "service_name": "search-service",
  "alert_type": "ServiceDegradation",
  "environment": "production"
}
```

Tool invocation:

```python
get_service_metrics(
    service_name="search-service"
)

get_service_health(
    service_name="search-service"
)

get_recent_deployments(
    service_name="search-service"
)
```

The agent extracts relevant fields and passes them to the selected tools.

Flow:

```text
Alert
 ↓
Extract Service Name
 ↓
Tool Parameters
 ↓
Tool Execution
```

---

# 5D. How does the Tool Registry work?

### Answer

The Tool Registry acts as a lookup table between tool names and implementations.

Example:

```python
TOOL_REGISTRY = {
    "get_service_metrics": get_service_metrics,
    "get_service_health": get_service_health,
    "get_recent_deployments": get_recent_deployments,
}
```

The planner returns tool names:

```python
[
    "get_service_metrics",
    "get_recent_deployments",
]
```

The executor resolves them through the registry:

```python
tool_fn = TOOL_REGISTRY[tool_name]
result = await tool_fn(service_name)
```

Benefits:

* Decouples planning from execution
* Makes tools easy to add
* Keeps agent logic clean
* Enables future plugin architectures

---

# 5E. What happens if a tool fails?

### Answer

Currently the system captures tool failures and continues the investigation whenever possible.

Example:

```text
get_service_metrics
        ↓
Timeout
```

Recorded as:

```python
{
    "error": "metrics unavailable"
}
```

The remaining tools still execute.

This prevents a single dependency from blocking the entire investigation.

Future improvements:

* Retry policies
* Circuit breakers
* Partial-failure handling
* Confidence score adjustments

---

# 5F. How would tool selection evolve in a production system?

### Answer

Current approach:

```text
Incident Type
        ↓
Static Tool Plan
```

Production approach:

```text
Alert
 ↓
Planner Agent
 ↓
Dynamic Tool Selection
 ↓
Tool Execution
 ↓
Reflection
 ↓
Additional Tools
```

Example:

```text
Latency Alert
 ↓
Metrics Tool
 ↓
Detect Deployment Correlation
 ↓
Deployment Tool
 ↓
Detect DB Latency
 ↓
Database Tool
```

This becomes an iterative investigation process rather than a fixed workflow.

For that level of complexity, I would likely introduce:

* OpenAI Agents SDK
* LangGraph
* Google ADK
* Multi-agent workflows

```
```


# 6. Why execute tools before calling the LLM?

### Answer

LLMs are reasoning engines, not data retrieval engines.

The LLM should analyze evidence rather than search for evidence.

Therefore:

```text
Tool Execution
↓
Evidence Collection
↓
Prompt Construction
↓
LLM Analysis
```

This reduces hallucinations and improves consistency.

---

# 7. How do you reduce hallucinations?

### Answer

Several techniques:

1. Structured prompts
2. Tool-generated evidence
3. Deterministic temperature settings
4. Structured JSON outputs
5. Pydantic validation
6. Evaluation harness

The model is instructed to use only available evidence.

---

# 8. Why use Pydantic validation?

### Answer

LLMs can return malformed outputs.

Pydantic ensures:

```python
IncidentAnalysis
```

always contains:

* severity
* root_cause
* confidence
* recommendations
* tools_used
* investigation_steps

This protects downstream systems from invalid responses.

---

# 9. Why OpenRouter instead of OpenAI directly?

### Answer

OpenRouter provides:

* Model flexibility
* Cost optimization
* Easy experimentation

I can switch between:

* Qwen
* DeepSeek
* Gemini
* OpenAI-compatible models

without changing application code.

---

# 10. How would you support multiple models?

### Answer

The system already uses:

```env
MODEL=
```

Changing the model requires only configuration changes.

Future improvements:

```text
Latency Model
Reasoning Model
Fallback Model
```

selected dynamically.

---

# 11. Why Langfuse?

### Answer

AI systems require observability.

Traditional logging is insufficient.

Langfuse provides:

* Prompt tracing
* Tool tracing
* LLM response tracking
* Workflow visibility

This makes debugging significantly easier.

---

# 12. What do you trace?

### Answer

I trace:

```text
Alert
↓
Tool Planning
↓
Tool Execution
↓
Prompt
↓
OpenRouter Request
↓
Response
```

Every investigation becomes observable.

---

# 13. Why create an Evaluation Harness?

### Answer

A working AI system is not enough.

We need to measure quality.

The evaluation framework validates:

* Severity correctness
* Tool selection
* Root cause quality
* Response latency

This helps detect regressions when prompts or models change.

---

# 14. Why Golden Datasets?

### Answer

Golden datasets provide reproducible benchmarks.

Every release is tested against the same incidents.

This creates measurable quality standards.

---

# 15. Why GitHub Actions?

### Answer

Manual evaluation is unreliable.

GitHub Actions automatically:

```text
Push
↓
Evaluation
↓
Report
↓
Pass/Fail
```

This introduces AI quality gates similar to unit tests.

---

# 16. What is Tool Mode?

### Answer

Tool Mode separates:

```text
Mock Tools
```

from

```text
Real Integrations
```

Current deployment uses:

```env
TOOL_MODE=mock
```

Future deployments can use:

```env
TOOL_MODE=real
```

without changing the agent logic.

---

# 17. Why deploy with Mock Mode?

### Answer

Portfolio projects should be runnable by anyone.

Requiring Kubernetes or Prometheus would make the demo difficult.

Mock mode provides:

* Stable demonstrations
* Easy deployment
* Reproducible evaluations

while preserving the architecture for real integrations.

---

# 18. How would you integrate Kubernetes?

### Answer

Replace:

```python
get_pod_logs()
get_deployment_status()
```

with Kubernetes API calls.

Example:

```python
from kubernetes import client
```

The rest of the agent remains unchanged.

---

# 19. How would you integrate Prometheus?

### Answer

Replace:

```python
get_service_metrics()
```

with Prometheus queries.

Example:

```promql
histogram_quantile(
  0.95,
  rate(http_request_duration_seconds_bucket[5m])
)
```

The tool interface remains unchanged.

---

# 20. What would you improve next?

### Answer

Priority order:

1. Kubernetes Integration
2. Prometheus Integration
3. Grafana Deep Links
4. Incident Chat Assistant
5. Authentication
6. Historical Incident Search
7. Multi-Agent Investigations

---

# 21. What are the biggest limitations today?

### Answer

1. Mock telemetry
2. Single-agent workflow
3. Limited incident categories
4. No conversational follow-up
5. No real infrastructure integrations

The architecture intentionally allows these to be added incrementally.

---

# 22. What are the strongest engineering decisions in this project?

### Answer

1. Agent-first architecture
2. Tool abstraction layer
3. Structured outputs
4. Pydantic validation
5. Langfuse observability
6. Evaluation framework
7. CI quality gates
8. Deployment-ready configuration

These decisions make the system production-oriented rather than a simple LLM demo.


# 23. Why did you choose static tool routing instead of dynamic tool selection?

### Answer

I intentionally chose static tool routing because the problem space is currently small and well-defined.

Current flow:

```text
Alert
 ↓
Classification
 ↓
Predefined Investigation Plan
 ↓
Tool Execution
```

Example:

```text
Latency Incident
 ↓
get_service_metrics
get_recent_deployments
get_service_health
```

instead of:

```text
Alert
 ↓
LLM decides tools
 ↓
Tool Execution
```

### Benefits

#### Predictability

The same incident type always follows the same investigation workflow.

Example:

```text
Latency
 ↓
Always Metrics + Deployments + Health
```

This makes behavior easier to reason about.

#### Easier Debugging

If the agent selects an incorrect tool, I immediately know where the problem exists:

```text
Classification
or
Tool Plan Mapping
```

instead of investigating LLM reasoning.

#### Easier Evaluation

The evaluation harness can validate:

```text
Expected Tools
vs
Actual Tools
```

which would be much harder with dynamic planning.

#### Lower Cost

No additional LLM call is required for tool planning.

#### Lower Latency

Tool selection is a simple lookup operation.

---

### When would I move to dynamic routing?

If the system grows to:

```text
50+ Tools
Multiple Infrastructure Sources
Cross-System Investigations
```

I would introduce:

* OpenAI Function Calling
* OpenAI Agents SDK
* LangGraph
* Google ADK

for dynamic planning.

---

# 24. How are tool parameters passed?

### Answer

Tool parameters are derived directly from the incoming alert.

Incoming alert:

```json
{
  "service_name": "search-service",
  "alert_type": "ServiceDegradation",
  "environment": "production"
}
```

Agent:

```python
service_name = alert["service_name"]
```

Tool invocation:

```python
get_service_metrics(service_name)

get_service_health(service_name)

get_recent_deployments(service_name)
```

Flow:

```text
Alert
 ↓
Parameter Extraction
 ↓
Tool Invocation
 ↓
Tool Result
```

This keeps tool interfaces simple and consistent.

---

# 25. How would you scale this to 50+ tools?

### Answer

The current approach works well because the system contains a small number of tools.

Current:

```text
4 Incident Types
6 Tools
```

Future:

```text
50+ Tools
Multiple Systems
```

Examples:

```text
Kubernetes
Prometheus
Grafana
PagerDuty
Jira
ServiceNow
AWS
Datadog
ArgoCD
```

At that scale I would introduce:

### Planner Agent

Instead of:

```python
if incident_type == "latency":
```

I would use:

```text
Planner Agent
 ↓
Tool Selection
 ↓
Execution
```

### Tool Metadata

Each tool would declare:

```python
{
    "name": "get_service_metrics",
    "description": "...",
    "required_inputs": [
        "service_name"
    ]
}
```

### Function Calling

The LLM would select tools based on metadata.

Example:

```text
Latency Alert
 ↓
Planner
 ↓
Metrics Tool
 ↓
Deployment Tool
 ↓
Database Tool
```

### Reflection Loop

The agent could execute additional tools if the first investigation does not provide sufficient evidence.

---

# 26. What happens when a tool fails?

### Answer

The system is designed to tolerate partial failures.

Example:

```text
get_service_metrics()
 ↓
Timeout
```

Instead of failing the entire investigation:

```text
Metrics Tool Failed
 ↓
Continue Investigation
 ↓
Run Remaining Tools
```

Tool result:

```json
{
  "error": "metrics unavailable"
}
```

The LLM still receives:

```text
Logs
Deployments
Health
```

and can continue reasoning.

### Why?

Production systems frequently experience:

* API timeouts
* Rate limits
* Service outages
* Authentication failures

A single dependency should not prevent investigation.

### Future Improvements

* Retries
* Circuit Breakers
* Fallback Tools
* Confidence Score Reduction
* Error Categorization

---

# 27. Why not use OpenAI Function Calling?

### Answer

Function Calling is powerful but introduces additional complexity that was not necessary for the first version.

Current workflow:

```text
Classification
 ↓
Tool Plan
 ↓
Execution
 ↓
LLM Analysis
```

Function Calling workflow:

```text
LLM
 ↓
Tool Selection
 ↓
Tool Execution
 ↓
LLM
 ↓
Tool Selection
 ↓
...
```

### Why I chose not to use it initially

#### Simpler Architecture

The current workflow is easy to understand and debug.

#### Better Determinism

The same alert always follows the same investigation path.

#### Easier Evaluation

Tool selection can be validated directly.

#### Faster Execution

No additional planning LLM call.

#### Lower Cost

Fewer model invocations.

---

### When would Function Calling make sense?

When:

```text
Many Tools
Unknown Investigation Paths
Dynamic Discovery
Multi-step Reasoning
```

Example:

```text
Latency Alert
 ↓
Metrics Tool
 ↓
Database Tool
 ↓
Kubernetes Tool
 ↓
Grafana Tool
```

The exact path is not known in advance.

At that point I would likely introduce:

* OpenAI Function Calling
* OpenAI Agents SDK
* LangGraph
* Google ADK

to enable dynamic investigations.

For the current scope, deterministic planning provided a better balance of simplicity, explainability, and reliability.
