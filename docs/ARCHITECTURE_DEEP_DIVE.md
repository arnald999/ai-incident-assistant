# AI Incident Assistant - Architecture Deep Dive

This document explains the internal architecture, request flow, tool orchestration, AI workflow, and file-level mapping.

---

# High-Level Flow

```text
User
 │
 ▼
React Dashboard
 │
 ▼
FastAPI API
 │
 ▼
Incident Agent
 │
 ▼
Incident Classification
 │
 ▼
Tool Planning
 │
 ▼
Tool Execution
 │
 ▼
Prompt Construction
 │
 ▼
OpenRouter LLM
 │
 ▼
Pydantic Validation
 │
 ▼
Response
 │
 ▼
React Dashboard
```

---

# Request Flow Mapping

## Frontend

### File

```text
frontend/src/components/AlertForm.tsx
```

Responsible for:

* Collecting alert details
* Submitting incidents

Example:

```json
{
  "service_name": "search-service",
  "alert_type": "ServiceDegradation",
  "message": "P95 latency increased from 150ms to 2.5s",
  "environment": "production"
}
```

---

### File

```text
frontend/src/api/incidentApi.ts
```

Responsible for:

* Axios API calls
* Backend communication

Flow:

```text
AlertForm
    ↓
incidentApi.ts
    ↓
POST /api/alerts/analyze
```

---

# Backend API Layer

### File

```text
backend/app/api/alerts.py
```

Entry point for incident analysis.

Endpoint:

```python
POST /api/alerts/analyze
```

Flow:

```text
Incoming Alert
        ↓
Incident Agent
        ↓
Incident Analysis
```

---

# Agent Layer

### File

```text
backend/app/agents/incident_agent.py
```

This is the heart of the system.

Responsibilities:

1. Classify incident
2. Plan investigation
3. Execute tools
4. Build investigation trace
5. Generate analysis

Flow:

```text
Alert
 ↓
classify_incident()
 ↓
plan_tools()
 ↓
execute_tools()
 ↓
build_investigation_steps()
 ↓
generate_structured_incident_analysis()
```

---

# Incident Classification

### File

```text
backend/app/agents/incident_agent.py
```

Method:

```python
classify_incident()
```

Current categories:

```text
startup_failure
latency
cpu
memory
unknown
```

Example:

```text
CrashLoopBackOff
↓
startup_failure
```

---

# Tool Planning

### File

```text
backend/app/agents/incident_agent.py
```

Method:

```python
plan_tools()
```

Maps incident type to tools.

Example:

```python
latency
```

returns:

```python
[
    "get_service_metrics",
    "get_recent_deployments",
    "get_service_health",
]
```

---

# Tool Registry

### File

```text
backend/app/tools/registry.py
```

Purpose:

Central registry for all tools.

Example:

```python
TOOL_REGISTRY = {
    "get_service_metrics": get_service_metrics,
    "get_service_health": get_service_health,
    "get_recent_deployments": get_recent_deployments,
}
```

Benefits:

* Dynamic tool execution
* Easy future expansion
* Decoupled architecture

Flow:

```text
Tool Name
     ↓
Registry Lookup
     ↓
Actual Function
```

---

# Tool Execution

## Metrics Tool

### File

```text
backend/app/tools/metrics.py
```

Method:

```python
get_service_metrics()
```

Returns:

```python
{
    "p95_latency_ms": 2500,
    "cpu_percent": 45,
    "memory_percent": 60,
}
```

Future:

```text
Prometheus
```

---

## Health Tool

### File

```text
backend/app/tools/health.py
```

Method:

```python
get_service_health()
```

Returns:

```python
{
    "status": "degraded"
}
```

Future:

```text
Prometheus
Grafana
```

---

## Deployment Tool

### File

```text
backend/app/tools/deployments.py
```

Method:

```python
get_deployment_status()
```

Returns deployment state.

Future:

```text
Kubernetes API
```

---

## Recent Deployments Tool

### File

```text
backend/app/tools/releases.py
```

Method:

```python
get_recent_deployments()
```

Returns:

```python
{
    "version": "v2.3.1"
}
```

Future:

```text
ArgoCD
GitHub Deployments
Jenkins
```

---

## Incident History Tool

### File

```text
backend/app/tools/incidents.py
```

Method:

```python
get_recent_incidents()
```

Returns:

```python
Historical incidents
```

Future:

```text
ServiceNow
Jira
PagerDuty
```

---

## Logs Tool

### File

```text
backend/app/tools/logs.py
```

Method:

```python
get_pod_logs()
```

Returns:

```text
Pod logs
```

Future:

```text
Kubernetes Logs API
```

---

# Tool Mode Architecture

### File

```text
backend/app/config.py
```

Configuration:

```env
TOOL_MODE=mock
```

Current:

```text
Mock Tools
```

Future:

```env
TOOL_MODE=real
```

Flow:

