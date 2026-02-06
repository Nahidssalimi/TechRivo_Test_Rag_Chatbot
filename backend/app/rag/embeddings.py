

from openai import OpenAI
from typing import List, Dict
import numpy as np
from app.config import settings


class EmbeddingService:
    """Handles text-to-vector conversion using OpenAI embeddings"""
    
    def __init__(self):
        """Initialize OpenAI client with API key from config"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"
        self.dimension = 1536

    def embed_text(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error creating embedding: {str(e)}")
            return None

    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(embeddings)
                print(f"Embedded batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
            except Exception as e:
                print(f"Error embedding batch {i//batch_size + 1}: {str(e)}")
                all_embeddings.extend([None] * len(batch))
        return all_embeddings

    def embed_documents(self, documents: List[Dict[str, any]]) -> List[Dict[str, any]]:
        texts = [doc['content'] for doc in documents]
        embeddings = self.embed_batch(texts)
        for doc, embedding in zip(documents, embeddings):
            doc['embedding'] = embedding
        valid_documents = [doc for doc in documents if doc['embedding'] is not None]
        print(f"Successfully embedded {len(valid_documents)}/{len(documents)} documents")
        return valid_documents

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)
