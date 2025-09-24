# chatbot/rag_pipeline.py
from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

load_dotenv()  # Load OPENAI_API_KEY


# 1. Load documents
def load_documents(filepath: str) -> List[Document]:
    loader = Docx2txtLoader(filepath)
    return loader.load()


# 2. Filter metadata
def filter_documents(docs: List[Document]) -> List[Document]:
    filtered_docs: List[Document] = []
    for doc in docs:
        source = doc.metadata.get("source")
        filtered_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": source}
            )
        )
    return filtered_docs


# 3. Split into chunks
def text_split(docs: List[Document]):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)


# 4. Build vectorstore
def build_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


# 5. Build Conversational Retrieval QA Chain with memory
def build_conversational_chain(vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    llm = ChatOpenAI()

    # ConversationalRetrievalChain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        verbose=True
    )
    return qa_chain


# 6. Full pipeline function
def run_rag(filepath: str, query: str, chain=None):
    if chain is None:
        docs = load_documents(filepath)
        filtered = filter_documents(docs)
        chunks = text_split(filtered)
        vector_store = build_vectorstore(chunks)
        chain = build_conversational_chain(vector_store)

    response = chain({"question": query})
    return response["answer"], chain
