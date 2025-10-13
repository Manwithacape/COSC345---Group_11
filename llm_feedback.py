# File that the llm comes from for the paragraph in the collection
# llm_feedback.py
import os
from typing import Dict, Any
import sys 

from dotenv import load_dotenv
from pydantic import BaseModel
from google import genai

# Model choice: fast & cheap; switch to "gemini-2.5-pro" for higher fidelity.
MODEL = "gemini-2.5-flash"


class Paragraph(BaseModel):
    paragraph: str


# Load .env so the Gemini key can be provided outside source control.
load_dotenv()

def get_executable_dir():
    """Get the directory where the executable is located."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def get_api_key_from_config():
    """Load the Gemini API key from a config.json file in the executable directory."""
    import json
    
    # Look for config.json in the same directory as the executable
    exe_dir = get_executable_dir()
    config_path = os.path.join(exe_dir, "config.json")
    
    print(f"Looking for config.json at: {config_path}")
    
    try:
        with open(config_path, "r") as f:
            print("Loading API key from config.json")
            config = json.load(f)
            return config.get("gemini_api_key")
    except FileNotFoundError:
        print(f"config.json not found at {config_path}")
        return None
    except Exception as e:
        print(f"Error reading config.json: {e}")
        return None

def _build_client() -> genai.Client:
    """Return a configured Gemini client or raise for missing credentials."""

    # Try to get the API key from environment variables or config file
    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GENAI_API_KEY")
    )


    ## If not found in env, try config file
    if not api_key:

        print("GEMINI_API_KEY not found in environment variables. Trying config file...")
        api_key = get_api_key_from_config();

        # If still not found crash with an error
        if not api_key:
            raise RuntimeError(
                "Missing Gemini API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY) in your environment, or provide it in config.json"
            )
        
    print("Using Gemini API key:", api_key[:4] + "..." + api_key[-4:])  # Print partial key for verification
    return genai.Client(api_key=api_key)


# Singleton client (reads GEMINI_API_KEY / GOOGLE_API_KEY from env)
_client = _build_client()

_SYSTEM = (
    "You are a photography assistant. Only use facts explicitly provided in <facts>...</facts>. "
    """If a detail isn't present, omit it (do not invent it). 
    Do not mention anything about resolution
    Write one concise paragraph about the collection only refering to the above facts and what could possibly be improved."""
)


def _pack_facts(facts: Dict[str, Any]) -> str:
    # Keep it explicit and small so the model can't wander
    import json

    return "<facts>\n" + json.dumps(facts, indent=2, ensure_ascii=False) + "\n</facts>"


def make_paragraph(user_prompt: str, facts: Dict[str, Any]) -> str:
    """
    Returns a short paragraph that paraphrases only the provided facts.

    NOTE: Parameter order is (user_prompt, facts) to match callers.
    """
    contents = _SYSTEM + "\n\nTask: " + user_prompt + "\n\n" + _pack_facts(facts)

    resp = _client.models.generate_content(
        model=MODEL,
        contents=contents,
        # Constrain output to a single 'paragraph' string.
        config={
            "temperature": 0.15,
            "response_mime_type": "application/json",
            "response_schema": Paragraph,  # Pydantic schema → structured output
        },
    )
    # Prefer parsed (schema-validated) text; fall back to raw
    parsed = getattr(resp, "parsed", None)
    return parsed.paragraph if parsed else resp.text
