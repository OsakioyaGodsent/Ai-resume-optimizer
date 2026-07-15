import re
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, field_validator

PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")

class LeadPayload(BaseModel):
    name: str
    email: EmailStr
    phone: str
    source: str
    # New fields to pass down to our AI analysis engine
    resume_text: Optional[str] = None
    job_description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        clean_name = value.strip()
        if len(clean_name) < 2:
            raise ValueError("Name is structurally too short to be valid (minimum 2 characters).")
        return clean_name

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        clean_phone = value.strip().replace(" ", "")
        if not PHONE_REGEX.match(clean_phone):
            raise ValueError("Phone number must be a valid international format (e.g., +1234567890).")
        return clean_phone

    @field_validator("source")
    @classmethod
    def sanitize_source(cls, value: str) -> str:
        return value.strip().lower()