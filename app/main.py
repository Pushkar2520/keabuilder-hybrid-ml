from fastapi import FastAPI

from app.config import settings
from app.schemas import LeadInput, LeadIntelligenceResponse, ScoreBreakdown
from app.scoring import calculate_rule_score
from app.semantic_engine import semantic_engine
from app.llm_engine import get_llm_recommendation
from app.recommender import recommend_funnel
from app.workflow import build_automation_workflow


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Hybrid ML Lead Intelligence API for KeaBuilder. "
        "Combines rule-based scoring, semantic similarity, and optional LLM reasoning."
    )
)


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "semantic_model": settings.SEMANTIC_MODEL_NAME,
        "llm_enabled": settings.USE_LLM
    }


@app.post("/api/v1/analyze-lead", response_model=LeadIntelligenceResponse)
def analyze_lead(lead: LeadInput):
    rule_score = calculate_rule_score(lead)

    semantic_score = semantic_engine.calculate_semantic_score(lead)

    llm_result = get_llm_recommendation(
        lead=lead,
        rule_score=rule_score,
        semantic_score=semantic_score
    )

    llm_confidence_score = float(
        llm_result.get("llm_confidence_score", 50.0)
    )

    final_score = (
        rule_score * settings.RULE_WEIGHT
        + semantic_score * settings.SEMANTIC_WEIGHT
        + llm_confidence_score * settings.LLM_WEIGHT
    )

    final_score = round(final_score, 2)

    if final_score >= 75:
        lead_quality = "high_intent"
    elif final_score >= 45:
        lead_quality = "medium_intent"
    else:
        lead_quality = "low_intent"

    recommended_funnel = recommend_funnel(lead, lead_quality)

    recommended_action = llm_result.get(
        "recommended_action",
        "send_nurture_sequence"
    )

    automation_workflow = build_automation_workflow(
        lead_quality=lead_quality,
        recommended_action=recommended_action,
        recommended_funnel=recommended_funnel
    )

    return LeadIntelligenceResponse(
        lead_quality=lead_quality,
        recommended_funnel=recommended_funnel,
        recommended_action=recommended_action,
        score_breakdown=ScoreBreakdown(
            rule_score=round(rule_score, 2),
            semantic_score=round(semantic_score, 2),
            llm_confidence_score=round(llm_confidence_score, 2),
            final_score=final_score
        ),
        automation_workflow=automation_workflow,
        explanation=llm_result.get(
            "explanation",
            "Lead analyzed using hybrid scoring."
        ),
        metadata={
            "scoring_method": "hybrid_rule_semantic_llm",
            "rule_weight": settings.RULE_WEIGHT,
            "semantic_weight": settings.SEMANTIC_WEIGHT,
            "llm_weight": settings.LLM_WEIGHT
        }
    )