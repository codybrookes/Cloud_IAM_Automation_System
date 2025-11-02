# Cloud_IAM_Automation_System
(Systems- AWS+Python) Used to secure user and role management in AWS 

## Project summary

This project shows how to automate the creation and management of AWS IAM users and roles using a Python Lambda function. It focuses on:

Security best practices: Least-privilege permissions and full logging via CloudTrail.
Serverless automation: Fully automated user and role management using Lambda.
Notifications: Email alerts using Amazon SES for newly provisioned users.

**Key features**
- Automatically create IAM users from a CSV stored in S3.
- Attach least-privilege managed or custom policies to users.
- Send notification emails through SES when users are created.
- Log all identity events with CloudTrail.
- Monitor critical events with CloudWatch metric filters and alarms

---

## Architecture

S3 (users.csv) → AWS Lambda (Python, Boto3) → IAM APIs (CreateUser, AttachUserPolicy)  
Lambda → SES (send email)  
CloudTrail → S3 & CloudWatch → Alarms/SNS

---

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
- `IAMAutomation_json_policy.json` — example IAM policy for Lambda execution role
- `README.md` — this file

---

## Security considerations & notes
- Prefer temporary credentials and IAM Identity Center for human access.
- Avoid automatically creating access keys; create them only if required and rotate regularly.
- Keep CloudTrail logs in a separate, secured S3 bucket for auditing.
- Start with AWS managed policies then narrow to customer-managed least-privilege policies.

