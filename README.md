# KeaBuilder Hybrid ML Lead Intelligence System

## Problem Statement

KeaBuilder is a SaaS platform used for:

- Funnel creation
- Lead capture
- CRM workflows
- Marketing automation
- AI-assisted business workflows

A major challenge in such platforms is identifying which incoming leads are high-quality and determining what actions should be triggered automatically.

This project implements a lightweight Hybrid ML Lead Intelligence System that:

- analyzes incoming lead data,
- performs hybrid scoring,
- understands semantic intent,
- recommends funnels,
- and suggests automation workflows.

The goal of this assignment is not heavy ML training, but practical ML system design and production-oriented architecture.

---

# Project Objective

The system simulates how KeaBuilder could intelligently process leads in real-world SaaS workflows.

Example capabilities:

- Detect high-intent leads
- Recommend appropriate sales funnels
- Trigger automation workflows
- Assign CRM tags
- Generate explainable predictions

---

# Project Structure

```text
keabuilder-hybrid-ml-assignment/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── scoring.py
│   ├── semantic_engine.py
│   ├── llm_engine.py
│   ├── recommender.py
│   └── workflow.py
│
├── sample_outputs/
│   └── sample_response.json
│
├── .env.example
├── requirements.txt
└── README.md
```

---

# System Architecture

```text
Lead Input
   ↓
Rule-Based Scoring Engine
   ↓
Semantic Similarity Engine
   ↓
LLM Recommendation Layer
   ↓
Final Weighted Score
   ↓
Funnel Recommendation
   ↓
Automation Workflow Suggestion
   ↓
JSON API Response
```

---

# High-Level Data Flow

```text
User / CRM / Funnel
   ↓
FastAPI Endpoint
   ↓
Lead Validation (Pydantic)
   ↓
Rule-Based Scoring
   ↓
Semantic Embedding Similarity
   ↓
Optional LLM Reasoning
   ↓
Weighted Final Score
   ↓
Recommendation Engine
   ↓
Automation Workflow Generator
   ↓
Structured JSON Response
```

---

# Why Hybrid Architecture?

Instead of using only one approach, this project combines:

| Layer | Purpose |
|---|---|
| Rule-Based Logic | Handles explicit business signals |
| Semantic Similarity | Understands contextual intent |
| LLM Reasoning | Generates explainable recommendations |

This architecture improves:

- Explainability
- Scalability
- Flexibility
- SaaS integration capability

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core backend language |
| FastAPI | High-performance API framework |
| Pydantic | Request/response validation |
| SentenceTransformers | Text embeddings |
| all-MiniLM-L6-v2 | Semantic similarity model |
| Scikit-learn | Cosine similarity calculation |
| NumPy | Numerical computations |
| Uvicorn | ASGI server |
| Mistral API (optional) | LLM reasoning layer |
| dotenv | Environment variable management |

---

# File-by-File Explanation

---

## `main.py`

### Purpose

Acts as the main application entry point.

### Responsibilities

- Initializes FastAPI
- Defines API routes
- Orchestrates all ML layers
- Aggregates final outputs
- Returns structured prediction responses

### Data Flow

```text
API Request
   ↓
main.py
   ↓
scoring.py
semantic_engine.py
llm_engine.py
   ↓
recommender.py
workflow.py
   ↓
Final JSON Response
```

---

## `config.py`

### Purpose

Centralized configuration management.

### Responsibilities

- Loads environment variables
- Stores model settings
- Stores scoring weights
- Controls feature flags

### Why Important

Keeps the application configurable and deployment-friendly.

---

## `schemas.py`

### Purpose

Defines all request and response schemas.

### Responsibilities

- Input validation
- Structured API contracts
- Typed response models

### Tech Used

- Pydantic

---

## `scoring.py`

### Purpose

Implements deterministic business scoring.

### Responsibilities

Scores explicit business signals such as:

- Budget
- Timeline urgency
- Lead source
- Goal clarity
- Business type

### Example Logic

```text
High Budget → Higher Intent
Urgent Timeline → Higher Conversion Probability
Paid Ads / Referral → Better Lead Quality
```

### Why Used

Rule-based logic provides explainability and predictable scoring behavior.

---

## `semantic_engine.py`

### Purpose

Implements embedding-based semantic similarity scoring.

### Responsibilities

- Converts text into vector embeddings
- Compares lead intent against reference patterns
- Generates semantic intent score

### Tech Used

| Technology | Role |
|---|---|
| SentenceTransformers | Embedding generation |
| all-MiniLM-L6-v2 | Lightweight semantic model |
| Cosine Similarity | Vector comparison |

### Pipeline

```text
Lead Goal Text
   ↓
SentenceTransformer
   ↓
Vector Embedding
   ↓
Cosine Similarity
   ↓
Top Intent Similarity Score
```

### Why Used

This allows the system to understand contextual meaning instead of exact keyword matching.

---

## `llm_engine.py`

### Purpose

Provides optional reasoning and recommendation generation.

### Responsibilities

- Generates explanations
- Suggests actions
- Predicts lead quality
- Adds human-readable reasoning

### Features

