# rag/responder.py

from typing import Dict


class FinalResponseAgent:
    """
    Returns the final, user-facing response after validation.
    """

    def respond(
        self,
        answer: str,
        validation: Dict,
    ) -> str:
        """
        Produce the final response to the user.
        """
        if not validation.get("is_valid", False):
            return (
                "I’m unable to provide a reliable answer to this question "
                "based on the document content."
            )

        return answer.strip()
