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
        
    # Generic RAG fallback
    return DummyMessage("The archive acknowledges your query, but requires specific tool invocations to alter the canonical state.", [])
