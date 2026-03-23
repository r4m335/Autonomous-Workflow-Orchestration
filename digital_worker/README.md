# Adaptive Digital Worker Platform for BPOs & ITeS

This platform provides a highly resilient, **Adaptive Multi-Agent Execution Engine** designed to automate complex, multi-step workflows in the BPO and ITeS sectors. Unlike traditional RPA, this system uses agentic AI to reason under uncertainty, handle messy inputs, and adapt to system changes without manual reprogramming.

## Key Features

- **Adaptive Multi-Agent Architecture**: Built with LangGraph, featuring specialized agents for Input Parsing, Dynamic Decision Mapping, UI/API Execution, Validation, and Exception/Negotiation handling.
- **Dynamic DAG Generation**: Workflows are not hardcoded; the Decision Agent maps intent to a Directed Acyclic Graph (DAG) on the fly.
- **Self-Healing & Human-in-the-Loop**: The Exception Agent detects anomalies and low-confidence validations, attempting self-healing retry loops or escalating to a human queue.
- **Shared Persistent Memory**: Uses ChromaDB for vector-based context sharing and historical pattern mining.
- **Hybrid Automation**: Seamlessly switches between API calls and Playwright-based browser automation for legacy systems.
- **Observability Dashboard**: Real-time visualization of workflow execution and detailed audit trails.

## Project Structure

```text
digital_worker/
├── agents/             # Role-specialized agents (Input, Decision, Execution, etc.)
├── api/                # FastAPI backend, Dashboard UI, and Connectors
├── core/               # LangGraph DAG engine, State Manager, and Models
├── database/           # SQLite schema and audit logging logic
├── memory/             # ChromaDB vector store and pattern mining
├── workflows/          # Declarative JSON workflow definitions
├── requirements.txt    # Project dependencies
└── README.md           # You are here
```

## Getting Started

### 1. Installation
```powershell
pip install -r requirements.txt
playwright install chromium
```

### 2. Run the Platform
```powershell
# Start the FastAPI server with the Dashboard
python api/main.py
```

### 3. Access the Control Panel
Open your browser to:
- **Dashboard**: [http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html)
- **API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4. Run Tests
```powershell
python test_advanced_dag.py
python test_negotiation.py
```

## 50% Workforce Reduction Claim
By automating the "swivel chair" work and handling exceptions autonomously, this platform allows IT firms to move from selling man-hours to selling outcomes, enabling projects to be delivered with significantly fewer junior resources.
