
# Agentic RAG System with OCR (LangGraph + DeepSeek + ChromaDB)

## Overview

This project implements a **Retrieval-Augmented Generation (RAG) system** that allows users to upload documents (PDFs or images), extract text using **OCR**, and **chat with the document content** through an **agentic workflow orchestrated with LangGraph**.

The system is designed to reflect **real-world AI system architecture**, emphasizing:

-   Unstructured document ingestion
    
-   OCR-based text extraction
    
-   Vector search with persistence
    
-   LLM-based question answering
    
-   Agentic control flow with validation and retries
    

A **Streamlit frontend** is provided for interactive usage.

----------

## Key Features

-   **Document ingestion**
    
    -   Supports standard PDFs, scanned PDFs, and image documents
        
-   **OCR (Mandatory)**
    
    -   Uses **DeepSeek OCR** via DeepInfra’s OpenAI-compatible API
        
-   **Text processing**
    
    -   OCR normalization and cleanup
        
    -   Paragraph-aware semantic chunking
        
-   **Embeddings & Vector Store**
    
    -   OpenAI embeddings
        
    -   Persistent **ChromaDB** vector store
        
-   **Agentic RAG Pipeline (LangGraph)**
    
    -   Retriever Agent
        
    -   Generator Agent
        
    -   Validator Agent (hallucination & grounding check)
        
    -   Final Response Agent
        
    -   Conditional routing + retry loop
        
-   **Frontend**
    
    -   Streamlit UI for upload and chat
        
-   **Secure configuration**
    
    -   Environment variables only (no hardcoded credentials)
        

----------

## System Architecture

### High-Level Flow

`User uploads document
        ↓
Document Loader
        ↓
OCR (DeepSeek OCR)
        ↓ Text Cleaning
        ↓
Semantic Chunking
        ↓
Embeddings
        ↓
ChromaDB (Persistent)
        ↓ User asks a question
        ↓
LangGraph Agentic Workflow
        ↓
Validated Answer` 

----------

## Agentic Workflow (LangGraph)

The core of the system is a **LangGraph-based agentic workflow**.

### Agents / Nodes

1.  **Retriever Agent**
    
    -   Fetches top-K relevant chunks from ChromaDB
        
2.  **Generator Agent**
    
    -   Uses GPT-4o-mini
        
    -   Generates answers strictly grounded in retrieved context
        
3.  **Validator Agent**
    
    -   Verifies answer grounding and relevance
        
    -   Detects hallucinations conservatively
        
4.  **Final Response Agent**
    
    -   Returns a clean, user-facing answer
        

### Control Flow Logic

-   Shared state is passed between agents
    
-   Validation outcome determines the next step
    
-   If validation fails and retry limit is not reached:
    
    -   The system retries answer generation
        
-   Otherwise:
    
    -   The workflow terminates with a final response
        

This satisfies the requirement for **conditional transitions and retry loops**.

----------

## Project Structure

`rag-langgraph-ocr/
│
├── config/ # Configuration & prompts ├── data/ # Raw data, OCR output, processed text, ChromaDB ├── ingestion/ # Loader, OCR, cleaning, chunking ├── embeddings/ # Embedder abstraction + vector store ├── rag/ # Retriever, generator, validator, responder ├── graph/ # LangGraph state, nodes, edges, workflow ├── services/ # Ingestion & chat service layer ├── frontend/ # Streamlit app (component-based) ├── requirements.txt
└── README.md` 

----------

## OCR Choice: DeepSeek OCR

The assignment specifies **DeepSeek OCR as mandatory**.

This system uses **DeepSeek OCR via DeepInfra**, leveraging their OpenAI-compatible API:

-   Supports image URLs and base64 image payloads
    
-   Works for scanned PDFs (via PDF → image conversion)
    
-   Cleanly isolated in `ingestion/ocr.py`
    

The OCR layer is modular and could be swapped if required, without changing downstream logic.

----------

## Configuration & Environment Variables

All credentials and configuration are loaded from environment variables.

Example `.env` file:

`OPENAI_API_KEY=your_openai_key_here
DEEPSEEK_API_KEY=your_deepinfra_key_here` 

No secrets are hardcoded anywhere in the codebase.

----------

## Running the Application

### 1. Install dependencies

`pip install -r requirements.txt` 

> Note: `pdf2image` requires **Poppler** installed on your system.

### 2. Start the Streamlit app

`streamlit run frontend/app.py` 

### 3. Usage

1.  Upload a PDF or image document
    
2.  Click **Ingest Document**
    
3.  Ask questions about the document content
    
4.  Receive validated, grounded answers
    

----------

## Design Decisions & Rationale

-   **Agent separation**  
    Each responsibility (retrieve, generate, validate, respond) is isolated to its own agent.
    
-   **Validation-driven retries**  
    Retries are only triggered when the validator detects hallucination or lack of grounding.
    
-   **Persistent vector store**  
    ChromaDB persistence ensures documents remain searchable across sessions.
    
-   **Service layer abstraction**  
    Frontend communicates only with service interfaces, not internal logic.
    
-   **Deterministic behavior**  
    Low temperature generation and conservative validation reduce hallucinations.# Agentic RAG System with OCR (LangGraph + DeepSeek + ChromaDB)