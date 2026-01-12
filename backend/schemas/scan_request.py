# backend/schemas/scan_request.py

from pydantic import BaseModel, Field
from typing import Optional


class ScanRequest(BaseModel):
    """
    Request model for initiating an IAM security scan.
    No AWS credentials are accepted via API for security reasons.
    """

    scan_name: Optional[str] = Field(
        default=None,
        description="Optional human-readable name for the scan job"
    )

    include_inline_policies: bool = Field(
        default=True,
        description="Whether to include inline IAM policies in the scan"
    )

    include_managed_policies: bool = Field(
        default=True,
        description="Whether to include attached managed IAM policies in the scan"
    )

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "scan_name": "prod-iam-scan",
                "include_inline_policies": True,
                "include_managed_policies": True
            }
        }
