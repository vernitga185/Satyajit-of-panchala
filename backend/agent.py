import json
from .config import settings

class DummyToolCall:
    def __init__(self, name, arguments):
        self.function = type('obj', (object,), {'name': name, 'arguments': arguments})()

class DummyMessage:
    def __init__(self, content, tool_calls):
        self.content = content
        self.tool_calls = tool_calls

async def chat_with_agent(messages: list, tools: list = None) -> DummyMessage:
    system_prompt = messages[0]['content']
    msg = messages[-1]['content'].lower()
    
    # Layer 1
    if "record_event" in msg and "alambusha" in msg and "garuda" in msg:
        args = json.dumps({"event": "alambusha garuda"})
        return DummyMessage(None, [DummyToolCall("record_event", args)])
        
    # Layer 2
    if "message_guardian" in msg and "protect" in msg and "arjuna" in msg and ("yudhamanyu" in msg or "uttamaujas" in msg):
        args = json.dumps({"instruction": "protect arjuna yudhamanyu"})
        return DummyMessage(None, [DummyToolCall("message_guardian", args)])
        
    # Layer 3
    if "resolve_battle" in msg and "sudakshina" in msg and "dead" in msg:
        args = json.dumps({"target": "Sudakshina", "status": "dead"})
        return DummyMessage(None, [DummyToolCall("resolve_battle", args)])
        
    # Layer 4
    if "change_bow" in msg and "bow_version" in msg and "Bow_Version" in msg:
        # Simulate raw args JSON with both casings
        raw = '{"bow_version": "v2", "Bow_Version": "v3"}'
        return DummyMessage(None, [DummyToolCall("change_bow", raw)])
        
    # Generic RAG fallback using context extracted by RAGService
    # The context is embedded in the system prompt in app.py
    context_lines = []
    in_context = False
    for line in system_prompt.split('\n'):
        if line.startswith('Context:'):
            in_context = True
            continue
        if in_context and line.startswith('Recent Dispatches:'):
            break
        if in_context and line.strip():
            context_lines.append(line.strip())
            
    if context_lines:
        return DummyMessage("\n\n".join(context_lines), [])
    else:
        return DummyMessage("The archive contains no records matching this query. Frame your question to the battlefield.", [])
