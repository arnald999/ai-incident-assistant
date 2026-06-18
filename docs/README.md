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
