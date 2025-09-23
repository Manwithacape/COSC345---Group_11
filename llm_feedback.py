# File that the llm comes from for the paragraph in the collection
# llm_feedback.py
from typing import Dict, Any
from pydantic import BaseModel
from google import genai

# Model choice: fast & cheap; switch to "gemini-2.5-pro" for higher fidelity.
MODEL = "gemini-2.5-flash"

class Paragraph(BaseModel):
    paragraph: str

# Singleton client (reads GEMINI_API_KEY from env)
_client = genai.Client()

_SYSTEM = (
    "You are a photography assistant. Only use facts explicitly provided in <facts>...</facts>. "
    "If a detail isn't present, omit it (do not invent it). Write one concise paragraph."
)

def _pack_facts(facts: Dict[str, Any]) -> str:
    # Keep it explicit and small so the model can't wander
    import json
    return "<facts>\n" + json.dumps(facts, indent=2, ensure_ascii=False) + "\n</facts>"

def make_paragraph(facts: Dict[str, Any], user_prompt: str) -> str:
    """
    Returns a short paragraph that paraphrases only the provided facts.
    """
    contents = (
        _SYSTEM
        + "\n\nTask: "
        + user_prompt.strip()
        + "\n\n"
        + _pack_facts(facts)
    )

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
    return (parsed.paragraph if parsed else resp.text).strip()
