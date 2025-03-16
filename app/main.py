from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="FAQ Chatbot API", version="1.1.0")

# Configure rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS middleware
origins = [
    "http://localhost:5000",
    "https://your-heroku-app.herokuapp.com",
    "https://your-production-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining"],
    max_age=600
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize components
embeddings = OpenAIEmbeddings()
vector_store = None

class Query(BaseModel):
    question: str

def initialize_qa():
    global vector_store
    try:
        logger.info("Initializing QA system...")
        
        # Load document
        loader = PyPDFLoader("app/faqs/custom_faq.pdf")
        pages = loader.load_and_split()
        
        # Create and save vector store
        vector_store = FAISS.from_documents(pages, embeddings)
        vector_store.save_local("app/vector_store/faiss_index")
        logger.info("Vector store initialized successfully")
        
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
        raise RuntimeError("Failed to initialize QA system")

@app.on_event("startup")
async def startup_event():
    initialize_qa()

@app.post("/ask", summary="Ask a question", response_description="AI-generated answer")
@limiter.limit("10/minute")
async def ask_question(request: Request, query: Query):
    """
    Process user questions and return AI-generated answers based on FAQ content
    """
    try:
        logger.info(f"Processing question: {query.question}")
        
        # Load vector store with safety override
        vector_store = FAISS.load_local(
            "app/vector_store/faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Create QA chain with enhanced parameters
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(
                temperature=0,
                max_tokens=500,
                model_name="gpt-3.5-turbo-instruct"
            ),
            chain_type="stuff",
            retriever=vector_store.as_retriever(
                search_kwargs={"k": 3}
            )
        )
        
        result = qa.invoke({"query": query.question})
        return {"answer": result["result"]}
    
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing your question. Please try again."
        )

@app.get("/health", summary="Service health check")
def health_check():
    """
    Returns service health status and version information
    """
    return {
        "status": "healthy",
        "version": "1.1.0",
        "features": {
            "rate_limit": "10 requests/minute",
            "model": "gpt-3.5-turbo-instruct",
            "vector_store": "FAISS",
            "embeddings": "OpenAI"
        }
    }