```text
Tool Request
      ↓
Tool Mode Check
      ↓
Mock Implementation
      OR
Real Integration
```

---

# Investigation Trace

### File

```text
backend/app/agents/incident_agent.py
```

Method:

```python
build_investigation_steps()
```

Produces:

```json
{
  "investigation_steps": [
    "Classified incident as latency",
    "Selected investigation tools",
    "Executed metrics tool",
    "Generated diagnosis"
  ]
}
```

Purpose:

* Explainability
* Debugging
* Transparency

---

# Prompt Engineering

### File

```text
backend/app/services/prompts.py
```

Method:

```python
build_incident_prompt()
```

Combines:

```text
Alert
+
Tool Results
+
Investigation Steps
```

into a single prompt.

Flow:

```text
Context Collection
        ↓
Prompt Construction
        ↓
LLM
```

---

# LLM Layer

### File

```text
backend/app/services/llm_service.py
```

Responsible for:

* OpenRouter integration
* Prompt execution
* Structured output generation

Model:

```env
MODEL=qwen/qwen3-30b-a3b:free
```

Current provider:

```text
OpenRouter
```

Future:

```text
OpenAI
Gemini
Claude
DeepSeek
```

---

# Langfuse Integration

### File

```text
backend/app/services/langfuse_service.py
```

Purpose:

* Prompt tracing
* Tool tracing
* Workflow tracing

Flow:

```text
Incident
 ↓
Trace
 ↓
Generation
 ↓
Tool Calls
 ↓
Output
```

---

# Validation Layer

### File

```text
backend/app/models/incident.py
```

Pydantic Models:

```python
Recommendation
IncidentAnalysis
```

Guarantees:

```text
Valid Schema
Valid Types
Consistent Outputs
```

---

# Evaluation Framework

## Dataset

### File

```text
backend/evaluations/golden_dataset.json
```

Contains:

```text
Expected incidents
Expected severity
Expected tools
Expected root causes
```

---

## Evaluator

### File

```text
backend/evaluations/evaluator.py
```

Measures:

* Severity correctness
* Tool correctness
* Root cause quality
* Latency

---

## Reports

### File

```text
backend/evaluations/reports/latest_report.json
```

Stores:

```text
Evaluation results
Accuracy
Pass/Fail
```

---

# GitHub Actions

### File

```text
.github/workflows/evaluation.yml
```

Pipeline:

```text
Push
 ↓
Install Dependencies
 ↓
Run Evaluator
 ↓
Generate Report
 ↓
Upload Artifact
```

---

# Why This Architecture?

Benefits:

1. Modular
2. Testable
3. Observable
4. Deployment Ready
5. Easy Tool Expansion
6. Easy Model Switching
7. Evaluation Driven

The architecture intentionally separates:

```text
Agent Logic
Tool Logic
Prompt Logic
LLM Logic
Validation Logic
Observability Logic
Evaluation Logic
```

This keeps the system maintainable as it grows into real Kubernetes and Prometheus integrations.


# Agent Development Kit (ADK) Mapping

Although this project does not currently use a formal Agent Development Kit such as:

* OpenAI Agents SDK
* Google ADK
* LangGraph
* CrewAI
* AutoGen

it implements the same core agent primitives manually.

This was an intentional design decision to better understand and control the underlying orchestration logic.

## ADK Concept Mapping

| ADK Concept        | Project Implementation                       |
| ------------------ | -------------------------------------------- |
| Agent              | `backend/app/agents/incident_agent.py`       |
| Tool Registry      | `backend/app/tools/registry.py`              |
| Tool Execution     | `execute_tools()`                            |
| Planning           | `plan_tools()`                               |
| State              | `alert + tool_results + investigation_steps` |
| Prompt Engineering | `backend/app/services/prompts.py`            |
| LLM Invocation     | `backend/app/services/llm_service.py`        |
| Validation         | `Pydantic Models`                            |
| Tracing            | `Langfuse`                                   |
| Evaluation         | `backend/evaluations/`                       |

## Why Not Use an ADK?

The current workflow consists of:

```text
Alert
 ↓
Classification
 ↓
Tool Planning
 ↓
Tool Execution
 ↓
Prompt Construction
 ↓
LLM Analysis
 ↓
Validation
```

Because the workflow is deterministic and uses a single agent, introducing an ADK would add additional abstraction without significant benefits.

Building the orchestration layer manually provided a deeper understanding of:

* Agent execution flow
* Tool routing
* Context construction
* Prompt engineering
* Structured outputs
* Evaluation-driven development

## Future Evolution

As the platform grows, an ADK could be introduced for:

* Multi-agent collaboration
* Human-in-the-loop approvals
* Stateful workflows
* Memory management
* Advanced routing logic

Potential future frameworks:

* OpenAI Agents SDK
* LangGraph
* Google ADK

The current architecture was intentionally designed so that these frameworks can be introduced later without major changes to the existing tool and service layers.
