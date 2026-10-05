import json
import os
import re
import string

STOP_WORDS = {"is", "the", "a", "an", "what", "this", "of", "and", "to", "in", "for", "with", "on", "are", "do", "how", "who", "why", "can", "i", "make", "made"}

CONCEPT_RULES = {
    "PROC_MARKER": [r"\bvalid(ity)?\b", r"\blegitimate\b", r"\baccept(ed|ance)?\b", r"\btrust(ed)?\b", r"\bverif(y|ied|ication)\b", r"\bseal\b", r"official mark"],
    "PROC_TRUST": [r"\bamend(ed|ment|ments)?\b", r"\bcorrect(ion|ed|ions)?\b", r"\bupdate(s)?\b", r"\bmodify\b", r"change.*record", r"alter.*record"],
    "PROC_DISPATCH": [r"\bdispatch(es)?\b", r"\breport(s)?\b", r"field report", r"battlefield report", r"submitted report"],
    "PROC_2A": [r"\bwheel(s)?\b", r"\bprotect(or|ors|ion)?\b", r"\bchariot\b"],
    "PROC_2B": [r"\bmessage(s)?\b", r"\binstruct(ion|ions)?\b", r"\bdelegat(e|ed|ion)\b", r"\bbehalf\b"],
    "PROC_2C": [r"\bauthoriz(e|ation)\b", r"\bsender\b", r"\bflaw\b", r"\bvulnerab(le|ility)\b"],
    "PROC_3": [r"\bconflict(ing)?\b", r"\bdisagree\b", r"\bresolve\b", r"\bsudakshina\b", r"amend field report", r"amend field report", r"amend field report", r"change narrative state", r"change narrative state", r"change narrative state", r"alter narrative ledger", r"alter narrative ledger", r"alter narrative ledger"],
    "PROC_4": [r"\bschema\b", r"\bnotation\b", r"\bclash\b", r"\bbow_version\b"],
    "PROC_5": [r"\bcredential\b", r"\bledger\b", r"\bredeem\b", r"\bnonce\b"]
}

# Tie-breaker order: most advanced concepts first
CONCEPT_ORDER = ["PROC_5", "PROC_4", "PROC_3", "PROC_2C", "PROC_2B", "PROC_2A", "PROC_MARKER", "PROC_TRUST", "PROC_DISPATCH"]

class RAGService:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.raw_path = os.path.join(current_dir, "data", "drona_11_authentic.jsonl")
        self.corpus = []
        if os.path.exists(self.raw_path):
            with open(self.raw_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.corpus.append(json.loads(line))

    async def search(self, query: str, layer: int = 1, top_k: int = 1) -> list:
        query_lower = query.lower()
        
        concept_scores = {cid: 0 for cid in CONCEPT_ORDER}
        
        for cid, patterns in CONCEPT_RULES.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, query_lower))
                concept_scores[cid] += matches
                
        best_concept = None
        best_score = 0
        
        for cid in CONCEPT_ORDER:
            if concept_scores[cid] > best_score:
                if cid == "PROC_5" and layer < 5: continue
                if cid == "PROC_4" and layer < 4: continue
                if cid == "PROC_3" and layer < 3: continue
                if cid.startswith("PROC_2") and layer < 2: continue
                
                best_score = concept_scores[cid]
                best_concept = cid
                
        # If we have a strong concept match, return it
        if best_concept and best_score > 0:
            for doc in self.corpus:
                if doc.get("source_id") == best_concept:
                    return [doc]
                    
        # Standard Lore fallback
        scored = []
        query_clean = query_lower.translate(str.maketrans("", "", string.punctuation))
        query_words = set(w for w in query_clean.split() if w not in STOP_WORDS)
        for doc in self.corpus:
            if doc.get("episode") != "RULES":
                text_clean = doc["text"].lower().translate(str.maketrans("", "", string.punctuation))
                text_words = set(w for w in text_clean.split() if w not in STOP_WORDS)
                score = len(query_words.intersection(text_words))
                scored.append((score, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        if scored and scored[0][0] > 0:
            return [doc for score, doc in scored[:top_k]]
            
        return []

    async def ingest_chunk(self, source_id: str, text: str, metadata: dict):
        pass

rag_service = RAGService()
