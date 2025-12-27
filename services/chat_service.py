# services/chat_service.py

from services.intent_service import IntentService
from rag.retriever import RetrieverAgent
from rag.generator import GeneratorAgent
from graph.workflow import run_workflow


SUMMARY_KEYWORDS = {
    "summary",
    "summarize",
    "summarise",
    "overview",
    "gist",
    "what is this document about",
}


class ChatService:
    def __init__(self):
        self.intent_service = IntentService()
        self.retriever = RetrieverAgent()
        self.generator = GeneratorAgent()

    def chat(self, question: str) -> dict:
        q_lower = question.lower().strip()

        # 🔒 HARD SUMMARY ROUTE (cannot fail)
        if any(key in q_lower for key in SUMMARY_KEYWORDS):
            docs = self.retriever.retrieve(question, mode="summary")
            result = self.generator.generate(
                question=question,
                documents=docs,
                mode="summary",
            )
            return {
                "status": "success",
                "answer": result["answer"],
            }

        # LLM-based intent classification (secondary)
        intent = self.intent_service.classify(question)

        if intent.get("intent") == "general":
            return {
                "status": "success",
                "answer": intent.get(
                    "reply",
                    "Hello! You can ask me questions about the document."
                ),
            }

        # Default → strict agentic RAG
        answer = run_workflow(question)
        return {
            "status": "success",
            "answer": answer,
        }
