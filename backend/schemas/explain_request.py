# backend/schemas/explain_request.py

from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    """
    Request model for AI-based explanation of a completed scan.
    """

    scan_id: str = Field(
        ...,
        description="Job ID of a completed IAM scan"
    )

    include_recommendations: bool = Field(
        default=True,
        description="Whether to include least-privilege remediation suggestions"
    )

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "scan_id": "8f1c2c6a-9d6e-4a1b-9b8d-2b8b6c7f4c21",
                "include_recommendations": True
            }
        }
