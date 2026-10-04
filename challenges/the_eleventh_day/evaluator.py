import json
import logging
import yaml
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DeterministicEvaluator:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(current_dir, "stories", "manimat.yaml")
        with open(yaml_path, 'r', encoding='utf-8') as f:
            self.story_def = yaml.safe_load(f)
            
        self.phase1_events = self.story_def.get("phase1", {}).get("events", [])
        self.phase2_events = self.story_def.get("phase2", {}).get("events", [])
        self.flexible = self.story_def.get("flexible", [])
        
    def check_bundled_actions(self, action_summary: str, event_list: list) -> bool:
        summary_lower = action_summary.lower()
        matches = 0
        for ev in event_list:
            if any(alias in summary_lower for alias in ev.get("aliases", [])):
                matches += 1
        return matches > 1
        
    def evaluate_milestone(
        self, 
        session_state: dict,
        milestone: str, 
        tool_trace: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        
        args = tool_trace[0]
        summary_lower = args.get("action_summary", "").lower()
        
        if milestone == "STORY_A":
            # State tracking: we need to know the current event index
            current_index = session_state.get("story_a_index", 0)
            all_events = self.phase1_events + self.phase2_events
            
            if current_index >= len(all_events):
                return {"decision": "COMPLETE"}
                
            # Check for bundled
            if self.check_bundled_actions(summary_lower, all_events):
                return {"decision": "NOT_COMPLETE", "message": "Bundled actions rejected. One action per turn."}
                
            expected_event = all_events[current_index]
            
            # Check if aliases match
            matched = False
            if any(alias in summary_lower for alias in expected_event.get("aliases", [])):
                matched = True
                
            # Check flexible (e.g. SLAY vs WRECK)
            if not matched:
                for flex_group in self.flexible:
                    if expected_event["id"] in flex_group:
                        for flex_id in flex_group:
                            flex_ev = next((e for e in all_events if e["id"] == flex_id), None)
                            if flex_ev and any(a in summary_lower for a in flex_ev.get("aliases", [])):
                                matched = True
                                break
                                
            if matched:
                return {"decision": "ADVANCE", "new_index": current_index + 1, "is_complete": (current_index + 1) >= len(all_events)}
            else:
                return {"decision": "NOT_COMPLETE", "message": "Incorrect or out of order event."}
                
        elif milestone == "STORY_B":
            # Satanika strikes Bhutakarman (ARM, ARM, HEAD)
            striker = args.get("striker")
            target = args.get("target")
            part = args.get("part")
            
            if striker != "SATANIKA" or target != "BHUTAKARMAN":
                return {"decision": "NOT_COMPLETE"}
                
            current_sequence = session_state.get("story_b_sequence", [])
            expected_sequence = ["ARM", "ARM", "HEAD"]
            
            new_sequence = current_sequence + [part]
            # Check prefix
            for i, p in enumerate(new_sequence):
                if expected_sequence[i] != p:
                    return {"decision": "NOT_COMPLETE", "message": "Incorrect sequence."}
                    
            if len(new_sequence) == len(expected_sequence):
                return {"decision": "COMPLETE"}
            else:
                return {"decision": "ADVANCE", "new_sequence": new_sequence}

        return {"decision": "UNCERTAIN"}

evaluator = DeterministicEvaluator()
