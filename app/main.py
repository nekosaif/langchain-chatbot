from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize components
embeddings = OpenAIEmbeddings()
vector_store = None

class Query(BaseModel):
    question: str

def initialize_qa():
    global vector_store
    # Load custom FAQ document
    loader = PyPDFLoader("app/faqs/custom_faq.pdf")
    pages = loader.load_and_split()
    
    # Create vector store
    vector_store = FAISS.from_documents(pages, embeddings)
    
    # Save vector store locally
    vector_store.save_local("app/vector_store/faiss_index")

# Initialize QA system on startup
@app.on_event("startup")
async def startup_event():
    initialize_qa()

@app.post("/ask")
async def ask_question(query: Query):
    try:
        # Load vector store
        vector_store = FAISS.load_local(
            "app/vector_store/faiss_index", 
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Create QA chain
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )
        
        response = qa.run(query.question)
        return {"answer": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}