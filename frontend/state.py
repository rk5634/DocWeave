# frontend/state.py

import streamlit as st


def init_session_state():
    if "documents_ingested" not in st.session_state:
        st.session_state.documents_ingested = False

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
