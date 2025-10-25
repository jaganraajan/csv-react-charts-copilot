from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

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

# Initialize Azure OpenAI client
client = None
try:
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    if azure_endpoint and azure_api_key:
        client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=azure_api_key,
            api_version="2024-02-15-preview"
        )
except Exception as e:
    print(f"Warning: Azure OpenAI client initialization failed: {e}")

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "CSV Charts Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "azure_openai_configured": client is not None
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """
    Simple chatbot endpoint using Azure OpenAI.
    For now, this is a basic chatbot unrelated to CSV files.
    """
    if not client:
        raise HTTPException(
            status_code=503,
            detail="Azure OpenAI is not configured. Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT_NAME environment variables."
        )
    
    try:
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        response = client.chat.completions.create(
            model=azure_deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Provide concise and friendly responses."
                },
                {
                    "role": "user",
                    "content": chat_message.message
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message.content
        
        return ChatResponse(response=assistant_message)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Azure OpenAI: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
