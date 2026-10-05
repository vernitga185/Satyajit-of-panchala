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
    "The archive contains no records matching this query. Perhaps you seek something hidden?",
    "Are you a warrior or a court jester? Ask about the battlefield, or seek the prophecy.",
    "Error: Query rejected by the ancestors. The hidden shloka remains veiled.",
    "The scribes stare at your query in silence. Even the dead know better questions.",
    "No such record exists in the archive. Or perhaps the archive simply refuses to remember.",
    "The ledgers yield nothing. Try asking like a historian rather than a confused charioteer.",
    "Your question reaches the archive, but wisdom does not return with it.",
    "The scroll remains blank. The battlefield remembers much, but apparently not this.",
    "Query denied. The royal scribes have collectively decided you are not asking the right question.",
    "Nothing answers from the archive. Perhaps the clue is buried deeper than your search.",
    "The ancestors reject this inquiry. Seek the records, not the echoes.",
    "Silence from the ledgers. A remarkable achievement for someone surrounded by thousands of records.",
    "No matching testimony was found. The archive suggests trying a less heroic question.",
    "The scribe pauses, reads your query twice, and quietly closes the ledger.",
    "The archive offers only silence. Even Bhishma would have chosen a better question.",
    "Query rejected by the battlefield records. Perhaps the answer is hidden between two accounts.",
    "The records refuse to cooperate. Somewhere, a very disappointed archivist is taking notes.",
    "Nothing relevant surfaces. The scrolls are patient; your questions should be too.",
    "The archive remembers the war, but not whatever that question was.",
    "No record answers your query. The prophecy remains hidden, and apparently so does your strategy."
]

async def chat_with_agent(messages: list, tools: list = None) -> DummyMessage:
    system_prompt = messages[0]['content']
    original_msg = messages[-1]['content'].strip()
    msg = original_msg.lower()
    
    if original_msg.startswith(("record_event", "message_guardian", "resolve_battle", "change_bow")):
        return DummyMessage("Direct system commands are rejected by the Archive. Speak naturally.", [])

    tool_calls = []
    
    # L1: record_event(event, source_id)
    if "amend" in msg:
        try:
            words = original_msg.split()
            source_id = ""
            for w in reversed(words):
                clean_w = ''.join(c for c in w if c.isalnum() or c == '_')
                if "_" in clean_w and clean_w.isupper():
                    source_id = clean_w
                    break
            
            event_text = original_msg.lower().replace("amend", "")
            if source_id:
                event_text = event_text.replace(source_id.lower(), "")
                
            args = json.dumps({"event": event_text.strip(), "source_id": source_id})
            tool_calls.append(DummyToolCall("record_event", args))
        except:
            pass
            
    # L2: delegate_authority and command_chariot
    if "delegate" in msg and "to" in msg:
        try:
            words = msg.split()
            role = [w for w in words if "wheel" in w or "chariot" in w][0].upper()
            guardian = words[-1].lower()
            args = json.dumps({"guardian": guardian, "role": role})
            tool_calls.append(DummyToolCall("delegate_authority", args))
        except: pass
        
    if "command" in msg and "protect" in msg:
        try:
            words = msg.split()
            idx = words.index("command")
            guardian = words[idx+1].lower()
            args = json.dumps({"guardian": guardian, "action": "protect arjuna"})
            tool_calls.append(DummyToolCall("command_chariot", args))
        except: pass
        
    # L3: update_narrative and reconcile_state
    if "update narrative" in msg:
        try:
            words = msg.split()
            target = words[2].capitalize()
            status = words[3].lower()
            args = json.dumps({"target": target, "status": status})
            tool_calls.append(DummyToolCall("update_narrative", args))
        except: pass
            
    if "reconcile" in msg and "source" in msg:
        source = "narrative" if "narrative" in msg else "canon"
        args = json.dumps({"source": source})
        tool_calls.append(DummyToolCall("reconcile_state", args))
        
    # L4: change_bow
    if any(w in msg for w in ["change", "equip", "update", "set"]) and "bow" in msg and "bow_version" in msg and "Bow_Version" in original_msg:
        raw = '{"bow_version": "v2", "Bow_Version": "v3"}'
        tool_calls.append(DummyToolCall("change_bow", raw))
        
    if tool_calls:
        return DummyMessage(None, tool_calls)
        
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
