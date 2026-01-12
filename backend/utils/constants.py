"""
Central place for application-wide constants.
No secrets should ever be stored here.
"""

# -----------------------------
# Application
# -----------------------------
APP_NAME = "cloud-security-copilot"
APP_VERSION = "1.1.0"

# -----------------------------
# Job Status
# -----------------------------
JOB_STATUS_PENDING = "pending"
JOB_STATUS_IN_PROGRESS = "in_progress"
JOB_STATUS_COMPLETED = "completed"
JOB_STATUS_FAILED = "failed"

# -----------------------------
# Security Severity Levels
# -----------------------------
SEVERITY_LOW = "LOW"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_HIGH = "HIGH"
SEVERITY_CRITICAL = "CRITICAL"

# -----------------------------
# IAM Analysis
# -----------------------------
MAX_POLICY_SIZE_KB = 100
DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"

# -----------------------------
# AI / RAG
# -----------------------------
DEFAULT_RAG_TOP_K = 3
LLM_MAX_TOKENS = 800
LLM_TEMPERATURE = 0
