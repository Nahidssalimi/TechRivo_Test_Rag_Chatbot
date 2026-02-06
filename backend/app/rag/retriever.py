"""
Retrieval service for finding relevant documents
Prepares context for LLM generation
"""

from typing import List, Dict, Optional
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.config import settings


class Retriever:
    """Handles document retrieval and context preparation"""
    
    def __init__(self):
        """Initialize embedder and vector store"""
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore(collection_name="techrivo_docs")
    
    def retrieve_context(
        self,
        query: str,
        top_k: int = None,
        min_relevance: float = -1.0
    ) -> List[Dict[str, any]]:
        """
        Retrieve relevant context for a query
        
        Args:
            query: User's question
            top_k: Number of documents to retrieve (default from settings)
            min_relevance: Minimum relevance score (default -1.0 to allow negative scores)
            
        Returns:
            List of relevant document chunks with metadata
        """
        if top_k is None:
            top_k = settings.RETRIEVAL_TOP_K
        
  
        query_embedding = self.embedder.embed_text(query)
        
        if query_embedding is None:
            print("Failed to embed query")
            return []
        
  
        results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=top_k
        )
        
       
        for r in results:
            print(f"  → distance: {r.get('distance')}, relevance: {r.get('relevance_score')}, title: {r.get('metadata', {}).get('title', 'unknown')}")
        
        
        filtered_results = [
            r for r in results 
            if r.get('relevance_score', -999) >= min_relevance
        ]
        
        print(f"Retrieved {len(filtered_results)} relevant documents (min relevance: {min_relevance})")
        
        return filtered_results
    
    def format_context(self, documents: List[Dict[str, any]]) -> str:
        """
        Format retrieved documents into context string for LLM
        
        Args:
            documents: List of retrieved document chunks
            
        Returns:
            Formatted context string
        """
        if not documents:
            return ""
        
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            relevance = doc.get('relevance_score', 0)
            
      
            source = metadata.get('source', 'Unknown')
            doc_type = metadata.get('type', 'document')
      
            section = f"[Source {i}] ({doc_type} - relevance: {relevance:.2f})\n"
            section += f"From: {source}\n"
            section += f"Content: {content}\n"
            
            context_parts.append(section)
        
        return "\n---\n".join(context_parts)
    
    def get_context_for_query(
        self,
        query: str,
        top_k: int = None,
        min_relevance: float = -1.0
    ) -> tuple[str, List[Dict]]:
        """
        Get formatted context and source documents for a query
        
        Returns:
            Tuple of (formatted_context_string, list_of_source_documents)
        """
  
        documents = self.retrieve_context(
            query=query,
            top_k=top_k,
            min_relevance=min_relevance
        )
        
   
        context_string = self.format_context(documents)
        
        return context_string, documents
    
    def enhance_query(self, query: str, conversation_history: List[Dict] = None) -> str:
        """
        Enhance query with conversation context if needed
        Useful for follow-up questions
        
        Args:
            query: Current user query
            conversation_history: Previous messages
            
        Returns:
            Enhanced query string
        """
        if not conversation_history or len(conversation_history) == 0:
            return query
        
     
        recent_history = conversation_history[-3:] if len(conversation_history) > 3 else conversation_history
        
      
        history_context = []
        for msg in recent_history:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if content:
                history_context.append(f"{role}: {content}")
        
      
        enhanced = f"Previous conversation:\n{chr(10).join(history_context)}\n\nCurrent question: {query}"
        
        return enhanced











