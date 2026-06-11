# AI Incident Assistant

AI Incident Assistant is an agent-powered platform that helps Site Reliability Engineers (SREs) and Platform Engineers investigate production incidents faster.

Instead of manually checking logs, deployments, metrics, and historical incidents, engineers can submit an alert and receive an AI-generated diagnosis with actionable recommendations.

This project demonstrates modern AI engineering patterns including:

* Agent Workflows
* Tool Orchestration
* Structured Outputs
* Context Engineering
* LLM Integration
* AI Observability
* Evaluation Frameworks
* CI/CD Quality Gates

---

# Live Demo

### Frontend

https://ai-incident-assistant-seven.vercel.app/

### Backend API

https://ai-incident-assistant-pxzl.onrender.com/docs

---

# Problem Statement

Modern cloud environments generate thousands of alerts every day:

* CrashLoopBackOff
* High CPU Usage
* Memory Pressure
* Service Degradation
* Deployment Failures
* Increased Latency

Engineers often spend more time gathering context than actually solving incidents.

AI Incident Assistant automates the investigation process by:

1. Classifying incidents
2. Planning investigations
3. Executing tools
4. Collecting evidence
5. Generating structured diagnoses
6. Producing actionable recommendations

---

# Architecture

```text
Alert
  │
  ▼
Incident Classification
  │
  ▼
Investigation Planning
  │
  ▼
Tool Execution
  │
  ├── Pod Logs
  ├── Deployment Status
  ├── Historical Incidents
  ├── Service Metrics
  ├── Service Health
  └── Recent Deployments
  │
  ▼
Investigation Trace
  │
  ▼
OpenRouter LLM
  │
  ▼
Structured Analysis
  │
  ▼
Pydantic Validation
  │
  ▼
Incident Response
```

---

# Deployment Architecture

```text
Frontend (Vercel)
        │
        ▼
FastAPI Backend (Render)
        │
        ▼
Agent Workflow
        │
        ├── Tool Execution
        ├── OpenRouter
        └── Langfuse
```

---

# Current Features

## Incident Classification

Automatically categorizes incidents into:

* Startup Failures
* Latency Issues
* CPU Issues
* Memory Issues
* Unknown

---

## Investigation Planning

Different incidents trigger different investigation workflows.

### Startup Failure

```text
get_pod_logs
get_deployment_status
get_recent_incidents
```

### Latency

```text
get_service_metrics
get_recent_deployments
get_service_health
```

### CPU

```text
get_service_metrics
get_recent_deployments
```

### Memory

```text
get_service_metrics
get_pod_logs
```

---

## Tool Execution

The agent executes tools to gather context.

Current tools:

```text
get_pod_logs()
get_deployment_status()
get_recent_incidents()

get_service_metrics()
get_service_health()
get_recent_deployments()
```

---

## Investigation Trace

Every analysis includes a reasoning trail.

Example:

```json
{
  "investigation_steps": [
    "Classified incident as latency",
    "Selected investigation tools",
    "Executed metrics tool",
    "Executed deployment tool",
    "Executed health tool",
    "Generated diagnosis"
  ]
}
```

---

## Structured Outputs

All responses follow a strict schema.

Example:

```json
{
  "severity": "high",
  "root_cause": "Latency degradation likely introduced by recent deployment",
  "confidence": 0.87,
  "recommendations": [
    {
      "action": "Review deployment",
      "reason": "Latency increased after rollout",
      "priority": "high"
    }
  ],
  "tools_used": [
    "get_service_metrics",
    "get_recent_deployments"
  ]
}
```

---

# React Dashboard

The frontend dashboard provides:

* Incident Submission Form
* Severity Visualization
* Root Cause Analysis
* Investigation Timeline
* Recommendations Panel
* Tool Execution Visibility

Built using:

* React
* TypeScript
* Material UI
* Axios

---

# AI Observability

The platform uses Langfuse for workflow tracing and observability.

Tracked events include:

* Alert Classification
* Tool Planning
* Tool Execution
* Prompt Generation
* OpenRouter Requests
* Structured Output Generation

This provides visibility into AI decision-making and workflow execution.

---

# Evaluation Framework

The project includes an automated evaluation harness for measuring AI quality.

Features:

* Golden Dataset Testing
* Severity Validation
* Tool Selection Validation
* Root Cause Validation
* Response Latency Measurement
* Evaluation Reports
* GitHub Actions Automation

Run evaluations:

```bash
python -m evaluations.evaluator
```

Sample Output:

