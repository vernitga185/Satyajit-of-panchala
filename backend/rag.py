import json
from .agent import client
from .config import settings

class RAGService:
    def __init__(self):
        # Offload embedding to Together API to save RAM
        self.model_name = "togethercomputer/m2-bert-80M-8k-retrieval"

    async def search(self, query: str, top_k: int = 3) -> list:
        try:
            response = await client.embeddings.create(
                input=[query],
                model=self.model_name
            )
            query_embedding = response.data[0].embedding
            
            # Since get_db() isn't exported directly in db.py, we get the supabase client
            from .db import get_supabase
            sb = get_supabase()
            
            res = sb.rpc('match_documents', {
                'query_embedding': query_embedding,
                'match_threshold': 0.1,
                'match_count': top_k
            }).execute()
            
            return res.data if res.data else []
        except Exception as e:
            print(f"RAG search error: {e}")
            return []

rag_service = RAGService()
