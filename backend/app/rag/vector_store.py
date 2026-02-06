"""
Vector database for storing and retrieving document embeddings
Uses ChromaDB for efficient similarity search
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import uuid
from app.config import settings


class VectorStore:
    """Manages vector storage and retrieval using ChromaDB"""
    
    def __init__(self, collection_name: str = "techrivo_docs"):
        """
        Initialize ChromaDB client and collection
        
        Args:
            collection_name: Name of the collection to store documents
        """
      
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        self.collection_name = collection_name
        

        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "TechRivo company documents and knowledge base"}
            )
            print(f"Created new collection: {collection_name}")
    
    def add_documents(self, documents: List[Dict[str, any]]) -> int:
        """
        Add documents with embeddings to the vector store
        
        Args:
            documents: List of dicts with 'content', 'embedding', and 'metadata'
            
        Returns:
            Number of documents successfully added
        """
        if not documents:
            print("No documents to add")
            return 0
        
 
        ids = []
        embeddings = []
        metadatas = []
        documents_text = []
        
        for doc in documents:
        
            doc_id = str(uuid.uuid4())
            
           
            embedding = doc.get('embedding')
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            
           
            if embedding is None:
                continue
            
            ids.append(doc_id)
            embeddings.append(embedding)
            documents_text.append(content)
            
           
            clean_metadata = {}
            for key, value in metadata.items():
                if isinstance(value, (str, int, float)):
                    clean_metadata[key] = value
                elif isinstance(value, list):
                    clean_metadata[key] = str(value)
                else:
                    clean_metadata[key] = str(value)
            
            metadatas.append(clean_metadata)
        
 
        if ids:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents_text,
                metadatas=metadatas
            )
            print(f"Added {len(ids)} documents to vector store")
            return len(ids)
        
        return 0
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict[str, any]]:
        """
        Search for similar documents using query embedding
        
        Args:
            query_embedding: Vector representation of the query
            n_results: Number of results to return
            filter_metadata: Optional metadata filters (e.g., {"type": "pdf"})
            
        Returns:
            List of relevant documents with content, metadata, and distance scores
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata,
                include=["documents", "metadatas", "distances"]
            )
            
         
            formatted_results = []
            
            if results['documents'] and len(results['documents']) > 0:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i],
                        'relevance_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                    })
            
            return formatted_results
        
        except Exception as e:
            print(f"Error searching vector store: {str(e)}")
            return []
    
    def delete_collection(self):
        """Delete the entire collection (use with caution!)"""
        try:
            self.client.delete_collection(name=self.collection_name)
            print(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            print(f"Error deleting collection: {str(e)}")
    
    def get_collection_count(self) -> int:
        """Get total number of documents in collection"""
        try:
            return self.collection.count()
        except:
            return 0
    
    def reset_collection(self):
        """Reset collection - delete and recreate"""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "TechRivo company documents and knowledge base"}
            )
            print(f"Reset collection: {self.collection_name}")
        except Exception as e:
            print(f"Error resetting collection: {str(e)}")
