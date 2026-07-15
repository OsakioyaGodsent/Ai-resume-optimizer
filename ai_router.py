from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai_optimizer import analyze_resume_fit

router = APIRouter(prefix="/api/v1/optimize", tags=["AI Resume Optimizer"])


# Request Schema specific to Project 1's interface
class OptimizationRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/analyze")
async def optimize_resume(payload: OptimizationRequest):
    if not payload.resume_text.strip() or not payload.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Both resume_text and job_description must contain content."
        )

    # Run the Gemini evaluation
    analysis = await analyze_resume_fit(payload.resume_text, payload.job_description)

    # Calculate quick visual metrics for a potential frontend UI dashboard
    match_score = analysis.get("match_score", 0)
    if match_score >= 80:
        grade = "Excellent Match"
    elif match_score >= 50:
        grade = "Moderate Match (Needs Optimization)"
    else:
        grade = "Low Match (Severe Gaps)"

    return {
        "status": "success",
        "optimization_grade": grade,
        "results": analysis
    }