# 🤖 RAG Chatbot

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

A **Retrieval-Augmented Generation (RAG)** chatbot that lets you chat with your PDF documents using Google's Gemini AI.

---

## ✨ Features

- 📄 **PDF Upload** - Drag & drop your documents
- 🧠 **Smart Context** - ChromaDB vector store for semantic search
- 💬 **Natural Chat** - Ask questions in plain English
- ⚡ **Fast Responses** - Powered by Gemini 2.5 Flash
- 🐳 **Docker Ready** - One command deployment
- 📊 **Document Stats** - Track uploaded files & chunks

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/DanielRad111/RAG-Chatbot.git
cd RAG-Chatbot

# Configure API key
cp .env.example .env
# Edit .env and add your Google API key

# Run with Docker
docker-compose up --build -d
```

🌐 Open **http://localhost:8501**

### Option 2: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp config.example.py config.py
# Edit config.py and add your Google API key

# Run the app
streamlit run main.py
```

---

## 🔑 Get Your API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy the key to your `.env` or `config.py` file

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web UI Framework |
| **Google Gemini** | LLM & Embeddings |
| **ChromaDB** | Vector Database |
| **LangChain** | Document Processing |
| **Docker** | Containerization |

---

## 📁 Project Structure

```
RAG-Chatbot/
├── main.py              # Main application
├── config.py            # API keys (gitignored)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container definition
├── docker-compose.yml   # Docker orchestration
├── docs/                # Uploaded PDFs
└── README.md
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 👤 Author

**Daniel Rad**

- GitHub: [@DanielRad111](https://github.com/DanielRad111)

---

<p align="center">
  Made with ❤️ and ☕
</p>
