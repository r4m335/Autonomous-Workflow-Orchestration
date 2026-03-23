from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from core.models import WorkflowState
from core.state_manager import state_manager
from core.logger import logger
from core.config import settings

# Import agent nodes
from agents.input_agent import node_input_agent
from agents.decision_agent import node_decision_agent
from agents.execution_agent import node_execution_agent
from agents.validation_agent import node_validation_agent
from agents.exception_agent import node_exception_agent
from agents.negotiation_agent import node_negotiation_agent

def orchestrate_workflow():
    workflow = StateGraph(WorkflowState)

    # Add Nodes
    workflow.add_node("input", node_input_agent)
    workflow.add_node("decision", node_decision_agent)
    workflow.add_node("execution", node_execution_agent)
    workflow.add_node("validation", node_validation_agent)
    workflow.add_node("exception", node_exception_agent)
    workflow.add_node("negotiation", node_negotiation_agent)

    # Define Edges
    workflow.set_entry_point("input")
    workflow.add_edge("input", "decision")
    workflow.add_edge("decision", "execution")
    workflow.add_edge("execution", "validation")

    # Routing Logic
    def route_after_validation(state: WorkflowState):
        score = state.get("validation_score", 0)
        logger.info(f"Routing logic (Score: {score})", thread_id=state.get("job_id", "unknown"))
        
        if score >= settings.validation_threshold:
            return END
        elif 0.5 <= score < settings.validation_threshold:
            return "negotiation"
        else:
            return "exception"

    workflow.add_conditional_edges("validation", route_after_validation, {
        END: END,
        "negotiation": "negotiation",
        "exception": "exception"
    })

    workflow.add_edge("negotiation", END)
    workflow.add_edge("exception", END)

    return workflow.compile(checkpointer=state_manager.get_checkpointer())

dag_app = orchestrate_workflow()
