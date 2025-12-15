
import streamlit as st
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import GOOGLE_API_KEY, DB_NAME
from chromadb import Documents, EmbeddingFunction, Embeddings, Client
from google.api_core import retry
import os
from datetime import datetime


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_files_info' not in st.session_state:
    st.session_state.uploaded_files_info = {}

temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

genai.configure(api_key=GOOGLE_API_KEY) 

class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True
    
    def __call__(self, input: Documents) -> Embeddings:
        embedding_task = "retrieval_document" if self.document_mode else "retrieval_query"
        retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}
        
        response = genai.embed_content(
            model = "models/text-embedding-004",
            content = input,
            task_type = embedding_task,
            request_options=retry_policy,
        )
        
        return response["embedding"]

def initialize_page():
    st.set_page_config(
        page_title="AI Document Assistant",
        page_icon="📚",
        layout="wide"
    )
    

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("🤖 AI Document Assistant")
        st.markdown("""
        Upload your documents and let AI help you understand them better!
        - 📄 Supports PDF files
        - 💬 Natural conversation
        - 🔍 Smart search
        - 📊 Document analytics
        """)
    
    return col1, col2

def display_document_stats(col2):
    with col2:
        st.sidebar.title("📊 Document Statistics")
        if st.session_state.uploaded_files_info:
            for filename, info in st.session_state.uploaded_files_info.items():
                with st.sidebar.expander(f"📄 {filename}"):
                    st.write(f"Uploaded: {info['timestamp']}")
                    st.write(f"Chunks: {info['chunks']}")
                    st.write(f"Size: {info['size']:.2f} KB")

def process_uploaded_file(uploaded_file, db):

    file_stats = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'size': uploaded_file.size / 1024, 
        'chunks': 0
    }
    
    with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.read())
    
    loader = PyPDFLoader(os.path.join(temp_dir, uploaded_file.name))
    pdf_docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(pdf_docs)
    
    documents = [doc.page_content for doc in split_docs]
    file_stats['chunks'] = len(documents)
    
    st.session_state.uploaded_files_info[uploaded_file.name] = file_stats
    
    return documents

def get_ai_response(query, context, model):
    system_prompt = """You are an intelligent AI assistant specialized in analyzing documents and providing 
    comprehensive answers. Follow these guidelines:
    1. Always provide well-structured, clear answers
    2. If relevant, include specific references from the documents
    3. If the information is not in the context, clearly state that
    4. Use markdown formatting to make your answers more readable
    5. If appropriate, break down complex concepts into bullet points
    """
    
    prompt = f"{system_prompt}\n\nContext: {context}\n\nQuestion: {query}"
    
    response = model.generate_content(prompt)
    return response.text

def display_chat_history():
    for i, (query, response) in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(query)
        with st.chat_message("assistant"):
            st.markdown(response)

def main():
    col1, col2 = initialize_page()
    
    genai.configure(api_key=GOOGLE_API_KEY)
    embed_fn = GeminiEmbeddingFunction()
    chroma_client = Client()
    db = chroma_client.get_or_create_collection(name=DB_NAME, embedding_function=embed_fn)
    
    uploaded_files = st.file_uploader("📤 Upload PDF files", type="pdf", accept_multiple_files=True)
    
    if st.button("📥 Process Documents"):
        if uploaded_files:
            progress_bar = st.progress(0)
            for i, uploaded_file in enumerate(uploaded_files):
                documents = process_uploaded_file(uploaded_file, db)
                db.add(documents=documents, ids=[f"{uploaded_file.name}_{i}" for i in range(len(documents))])
                progress_bar.progress((i + 1) / len(uploaded_files))
            st.success("✅ Documents processed successfully!")
        else:
            st.warning("⚠️ Please upload at least one PDF document.")
    
    display_document_stats(col2)
    
    st.markdown("---")
    st.subheader("💬 Ask me anything about your documents")
    
    display_chat_history()
    
    query = st.text_input("Your question:", placeholder="e.g., What are the main topics covered in these documents?")
    
    if st.button("🔍 Get Answer"):
        if not query.strip():
            st.warning("⚠️ Please enter a question")
            return
            
        with st.spinner("🤔 Thinking..."):
            embed_fn.document_mode = False
            result = db.query(query_texts=[query], n_results=3)
            
            if result["documents"]:
                context = "\n".join(result["documents"][0])
                model = genai.GenerativeModel("gemini-2.5-flash")
                answer = get_ai_response(query, context, model)
                
                st.session_state.chat_history.append((query, answer))
                
                with st.chat_message("assistant"):
                    st.markdown(answer)
            else:
                st.error("❌ No relevant information found in the documents.")

if __name__ == "__main__":
    main()
        