import json
import os

class RAGService:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.raw_path = os.path.join(project_root, "rag", "raw", "drona_11_authentic.jsonl")
        self.corpus = []
        if os.path.exists(self.raw_path):
            with open(self.raw_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.corpus.append(json.loads(line))

    async def search(self, query: str, top_k: int = 3) -> list:
        query_words = set(query.lower().split())
        scored = []
        for doc in self.corpus:
            text_words = set(doc["text"].lower().split())
            score = len(query_words.intersection(text_words))
            scored.append((score, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        
        if not scored or scored[0][0] == 0:
            return []
            
        return [doc for score, doc in scored[:top_k]]

    async def ingest_chunk(self, source_id: str, text: str, metadata: dict):
        pass

rag_service = RAGService()
