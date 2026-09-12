import json
import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("ai_home_hub.openai")

_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
_client = None


class OpenAIServiceError(Exception):
    pass


def _get_client():
    global _client
    if _client is not None:
        return _client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIServiceError("OpenAI API key is not configured.")
    from openai import OpenAI

    _client = OpenAI(api_key=api_key)
    return _client


def chat_json(system_prompt: str, user_prompt: str) -> dict:
    """Sends a system/user prompt pair to the configured model and returns the parsed
    JSON object from the response. Raises OpenAIServiceError on any failure without
    leaking provider internals or secrets."""
    client = _get_client()
    try:
        logger.info("openai.chat_json.request model=%s", _MODEL)
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            timeout=30,
        )
        content = response.choices[0].message.content
        result = json.loads(content)
        logger.info("openai.chat_json.success model=%s", _MODEL)
        return result
    except OpenAIServiceError:
        raise
    except json.JSONDecodeError as exc:
        logger.error("openai.chat_json.invalid_json")
        raise OpenAIServiceError("The AI service returned an unreadable response.") from exc
    except Exception as exc:  # noqa: BLE001 - centralize all provider errors here
        logger.error("openai.chat_json.failed error_type=%s", type(exc).__name__)
        raise OpenAIServiceError("The AI service is currently unavailable.") from exc
