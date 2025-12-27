# frontend/app.py

import streamlit as st

from services.ingestion_service import IngestionService
from services.chat_service import ChatService
from frontend.state import init_session_state
from frontend.components.sidebar import render_sidebar
from frontend.components.chat import render_chat


st.set_page_config(
    page_title="Agentic RAG with OCR",
    layout="wide",
)


def main():
    init_session_state()

    ingestion_service = IngestionService()
    chat_service = ChatService()

    st.title("📄 Agentic RAG System with OCR")
    st.caption(
        "Upload documents and chat with their content using an agentic LangGraph workflow."
    )

    render_sidebar(ingestion_service)
    render_chat(chat_service)


if __name__ == "__main__":
    main()
