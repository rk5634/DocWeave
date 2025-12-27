from langgraph.graph import StateGraph, END

from graph.state import GraphState
from graph.nodes import (
    retriever_node,
    generator_node,
    validator_node,
    responder_node,
    retry_node,
)
from graph.edges import route_after_validation


def build_workflow():
    graph = StateGraph(GraphState)

    # Nodes
    graph.add_node("retriever", retriever_node)
    graph.add_node("generator", generator_node)
    graph.add_node("validator", validator_node)
    graph.add_node("retry", retry_node)
    graph.add_node("responder", responder_node)

    # Entry
    graph.set_entry_point("retriever")

    # Linear flow
    graph.add_edge("retriever", "generator")
    graph.add_edge("generator", "validator")

    # Conditional routing
    graph.add_conditional_edges(
        "validator",
        route_after_validation,
        {
            "retry_generator": "retry",
            "final_responder": "responder",
        },
    )

    # Retry path
    graph.add_edge("retry", "generator")

    # Exit
    graph.add_edge("responder", END)

    return graph.compile()


def run_workflow(question: str) -> str:
    app = build_workflow()

    final_state = app.invoke(
        {
            "question": question,
            "retry_count": 0,
        }
    )

    return final_state.get("final_answer", "")
