from langgraph.graph import StateGraph, END
from core.models import WorkflowState
from core.state_manager import state_manager
from typing import Dict, Any

# We will implement the nodes (agents) in the `agents` folder.
# For now, we import them or define placeholders if they don't exist yet.
from agents.input_agent import node_input_agent
from agents.decision_agent import node_decision_agent
from agents.execution_agent import node_execution_agent
from agents.validation_agent import node_validation_agent
from agents.exception_agent import node_exception_agent
from agents.negotiation_agent import node_negotiation_agent

def route_decision(state: WorkflowState):
    """Router after the Decision Agent dynamically maps intent."""
    intent = state.get("intent", "unknown")
    if intent == "escalate" or state.get("exceptions"):
        return "exception_agent"
    return "execution_agent"

def route_validation(state: WorkflowState):
    """Router after Validation Agent."""
    score = state.get("validation_score", 0.0)
    
    # Mismatch logic (e.g., if score is low because of price discrepancy)
    if 0.5 < score < 0.8:
        return "negotiation_agent"
        
    if score >= 0.8:
        return END
    else:
        return "exception_agent"

def build_workflow_dag() -> StateGraph:
    """
    Constructs the dynamic multi-agent DAG.
    Explicit task graph enabling branching, retries, and context-awareness.
    """
    graph = StateGraph(WorkflowState)
    
    # Add Nodes (Role-Specialized Agents)
    graph.add_node("input_agent", node_input_agent)
    graph.add_node("decision_agent", node_decision_agent)
    graph.add_node("execution_agent", node_execution_agent)
    graph.add_node("validation_agent", node_validation_agent)
    graph.add_node("exception_agent", node_exception_agent)
    graph.add_node("negotiation_agent", node_negotiation_agent)
    
    # Define primary edge flow
    graph.set_entry_point("input_agent")
    
    # From input parsing to decision mapping
    graph.add_edge("input_agent", "decision_agent")
    
    # From decision to either execution or exception (context-aware branching)
    graph.add_conditional_edges(
        "decision_agent", 
        route_decision,
        {
            "execution_agent": "execution_agent",
            "exception_agent": "exception_agent"
        }
    )
    
    # From execution to validation
    graph.add_edge("execution_agent", "validation_agent")
    
    # From validation to End or Exception handling
    graph.add_conditional_edges(
        "validation_agent",
        route_validation,
        {
            END: END,
            "exception_agent": "exception_agent",
            "negotiation_agent": "negotiation_agent"
        }
    )
    
    # Negotiation agent goes to End (or could loop back)
    graph.add_edge("negotiation_agent", END)
    
    # Exception agent can loop back to decision agent (Self-healing retry) or exit
    # Simplification: looping back to decision_agent to re-plan
    def route_exception(state: WorkflowState):
        if len(state.get("exceptions", [])) > 3: # Escalate permanently
            return END
        # Self-healing loop
        return "decision_agent"
        
    graph.add_conditional_edges(
        "exception_agent",
        route_exception,
        {
            "decision_agent": "decision_agent",
            END: END
        }
    )
    
    # Compile with memory saver for reliable checkpoints and rollback capabilities
    return graph.compile(checkpointer=state_manager.get_checkpointer())

# Singleton compiled DAG
dag_app = build_workflow_dag()
