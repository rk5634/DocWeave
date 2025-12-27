# frontend/components/chat.py

import streamlit as st


def render_chat(chat_service):
    st.header("💬 Chat with Your Documents")

    if not st.session_state.documents_ingested:
        st.warning("Ingest a document before asking questions.")
        return

    # Render chat history
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

    # Chat input
    question = st.chat_input("Ask a question about the document...")

    if question:
        # User message
        st.session_state.chat_history.append(
            {"role": "user", "content": question}
        )
        with st.chat_message("user"):
            st.markdown(question)

        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_service.chat(question)
                answer = response.get("answer", "Something went wrong.")
                st.markdown(answer)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )
