<body>

<h1>🚦 Traffic Route Analyzer</h1>

<p>
The <strong>Traffic Route Analyzer</strong> is a backend service that:
</p>

<ul>
  <li>Optimizes traffic routing using <strong>PuLP</strong> (linear programming)</li>
  <li>Uses <strong>Groq Llama</strong> to generate human-readable explanations</li>
  <li>Provides a clean <strong>REST API</strong> with FastAPI</li>
  <li>Accepts nodes, edges, demand and performs min-cost flow optimization</li>
</ul>

<hr>

<h2>📁 Project Structure</h2>

<pre>
TRAFFIC_ROUTE_ANALYZER/
├── app.py                (FastAPI server + LLM explanation)
├── tools/
│   ├── solver_pulp.py    (PuLP optimization)
│   └── __init__.py
├── .env                  (GROQ_API_KEY)
├── requirements.txt
└── myvenv/               (optional virtual environment)
</pre>

<hr>

<h2>🧠 How It Works</h2>

<p>
The system performs:
</p>

<ol>
  <li>Input validation via FastAPI</li>
  <li>Min-cost flow optimization using PuLP</li>
  <li>LLM explanation generation using Groq's Llama model</li>
  <li>Returns both raw solver results and easy-to-understand text</li>
</ol>

<hr>

<h2>🔐 Environment Variables</h2>

<p>Create a <code>.env</code> file:</p>

<pre>
GROQ_API_KEY=your_groq_key_here
</pre>

<hr>

<h2>🚀 Running the Server</h2>

<pre>
uvicorn app:app --reload
</pre>

<p>API available at:</p>

<ul>
  <li><code>http://127.0.0.1:8000/</code></li>
  <li><code>http://127.0.0.1:8000/docs</code></li>
</ul>

<hr>

<h2>📡 API Endpoint</h2>

<h3><code>POST /solve-routing</code></h3>

<p>Solves a traffic optimization problem.</p>

<h3>Request Body</h3>

<pre>
{
  "nodes": ["A", "B", "C", "D"],
  "edges": [
    { "from_": "A", "to": "B", "capacity": 100, "cost": 4 },
    { "from_": "A", "to": "C", "capacity": 80,  "cost": 3 },
    { "from_": "B", "to": "D", "capacity": 70,  "cost": 2 },
    { "from_": "C", "to": "D", "capacity": 90,  "cost": 1 }
  ],
  "source": "A",
  "sink": "D",
  "demand": 120
}
</pre>

<h3>Example Response</h3>

<pre>
{
  "status": "success",
  "solver_result": {
    "status": "Optimal",
    "total_cost": 560.0,
    "flows": [
        { "from": "A", "to": "B", "flow": 40.0 },
        { "from": "A", "to": "C", "flow": 80.0 },
        { "from": "B", "to": "D", "flow": 40.0 },
        { "from": "C", "to": "D", "flow": 80.0 }
    ]
  },
  "llm_explanation": "This result is about finding the best way to route traffic..."
}
</pre>

<hr>

<h2>📐 Optimization Model (PuLP)</h2>

<p>The model creates a variable for each edge:</p>

<pre>flow[u,v] ≥ 0</pre>

<p>Main constraints:</p>

<ul>
  <li><strong>Capacity</strong>: flow ≤ capacity</li>
  <li><strong>Source</strong>: outflow − inflow = demand</li>
  <li><strong>Sink</strong>: inflow − outflow = demand</li>
  <li><strong>Intermediate nodes</strong>: inflow = outflow</li>
</ul>

<p><strong>Objective:</strong></p>

<pre>Minimize Σ (cost[u,v] × flow[u,v])</pre>

<hr>

<h2>🔮 Future Enhancements</h2>

<ul>
  <li>Tool-calling LLM agents (LangChain)</li>
  <li>Traffic visualization graph output</li>
  <li>Support multiple origin-destination pairs</li>
  <li>History logging with a database</li>
  <li>Web UI (React or Flutter)</li>
</ul>

<hr>

<p>
Built using FastAPI, PuLP, and Groq Llama.
</p>

</body>