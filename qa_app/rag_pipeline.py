# chatbot/rag_pipeline.py
from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()  # load your .env with OPENAI_API_KEY


# 1. Load documents (DOCX here, you can add PDF/TXT too)
def load_documents(filepath: str) -> List[Document]:
    loader = Docx2txtLoader(filepath)
    return loader.load()


# 2. Filter documents (keep only page_content + source metadata)
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


# 3. Split text into chunks
def text_split(docs: List[Document]):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)


# 4. Build VectorStore + Retriever
def build_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    return retriever


# 5. Create the QA Chain
def build_qa_chain(retriever):
    system_prompt = """
    You are a helpful assistant.
    You must only answer from the given text.
    If you don't have sufficient context, just say "I don't know".
    {context}\n
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    model = ChatOpenAI()
    question_answer_chain = create_stuff_documents_chain(model, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    return rag_chain


# 6. Full pipeline function
def run_rag(filepath: str, query: str):
    docs = load_documents(filepath)
    filtered = filter_documents(docs)
    chunks = text_split(filtered)
    retriever = build_vectorstore(chunks)
    rag_chain = build_qa_chain(retriever)

    response = rag_chain.invoke({"input": query})
    return response["answer"]
