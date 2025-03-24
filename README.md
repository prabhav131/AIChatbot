# 🤖 AI Chatbot  

## 🚀 About  

This repository contains an **AI-powered chatbot** that understands natural language, processes queries, and provides intelligent responses. It can be integrated into various applications, such as customer support, personal assistants, and automation workflows.  

## 🔹 Features  

- ✅ **Natural Language Understanding (NLU)** – Detects user intent and extracts key entities.  
- ✅ **Multi-Intent Handling** – Routes queries to appropriate modules (e.g., RAG, email, API calls).  
- ✅ **Memory & Context Awareness** – Maintains conversation history for better responses.  
- ✅ **Retrieval-Augmented Generation (RAG)** – Fetches relevant documents for knowledge-based answers.  
- ✅ **Extensible Architecture** – Supports additional tools like scheduling, automation, and more.

Frameworks used:
    - langchain
    - ollama
    - FAISS
    - spacy

LLMs tested:
    - phi3 mini
    - tinyllama
    - tinydolphin
    - phi1.5
    - orca mini
    - dolphin-phi

LLMs used in this version:
    - orca mini
    - dolphin-phi
    - tinydolphin


Instructions to run the code:

1. Create a virtual enviornment inside the repo after cloning the repo
2. install the requirements using "pip install -r requirements.txt"
3. run  "ollama pull tinydolphin" to install the model locally
4. run  "ollama pull orca-mini" to install the model locally
5. run  "ollama pull dolphin-phi" to install the model locally
6. run "python chatbot.py" and start conversing
