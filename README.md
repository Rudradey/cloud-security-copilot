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

🔑 Environment Setup (VERY IMPORTANT)

This project does **NOT** use `aws configure`.

All credentials are loaded from a `.env` file.

---

### 1️⃣ Create `.env` file

Create a file named `.env` in the project root:

cloud-security-copilot/.env

yaml
Copy code

---

### 2️⃣ Add your credentials

.env
# AWS credentials (READ-ONLY recommended)
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY

AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY

AWS_DEFAULT_REGION=ap-south-1

# LLM provider
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
⚠️ Important

This file is local only

It is ignored by .gitignore

Every user must create their own .env file

🔐 Required AWS Permissions
Your AWS credentials must have read-only access.

Recommended AWS managed policies:
IAMReadOnlyAccess

OR SecurityAudit

❌ Do NOT use admin credentials

---



## ▶️ How to Run the Project

1️⃣ Clone the repository


git clone https://github.com/Rudradey/cloud-security-copilot.git

cd cloud-security-copilot



2️⃣ Create and activate virtual environment

python -m venv venv

venv\Scripts\activate

Linux / macOS



python3 -m venv venv

source venv/bin/activate



3️⃣ Install dependencies


pip install -r requirements.txt

pip install -r backend/requirements.txt

pip install -r frontend/requirements.txt



4️⃣ Run the application

Option A — Manual (2 terminals)

Terminal 1 — Backend



uvicorn backend.main:app --reload

Terminal 2 — Frontend

streamlit run frontend/streamlit_app.py



Option B — Windows (Recommended)


.\run_dev.ps1

This starts both backend and frontend automatically.


## 🖥️ Using the Application
Open the Streamlit UI in your browser


Click Start IAM Scan


Wait for scan completion


View:


IAM roles


Policy risk scores


Security findings


Click Explain Findings to get AI-generated explanations and secure policy suggestions


👉 No manual input is required in the UI.



## 🧠 How Credentials Are Used
AWS credentials are loaded from .env


LLM API key is loaded from .env


python-dotenv loads environment variables


boto3 automatically uses them


Credentials are never logged or exposed


This design is secure for local development and demos.



## 📌 Disclaimer
This project is for educational and portfolio purposes.


Do not run against production AWS accounts without proper authorization.




## 👤 Author
Rudra Dey

Cybersecurity | Cloud Security | AI Systems

