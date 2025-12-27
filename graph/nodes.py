# graph/nodes.py

from typing import Dict

from graph.state import GraphState
from rag.retriever import RetrieverAgent
from rag.generator import GeneratorAgent
from rag.validator import ValidatorAgent
from rag.responder import FinalResponseAgent



retriever_agent = RetrieverAgent()
generator_agent = GeneratorAgent()
validator_agent = ValidatorAgent()
responder_agent = FinalResponseAgent()


def retriever_node(state: GraphState) -> GraphState:
    """
    Retrieve relevant document chunks for the user's question.
    """

    documents = retriever_agent.retrieve(state["question"])
    return {
        **state,
        "documents": documents,
    }


def generator_node(state: GraphState) -> GraphState:
    """
    Generate an answer based on retrieved documents.
    """
    result = generator_agent.generate(
        question=state["question"],
        documents=state.get("documents", []),
    )


    return {
        **state,
        "answer": result["answer"],
        "used_context": result["used_context"],
    }


def validator_node(state: GraphState) -> GraphState:
    """
    Validate the generated answer against the document context.
    """
    validation = validator_agent.validate(
        question=state["question"],
        answer=state.get("answer", ""),
        documents=state.get("used_context", []),
    )


    return {
        **state,
        "validation": validation,
    }


def responder_node(state: GraphState) -> GraphState:
    """
    Produce the final user-facing answer.
    """
    final_answer = responder_agent.respond(
        answer=state.get("answer", ""),
        validation=state.get("validation", {}),
    )

    return {
        **state,
        "final_answer": final_answer,
    }


def retry_node(state: GraphState) -> GraphState:
    return {
        **state,
        "retry_count": state.get("retry_count", 0) + 1,
    }