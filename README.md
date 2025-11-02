# Cloud_IAM_Automation_System
(Systems- AWS+Python) Used to secure user and role management in AWS 

# AWS IAM Automation & Monitoring System

**Automated, secure IAM provisioning with audit logging and email alerts.**

---

## Project summary

This project demonstrates automating AWS IAM user and role provisioning using a Python Lambda function. It emphasizes security best practices (least privilege, logging via CloudTrail), serverless automation, and email notifications through SES.

**Key features**
- Create IAM users from a CSV file (S3).
- Attach least-privilege managed/custom policies.
- Send verification/notification emails via SES.
- CloudTrail logging for all identity events.
- CloudWatch metric filters/alarms for monitoring.

---

## Architecture

S3 (users.csv) → AWS Lambda (Python, Boto3) → IAM APIs (CreateUser, AttachUserPolicy)  
Lambda → SES (send email)  
CloudTrail → S3 & CloudWatch → Alarms/SNS

---

## Getting started (for beginners)

### Prerequisites
- AWS account with administrative privileges for initial setup.
- AWS CLI configured (`aws configure`).
- Python 3.9+ and `pip`.
- (Optional) AWS SAM CLI for deployment.

### 1) Prepare input CSV
Create `users.csv` with columns: Upload to S3 (e.g., `my-iam-provisioning-bucket/users.csv`).

### 2) SES setup
1. Verify the `From` email (or domain) in Amazon SES.
2. If SES in sandbox, verify recipient emails too.
See AWS SES docs for verification and sending details.

### 3) Deploy Lambda (quick)
- Create new Lambda function (Python 3.9+).
- Paste `iam_automation.py` as the handler code.
- Add environment variables:
  - `INPUT_S3_BUCKET`: your S3 bucket
  - `INPUT_S3_KEY`: `users.csv`
  - `SES_FROM`: verified SES email
  - `SES_REGION`: your SES region
- Attach an IAM role with the permissions shown in `lambda-policy.json`.

### 4) Test
- Invoke the Lambda using the test button in the console or upload a file and run the function. Check CloudWatch logs and your email for alerts.

---

## Files in this repo
- `iam_automation.py` — Lambda-compatible script
- `lambda-policy.json` — example IAM policy for Lambda execution role
- `template.yaml` — (optional) SAM template for deployment
- `README.md` — this file

---

## Security considerations & notes
- Prefer temporary credentials and IAM Identity Center for human access.
- Avoid automatically creating access keys; create them only if required and rotate regularly.
- Keep CloudTrail logs in a separate, secured S3 bucket for auditing.
- Start with AWS managed policies then narrow to customer-managed least-privilege policies.

