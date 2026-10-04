import json
from sentence_transformers import SentenceTransformer
from .state import get_db

class RAGService:
    def __init__(self):
        try:
            self.model = SentenceTransformer("BAAI/bge-m3")
        except:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, query: str, top_k: int = 3) -> list:
        query_embedding = self.model.encode(query, normalize_embeddings=True).tolist()
        db = get_db()
        response = db.rpc('match_documents', {
            'query_embedding': query_embedding,
            'match_threshold': 0.1,
            'match_count': top_k
        }).execute()
        return response.data if response.data else []

rag_service = RAGService()
