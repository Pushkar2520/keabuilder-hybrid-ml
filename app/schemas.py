from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class LeadInput(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)

    business_type: str = Field(
        ...,
        description="Business category such as Real Estate, Coaching, Agency, Ecommerce"
    )

    goal: str = Field(
        ...,
        description="Lead objective or requirement"
    )

    budget: Optional[float] = Field(
        default=None,
        ge=0,
        description="Estimated budget in local currency"
    )

    timeline: Optional[str] = Field(
        default=None,
        description="Expected buying or implementation timeline"
    )

    source: Optional[str] = Field(
        default=None,
        description="Lead source such as Facebook Ads, Google Ads, Organic, Referral"
    )

    company_size: Optional[str] = None
    message: Optional[str] = None


class ScoreBreakdown(BaseModel):
    rule_score: float
    semantic_score: float
    llm_confidence_score: float
    final_score: float


class AutomationWorkflow(BaseModel):
    crm_tag: str
    email_sequence: str
    notify_sales_team: bool
    next_step: str


class LeadIntelligenceResponse(BaseModel):
    lead_quality: str
    recommended_funnel: str
    recommended_action: str
    score_breakdown: ScoreBreakdown
    automation_workflow: AutomationWorkflow
    explanation: str
    metadata: Dict[str, Any]