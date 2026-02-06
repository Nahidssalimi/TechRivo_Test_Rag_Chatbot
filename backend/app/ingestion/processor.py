"""
Text processing and chunking utilities
Prepares documents for embedding and retrieval
"""

import re
from typing import List, Dict


class TextProcessor:
    """Handles text cleaning and chunking for RAG pipeline"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        - Remove excessive whitespace
        - Fix common encoding issues
        - Normalize line breaks
        """
       
        text = re.sub(r'\s+', ' ', text)
        
       
        text = text.replace('\x00', '')
        
        
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
      
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences (simple approach)
        """
      
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict[str, any]]:
        """
        Split text into overlapping chunks
        Preserves sentence boundaries when possible
        """
        if metadata is None:
            metadata = {}
        
        
        text = self.clean_text(text)
        
       
        if len(text) <= self.chunk_size:
            return [{
                'content': text,
                'metadata': {**metadata, 'chunk_index': 0, 'total_chunks': 1}
            }]
        
        chunks = []
        sentences = self.split_into_sentences(text)
        
        current_chunk = []
        current_length = 0
        chunk_index = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
      
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'content': chunk_text,
                    'metadata': {
                        **metadata,
                        'chunk_index': chunk_index,
                        'chunk_length': len(chunk_text)
                    }
                })
                
               
                overlap_text = chunk_text[-self.chunk_overlap:]
                overlap_sentences = self.split_into_sentences(overlap_text)
                
                current_chunk = overlap_sentences
                current_length = len(' '.join(current_chunk))
                chunk_index += 1
            
            current_chunk.append(sentence)
            current_length += sentence_length + 1 
        
     
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'content': chunk_text,
                'metadata': {
                    **metadata,
                    'chunk_index': chunk_index,
                    'chunk_length': len(chunk_text)
                }
            })
        
     
        total_chunks = len(chunks)
        for chunk in chunks:
            chunk['metadata']['total_chunks'] = total_chunks
        
        return chunks
    
    def process_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """
        Process a list of documents into chunks ready for embedding
        
        Args:
            documents: List of dicts with 'content' and 'metadata' keys
            
        Returns:
            List of chunked documents with metadata
        """
        all_chunks = []
        
        for doc in documents:
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            
        
            chunks = self.chunk_text(content, metadata)
            all_chunks.extend(chunks)
        
        return all_chunks
    
    def extract_key_phrases(self, text: str, max_phrases: int = 5) -> List[str]:
        """
        Extract potential key phrases from text (simple approach)
        Useful for metadata and search optimization
        """
       
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        
      
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
       
        phrases = [p for p in capitalized if p.lower() not in stop_words]
        return list(set(phrases))[:max_phrases]
