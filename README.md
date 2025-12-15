# AI Document Assistant (RAG)
# RAG Project 📄🤖

A Retrieval-Augmented Generation (RAG) application that allows you to chat with your PDF documents using Google's Gemini Pro model.

## Features
- 📤 **PDF Upload**: Drag and drop support.
- 🧠 **Smart Context**: Uses ChromaDB to find relevant info.
- 💬 **Interactive Chat**: Ask questions about your documents.
- ⚡ **Fast & Efficient**: Built with Streamlit and Gemini.

## 🚀 Quick Start (Python)

The easiest way to run the app:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   - Open `config.py` and add your Google API Key.

3. **Run the App**:
   ```bash
   streamlit run main.py
   ```
   
   Access at `http://localhost:8501`.

## 🐳 Docker Deployment (Optional)

To run the application in a container (Deployment Ready/CV Ready):

*Instructions coming soon...*
for production deployment.

## How to Run

### Option 1: Next.js App (Docker) - Recommended
This version is production-ready and runs in a container.

1. Go to the Next.js directory:
   ```bash
   cd rag-nextjs
   ```
2. Start with Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
3. Open `http://localhost:3000`.

### Option 2: Python Streamlit App
This version runs locally using Python.

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run main.py
   ```
3. Open `http://localhost:8501`.
