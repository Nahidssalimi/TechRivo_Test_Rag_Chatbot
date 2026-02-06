"""
Health check endpoints
Monitor server and knowledge base status
"""

from fastapi import APIRouter
from app.rag.rag_pipeline import RAGPipeline

router = APIRouter()


rag_pipeline = RAGPipeline()


@router.get("/health")
async def health_check():
    """
    Check if the API is running
    """
    return {
        "status": "healthy",
        "message": "TechRivo AI Assistant is running"
    }


@router.get("/health/knowledge-base")
async def knowledge_base_status():
    """
    Check knowledge base status and statistics
    """
    stats = rag_pipeline.get_stats()
    
    return {
        "status": "healthy" if stats['status'] == 'ready' else "empty",
        "total_chunks": stats['total_chunks'],
        "message": f"Knowledge base contains {stats['total_chunks']} document chunks"
    }
