"""
Chat endpoints
Handle user messages and generate responses
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json
from app.rag.rag_agent import RAGAgent

router = APIRouter()


rag_agent = RAGAgent()


class Message(BaseModel):
    """Message model"""
    role: str  
    content: str


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    conversation_history: Optional[List[Message]] = None
    stream: bool = True 


class ChatResponse(BaseModel):
    """Chat response model"""
    answer: str
    sources: Optional[List[dict]] = None
    context_used: bool
    num_sources: int


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message and get a response (non-streaming)
    
    Args:
        request: ChatRequest with message and optional history
        
    Returns:
        ChatResponse with answer and sources
    """
    try:
       
        history = None
        if request.conversation_history:
            history = [msg.dict() for msg in request.conversation_history]
        
       
        response = rag_agent.chat(
            query=request.message,
            conversation_history=history
        )
        
        return ChatResponse(**response)
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Send a message and get a streaming response
    
    Args:
        request: ChatRequest with message and optional history
        
    Returns:
        StreamingResponse with server-sent events
    """
    try:
       
        history = None
        if request.conversation_history:
            history = [msg.dict() for msg in request.conversation_history]
        
       
        use_retrieval = rag_agent.should_use_retrieval(request.message)
        
        async def generate():
            """Generator for streaming response"""
            if use_retrieval:
            
                async for chunk in rag_agent.answer_question_stream(
                    query=request.message,
                    conversation_history=history
                ):
                    
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            else:
               
                response = rag_agent.answer_without_context(
                    query=request.message,
                    conversation_history=history
                )
             
                yield f"data: {json.dumps({'chunk': response})}\n\n"
            
       
            yield f"data: {json.dumps({'done': True})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    except Exception as e:
        print(f"Error in chat stream endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
