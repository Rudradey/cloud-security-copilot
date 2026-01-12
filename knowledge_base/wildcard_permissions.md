Wildcard permissions (*) in IAM policies allow unrestricted access
to AWS services or resources. This violates the principle of least
privilege and is a common root cause of cloud breaches.

Best Practice:
- Replace "*" with specific actions
- Scope resources using ARNs
- Use conditions where possible
