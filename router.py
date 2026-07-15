import uuid
import httpx
from fastapi import APIRouter
from schemas import LeadPayload
from ai_optimizer import analyze_resume_fit  # Import our AI module!

router = APIRouter(prefix="/api/v1", tags=["Leads"])

MOCK_CRM_WEBHOOK_URL = "https://httpbin.org/post"


@router.post("/leads")
async def route_lead(payload: LeadPayload):
    lead_id = str(uuid.uuid4())
    webhook_status = "Skipped (Standard Route)"
    ai_feedback = None

    # Conditional logic matrix routing
    if payload.source in ["premium", "vip"]:
        assigned_route = "HIGH_PRIORITY_QUEUE"
        status = "Escalated to sales desk instantly."

        # Trigger the AI Optimization Engine if data is provided!
        if payload.resume_text and payload.job_description:
            # Call our Google Gemini engine asynchronously
            ai_feedback = await analyze_resume_fit(payload.resume_text, payload.job_description)
        else:
            ai_feedback = {
                "message": "Premium processing active, but resume_text or job_description was missing from submission."
            }

        # Webhook Simulation: Forwarding the data downstream
        try:
            async with httpx.AsyncClient() as client:
                forwarding_payload = {
                    "event": "lead.priority_escalation",
                    "lead_tracking_id": lead_id,
                    "lead_data": payload.model_dump(),
                    "ai_evaluation": ai_feedback
                }
                await client.post(MOCK_CRM_WEBHOOK_URL, json=forwarding_payload, timeout=5.0)
                webhook_status = "Successfully dispatched payload with AI feedback to CRM backend."
        except httpx.RequestError as exc:
            webhook_status = f"Webhook transmission failed: {exc}"

    else:
        assigned_route = "STANDARD_NURTURE_QUEUE"
        status = "Assigned to general automation sequence."

    return {
        "success": True,
        "lead_id": lead_id,
        "assigned_route": assigned_route,
        "status": status,
        "webhook_delivery": webhook_status,
        "ai_analysis": ai_feedback,
        "processed_payload": payload
    }