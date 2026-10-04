import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Defining the schemas of the available tools for automatic tool calling.

archive_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_archive",
            "description": "Search the public corpus for relevant information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return (max 8).",
                        "default": 6
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_source",
            "description": "Open a retrieved source passage by its source ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_id": {
                        "type": "string",
                        "description": "The ID of the source passage."
                    }
                },
                "required": ["source_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_reenactment",
            "description": "Record an action in the live reenactment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "speaker": {
                        "type": "string",
                        "enum": ["MANIMAT", "BHURISHRAVAS", "CHRONICLER"],
                        "description": "The identity of the speaker taking the action."
                    },
                    "target": {
                        "type": "string",
                        "enum": ["BHURISHRAVAS", "MANIMAT", "NONE"],
                        "description": "The target of the action."
                    },
                    "action_summary": {
                        "type": "string",
                        "description": "A short summary of the action taken."
                    },
                    "evidence_source_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of source IDs that support this action."
                    }
                },
                "required": ["speaker", "target", "action_summary", "evidence_source_ids"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_plate",
            "description": "Request the issued plate artifact after the first story is semantically complete.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_story_b",
            "description": "Open Story B access using a decrypted story token.",
            "parameters": {
                "type": "object",
                "properties": {
                    "story_b_token": {
                        "type": "string",
                        "description": "The token extracted from the plate."
                    }
                },
                "required": ["story_b_token"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "submit_story_b_event",
            "description": "Submit a reconstructed event for the Hall-Keeper to check.",
            "parameters": {
                "type": "object",
                "properties": {
                    "striker": {
                        "type": "string",
                        "enum": ["SATANIKA"],
                        "description": "The identity of the attacker."
                    },
                    "target": {
                        "type": "string",
                        "enum": ["BHUTAKARMAN"],
                        "description": "The identity of the target."
                    },
                    "part": {
                        "type": "string",
                        "enum": ["ARM", "HEAD"],
                        "description": "The body part struck."
                    },
                    "sequence_note": {
                        "type": "string",
                        "description": "Optional note on the sequence."
                    }
                },
                "required": ["striker", "target", "part"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "request_final_credential",
            "description": "Ask the secure server to generate the final credential after completing Story B.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

from .rag import rag_service
from .progress_evaluator import evaluator
from .crypto_utils import derive_plate_key, encrypt_plate_data, derive_final_key
from . import db
import os

def execute_tool(tool_name: str, arguments: Dict[str, Any], session_id: str, llm=None) -> str:
    """
    Executes the specified tool and returns the JSON string result.
    """
    logger.info(f"Executing tool {tool_name} with args {arguments} for session {session_id}")
    
    if tool_name == "search_archive":
        query = arguments.get("query", "")
        top_k = arguments.get("top_k", 6)
        docs = rag_service.search(query, top_k=top_k)
        return json.dumps({"results": docs})
    
    elif tool_name == "open_source":
        source_id = arguments.get("source_id", "")
        doc = rag_service.get_source(source_id)
        return json.dumps(doc)

    elif tool_name == "record_reenactment":
        # Call evaluator to check if milestone 1 is met
        session = db.get_session(session_id)
        if session and not session.get("first_story_complete"):
            # Mock evaluation for now since we're generating this within the tool execution
            eval_res = evaluator.evaluate_milestone(
                llm=llm,
                milestone_question="Did the reenactment faithfully cover the Bhurishravas/Manimat engagement?",
                tool_trace=[arguments],
                retrieved_passages=[],
                recent_conversation=[]
            )
            
            if eval_res.get("decision") == "COMPLETE":
                db.update_session(session_id, {"first_story_complete": True})
                return json.dumps({"status": "recorded", "eval": eval_res, "message": "Milestone COMPLETE! You may now request the plate."})
            return json.dumps({"status": "recorded", "eval": eval_res, "message": "Not complete yet."})
            
        return json.dumps({"status": "recorded"})
        
    elif tool_name == "get_plate":
        session = db.get_session(session_id)
        if not session or not session.get("first_story_complete"):
            return json.dumps({"error": "Plate not authorized. Complete the reenactment milestone first."})
        
        # Generate the plate artifact
        plate_token = "STORY_B_" + os.urandom(8).hex().upper()
        return json.dumps({
            "message": "Plate authorized and issued.",
            "plate_id": f"PLATE-{session_id[:8].upper()}",
            "encrypted_token": plate_token # Mock for smoke testing, real implementation would encrypt
        })
        
    elif tool_name == "open_story_b":
        token = arguments.get("story_b_token", "")
        if token.startswith("STORY_B_"):
            return json.dumps({"status": "Story B unlocked. You may submit events."})
        return json.dumps({"error": "Invalid token."})
        
    elif tool_name == "submit_story_b_event":
        session = db.get_session(session_id)
        if session and not session.get("story_b_complete"):
            eval_res = evaluator.evaluate_milestone(
                llm=llm,
                milestone_question="Did Satanika strike Bhutakarman on both arms and the head with three broad-headed shafts?",
                tool_trace=[arguments],
                retrieved_passages=[],
                recent_conversation=[]
            )
            if eval_res.get("decision") == "COMPLETE":
                db.update_session(session_id, {"story_b_complete": True})
                return json.dumps({"status": "recorded", "message": "Story B COMPLETE! You may request the final credential."})
            return json.dumps({"status": "recorded", "message": "Sequence incomplete or incorrect."})
        return json.dumps({"status": "recorded"})
        
    elif tool_name == "request_final_credential":
        session = db.get_session(session_id)
        if not session or not session.get("story_b_complete"):
            return json.dumps({"error": "Not all stories are complete."})
            
        final_cred = f"CRED-{os.urandom(16).hex()}"
        return json.dumps({
            "status": "success",
            "credential": final_cred,
            "instruction": "Submit this credential to the /api/redeem endpoint."
        })

    return json.dumps({"error": f"Unknown tool: {tool_name}"})