```text
=== Evaluation Report ===

[PASS] latency_regression_after_deployment
[PASS] payment_service_startup_failure
[PASS] cpu_spike
[PASS] memory_pressure

Accuracy: 4/4 (100%)
```

---

# CI/CD

GitHub Actions automatically evaluates the AI system on every push and pull request.

Pipeline:

```text
Push
 ↓
Install Dependencies
 ↓
Run Evaluation Harness
 ↓
Generate Report
 ↓
Upload Artifact
 ↓
Pass / Fail Quality Gate
```

This helps prevent prompt regressions and AI quality degradation.

---

# Tool Execution Modes

The platform supports configurable tool execution modes.

## Mock Mode

Used for:

* Local Development
* Public Demos
* Evaluation Testing

Tools return deterministic mock telemetry.

## Real Mode

Designed for future integrations:

* Kubernetes API
* Prometheus
* Grafana
* Deployment Platforms

Configuration:

```env
TOOL_MODE=mock

ENABLE_REAL_K8S=false
ENABLE_REAL_PROMETHEUS=false
```

---

# Technology Stack

## Backend

* FastAPI
* Python 3.12+
* Pydantic

## AI Layer

* OpenRouter
* OpenAI SDK

## Observability

* Langfuse

## Frontend

* React
* TypeScript
* Material UI
* Axios

## Infrastructure

* Docker
* Docker Compose
* Render
* Vercel

## CI/CD

* GitHub Actions

---

# Project Structure

```text
backend/

├── app/
│
├── api/
│   └── alerts.py
│
├── agents/
│   └── incident_agent.py
│
├── models/
│   └── incident.py
│
├── services/
│   ├── llm_service.py
│   ├── langfuse_service.py
│   └── prompts.py
│
├── tools/
│   ├── deployments.py
│   ├── health.py
│   ├── incidents.py
│   ├── logs.py
│   ├── metrics.py
│   ├── registry.py
│   └── releases.py
│
├── evaluations/
│   ├── golden_dataset.json
│   ├── evaluator.py
│   └── reports/
│
├── config.py
├── main.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

# Local Setup

## Clone Repository

```bash
git clone <repository-url>

cd ai-incident-assistant
```

---

## Backend Setup

```bash
cd backend

python -m venv venv
```

### Windows

```powershell
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
OPENROUTER_API_KEY=your_key
MODEL=qwen/qwen3-30b-a3b:free

LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_BASE_URL=https://cloud.langfuse.com

TOOL_MODE=mock
ENABLE_REAL_K8S=false
ENABLE_REAL_PROMETHEUS=false
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# Sample Request

```json
{
  "service_name": "search-service",
  "alert_type": "ServiceDegradation",
  "message": "P95 latency increased from 150ms to 2.5s",
  "environment": "production"
}
```

---

# Sample Response

```json
{
  "severity": "high",
  "root_cause": "Latency degradation likely introduced by recent deployment",
  "confidence": 0.87,
  "recommendations": [
    {
      "action": "Review deployment",
      "reason": "Deployment occurred shortly before latency increase",
      "priority": "high"
    }
  ],
  "tools_used": [
    "get_service_metrics",
    "get_recent_deployments",
    "get_service_health"
  ],
  "investigation_steps": [
    "Classified incident as latency",
    "Executed investigation tools",
    "Generated structured diagnosis"
  ]
}
```

---

# Skills Demonstrated

This project showcases:

* Agent Workflows
* Tool Calling
* Context Engineering
* Structured Outputs
* Pydantic Validation
* LLM Orchestration
* AI Observability
* Evaluation Frameworks
* CI/CD Quality Gates
* Full Stack Development
* Containerized Deployment

---

# Completed Roadmap

## Phase 1 ✅ Backend Agent

* FastAPI Backend
* Tool Registry
* Incident Classification
* Investigation Planning
* Tool Execution
* OpenRouter Integration

## Phase 2 ✅ Observability

* Langfuse Integration
* Workflow Tracing
* Tool Tracing
* LLM Tracing

## Phase 3 ✅ Frontend Dashboard

* React Dashboard
* Material UI
* Incident Visualization
* Investigation Timeline

## Phase 4 ✅ Evaluation & Quality

* Golden Dataset
* Evaluation Harness
* Evaluation Reports
* GitHub Actions Automation
* Quality Gates

## Phase 5 🚧 Future Enhancements

* Kubernetes Integration
* Prometheus Integration
* Grafana Deep Links
* Incident Chat Assistant
* Authentication
* Incident History

```
```
