import logging
# Absolute Import: This tells Python to look inside the backend package

from backend.aws_scanner import scan_roles_and_policies

logger = logging.getLogger("cloud-security-copilot")

def run_iam_scan():
    """
    Orchestrates IAM scanning.
    This service connects the API to the low-level AWS scanner logic.
    """
    try:
        logger.info("Service: Initiating AWS IAM scan roles and policies")
        results = scan_roles_and_policies()
        return results
    except Exception as e:
        logger.error(f"Service: IAM scan failed in orchestration layer: {str(e)}")
        raise e