- Optional LLM usage
- Fallback deterministic logic
- Failure-safe architecture

### Why Important

Production systems should degrade gracefully if external LLM APIs fail.

---

## `recommender.py`

### Purpose

Maps lead characteristics to funnel strategies.

### Responsibilities

- Recommend funnel type
- Select suitable sales workflow
- Align lead intent with product workflows

### Example

```text
Real Estate + Buyer Leads
   ↓
real_estate_buyer_lead_funnel
```

---

## `workflow.py`

### Purpose

Generates downstream automation workflows.

### Responsibilities

- CRM tagging
- Email sequence assignment
- Sales notification logic
- Workflow recommendations

### Example

```text
High Intent Lead
   ↓
Notify Sales Team
Assign CRM Tag
Trigger Follow-up Sequence
```

---

## `sample_outputs/sample_response.json`

### Purpose

Contains sample API output.

### Why Important

- Testing
- Demonstration
- Validation
- API documentation

---

## `requirements.txt`

### Purpose

Contains all Python dependencies required to run the application.

---

## `.env.example`

### Purpose

Provides environment configuration template.

### Stores

- API keys
- Model settings
- Feature flags

---

# Hybrid ML Pipeline

## Step 1 — Lead Input

The system receives lead data through the API.

### Example

```json
{
  "business_type": "Real Estate",
  "goal": "Generate buyer leads urgently",
  "budget": 75000
}
```

---

## Step 2 — Rule-Based Scoring

Business signals are scored deterministically.

### Example

```text
Urgent timeline → +20
High budget → +25
Paid Ads source → +10
```

---

## Step 3 — Semantic Similarity Scoring

The system compares lead intent against high-converting reference patterns.

### Example

```text
"Generate buyer leads urgently"
```

Compared against:

```text
"I want a sales funnel for real estate leads"
```

Using:

```text
Cosine similarity on embeddings
```

---

## Step 4 — LLM Recommendation Layer

Optional reasoning layer generates:

- explanation,
- recommended actions,
- confidence score,
- lead quality reasoning.

---

## Step 5 — Final Weighted Score

### Formula

```text
final_score =
(rule_score × 0.40)
+ (semantic_score × 0.40)
+ (llm_confidence_score × 0.20)
```

---

## Step 6 — Funnel Recommendation

System recommends most appropriate funnel.

### Example

```text
real_estate_buyer_lead_funnel
```

---

## Step 7 — Automation Workflow Generation

System generates automation actions.

### Example

```text
CRM Tag
Email Sequence
Sales Notification
Next-Step Recommendation
```

---

# API Endpoints

---

## Health Check

```http
GET /health
```

### Response

```json
{
  "status": "healthy"
}
```

---

## Analyze Lead

```http
POST /api/v1/analyze-lead
```

### Sample Input

```json
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "business_type": "Real Estate",
  "goal": "I want to generate buyer leads urgently using Facebook Ads and automate follow-ups.",
  "budget": 75000,
  "timeline": "urgent",
  "source": "Facebook Ads",
  "company_size": "small team",
  "message": "We need a funnel that captures real estate buyer leads and automatically books discovery calls."
}
```

---

# Sample Output

```json
{
  "lead_quality": "high_intent",
  "recommended_funnel": "real_estate_buyer_lead_funnel",
  "recommended_action": "schedule_discovery_call",
  "score_breakdown": {
    "rule_score": 95.0,
    "semantic_score": 88.42,
    "llm_confidence_score": 91.71,
    "final_score": 91.19
  }
}
```

---

# Production Deployment Approach

Since KeaBuilder uses a Node.js backend, the ML service would be deployed independently.

## Proposed Architecture

```text
Frontend
   ↓
Node.js Backend
   ↓ REST API
Python FastAPI ML Service
   ↓
Embedding + LLM Engines
```

## Why This Architecture?

Benefits:

- Independent scaling
- Model isolation
- Easier deployments
- Better monitoring
- Fault isolation
- Flexible model upgrades

---

# Production Improvements

Future improvements may include:

- Historical lead conversion training
- Supervised ML models
- Real-time analytics
- Feedback learning loops
- Vector databases
- A/B testing optimization
- User personalization
- RAG-based lead reasoning

---

# How to Run

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Server

```bash
python -m uvicorn app.main:app --reload
```

---

# Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Postman Testing

## Endpoint

```text
POST http://127.0.0.1:8000/api/v1/analyze-lead
```

## Method

```text
POST
```

## Body Type

```text
raw → JSON
```

---

# Key Design Decisions

| Decision | Reason |
|---|---|
| Hybrid Architecture | Balances explainability + ML intelligence |
| FastAPI | Lightweight and production-ready |
| SentenceTransformers | Efficient semantic similarity |
| Optional LLM Layer | Explainable recommendations |
| Fallback Logic | Graceful degradation |
| Modular Files | Scalability and maintainability |

---

# Conclusion

This project demonstrates a practical production-oriented ML feature that could realistically integrate into KeaBuilder’s SaaS ecosystem.

The system combines:

- deterministic scoring,
- semantic understanding,
- and optional LLM reasoning

to generate explainable lead intelligence and automation recommendations.