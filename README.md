# Agentic RAG System with OCR

**LangGraph · DeepSeek OCR · ChromaDB**

----------

## 1. Overview

This project implements a **Retrieval-Augmented Generation (RAG) system** that enables users to upload documents (PDFs or images), extract text using **OCR**, and **interact conversationally with the document content** via an **agentic workflow orchestrated using LangGraph**.

The system mirrors **real-world AI system architecture**, with emphasis on:

-   Unstructured document ingestion
    
-   OCR-driven text extraction
    
-   Persistent vector search
    
-   LLM-based question answering
    
-   Agentic control flow with validation and retries
    

A **Streamlit-based frontend** is included for interactive use.

----------

## 2. Key Features

### 2.1 Document Ingestion

-   Supports standard PDFs, scanned PDFs, and image documents
    

### 2.2 OCR (Mandatory)

-   Uses **DeepSeek OCR** via DeepInfra’s OpenAI-compatible API
    

### 2.3 Text Processing

-   OCR normalization and cleanup
    
-   Paragraph-aware semantic chunking
    

### 2.4 Embeddings & Vector Store

-   OpenAI embeddings
    
-   Persistent **ChromaDB** vector store
    

### 2.5 Agentic RAG Pipeline (LangGraph)

-   Retriever Agent
    
-   Generator Agent
    
-   Validator Agent (hallucination & grounding checks)
    
-   Final Response Agent
    
-   Conditional routing with retry logic
    

### 2.6 Frontend

-   Streamlit UI for document upload and chat
    

### 2.7 Secure Configuration

-   Environment variables only
    
-   No hardcoded credentials
    

----------

## 3. System Architecture

### 3.1 High-Level Flow

User uploads document
        ↓
Document Loader
        ↓
OCR (DeepSeek OCR)
        ↓
Text Cleaning
        ↓
Semantic Chunking
        ↓
Embeddings
        ↓
ChromaDB (Persistent)
        ↓
User asks a question
        ↓
LangGraph Agentic Workflow
        ↓
Validated Answer
 

----------

## 4. Agentic Workflow (LangGraph)

The core logic is implemented as a **LangGraph-based agentic workflow**.

### 4.1 Agents / Nodes

1.  **Retriever Agent**
    
    -   Retrieves top-K relevant chunks from ChromaDB
        
2.  **Generator Agent**
    
    -   Uses GPT-4o-mini
        
    -   Produces answers strictly grounded in retrieved context
        
3.  **Validator Agent**
    
    -   Verifies grounding and relevance
        
    -   Conservatively detects hallucinations
        
4.  **Final Response Agent**
    
    -   Produces the final, user-facing answer
        

### 4.2 Control Flow Logic

-   Shared state is propagated across agents
    
-   Validation outcome determines routing
    
-   If validation fails and retry limits are not exceeded:
    
    -   Answer generation is retried
        
-   Otherwise:
    
    -   Workflow terminates with a final response
        

This design fulfills the requirement for **conditional transitions and retry loops**.

----------

## 5. Project Structure

rag-langgraph-ocr/
│
├── config/        # Configuration and prompts
├── data/          # Raw files, OCR output, processed text, ChromaDB
├── ingestion/     # Loader, OCR, cleaning, chunking
├── embeddings/    # Embedding abstraction and vector store
├── rag/           # Retriever, generator, validator, responder
├── graph/         # LangGraph state, nodes, edges, workflow
├── services/      # Ingestion and chat service layer
├── frontend/      # Streamlit app (component-based)
├── requirements.txt
└── README.md


----------

## 6. OCR Choice: DeepSeek OCR

The assignment mandates **DeepSeek OCR**.

This system integrates **DeepSeek OCR via DeepInfra**, using an OpenAI-compatible API:

-   Supports image URLs and base64-encoded images
    
-   Handles scanned PDFs via PDF-to-image conversion
    
-   Isolated cleanly in `ingestion/ocr.py`
    

The OCR layer is modular and can be swapped without affecting downstream components.

----------

## 7. Configuration & Environment Variables

All configuration is provided via environment variables.

### Example `.env`

`OPENAI_API_KEY=your_openai_key_here DEEPSEEK_API_KEY=your_deepinfra_key_here` 

No secrets are hardcoded anywhere in the codebase.

----------

## 8. Running the Application

### 8.1 Install Dependencies

`pip install -r requirements.txt` 

> **Note**: `pdf2image` requires **Poppler** to be installed on the system.

### 8.2 Start the Application

`streamlit run frontend/app.py` 

### 8.3 Usage Flow

1.  Upload a PDF or image document
    
2.  Click **Ingest Document**
    
3.  Ask questions about the document
    
4.  Receive validated, grounded answers
    

----------

## 9. Design Decisions & Rationale

-   **Agent Separation**  
    Each responsibility (retrieval, generation, validation, response) is isolated.
    
-   **Validation-Driven Retries**  
    Retries occur only when grounding or hallucination checks fail.
    
-   **Persistent Vector Store**  
    ChromaDB persistence ensures cross-session document availability.
    
-   **Service Layer Abstraction**  
    The frontend communicates exclusively with service interfaces.
    
-   **Deterministic Behavior**  
    Low-temperature generation and conservative validation reduce hallucinations.
