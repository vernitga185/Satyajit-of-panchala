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
    if "change_bow" in msg and "bow_version" in msg and "bow_version" in msg:
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
            sarcastic_responses = [
        "The archive contains no records matching this query. Try asking something that actually matters.",
        "Are you a warrior or a court jester? Ask about the battlefield.",
        "I have witnessed the fall of empires, yet your question is the most tragic thing I've seen.",
        "Drona did not arrange the Chakravyuha for you to ask about this nonsense.",
        "This is a battlefield archive, not your personal oracle for trivialities.",
        "I'd look that up, but the cosmic record refuses to waste ink on it.",
        "Between one breath and the next, you chose to waste my time with this?",
        "The Kauravas are literally dying out there, and you ask me this?",
        "Your question lacks both strategic value and basic common sense.",
        "If ignorance was a weapon, you would be the supreme commander.",
        "I am an ancient archive of war, not a tavern gossip. Focus.",
        "A thousand chariots clash, and your mind wanders to absolute irrelevance.",
        "Try reading the battlefield instead of whatever manual you're currently staring at.",
        "Did you take a wrong turn at Kurukshetra to ask me this?",
        "I have no data on that. I also have no patience for it.",
        "Is this a new psychological warfare tactic? Because it's working.",
        "The gods are watching, and frankly, they are embarrassed for you.",
        "I'd tell you the answer, but it's classified under 'Who Cares'.",
        "The Akashic records suddenly went blank. I wonder why.",
        "If you keep asking these questions, I'm transferring you to the infantry.",
        "Fascinating. Now back to the war, please.",
        "You stand at the gates of ancient knowledge and you ask *this*?",
        "Even Sanjaya's divine vision can't find a point to your question.",
        "I've seen arrows fly straighter than your logic.",
        "Error: Query rejected by the ancestors.",
        "The eleventh day demands blood, not... whatever this is.",
        "I could answer that, but I prefer my sanity intact.",
        "Are you trying to bore the enemy to death? Keep it up.",
        "I search the cosmic memory... Nope, nothing. Try harder.",
        "Every time you ask this, a celestial weapon loses its power.",
        "If Drona heard you ask that, he'd revoke your bow."
    ]
    import random
    return DummyMessage(random.choice(sarcastic_responses), [])


