import json
import requests

from app.config import settings
from app.schemas import LeadInput


def get_llm_recommendation(
    lead: LeadInput,
    rule_score: float,
    semantic_score: float
) -> dict:
    """
    Optional LLM layer.

    If enabled, this layer generates recommendation metadata and a
    confidence estimate. If disabled or unavailable, the system returns
    a deterministic fallback.
    """

    if not settings.USE_LLM or not settings.MISTRAL_API_KEY:
        return _fallback_llm_response(lead, rule_score, semantic_score)

    prompt = _build_prompt(lead, rule_score, semantic_score)

    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": settings.MISTRAL_MODEL,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an AI product intelligence assistant "
                            "for KeaBuilder, a SaaS platform for funnels, "
                            "lead capture, CRM, chatbots, content generation, "
                            "and marketing automation. Return valid JSON only."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=20
        )

        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]

        return json.loads(content)

    except Exception:
        return _fallback_llm_response(lead, rule_score, semantic_score)


def _build_prompt(
    lead: LeadInput,
    rule_score: float,
    semantic_score: float
) -> str:
    return f"""
Analyze this lead for KeaBuilder.

Lead:
- Business Type: {lead.business_type}
- Goal: {lead.goal}
- Budget: {lead.budget}
- Timeline: {lead.timeline}
- Source: {lead.source}
- Company Size: {lead.company_size}
- Message: {lead.message}

Existing Scores:
- Rule Score: {rule_score}
- Semantic Intent Score: {semantic_score}

Return JSON only with this schema:
{{
  "llm_confidence_score": number,
  "lead_quality": "low_intent | medium_intent | high_intent",
  "recommended_funnel": string,
  "recommended_action": string,
  "explanation": string
}}
"""


def _fallback_llm_response(
    lead: LeadInput,
    rule_score: float,
    semantic_score: float
) -> dict:
    average_score = (rule_score + semantic_score) / 2

    if average_score >= 75:
        quality = "high_intent"
        action = "schedule_discovery_call"
    elif average_score >= 45:
        quality = "medium_intent"
        action = "send_nurture_sequence"
    else:
        quality = "low_intent"
        action = "send_educational_content"

    business = lead.business_type.lower().replace(" ", "_")

    return {
        "llm_confidence_score": round(average_score, 2),
        "lead_quality": quality,
        "recommended_funnel": f"{business}_lead_generation_funnel",
        "recommended_action": action,
        "explanation": (
            "The recommendation was generated using fallback logic because "
            "the external LLM layer is disabled or unavailable. The decision "
            "is based on rule-based business signals and semantic similarity "
            "against high-converting lead intent patterns."
        )
    }