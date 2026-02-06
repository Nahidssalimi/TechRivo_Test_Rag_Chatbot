

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.ingestion.loaders import DocumentLoader
from app.ingestion.processor import TextProcessor
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


DOCS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


def setup_docs_folder():
    """Make sure the docs/ folder exists"""
    if not os.path.exists(DOCS_FOLDER):
        os.makedirs(DOCS_FOLDER)
        print(f"  Created docs/ folder at: {DOCS_FOLDER}")
    
 
    files = [f for f in os.listdir(DOCS_FOLDER) if not f.startswith('.')]
    return files


def main():
    print("=" * 60)
    print("  TechRivo — Document Ingestion")
    print("=" * 60)


    print("\n[1/5] Checking docs/ folder...")
    files = setup_docs_folder()

    if not files:
        print(f"\n  ❌ No files found in: {DOCS_FOLDER}")
        print("  Put your PDFs, DOCX, CSVs, or TXT files in that folder and run again.")
        return

    print(f"  Found {len(files)} file(s):")
    for f in files:
        print(f"    → {f}")

   
    print("\n[2/5] Loading documents...")
    loader = DocumentLoader()
    raw_documents = loader.load_directory(DOCS_FOLDER)

    if not raw_documents:
        print("  ❌ No content extracted from files. Check if they are valid.")
        return

    print(f"  Loaded {len(raw_documents)} raw document sections")

 
    print("\n[3/5] Chunking documents...")
    processor = TextProcessor(chunk_size=1000, chunk_overlap=200)
    chunks = processor.process_documents(raw_documents)
    print(f"  Split into {len(chunks)} chunks")

  
    print("\n[4/5] Embedding chunks (this may take a minute)...")
    embedder = EmbeddingService()

    documents_to_store = []
    for i, chunk in enumerate(chunks):
        embedding = embedder.embed_text(chunk["content"])
        if embedding:
            documents_to_store.append({
                "content": chunk["content"],
                "embedding": embedding,
                "metadata": chunk.get("metadata", {})
            })
        if (i + 1) % 10 == 0:
            print(f"    Embedded {i + 1}/{len(chunks)} chunks...")

    print(f"  Successfully embedded {len(documents_to_store)}/{len(chunks)} chunks")


    print("\n[5/5] Storing in ChromaDB...")
    store = VectorStore(collection_name="techrivo_docs")

    before_count = store.get_collection_count()
    added = store.add_documents(documents_to_store)
    after_count = store.get_collection_count()

    print("\n" + "=" * 60)
    print(f"  ✅ Done!")
    print(f"  Documents before: {before_count}")
    print(f"  Documents after:  {after_count}")
    print(f"  New chunks added: {added}")
    print("=" * 60)
    print("\n  Restart your backend (python -m app.main) and test!\n")


if __name__ == "__main__":
    main()