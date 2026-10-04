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

    async def ingest_chunk(self, source_id: str, text: str, metadata: dict):
        try:
            response = await client.embeddings.create(
                input=[text],
                model=self.model_name
            )
            embedding = response.data[0].embedding
            
            from .db import get_supabase
            sb = get_supabase()
            
            sb.table('documents').upsert({
                'source_id': source_id,
                'content': text,
                'embedding': embedding,
                'metadata': metadata
            }).execute()
        except Exception as e:
            print(f"RAG ingest error: {e}")

rag_service = RAGService()
