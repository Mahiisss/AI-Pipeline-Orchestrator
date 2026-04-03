# AI Workflow Pipeline Builder 🚀

A full-stack visual workflow automation system that allows users to design, validate, and **execute** pipelines using a node-based interface.

Inspired by modern automation tools like **n8n** and **Apache Airflow**, this project focuses on workflow orchestration, execution, reliability, and system design.

---

## 🎥 Demo

▶️ **Project Walkthrough**
[Watch Demo Video](https://drive.google.com/file/d/1kYPZP2pNhYjL3BfiEaYOjUGBIlDCTQiu/view?usp=drive_link)

- Running the application
- Drag-and-drop node creation
- Connecting nodes to build pipelines
- DAG validation results
- Pipeline execution with live logs
- n8n webhook integration

---

## 🧠 Overview

This system enables users to build workflows by connecting nodes in a visual interface. Each workflow is represented as a **Directed Acyclic Graph (DAG)**, ensuring tasks execute in the correct order without cyclic dependencies.

The backend validates workflows and **executes them step-by-step**, supporting two trigger modes — manual UI button and event-driven n8n webhook triggers.

---

## 🏗️ System Architecture

```
Frontend (React + React Flow + Zustand)
              ↓
         Workflow JSON
              ↓
       FastAPI Backend
              ↓
┌─────────────────────────────────┐
│  Validation Engine              │
│  → DAG check (Kahn's Algorithm) │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  Execution Engine               │
│  → Runs nodes in topo order     │
│  → Passes data between nodes    │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  Trigger System                 │
│  → Manual UI button             │
│  → n8n Webhook                  │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  Logger                         │
│  → Tracks execution per node    │
│  → Success / Failure status     │
└─────────────────────────────────┘
```

---

## 🔁 Workflow Lifecycle

```
1. User designs workflow visually (drag and drop)
        ↓
2. Frontend sends workflow JSON to backend
        ↓
3. Backend validates DAG structure
        ↓
4. Workflow is triggered:
   → Approach 1: Manual "Run Pipeline" button
   → Approach 2: n8n Webhook trigger
        ↓
5. Execution engine runs nodes in topological order
        ↓
6. Logs generated for each node (success / failure)
```

---

## ⚙️ Core Features

### 🔹 Visual Workflow Editor
- Drag-and-drop node creation
- Connect nodes to define dependencies
- Real-time graph updates using React Flow
- Submit Pipeline button for DAG validation
- Run Pipeline button for execution

---

### 🔹 Reusable Node Architecture
A reusable **BaseNode component** eliminates duplication across all node implementations.

Each node supports:
- Configurable input fields
- Connection handles
- Dynamic parameters
- Customizable styling

---

### 🔹 Custom Node Types

| Node | Functionality |
|------|--------------|
| Input Node | Provides initial data to the pipeline |
| Transform Node | Modifies data (uppercase, lowercase, reverse) |
| Math Node | Performs arithmetic (add, subtract, multiply, divide) |
| API Node | Calls external REST APIs |
| Condition Node | Branching logic based on values |
| Output Node | Returns final result |
| Text Node | Dynamic variable inputs using `{{variable}}` syntax |
| Database Node | Simulates database operations |

---

### 🔹 DAG Validation Engine
- Detects cycles using **Kahn's Topological Sorting Algorithm**
- Prevents invalid workflows from executing
- Returns node count, edge count, and DAG status

---

### 🔹 Pipeline Execution Engine 🔥

Executes the pipeline node by node in topological order. Data flows from one node to the next automatically.

**Example flow:**
```
Input Node ("Hello World")
        ↓
Transform Node (uppercase → "HELLO WORLD")
        ↓
Output Node ("HELLO WORLD", final: true)
```

Each node type has its own execution logic:
- **Input** → provides starting data
- **Transform** → modifies text
- **Math** → performs calculations
- **API** → calls external URLs
- **Condition** → branching logic
- **Output** → returns final result

---

### 🔹 Two Trigger Approaches ⚡

#### Approach 1 — Manual UI Trigger
- User drags and connects nodes visually
- Clicks **"Run Pipeline"** button
- Frontend sends pipeline JSON to `/pipelines/execute`
- Execution logs shown on screen in real time

#### Approach 2 — n8n Webhook Trigger
- n8n sends a webhook HTTP request
- n8n HTTP Request node calls `/pipelines/execute`
- FastAPI executes the pipeline automatically
- Execution logs returned to n8n

```
n8n Webhook node
        ↓
n8n HTTP Request node
        ↓
POST http://127.0.0.1:8000/pipelines/execute
        ↓
FastAPI executes pipeline
        ↓
Execution logs returned to n8n
```

Both approaches use the **same execution engine** in the backend.

---

### 🔹 Execution Logging
- Tracks execution of each node
- Captures success/failure status per node
- Shows output data per node
- Displayed on frontend in real time

**Example log:**
```json
{
  "node_id": "2",
  "node_type": "transform",
  "status": "success",
  "output": {"output": "HELLO WORLD"},
  "error": null
}
```

---

### 🔹 Error Handling
- Prevents execution of invalid (cyclic) workflows
- Try-catch on every node execution
- Failed nodes are logged without crashing the pipeline
- CORS configured for frontend-backend communication

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/pipelines/parse` | Validate DAG structure |
| POST | `/pipelines/execute` | Execute pipeline node by node |

---

## 🏃 Running the Project

### 1. Run Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install fastapi uvicorn pydantic httpx
uvicorn main:app --reload
```
Backend: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

---

### 2. Run Frontend
```bash
cd frontend
npm install
npm start
```
Frontend: `http://localhost:3000`

---

### 3. Run n8n (for webhook trigger)
```bash
n8n start
```
n8n: `http://localhost:5678`

In n8n, create a workflow:
- **Webhook node** → listens for trigger
- **HTTP Request node** → POST to `http://127.0.0.1:8000/pipelines/execute`

---

## 🧪 Example API Request

```json
POST /pipelines/execute

{
  "nodes": [
    {"id": "1", "type": "input", "position": {"x": 0, "y": 0}, "data": {"value": "Hello World!"}},
    {"id": "2", "type": "transform", "position": {"x": 200, "y": 0}, "data": {"operation": "uppercase"}},
    {"id": "3", "type": "output", "position": {"x": 400, "y": 0}, "data": {}}
  ],
  "edges": [
    {"id": "e1", "source": "1", "target": "2"},
    {"id": "e2", "source": "2", "target": "3"}
  ]
}
```

**Response:**
```json
{
  "status": "completed",
  "num_nodes": 3,
  "num_edges": 2,
  "execution_log": [
    {"node_id": "1", "node_type": "input", "status": "success", "output": {"output": "Hello World!"}},
    {"node_id": "2", "node_type": "transform", "status": "success", "output": {"output": "HELLO WORLD!"}},
    {"node_id": "3", "node_type": "output", "status": "success", "output": {"final": true}}
  ]
}
```

---

## 🚀 Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| React | UI framework |
| React Flow | Visual node editor |
| Zustand | Global state management |
| JavaScript | Programming language |

### Backend
| Technology | Purpose |
|-----------|---------|
| Python | Programming language |
| FastAPI | REST API framework |
| Pydantic | Data validation |
| httpx | Async HTTP client |

### Automation & Integration
| Technology | Purpose |
|-----------|---------|
| n8n | Webhook trigger + HTTP Request |

### Algorithms
| Algorithm | Purpose |
|-----------|---------|
| Directed Acyclic Graph (DAG) | Pipeline structure |
| Kahn's Topological Sort | Cycle detection + execution order |
| Dependency Resolution | Node execution ordering |

---

## 🧠 What This Project Demonstrates

- Full-stack frontend + backend integration
- Visual workflow design systems
- Graph-based pipeline modeling
- DAG validation using Kahn's Topological Sorting Algorithm
- Pipeline execution engine with node-to-node data flow
- Event-driven architecture with webhook triggers
- n8n integration for external workflow triggering
- Debugging, logging, and system reliability
- Scalable and modular UI component architecture

---

## 🔮 Future Improvements

- Workflow scheduling (cron-style triggers)
- Retry and failure recovery per node
- Persistent workflow storage (MongoDB/PostgreSQL)
- Authentication and user management
- Real-time monitoring dashboard
- AI-powered nodes (LLM, embeddings)
- More n8n node integrations

---

## 🎯 Why This Project Matters

This project demonstrates the core concepts behind modern workflow automation platforms — visual pipeline design, DAG-based execution, webhook triggers, and real-time logging. It shows how complex business processes can be automated reliably and at scale using event-driven architecture.