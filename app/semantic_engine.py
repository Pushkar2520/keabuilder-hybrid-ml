import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from app.schemas import LeadInput


class SemanticIntentEngine:
    """
    Semantic similarity layer.

    This layer compares the incoming lead intent against reference
    intent patterns that represent high-converting SaaS/funnel leads.
    """

    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.SEMANTIC_MODEL_NAME)

        self.intent_examples = [
            "I want to generate qualified leads for my business",
            "I need a sales funnel for paid advertising campaigns",
            "I want to capture leads and follow up automatically",
            "I need a landing page that converts visitors into customers",
            "I want to automate CRM tagging and email follow-up",
            "I want to book more discovery calls from my website",
            "I need AI chatbot automation for lead qualification",
            "I want to improve funnel conversion and reduce drop-offs",
            "I need marketing automation for high intent leads",
            "I want a funnel for real estate buyer and seller leads"
        ]

        self.intent_embeddings = self.model.encode(
            self.intent_examples,
            normalize_embeddings=True
        )

    def calculate_semantic_score(self, lead: LeadInput) -> float:
        lead_text = self._build_lead_text(lead)

        lead_embedding = self.model.encode(
            [lead_text],
            normalize_embeddings=True
        )

        similarities = cosine_similarity(
            lead_embedding,
            self.intent_embeddings
        )[0]

        best_similarity = float(np.max(similarities))

        return round(best_similarity * 100, 2)

    @staticmethod
    def _build_lead_text(lead: LeadInput) -> str:
        parts = [
            lead.business_type,
            lead.goal,
            lead.timeline or "",
            lead.source or "",
            lead.company_size or "",
            lead.message or ""
        ]

        return " ".join(part for part in parts if part).strip()


semantic_engine = SemanticIntentEngine()