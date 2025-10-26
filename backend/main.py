from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pathlib import Path
from csv_agent import create_agent, run_agent
from openai import AzureOpenAI

# Langfuse imports (optional)
try:
    from langfuse.langchain import CallbackHandler
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    CallbackHandler = None

load_dotenv()

app = FastAPI(title="CSV Charts Chatbot API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CSV file storage
UPLOAD_DIR = Path("/tmp/csv_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
current_csv_file = None

# Initialize LangGraph agent
agent = None
client = None
langfuse_handler = None

try:
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=azure_api_key,
        api_version=azure_api_version
    )
    
    # Initialize Langfuse if credentials are available
    if LANGFUSE_AVAILABLE:
        langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        
        if langfuse_public_key and langfuse_secret_key:
            try:
                # Set host environment variable for Langfuse client
                os.environ["LANGFUSE_HOST"] = langfuse_host
                
                # Initialize CallbackHandler
                # Note: public_key can be passed explicitly or read from LANGFUSE_PUBLIC_KEY env var
                # secret_key is always read from LANGFUSE_SECRET_KEY env var in v3
                langfuse_handler = CallbackHandler(
                    public_key=langfuse_public_key,
                    update_trace=True  # Include chain details in traces
                )
                print("✓ Langfuse initialized successfully - tracing enabled")
                print(f"  Using Langfuse host: {langfuse_host}")
            except Exception as e:
                print(f"⚠ Langfuse initialization failed: {e} - tracing disabled")
                langfuse_handler = None
        else:
            print("ℹ Langfuse credentials not configured - tracing disabled")
    else:
        print("ℹ Langfuse package not installed - tracing disabled")
    
    # Setup agent using create_agent with optional Langfuse handler
    agent = create_agent(langfuse_handler)
except Exception as e:
    print(f"Warning: Agent initialization failed: {e}")

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class UploadResponse(BaseModel):
    message: str
    filename: str

@app.get("/")
async def root():
    return {"message": "CSV Charts Chatbot API with LangGraph Agent"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent_configured": agent is not None,
        "current_csv_file": current_csv_file,
        "langfuse_enabled": langfuse_handler is not None
    }

@app.post("/api/upload-csv", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file for analysis by the agent.
    """
    global current_csv_file
    
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        # Save the file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        current_csv_file = str(file_path)
        
        return UploadResponse(
            message="CSV file uploaded successfully",
            filename=file.filename
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """
    Chat endpoint using LangGraph agent with CSV tools.
    The agent can analyze CSV files and answer questions about them.
    """
    global current_csv_file
    
    if not agent:
        print("Agent is not configured properly.")
        raise HTTPException(
            status_code=503,
            detail="Agent is not configured. Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT_NAME environment variables."
        )
    
    try:
        print(f"Received message: {chat_message.message}")
        # Run the agent with the user message
        response = run_agent(agent, chat_message.message, current_csv_file)
        
        return ChatResponse(response=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
