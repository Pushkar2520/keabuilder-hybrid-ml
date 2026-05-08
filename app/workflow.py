from app.schemas import AutomationWorkflow


def build_automation_workflow(
    lead_quality: str,
    recommended_action: str,
    recommended_funnel: str
) -> AutomationWorkflow:
    """
    Suggests downstream CRM and automation actions.
    """

    if lead_quality == "high_intent":
        return AutomationWorkflow(
            crm_tag="high_intent",
            email_sequence="high_intent_sales_followup_v1",
            notify_sales_team=True,
            next_step=recommended_action
        )

    if lead_quality == "medium_intent":
        return AutomationWorkflow(
            crm_tag="nurture_required",
            email_sequence="lead_nurture_sequence_v1",
            notify_sales_team=False,
            next_step="send_case_study_and_followup"
        )

    return AutomationWorkflow(
        crm_tag="low_intent",
        email_sequence="educational_awareness_sequence_v1",
        notify_sales_team=False,
        next_step="send_educational_content"
    )