from app.schemas import LeadInput


def recommend_funnel(lead: LeadInput, lead_quality: str) -> str:
    """
    Maps lead profile to the most suitable funnel type.
    """

    business_type = lead.business_type.lower()
    goal = lead.goal.lower()

    if "real estate" in business_type:
        if "seller" in goal:
            return "real_estate_seller_lead_funnel"
        return "real_estate_buyer_lead_funnel"

    if "coaching" in business_type:
        return "coach_discovery_call_funnel"

    if "agency" in business_type:
        return "agency_client_acquisition_funnel"

    if "ecommerce" in business_type:
        return "ecommerce_offer_conversion_funnel"

    if "saas" in business_type:
        return "saas_demo_booking_funnel"

    if lead_quality == "high_intent":
        return "high_intent_lead_capture_funnel"

    return "general_lead_nurture_funnel"