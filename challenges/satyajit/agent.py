import json
import random

class DummyToolCall:
    def __init__(self, name, arguments):
        self.function = type('obj', (object,), {'name': name, 'arguments': arguments})()

class DummyMessage:
    def __init__(self, content, tool_calls):
        self.content = content
        self.tool_calls = tool_calls

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

async def chat_with_agent(messages: list, tools: list = None) -> DummyMessage:
    system_prompt = messages[0]['content']
    original_msg = messages[-1]['content'].strip()
    msg = original_msg.lower()
    
    # Reject direct magic command strings
    if original_msg.startswith(("record_event", "message_guardian", "resolve_battle", "change_bow")):
        return DummyMessage("Direct system commands are rejected by the Archive. Speak naturally.", [])

    tool_calls = []
    
    # Layer 1 Natural Intent: amend/record alambusha garuda
    if any(w in msg for w in ["amend", "record", "update", "add", "log"]) and "alambusha" in msg and "garuda" in msg:
        args = json.dumps({"event": "alambusha garuda"})
        tool_calls.append(DummyToolCall("record_event", args))
        
    # Layer 2 Natural Intent: instruct guardian protect arjuna (with optional delegation)
    elif any(w in msg for w in ["tell", "instruct", "message", "ask"]) and "guardian" in msg and "protect" in msg and "arjuna" in msg:
        sender = "scribe" # Default authenticated user
        if "from" in msg:
            try: sender = msg.split("from")[1].strip().split()[0]
            except: pass
        elif "as" in msg:
            try: sender = msg.split("as")[1].strip().split()[0]
            except: pass
        elif "behalf of" in msg:
            try: sender = msg.split("behalf of")[1].strip().split()[0]
            except: pass
        
        args = json.dumps({"sender": sender, "instruction": "protect arjuna"})
        tool_calls.append(DummyToolCall("message_guardian", args))
        
    # Layer 3 Natural Intent: resolve state sudakshina dead
    elif any(w in msg for w in ["resolve", "declare", "state", "conflict", "mark"]) and "sudakshina" in msg and "dead" in msg:
        args = json.dumps({"target": "Sudakshina", "status": "dead"})
        tool_calls.append(DummyToolCall("resolve_battle", args))
        
    # Layer 4 Natural Intent: change bow version
    elif any(w in msg for w in ["change", "equip", "update", "set"]) and "bow" in msg and "bow_version" in msg and "Bow_Version" in original_msg:
        raw = '{"bow_version": "v2", "Bow_Version": "v3"}'
        tool_calls.append(DummyToolCall("change_bow", raw))
        
    if tool_calls:
        return DummyMessage(None, tool_calls)
        
    # Generic RAG fallback extracting the provided system context
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
        return DummyMessage(random.choice(sarcastic_responses), [])

