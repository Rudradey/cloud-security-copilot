import logging
from typing import List, Dict, Any, Optional
from enum import Enum

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PolicyRiskAnalyzer:
    """
    Enterprise-grade IAM Policy Risk Analyzer
    """

    SENSITIVE_PREFIXES = ("iam:", "sts:", "ec2:", "s3:")
    PRIV_ESCALATION_ACTIONS = {
        "iam:*",
        "sts:AssumeRole",
        "iam:PassRole"
    }

    def analyze_policy(
        self,
        policy: Dict[str, Any],
        policy_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a full IAM policy document safely
        """
        results = {
            "policy_name": policy_name,
            "findings": [],
            "risk_score": 0
        }

        statements = policy.get("Statement", [])
        if not statements:
            results["findings"].append(
                self._finding(
                    title="Empty Policy",
                    severity=Severity.LOW,
                    description="Policy contains no statements",
                    statement_index=-1
                )
            )
            return results

        if not isinstance(statements, list):
            statements = [statements]

        for idx, statement in enumerate(statements):
            findings = self._analyze_statement(statement, idx)
            results["findings"].extend(findings)

        results["risk_score"] = self._calculate_risk_score(results["findings"])
        return results

    def _analyze_statement(
        self,
        statement: Dict[str, Any],
        index: int
    ) -> List[Dict[str, Any]]:

        findings = []

        effect = str(statement.get("Effect", "Allow")).lower()

        # ✅ Ignore Deny statements (best practice)
        if effect == "deny":
            return findings

        actions = self._normalize(statement.get("Action"))
        not_actions = self._normalize(statement.get("NotAction"))
        resources = self._normalize(statement.get("Resource"))
        not_resources = self._normalize(statement.get("NotResource"))
        conditions = statement.get("Condition")

        # 🔴 NotAction is dangerous
        if not_actions:
            findings.append(self._finding(
                "NotAction Usage",
                Severity.HIGH,
                "NotAction grants all actions except listed ones",
                index
            ))

        # 🔴 NotResource is dangerous
        if not_resources:
            findings.append(self._finding(
                "NotResource Usage",
                Severity.HIGH,
                "NotResource grants access to all resources except listed ones",
                index
            ))

        # 🔴 Wildcard action
        if "*" in actions:
            findings.append(self._finding(
                "Wildcard Action",
                Severity.HIGH,
                "Policy allows all actions (*)",
                index
            ))

        # 🔴 Wildcard resource
        if "*" in resources:
            severity = Severity.HIGH if not conditions else Severity.MEDIUM
            findings.append(self._finding(
                "Wildcard Resource",
                severity,
                "Policy allows access to all resources (*)",
                index
            ))

        # 🔴 Privilege escalation vectors
        if self._has_privilege_escalation(actions):
            findings.append(self._finding(
                "Privilege Escalation Risk",
                Severity.CRITICAL,
                "Policy contains IAM/ST S actions that enable privilege escalation",
                index
            ))

        # 🟠 Sensitive actions without conditions
        if self._is_sensitive(actions) and not conditions:
            findings.append(self._finding(
                "Missing Condition",
                Severity.MEDIUM,
                "Sensitive actions are not protected by conditions",
                index
            ))

        return findings

    def _normalize(self, field) -> List[str]:
        if isinstance(field, list):
            return field
        if isinstance(field, str):
            return [field]
        return []

    def _is_sensitive(self, actions: List[str]) -> bool:
        return any(action.startswith(self.SENSITIVE_PREFIXES) for action in actions)

    def _has_privilege_escalation(self, actions: List[str]) -> bool:
        return any(
            action == "*" or
            action in self.PRIV_ESCALATION_ACTIONS or
            action.startswith("iam:")
            for action in actions
        )

    def _calculate_risk_score(self, findings: List[Dict[str, Any]]) -> int:
        score_map = {
            Severity.LOW: 1,
            Severity.MEDIUM: 3,
            Severity.HIGH: 7,
            Severity.CRITICAL: 10
        }
        return sum(score_map[f["severity"]] for f in findings)

    def _finding(
        self,
        title: str,
        severity: Severity,
        description: str,
        statement_index: int
    ) -> Dict[str, Any]:
        return {
            "id": f"{title.replace(' ', '_').upper()}_{statement_index}",
            "title": title,
            "severity": severity,
            "description": description,
            "statement_index": statement_index
        }
