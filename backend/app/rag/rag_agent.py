"""
Main RAG Agent
Orchestrates retrieval and generation for question answering
"""

from typing import List, Dict, AsyncIterator
from app.rag.retriever import Retriever
from app.rag.llm_service import LLMService


class RAGAgent:
    """
    Main RAG agent that combines retrieval and generation
    This is the primary interface for answering questions
    """
    
    def __init__(self):
        """Initialize retriever and LLM service"""
        self.retriever = Retriever()
        self.llm = LLMService()
        print("RAG Agent initialized and ready")
    
    def answer_question(
        self,
        query: str,
        conversation_history: List[Dict] = None,
        top_k: int = 5,
        min_relevance: float = -1.0,
        include_sources: bool = True
    ) -> Dict[str, any]:
        """
        Answer a question using RAG
        """
        print(f"\nProcessing query: {query}")
       
        context_string, source_documents = self.retriever.get_context_for_query(
            query=query,
            top_k=top_k,
            min_relevance=min_relevance
        )
        
        print(f"Retrieved {len(source_documents)} relevant documents")
        
       
        if include_sources:
            response = self.llm.generate_with_sources(
                query=query,
                context=context_string,
                source_documents=source_documents,
                conversation_history=conversation_history
            )
        else:
            answer = self.llm.generate_response(
                query=query,
                context=context_string,
                conversation_history=conversation_history
            )
            response = {'answer': answer}
        
        response['context_used'] = len(source_documents) > 0
        response['num_sources'] = len(source_documents)
        
        return response
    
    async def answer_question_stream(
        self,
        query: str,
        conversation_history: List[Dict] = None,
        top_k: int = 5,
        min_relevance: float = -1.0
    ) -> AsyncIterator[str]:
        """
        Answer a question with streaming response
        """
        print(f"\nProcessing streaming query: {query}")
        
       
        context_string, source_documents = self.retriever.get_context_for_query(
            query=query,
            top_k=top_k,
            min_relevance=min_relevance
        )
        
        print(f"Retrieved {len(source_documents)} relevant documents")
        
 
        async for chunk in self.llm.generate_response_stream(
            query=query,
            context=context_string,
            conversation_history=conversation_history
        ):
            yield chunk
    
    def answer_without_context(
        self,
        query: str,
        conversation_history: List[Dict] = None
    ) -> str:
        """
        Answer a question without retrieval (general knowledge)
        """
        return self.llm.generate_response(
            query=query,
            context="",
            conversation_history=conversation_history
        )
    
    def should_use_retrieval(self, query: str) -> bool:
        """
        Determine if a query needs retrieval or can be answered directly
        """
        query_lower = query.lower().strip()
        
        simple_queries = [
            'hi', 'hello', 'hey', 'good morning', 'good afternoon',
            'good evening', 'thanks', 'thank you', 'bye', 'goodbye'
        ]
        
        if query_lower in simple_queries:
            return False
        
        if len(query_lower.split()) <= 2 and query_lower in ['how are you', 'whats up', "what's up"]:
            return False
        
        return True
    
    def chat(
        self,
        query: str,
        conversation_history: List[Dict] = None
    ) -> Dict[str, any]:
        """
        Smart chat function that decides whether to use retrieval
        """
        if self.should_use_retrieval(query):
            return self.answer_question(
                query=query,
                conversation_history=conversation_history
            )
        else:
            answer = self.answer_without_context(
                query=query,
                conversation_history=conversation_history
            )
            return {
                'answer': answer,
                'context_used': False,
                'num_sources': 0
            }










