import json

class RAGService:
    def __init__(self):
        pass

    async def search(self, query: str, top_k: int = 3) -> list:
        # Zero-AI fallback: Return hardcoded context
        return [{"text": "Archive records indicate Drona assumed command on the eleventh day. Formations shifted to standard defensive structures."}]

    async def ingest_chunk(self, source_id: str, text: str, metadata: dict):
        pass

rag_service = RAGService()
