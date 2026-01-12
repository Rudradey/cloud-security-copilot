🛡️ AI-Powered Cloud Security Copilot

AI-Powered Cloud Security Copilot is a **full-stack cloud security and AI project** that scans **AWS IAM roles and policies**, detects **security risks**, and explains them using **LLMs + RAG (Retrieval-Augmented Generation)**.

This project is built as an **industry-style security tool**, not a demo script.

---

## 🎯 What This Project Does

The application:

- 🔍 Scans AWS IAM roles and attached policies
- ⚠️ Detects common IAM security risks:
  - Wildcard permissions (`*`)
  - Over-privileged roles
  - Privilege-escalation risks
  - Missing policy conditions
- 🤖 Uses AI to:
  - Explain *why* a policy is risky
  - Suggest least-privilege alternatives
- 🖥️ Provides a modern **Streamlit dashboard** with:
  - One-click scan
  - Live scan status
  - Findings dashboard
  - AI security advisor

---

## 🧠 High-Level Architecture

Streamlit UI
↓
FastAPI Backend
↓
AWS IAM Scanner
↓
Policy Risk Analyzer
↓
RAG Engine (FAISS + Knowledge Base)
↓
LLM Security Explanation

yaml
Copy code

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- Boto3 (AWS SDK)

### Frontend
- Streamlit

### AI
- LLM (OpenAI or compatible)
- RAG using FAISS

### Cloud & Security
- AWS IAM (Read-only scanning)
- Secure credential handling
- No credentials via UI or API

---

## 🔐 Security Design (IMPORTANT)

- ❌ No AWS credentials are accepted via UI
- ❌ No secrets are stored in code
- ❌ No secrets are committed to GitHub
- ✅ Credentials are loaded from environment variables (`.env`)
- ✅ Each user runs the app using **their own AWS account**

This is **industry-standard local development practice**.

---

## ⚙️ Prerequisites

Before running the project, you need:

- Python **3.9 or higher**
- An AWS account
- AWS IAM **read-only credentials**
- An LLM API key (e.g. OpenAI)

---

## 🔑 Environment Setup (VERY IMPORTANT)

This project **does NOT use `aws configure`**.

All credentials are loaded from a `.env` file.

---

### 1️⃣ Create `.env` file

Create a file named `.env` in the **project root**:

cloud-security-copilot/.env

yaml
Copy code

---

### 2️⃣ Add your credentials

```env
# AWS credentials (READ-ONLY recommended)
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY
AWS_DEFAULT_REGION=ap-south-1

# LLM provider
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
⚠️ This file is local only
⚠️ It is ignored by .gitignore
⚠️ Every user must create their own .env

🔐 Required AWS Permissions
Your AWS credentials must have read-only access.

Recommended policies:

IAMReadOnlyAccess

OR SecurityAudit

❌ Do NOT use admin credentials

