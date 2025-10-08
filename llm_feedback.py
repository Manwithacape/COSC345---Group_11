# File that the llm comes from for the paragraph in the collection
# llm_feedback.py
import os
from typing import Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel
from google import genai

# Model choice: fast & cheap; switch to "gemini-2.5-pro" for higher fidelity.
MODEL = "gemini-2.5-flash"


class Paragraph(BaseModel):
    paragraph: str


# Load .env so the Gemini key can be provided outside source control.
load_dotenv()


def _build_client() -> genai.Client:
    """Return a configured Gemini client or raise for missing credentials."""
    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GENAI_API_KEY")
    )
    if not api_key:
        raise RuntimeError(
            "Missing Gemini API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY) in your environment."
        )
    return genai.Client(api_key=api_key)


# Singleton client (reads GEMINI_API_KEY / GOOGLE_API_KEY from env)
_client = _build_client()

_SYSTEM = (
    "You are a photography assistant. Only use facts explicitly provided in <facts>...</facts>. "
    """If a detail isn't present, omit it (do not invent it). 
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
