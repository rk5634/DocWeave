# frontend/components/sidebar.py

import streamlit as st


def render_sidebar(ingestion_service):
    with st.sidebar:
        st.header("📂 Document Ingestion")

        uploaded_file = st.file_uploader(
            "Upload a PDF or image document",
            type=["pdf", "png", "jpg", "jpeg"],
        )

        if uploaded_file and st.button("Ingest Document"):
            with st.spinner("Processing document..."):
                try:
                    result = ingestion_service.ingest(uploaded_file)
                    st.session_state.documents_ingested = True

                    st.success(
                        f"Document ingested successfully. "
                        f"Chunks created: {result['num_chunks']}"
                    )
                except Exception as e:
                    st.error(f"Ingestion failed: {e}")

        if not st.session_state.documents_ingested:
            st.info("Please upload and ingest at least one document.")
