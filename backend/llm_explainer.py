import os
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

# Local imports (works when running from backend/)
from backend.rag_engine import SecurityRAGEngine

# --------------------------------------------------
# Environment & Logging
# --------------------------------------------------
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class SecurityLLMExplainer:
    """
    Production-grade AI explainer for IAM security findings
    Uses RAG for grounding and enforces strict security constraints.
    """

    def __init__(self):
        self._validate_env()

        # LLM configuration (cost-safe + deterministic)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=800
        )

        # RAG engine (shared knowledge base)
        self.rag = SecurityRAGEngine()
        self.rag.build_or_load_knowledge_base()

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------
    def _validate_env(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY not set")

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------
    def explain_findings(
        self,
        role_name: str,
        policy_name: str,
        findings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Explain IAM findings using RAG + LLM safely.
        """

        if not findings:
            return {
                "summary": "No security risks detected.",
                "details": [],
                "recommended_policy": None
            }

        explanations = []

        for finding in findings:
            try:
                context = self.rag.retrieve_context(
                    query=f"{finding['title']} IAM security risk"
                )

                prompt = self._build_prompt(
                    role_name=role_name,
                    policy_name=policy_name,
                    finding=finding,
                    context=context
                )

                response = self.llm.invoke(prompt).content

            except Exception as e:
                logger.error(f"LLM/RAG error for finding {finding.get('id')}: {e}")
                response = (
                    "Unable to generate explanation due to an internal error. "
                    "Please review this finding manually."
                )

            explanations.append({
                "finding_id": finding.get("id"),
                "severity": finding.get("severity"),
                "explanation": response
            })

        recommended_policy = self._generate_secure_policy(
            role_name=role_name,
            policy_name=policy_name,
            findings=findings
        )

        return {
            "summary": "Security risks detected in IAM policy.",
            "details": explanations,
            "recommended_policy": recommended_policy
        }

    # --------------------------------------------------
    # Prompt Engineering (STRICT & SAFE)
    # --------------------------------------------------
    def _build_prompt(
        self,
        role_name: str,
        policy_name: str,
        finding: Dict[str, Any],
        context: str
    ) -> str:
        """
        Build a constrained prompt to prevent hallucinations.
        """

        return f"""
You are a senior cloud security engineer.

STRICT RULES:
- Use ONLY the provided security context.
- Do NOT invent permissions.
- Do NOT recommend wildcard actions.
- Do NOT output IAM policy JSON or code.
- Be factual, concise, and security-focused.

IAM ROLE: {role_name}
POLICY NAME: {policy_name}

SECURITY FINDING:
- Title: {finding.get('title')}
- Severity: {finding.get('severity')}
- Description: {finding.get('description')}

SECURITY CONTEXT:
{context}

TASK:
Explain:
1. Why this configuration is dangerous
2. What real-world impact it can cause
3. High-level mitigation strategy (no code)
"""

    # --------------------------------------------------
    # Secure Policy Generator (DETERMINISTIC)
    # --------------------------------------------------
    def _generate_secure_policy(
        self,
        role_name: str,
        policy_name: str,
        findings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Deterministic least-privilege policy template.
        LLM does NOT generate permissions.
        """

        return {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::example-bucket/*"
                    ],
                    "Condition": {
                        "Bool": {
                            "aws:SecureTransport": "true"
                        }
                    }
                }
            ],
            "_note": (
                "This is a conservative least-privilege template. "
                "Permissions must be refined per workload and findings."
            )
        }
