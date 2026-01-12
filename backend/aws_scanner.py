import boto3
import logging
import os
from datetime import datetime
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
from backend.policy_analyzer import PolicyRiskAnalyzer





load_dotenv()

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# AWS Client Configuration
# -----------------------------
AWS_CONFIG = Config(
    retries={"max_attempts": 5, "mode": "standard"},
    read_timeout=10,
    connect_timeout=5
)


# -----------------------------
# Environment Validation
# -----------------------------
def validate_env():
    if not os.getenv("AWS_DEFAULT_REGION"):
        raise EnvironmentError("AWS_DEFAULT_REGION not set")


def get_iam_client():
    return boto3.client(
        "iam",
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        config=AWS_CONFIG
    )


# -----------------------------
# IAM Fetch Helpers
# -----------------------------
def list_iam_roles(iam):
    roles = []
    paginator = iam.get_paginator("list_roles")

    for page in paginator.paginate():
        roles.extend(page.get("Roles", []))

    return roles


def get_attached_policies(iam, role_name):
    policies = []
    paginator = iam.get_paginator("list_attached_role_policies")

    for page in paginator.paginate(RoleName=role_name):
        policies.extend(page.get("AttachedPolicies", []))

    return policies


def get_inline_policies(iam, role_name):
    policies = []
    paginator = iam.get_paginator("list_role_policies")

    for page in paginator.paginate(RoleName=role_name):
        policies.extend(page.get("PolicyNames", []))

    return policies


def get_managed_policy_document(iam, policy_arn):
    policy = iam.get_policy(PolicyArn=policy_arn)
    version_id = policy["Policy"]["DefaultVersionId"]

    policy_version = iam.get_policy_version(
        PolicyArn=policy_arn,
        VersionId=version_id
    )

    return policy_version.get("PolicyVersion", {}).get("Document", {})


def get_inline_policy_document(iam, role_name, policy_name):
    response = iam.get_role_policy(
        RoleName=role_name,
        PolicyName=policy_name
    )
    return response.get("PolicyDocument", {})


# -----------------------------
# Main Scanner
# -----------------------------
def scan_roles_and_policies():
    validate_env()
    iam = get_iam_client()
    analyzer = PolicyRiskAnalyzer()

    results = {
        "scan_metadata": {
            "region": os.getenv("AWS_DEFAULT_REGION"),
            "scan_time": datetime.utcnow().isoformat()
        },
        "roles": []
    }

    try:
        roles = list_iam_roles(iam)

        for role in roles:
            role_name = role.get("RoleName")
            logger.info(f"Scanning role: {role_name}")

            role_data = {
                "RoleName": role_name,
                "Arn": role.get("Arn"),
                "AttachedPolicies": [],
                "InlinePolicies": []
            }

            # -----------------------------
            # Managed Policies
            # -----------------------------
            for policy in get_attached_policies(iam, role_name):
                try:
                    doc = get_managed_policy_document(iam, policy["PolicyArn"])

                    analysis = analyzer.analyze_policy(
                        policy=doc,
                        policy_name=policy["PolicyName"]
                    )

                    role_data["AttachedPolicies"].append({
                        "PolicyName": policy["PolicyName"],
                        "PolicyArn": policy["PolicyArn"],
                        "RiskScore": analysis["risk_score"],
                        "Findings": analysis["findings"]
                    })

                except ClientError as e:
                    logger.warning(
                        f"Failed to scan managed policy {policy['PolicyName']} on role {role_name}: {e}"
                    )

            # -----------------------------
            # Inline Policies
            # -----------------------------
            for policy_name in get_inline_policies(iam, role_name):
                try:
                    doc = get_inline_policy_document(iam, role_name, policy_name)

                    analysis = analyzer.analyze_policy(
                        policy=doc,
                        policy_name=policy_name
                    )

                    role_data["InlinePolicies"].append({
                        "PolicyName": policy_name,
                        "RiskScore": analysis["risk_score"],
                        "Findings": analysis["findings"]
                    })

                except ClientError as e:
                    logger.warning(
                        f"Failed to scan inline policy {policy_name} on role {role_name}: {e}"
                    )

            results["roles"].append(role_data)

        logger.info("IAM policy scan completed successfully")
        return results

    except NoCredentialsError:
        logger.critical("AWS credentials not found")
        raise
    except ClientError as e:
        logger.critical(f"AWS fatal error: {e}")
        raise


# -----------------------------
# Local Execution
# -----------------------------
if __name__ == "__main__":
    scan_data = scan_roles_and_policies()

    for role in scan_data["roles"]:
        logger.info(
            f"ROLE {role['RoleName']} | "
            f"Managed={len(role['AttachedPolicies'])} | "
            f"Inline={len(role['InlinePolicies'])}"
        )


