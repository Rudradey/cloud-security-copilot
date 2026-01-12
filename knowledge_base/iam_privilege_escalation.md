IAM privilege escalation occurs when permissions like iam:PassRole,
iam:AttachRolePolicy, or iam:* are granted.

Impact:
- Full AWS account compromise
- Persistent backdoor creation

Mitigation:
- Restrict IAM permissions tightly
- Use condition keys such as iam:PassedToService
