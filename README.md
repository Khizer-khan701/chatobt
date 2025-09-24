# 🤖 AI Document Q&A Chatbot

A simple **Django-based AI chatbot** that answers questions based on pre-loaded documents using **LangChain** and **OpenAI GPT**. Users can ask questions, and the chatbot retrieves answers from a **FAISS vector database** using **RAG (Retrieval-Augmented Generation)**.

---

## 🌟 Features

- Ask questions in natural language about your documents.  
- Semantic search with **FAISS** for accurate retrieval.  
- Context-aware answers powered by **LangChain + ChatOpenAI**.  
- Minimal, responsive, and **beautiful UI** built with **Bootstrap 5**.  
- Easy deployment using **Docker**.  

---

---

## ⚡ Installation & Setup

 **Clone the repository**

```bash
git clone https://github.com/Khizer-khan701/chatobt
cd chatbot
```


## Create a virtual environment & activate
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```
## Install dependencies
```bash
pip install -r requirements.txt
```

## Add environment variables in .env
OPENAI_API_KEY=your_openai_api_key

## Run Django migrations
python manage.py migrate

## Start the development server
python manage.py runserver

Visit http://127.0.0.1:8000/ask/
 to interact with the chatbot.