"""
Main RAG pipeline orchestrator
Coordinates document ingestion, embedding, and storage
"""

from typing import List, Dict, Optional
from app.ingestion.loaders import DocumentLoader
from app.ingestion.processor import TextProcessor
from app.ingestion.web_scraper import WebScraper
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


class RAGPipeline:
    """Orchestrates the entire RAG ingestion and retrieval pipeline"""
    
    def __init__(self):
        """Initialize all components of the RAG pipeline"""
        self.loader = DocumentLoader()
        self.processor = TextProcessor(chunk_size=1000, chunk_overlap=200)
        self.scraper = WebScraper(max_pages=50, delay=1.0)
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore(collection_name="techrivo_docs")
        
        print("RAG Pipeline initialized")
    
    def ingest_directory(self, directory_path: str) -> int:
        """
        Ingest all documents from a directory
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            Number of chunks successfully ingested
        """
        print(f"\n{'='*60}")
        print(f"INGESTING DIRECTORY: {directory_path}")
        print(f"{'='*60}\n")
        
   
        print("Step 1/4: Loading documents...")
        documents = self.loader.load_directory(directory_path)
        print(f"✓ Loaded {len(documents)} documents\n")
        
        if not documents:
            print("No documents found!")
            return 0
        
    
        print("Step 2/4: Processing and chunking...")
        chunks = self.processor.process_documents(documents)
        print(f"✓ Created {len(chunks)} chunks\n")
        
     
        print("Step 3/4: Creating embeddings...")
        embedded_chunks = self.embedder.embed_documents(chunks)
        print(f"✓ Embedded {len(embedded_chunks)} chunks\n")
        
  
        print("Step 4/4: Storing in vector database...")
        count = self.vector_store.add_documents(embedded_chunks)
        print(f"✓ Stored {count} chunks\n")
        
        print(f"{'='*60}")
        print(f"INGESTION COMPLETE: {count} chunks indexed")
        print(f"{'='*60}\n")
        
        return count
    
    def ingest_single_file(self, file_path: str) -> int:
        """
        Ingest a single document file
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Number of chunks successfully ingested
        """
        print(f"\n{'='*60}")
        print(f"INGESTING FILE: {file_path}")
        print(f"{'='*60}\n")
     
   
        print("Step 1/4: Loading document...")
        documents = self.loader.load_document(file_path)
        print(f"✓ Loaded document with {len(documents)} sections\n")
        
        if not documents:
            print("Failed to load document!")
            return 0
        
       
        print("Step 2/4: Processing and chunking...")
        chunks = self.processor.process_documents(documents)
        print(f"✓ Created {len(chunks)} chunks\n")
        
        
        print("Step 3/4: Creating embeddings...")
        embedded_chunks = self.embedder.embed_documents(chunks)
        print(f"✓ Embedded {len(embedded_chunks)} chunks\n")
        
   
        print("Step 4/4: Storing in vector database...")
        count = self.vector_store.add_documents(embedded_chunks)
        print(f"✓ Stored {count} chunks\n")
        
        print(f"{'='*60}")
        print(f"INGESTION COMPLETE: {count} chunks indexed")
        print(f"{'='*60}\n")
        
        return count
    
    def ingest_website(self, url: str, follow_links: bool = True) -> int:
        """
        Scrape and ingest content from a website
        
        Args:
            url: Starting URL to scrape
            follow_links: Whether to follow internal links
            
        Returns:
            Number of chunks successfully ingested
        """
        print(f"\n{'='*60}")
        print(f"INGESTING WEBSITE: {url}")
        print(f"{'='*60}\n")
        
        
        print("Step 1/4: Scraping website...")
        documents = self.scraper.scrape_website(url, follow_links=follow_links)
        print(f"✓ Scraped {len(documents)} pages\n")
        
        if not documents:
            print("No content scraped!")
            return 0
        
  
        print("Step 2/4: Processing and chunking...")
        chunks = self.processor.process_documents(documents)
        print(f"✓ Created {len(chunks)} chunks\n")
       
        print("Step 3/4: Creating embeddings...")
        embedded_chunks = self.embedder.embed_documents(chunks)
        print(f"✓ Embedded {len(embedded_chunks)} chunks\n")
        

        print("Step 4/4: Storing in vector database...")
        count = self.vector_store.add_documents(embedded_chunks)
        print(f"✓ Stored {count} chunks\n")
        
        print(f"{'='*60}")
        print(f"INGESTION COMPLETE: {count} chunks indexed")
        print(f"{'='*60}\n")
        
        return count
    
    def retrieve(self, query: str, n_results: int = 5) -> List[Dict[str, any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User's question
            n_results: Number of relevant chunks to retrieve
            
        Returns:
            List of relevant document chunks with metadata
        """
       
        query_embedding = self.embedder.embed_text(query)
        
        if query_embedding is None:
            return []
        
    
        results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=n_results
        )
        
        return results
    
    def get_stats(self) -> Dict[str, any]:
        """Get statistics about the knowledge base"""
        count = self.vector_store.get_collection_count()
        
        return {
            'total_chunks': count,
            'status': 'ready' if count > 0 else 'empty'
        }
    
    def reset_knowledge_base(self):
        """Reset the entire knowledge base (delete all data)"""
        print("\n⚠️  RESETTING KNOWLEDGE BASE...")
        self.vector_store.reset_collection()
        print("✓ Knowledge base reset complete\n")