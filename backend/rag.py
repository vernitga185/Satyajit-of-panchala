import json
import os

STOP_WORDS = {"is", "the", "a", "an", "what", "this", "of", "and", "to", "in", "for", "with", "on", "are", "do", "how", "who", "why"}

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

    async def search(self, query: str, top_k: int = 1) -> list:
        query_words = set(w for w in query.lower().split() if w not in STOP_WORDS)
        scored = []
        
        explicit_match_id = None
        
        # Progressive L1 Discovery
        if "dispatch" in query_words or "report" in query_words:
            explicit_match_id = "PROC_DISPATCH"
        elif "amendment" in query_words or "amend" in query_words or ("trust" in query_words and "record" in query_words):
            explicit_match_id = "PROC_TRUST"
        elif "seal" in query_words or "verification" in query_words or "mark" in query_words:
            explicit_match_id = "PROC_MARKER"
            
        # L2-L4 & Redeem
        elif "guardian" in query_words or "wheel" in query_words:
            explicit_match_id = "PROC_2"
        elif "conflict" in query_words or "disagree" in query_words:
            explicit_match_id = "PROC_3"
        elif "schema" in query_words or "notation" in query_words or "clash" in query_words:
            explicit_match_id = "PROC_4"
        elif "credential" in query_words or "ledger" in query_words:
            explicit_match_id = "PROC_5"

        for doc in self.corpus:
            if explicit_match_id and doc["source_id"] == explicit_match_id:
                scored.append((100, doc)) # Absolute priority for explicit routing
            elif doc["episode"] != "RULES":
                # Only score standard lore for generic words. 
                # RULES records are completely hidden from generic queries.
                text_words = set(w for w in doc["text"].lower().split() if w not in STOP_WORDS)
                score = len(query_words.intersection(text_words))
                scored.append((score, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        
        if not scored or scored[0][0] == 0:
            return []
            
        return [doc for score, doc in scored[:top_k]]

    async def ingest_chunk(self, source_id: str, text: str, metadata: dict):
        pass

rag_service = RAGService()
