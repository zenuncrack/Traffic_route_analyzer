import os
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel
from typing import List, Dict

from tools.solver_pulp import solve_routing



load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise ValueError("Missing GROQ_API_KEY")


class Edge(BaseModel):
    from_: str
    to: str
    capacity: float
    cost: float

class RoutingInput(BaseModel):
    nodes: List[str]
    edges: List[Edge]
    source: str
    sink: str
    demand: float



llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_KEY,
    temperature=0
)



app = FastAPI(title="Traffic Routing AI")


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/solve-routing")
def solve_route(input_data: RoutingInput):
    """Solve routing directly + LLM explanation."""

    edges = [
        {"from": e.from_, "to": e.to, "capacity": e.capacity, "cost": e.cost}
        for e in input_data.edges
    ]

    result = solve_routing(
        nodes=input_data.nodes,
        edges=edges,
        source=input_data.source,
        sink=input_data.sink,
        demand=input_data.demand
    )

    explanation = llm.invoke(
        f"Explain this traffic routing result in simple English:\n{result}"
    )

    return {
        "solver_result": result,
        "llm_explanation": explanation.content
    }
