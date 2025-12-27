# graph/edges.py

from graph.state import GraphState
from config.settings import MAX_GENERATION_RETRIES


def route_after_validation(state: GraphState) -> str:
    """
    Decide next step after validation.

    Returns:
        - "retry_generator": if answer is invalid and retries remain
        - "final_responder": otherwise
    """
    validation = state.get("validation", {})
    retry_count = state.get("retry_count", 0)

    is_valid = validation.get("is_valid", False)

    if not is_valid and retry_count < MAX_GENERATION_RETRIES:
        return "retry_generator"

    return "final_responder"


def increment_retry(state: GraphState) -> GraphState:
    """
    Increment retry counter when retrying generation.
    """
    return {
        **state,
        "retry_count": state.get("retry_count", 0) + 1,
    }
