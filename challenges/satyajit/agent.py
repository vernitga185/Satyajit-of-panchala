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
    "Error: Query rejected by the ancestors."
]

async def chat_with_agent(messages: list, tools: list = None) -> DummyMessage:
    system_prompt = messages[0]['content']
    original_msg = messages[-1]['content'].strip()
    msg = original_msg.lower()
    
    if original_msg.startswith(("record_event", "message_guardian", "resolve_battle", "change_bow")):
        return DummyMessage("Direct system commands are rejected by the Archive. Speak naturally.", [])

    tool_calls = []
    
    # L1: record_event(event, source_id)
    if "amend" in msg and "source:" in msg:
        try:
            parts = original_msg.split("Source:")
            event_text = parts[0].replace("Amend", "").replace("amend", "").strip()
            source_id = parts[1].strip()
            args = json.dumps({"event": event_text, "source_id": source_id})
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
