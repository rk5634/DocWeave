# graph/state.py

from typing import TypedDict, List, Dict, Optional


class GraphState(TypedDict, total=False):
    """
    Shared state passed between LangGraph nodes.
    """

    
    # User Input
    question: str

    
    # Retrieval Output
    documents: List[Dict]

    
    # Generation Output
    answer: str
    used_context: List[Dict]

    
    # Validation Output
    validation: Dict

    
    # Control Flow
    
    retry_count: int

    
    # Final Output
    final_answer: Optional[str]
