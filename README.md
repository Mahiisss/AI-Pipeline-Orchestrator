# 🧠 AI Workflow Pipeline Orchestrator

<div align="center">

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-Flow-61DAFB?style=for-the-badge&logo=react)
![n8n](https://img.shields.io/badge/n8n-Webhook-EA4B71?style=for-the-badge&logo=n8n)

**A full-stack visual workflow automation system — design, validate, and execute pipelines using a node-based interface.**

Inspired by **n8n** and **Apache Airflow**, built from scratch with a focus on DAG-based execution, reliability, and system design.

[🎥 Watch Demo](https://drive.google.com/file/d/1yR2eBKbOcjJFWWRYophAGfVax0seq1s9/view?usp=sharing) · [📖 API Docs](http://localhost:8000/docs) · [🚀 Getting Started](#-getting-started)

</div>

---

## 📽️ Demo

> ▶️ [**Watch Full Project Walkthrough**](https://drive.google.com/file/d/1yR2eBKbOcjJFWWRYophAGfVax0seq1s9/view?usp=sharing)

The demo covers:
- Drag-and-drop node creation & pipeline design
- DAG validation with real-time feedback
- Pipeline execution with live logs per node
- n8n webhook integration triggering the same execution engine

---

## 🧠 What Is This?

Most workflow tools are black boxes. This project builds one from the ground up.

Users visually connect nodes to form a **Directed Acyclic Graph (DAG)**. The backend validates the graph structure, resolves execution order using **Kahn's Topological Sort**, and runs each node in sequence — passing output data from one node as input to the next.

The result: a fully working mini-Airflow, built with React + FastAPI + n8n.

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────┐
│         Frontend (React + React Flow)     │
│   Drag-and-drop visual pipeline builder  │
└────────────────────┬─────────────────────┘
                     │ Workflow JSON (nodes + edges)
                     ▼
┌──────────────────────────────────────────┐
│           FastAPI Backend                │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  Validation Engine                 │  │
│  │  → Kahn's Algorithm (cycle detect) │  │
│  └────────────────────────────────────┘  │
│                     ↓                    │
│  ┌────────────────────────────────────┐  │
│  │  Execution Engine                  │  │
│  │  → Topological order execution     │  │
│  │  → Node-to-node data passing       │  │
│  └────────────────────────────────────┘  │
│                     ↓                    │
│  ┌────────────────────────────────────┐  │
│  │  Logger                            │  │
│  │  → Per-node success/failure logs   │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
                     ▲
         ┌───────────┴───────────┐
         │                       │
  Manual UI Trigger        n8n Webhook Trigger
  (Run Pipeline button)    (HTTP Request node)
```

---

## ⚡ Core Features

### 🎨 Visual Workflow Editor
- Drag-and-drop nodes onto a canvas
- Draw connections to define data flow
- Real-time graph updates powered by **React Flow**
- One-click **Submit** (validate) and **Run** (execute) buttons

### 🧩 8 Custom Node Types

| Node | What It Does |
|------|-------------|
| **Input** | Injects starting data into the pipeline |
| **Transform** | Mutates text — uppercase, lowercase, reverse |
| **Math** | Arithmetic — add, subtract, multiply, divide |
| **API** | Calls any external REST API |
| **Condition** | Branching logic based on runtime values |
| **Output** | Captures and returns the final result |
| **Text** | Dynamic inputs using `{{variable}}` syntax |
| **Database** | Simulated database read/write operations |

All nodes are built on a shared **BaseNode component** — configurable, extensible, zero duplication.

### 🔍 DAG Validation Engine
- Detects cycles using **Kahn's Topological Sorting Algorithm**
- Blocks invalid pipelines before execution
- Returns node count, edge count, and DAG validity status

### 🔥 Pipeline Execution Engine

Runs nodes in topological order. Data flows automatically from node to node.

```
Input("Hello World!")  →  Transform(uppercase)  →  Output("HELLO WORLD!")
```

Each node has isolated execution logic. A failed node is logged without crashing the rest of the pipeline.

### ⚡ Two Trigger Modes

**Mode 1 — Manual UI**
```
User clicks "Run Pipeline"
        ↓
Frontend POSTs workflow JSON
        ↓
POST /pipelines/execute
        ↓
Execution logs rendered live
```

**Mode 2 — n8n Webhook**
```
n8n Webhook node (trigger)
        ↓
n8n HTTP Request node
        ↓
POST http://127.0.0.1:8000/pipelines/execute
        ↓
Same execution engine — logs returned to n8n
```

Both modes share the **exact same backend execution engine** — no duplication.

---

## 🔗 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/pipelines/parse` | Validate DAG structure |
| `POST` | `/pipelines/execute` | Execute pipeline node by node |

### Example Request

```json
POST /pipelines/execute

{
  "nodes": [
    { "id": "1", "type": "input",     "data": { "value": "Hello World!" } },
    { "id": "2", "type": "transform", "data": { "operation": "uppercase" } },
    { "id": "3", "type": "output",    "data": {} }
  ],
  "edges": [
    { "id": "e1", "source": "1", "target": "2" },
    { "id": "e2", "source": "2", "target": "3" }
  ]
}
```

### Example Response

```json
{
  "status": "completed",
  "num_nodes": 3,
  "num_edges": 2,
  "execution_log": [
    { "node_id": "1", "node_type": "input",     "status": "success", "output": { "output": "Hello World!" } },
    { "node_id": "2", "node_type": "transform", "status": "success", "output": { "output": "HELLO WORLD!" } },
    { "node_id": "3", "node_type": "output",    "status": "success", "output": { "final": true } }
  ]
}
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- n8n (`npm install -g n8n`)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/AI-Pipeline-Orchestrator.git
cd AI-Pipeline-Orchestrator
```

### 2. Start the backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install fastapi uvicorn pydantic httpx
uvicorn main:app --reload
```

| | URL |
|---|---|
| 🖥️ Backend | http://localhost:8000 |
| 📖 API Docs | http://localhost:8000/docs |

### 3. Start the frontend

```bash
cd frontend
npm install
npm start
```

| | URL |
|---|---|
| 🌐 Frontend | http://localhost:3000 |

### 4. Start n8n (optional — for webhook trigger)

```bash
n8n start
```

| | URL |
|---|---|
| ⚙️ n8n Dashboard | http://localhost:5678 |

In n8n, create a workflow:
1. Add a **Webhook** node → set method to POST
2. Add an **HTTP Request** node → POST to `http://127.0.0.1:8000/pipelines/execute`
3. Pass your pipeline JSON as the request body

---

## 🛠️ Tech Stack

### Frontend
| Technology | Role |
|-----------|------|
| React | UI framework |
| React Flow | Visual node-graph editor |
| Zustand | Global state management |

### Backend
| Technology | Role |
|-----------|------|
| FastAPI | REST API framework |
| Pydantic | Request/response validation |
| httpx | Async HTTP client for API nodes |
| Uvicorn | ASGI server |

### Automation
| Technology | Role |
|-----------|------|
| n8n | Webhook trigger + HTTP orchestration |

### Algorithms
| Algorithm | Role |
|-----------|------|
| Kahn's Topological Sort | Cycle detection + execution ordering |
| DAG Traversal | Node dependency resolution |

---

## 🧠 What This Project Demonstrates

This isn't a tutorial project — it's a ground-up implementation of concepts used in production automation platforms:

- **Graph theory in practice** — DAG modeling, cycle detection, topological ordering
- **Execution engine design** — node-to-node data passing, isolated error handling per node
- **Event-driven architecture** — same engine triggered by both UI and external webhooks
- **Component architecture** — reusable BaseNode pattern across 8 node types, zero duplication
- **Full-stack integration** — React ↔ FastAPI ↔ n8n working together end-to-end
- **System reliability** — per-node logging, graceful failure handling, CORS configuration

---

## 🔮 Roadmap

- [ ] Workflow scheduling (cron-style triggers)
- [ ] Retry and failure recovery per node
- [ ] Persistent storage (MongoDB / PostgreSQL)
- [ ] Authentication and user workspaces
- [ ] Real-time monitoring dashboard
- [ ] AI-powered nodes (LLM, embeddings, vector search)
- [ ] Expanded n8n node integrations

---

<div align="center">

Built with ⚡ by [Mahi](https://github.com/your-username)

*Found this useful? Drop a ⭐ — it helps a lot!*

</div>