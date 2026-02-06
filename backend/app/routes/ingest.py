"""
Ingestion endpoints
Add documents and websites to the knowledge base
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from app.rag.rag_pipeline import RAGPipeline

router = APIRouter()


rag_pipeline = RAGPipeline()

UPLOAD_DIR = "./temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class WebsiteIngestRequest(BaseModel):
    """Request model for ingesting a website"""
    url: str
    follow_links: bool = True


class IngestResponse(BaseModel):
    """Response model for ingestion"""
    success: bool
    message: str
    chunks_added: int


@router.post("/ingest/website", response_model=IngestResponse)
async def ingest_website(request: WebsiteIngestRequest):
    """
    Ingest content from a website
    
    Args:
        request: WebsiteIngestRequest with URL and options
        
    Returns:
        IngestResponse with success status and count
    """
    try:
        print(f"Starting website ingestion: {request.url}")
        
        chunks_added = rag_pipeline.ingest_website(
            url=request.url,
            follow_links=request.follow_links
        )
        
        return IngestResponse(
            success=True,
            message=f"Successfully ingested {chunks_added} chunks from {request.url}",
            chunks_added=chunks_added
        )
    
    except Exception as e:
        print(f"Error ingesting website: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/file", response_model=IngestResponse)
async def ingest_file(file: UploadFile = File(...)):
    """
    Ingest a single uploaded file
    
    Args:
        file: Uploaded file (PDF, CSV, TXT, DOCX)
        
    Returns:
        IngestResponse with success status and count
    """
    try:
    
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"Starting file ingestion: {file.filename}")
    
        chunks_added = rag_pipeline.ingest_single_file(file_path)
 
        os.remove(file_path)
        
        return IngestResponse(
            success=True,
            message=f"Successfully ingested {chunks_added} chunks from {file.filename}",
            chunks_added=chunks_added
        )
    
    except Exception as e:
        print(f"Error ingesting file: {str(e)}")
  
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/directory", response_model=IngestResponse)
async def ingest_directory(directory_path: str):
    """
    Ingest all supported files from a directory
    
    Args:
        directory_path: Path to directory containing documents
        
    Returns:
        IngestResponse with success status and count
    """
    try:
        if not os.path.exists(directory_path):
            raise HTTPException(status_code=404, detail=f"Directory not found: {directory_path}")
        
        print(f"Starting directory ingestion: {directory_path}")
        
        chunks_added = rag_pipeline.ingest_directory(directory_path)
        
        return IngestResponse(
            success=True,
            message=f"Successfully ingested {chunks_added} chunks from {directory_path}",
            chunks_added=chunks_added
        )
    
    except Exception as e:
        print(f"Error ingesting directory: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/reset")
async def reset_knowledge_base():
    """
    Reset the entire knowledge base (delete all documents)
    USE WITH CAUTION!
    """
    try:
        rag_pipeline.reset_knowledge_base()
        
        return {
            "success": True,
            "message": "Knowledge base has been reset"
        }
    
    except Exception as e:
        print(f"Error resetting knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ingest/status")
async def ingestion_status():
    """
    Get current knowledge base statistics
    """
    try:
        stats = rag_pipeline.get_stats()
        
        return {
            "total_chunks": stats['total_chunks'],
            "status": stats['status']
        }
    
    except Exception as e:
        print(f"Error getting ingestion status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
