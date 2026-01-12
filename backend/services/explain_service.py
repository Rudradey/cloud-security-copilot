import logging
from typing import List, Dict, Any

# 1. Absolute Imports for Production
from backend.llm_explainer import SecurityLLMExplainer

logger = logging.getLogger("cloud-security-copilot")

def explain_scan_results(scan_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes EXISTING scan data and generates AI explanations.
    Does NOT run the scan again.
    """
    explainer = SecurityLLMExplainer()
    explanations = []

    # Check if scan_data is empty or invalid
    if not scan_data or "roles" not in scan_data:
        logger.warning("No roles found in scan data to explain.")
        return {"results": []}

    logger.info(f"Generating AI explanations for {len(scan_data['roles'])} roles")

    # 2. Iterate through the data passed from the jobs_db
    for role in scan_data["roles"]:
        role_name = role.get("RoleName", "Unknown")
        
        for policy in role.get("AttachedPolicies", []):
            policy_name = policy.get("PolicyName", "Unknown")
            findings = policy.get("Findings", [])

            # Only explain if there are actual security findings
            if findings:
                try:
                    explanation = explainer.explain_findings(
                        role_name=role_name,
                        policy_name=policy_name,
                        findings=findings
                    )
                    
                    explanations.append({
                        "Role": role_name,
                        "Policy": policy_name,
                        "Explanation": explanation
                    })
                except Exception as e:
                    logger.error(f"LLM failed to explain {policy_name}: {str(e)}")
                    continue

    return {
        "results": explanations,
        "summary": {
            "total_explained": len(explanations),
            "timestamp": scan_data.get("finished_at")
        }
    }