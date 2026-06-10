# AI Incident Assistant

AI Incident Assistant is an agent-powered platform that helps Site Reliability Engineers (SREs) and Platform Engineers investigate production incidents faster.

Instead of manually checking logs, deployments, metrics, and historical incidents, engineers can submit an alert and receive an AI-generated diagnosis with actionable recommendations.

This project demonstrates production AI engineering patterns including:

* Agent workflows
* Tool orchestration
* Structured outputs
* Context engineering
* LLM integration
* Production-grade API design

---

# Problem Statement

Modern cloud environments generate thousands of alerts every day:

* CrashLoopBackOff
* High CPU usage
* Memory pressure
* Service degradation
* Deployment failures
* Increased latency

Engineers often spend more time gathering context than actually solving incidents.

AI Incident Assistant automates the investigation process by:

1. Classifying incidents
2. Planning investigations
3. Executing tools
4. Collecting evidence
5. Generating structured diagnoses

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
LLM Structured Analysis
  │
  ▼
Pydantic Validation
  │
  ▼
Incident Response
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

Current mock tools:

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

## LLM Integration

The project uses OpenRouter for model access.

Benefits:

* Model agnostic
* Easy experimentation
* Cost-effective development
* Supports multiple providers

Examples:

* Qwen
* DeepSeek
* Gemini
* OpenAI-compatible models

---

# Technology Stack

## Backend

* FastAPI
* Python 3.12+
* Pydantic

## AI Layer

* OpenRouter
* OpenAI SDK

## Infrastructure

* Docker
* Docker Compose

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

cd ai-incident-assistant/backend
```

---

## Create Virtual Environment

### Windows

```powershell
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create:

```text
.env
```

Example:

```env
OPENROUTER_API_KEY=your_openrouter_api_key

MODEL=openrouter/free
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Docker Setup

Create:

```text
backend/.env
```

Run:

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000/docs
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

# Production AI Patterns Demonstrated

This project showcases:

* Agent Workflows
* Tool Calling
* Context Engineering
* Structured Outputs
* Pydantic Validation
* LLM Orchestration
* Fallback Mechanisms
* Containerized Deployment

---

# Roadmap

## Phase 1 ✅

* FastAPI Backend
* Tool Registry
* Incident Classification
* Investigation Planning
* Tool Execution
* Structured Outputs
* OpenRouter Integration
* Docker Support

## Phase 2

* OpenAI Function Calling
* LangGraph Workflows
* Langfuse Tracing
* OpenTelemetry

## Phase 3

* Evaluation Harness
* Golden Datasets
* LLM-as-Judge

## Phase 4

* React Dashboard
* Kubernetes Deployment
* AWS Bedrock Integration

---

# Portfolio Value

This project demonstrates practical skills relevant to:

* Forward Deployed Engineer
* AI Engineer
* Platform Engineer
* Solutions Architect

by combining AI systems, backend engineering, observability concepts, and production deployment patterns into a realistic incident-response workflow.
