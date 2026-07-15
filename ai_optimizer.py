import os
import json
from google import genai
from google.genai import types

# Initialize the Gemini client using the key from the loaded environment
client = genai.Client()


async def analyze_resume_fit(resume_text: str, job_description: str) -> dict:
    """
    Sends resume and job description to Gemini-3.1-flash-lite.
    Returns a structured dictionary of match analytics, including an optimized summary.
    """

    prompt = f"""
    You are an expert technical recruiter and ATS (Applicant Tracking System) optimization engine.
    Analyze the following Resume against the Job Description.

    Resume:
    \"\"\"{resume_text}\"\"\"

    Job Description:
    \"\"\"{job_description}\"\"\"

    You must output your complete response in valid JSON format. Do not wrap it in markdown blocks or code blocks.
    The JSON structure must match exactly this format:
    {{
        "match_score": 75, 
        "missing_keywords": ["Keyword1", "Keyword2"],
        "formatting_advice": ["Advice point 1", "Advice point 2"],
        "strategic_gaps": "A detailed paragraph explaining structural experience gaps.",
        "optimized_summary": "A high-impact, 3-to-4 sentence professional resume executive summary tailored perfectly to this job description. It must seamlessly integrate the missing keywords while remaining authentic to the resume's experience."
    }}

    Make sure match_score is an integer between 0 and 100.
    """

    try:
        # Run the generation request asynchronously using the stable gemini-3.1-flash-lite
        response = await client.aio.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        # Parse the JSON response
        result_data = json.loads(response.text.strip())
        return result_data

    except Exception as e:
        return {
            "error": "Failed to generate AI feedback.",
            "details": str(e),
            "match_score": 0,
            "missing_keywords": [],
            "formatting_advice": ["Could not load structural advice at this moment."],
            "strategic_gaps": "AI Engine temporarily unavailable.",
            "optimized_summary": "Unable to generate summary due to a system interruption."
        }