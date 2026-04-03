from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from collections import defaultdict
import httpx
import asyncio

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ─── Models ───────────────────────────────────────────────────────────────────

class Edge(BaseModel):
    id: str
    source: str
    target: str
    type: str = None


class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, Any]
    data: Dict[str, Any] = {}


class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


class ExecutionResult(BaseModel):
    node_id: str
    node_type: str
    status: str          # "success" or "failed"
    output: Any
    error: Optional[str] = None


# ─── DAG Validation (your original code) ──────────────────────────────────────

def is_dag(nodes: List[Node], edges: List[Edge]) -> bool:
    """Check if the graph is a DAG using Kahn's algorithm."""
    if not nodes:
        return True

    adjacency = defaultdict(list)
    in_degree = defaultdict(int)

    for node in nodes:
        in_degree[node.id] = 0

    for edge in edges:
        adjacency[edge.source].append(edge.target)
        in_degree[edge.target] += 1

    queue = [node_id for node_id in in_degree if in_degree[node_id] == 0]
    visited_count = 0

    while queue:
        current = queue.pop(0)
        visited_count += 1
        for neighbor in adjacency[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited_count == len(nodes)


# ─── Topological Sort ─────────────────────────────────────────────────────────

def topological_sort(nodes: List[Node], edges: List[Edge]) -> List[str]:
    """Return node IDs in topological execution order using Kahn's algorithm."""
    adjacency = defaultdict(list)
    in_degree = defaultdict(int)

    for node in nodes:
        in_degree[node.id] = 0

    for edge in edges:
        adjacency[edge.source].append(edge.target)
        in_degree[edge.target] += 1

    queue = [node_id for node_id in in_degree if in_degree[node_id] == 0]
    order = []

    while queue:
        current = queue.pop(0)
        order.append(current)
        for neighbor in adjacency[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order


# ─── Node Executors ───────────────────────────────────────────────────────────

async def execute_node(node: Node, input_data: Any) -> Any:
    """Execute a single node based on its type and return output data."""

    node_type = node.type.lower()

    # INPUT NODE — provides initial data
    if node_type in ["custominput", "input"]:
        value = node.data.get("value", "Hello from Input Node!")
        return {"output": value}

    # TRANSFORM NODE — modifies incoming data
    elif node_type in ["customtransform", "transform"]:
        operation = node.data.get("operation", "uppercase")
        text = str(input_data.get("output", input_data)) if isinstance(input_data, dict) else str(input_data)
        if operation == "uppercase":
            return {"output": text.upper()}
        elif operation == "lowercase":
            return {"output": text.lower()}
        elif operation == "reverse":
            return {"output": text[::-1]}
        else:
            return {"output": text}

    # MATH NODE — performs arithmetic
    elif node_type in ["custommath", "math"]:
        operation = node.data.get("operation", "add")
        a = float(node.data.get("a", 0))
        b = float(node.data.get("b", 0))
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            result = a / b if b != 0 else "Error: division by zero"
        else:
            result = a + b
        return {"output": result}

    # API NODE — calls an external API
    elif node_type in ["customapi", "api"]:
        url = node.data.get("url", "https://jsonplaceholder.typicode.com/posts/1")
        method = node.data.get("method", "GET").upper()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if method == "GET":
                    response = await client.get(url)
                elif method == "POST":
                    response = await client.post(url, json=input_data)
                else:
                    response = await client.get(url)
            return {"output": response.json(), "status_code": response.status_code}
        except Exception as e:
            return {"output": None, "error": str(e)}

    # CONDITION NODE — branching logic
    elif node_type in ["customcondition", "condition"]:
        condition_field = node.data.get("field", "output")
        condition_value = node.data.get("value", "")
        actual_value = str(input_data.get(condition_field, "")) if isinstance(input_data, dict) else str(input_data)
        passed = actual_value == condition_value
        return {"output": input_data, "condition_passed": passed}

    # OUTPUT NODE — returns final result
    elif node_type in ["customoutput", "output"]:
        return {"output": input_data, "final": True}

    # TEXT NODE — handles text input
    elif node_type in ["customtext", "text"]:
        text = node.data.get("text", "")
        return {"output": text}

    # UNKNOWN NODE TYPE
    else:
        return {"output": input_data, "note": f"Unknown node type: {node.type}"}


# ─── Execution Engine ─────────────────────────────────────────────────────────

async def execute_pipeline(nodes: List[Node], edges: List[Edge]) -> List[ExecutionResult]:
    """Execute all nodes in topological order, passing data between them."""

    order = topological_sort(nodes, edges)
    node_map = {node.id: node for node in nodes}

    # Build adjacency: which node feeds into which
    sources_of = defaultdict(list)   # node_id -> list of source node_ids
    for edge in edges:
        sources_of[edge.target].append(edge.source)

    results: Dict[str, Any] = {}     # node_id -> output data
    execution_log: List[ExecutionResult] = []

    for node_id in order:
        node = node_map[node_id]

        # Gather input from parent nodes
        parent_ids = sources_of[node_id]
        if parent_ids:
            # Use the last parent's output as input (simple chaining)
            input_data = results.get(parent_ids[-1], {})
        else:
            input_data = {}

        try:
            output = await execute_node(node, input_data)
            results[node_id] = output
            execution_log.append(ExecutionResult(
                node_id=node_id,
                node_type=node.type,
                status="success",
                output=output
            ))
        except Exception as e:
            results[node_id] = {}
            execution_log.append(ExecutionResult(
                node_id=node_id,
                node_type=node.type,
                status="failed",
                output=None,
                error=str(e)
            ))

    return execution_log


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}


@app.post('/pipelines/parse')
def parse_pipeline(pipeline: Pipeline):
    """Original endpoint — validates DAG structure."""
    try:
        num_nodes = len(pipeline.nodes)
        num_edges = len(pipeline.edges)
        is_dag_result = is_dag(pipeline.nodes, pipeline.edges)

        return {
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'is_dag': is_dag_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing pipeline: {str(e)}")


@app.post('/pipelines/execute')
async def execute_pipeline_endpoint(pipeline: Pipeline):
    """NEW endpoint — validates and executes the pipeline node by node."""
    try:
        # Step 1: Validate DAG first
        if not is_dag(pipeline.nodes, pipeline.edges):
            raise HTTPException(status_code=400, detail="Pipeline contains a cycle. Cannot execute.")

        # Step 2: Execute nodes in order
        logs = await execute_pipeline(pipeline.nodes, pipeline.edges)

        # Step 3: Return execution results
        return {
            "status": "completed",
            "num_nodes": len(pipeline.nodes),
            "num_edges": len(pipeline.edges),
            "execution_log": [log.dict() for log in logs]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")