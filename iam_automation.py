import os
import csv
import io
import boto3
from botocore.exceptions import ClientError

S3_BUCKET = os.environ.get("S3_BUCKET")  # set in Lambda env vars
S3_KEY = os.environ.get("S3_KEY")
SES_FROM = os.environ.get("SES_FROM")  # verified SES address
SES_REGION = os.environ.get("SES_REGION")  # change as needed
DEFAULT_ROLE_TRUST = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

iam = boto3.client("iam")
s3 = boto3.client("s3")
ses = boto3.client("ses", region_name=SES_REGION)

def read_csv_from_s3(bucket, key):
    resp = s3.get_object(Bucket=bucket, Key=key)
    content = resp["Body"].read().decode("utf-8")
    return csv.DictReader(io.StringIO(content))

def user_exists(username):
    try:
        iam.get_user(UserName=username)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            return False
        raise

def create_user(username):
    iam.create_user(UserName=username)
    # Optionally create access keys or console password — here we avoid creating long-lived creds
    print(f"Created user {username}")

def attach_policy_to_user(username, policy_arn):
    iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)
    print(f"Attached policy {policy_arn} to {username}")

def create_role_if_missing(role_name, assume_policy_doc=None):
    try:
        iam.get_role(RoleName=role_name)
        print(f"Role {role_name} exists")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            doc = assume_policy_doc or DEFAULT_ROLE_TRUST
            iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(doc))
            print(f"Created role {role_name}")
        else:
            raise

def send_email(to_address, subject, body_html, body_text=None):
    if not body_text:
        body_text = (body_html.replace("<br>", "\n").replace("<b>", "").replace("</b>", ""))
    ses.send_email(
        Source=SES_FROM,
        Destination={"ToAddresses": [to_address]},
        Message={
            "Subject": {"Data": subject},
            "Body": {
                "Text": {"Data": body_text},
                "Html": {"Data": body_html}
            }
        }
    )
    print(f"Sent email to {to_address}")

def lamda_handler(event, context):
    records = read_csv_from_s3(S3_BUCKET, S3_KEY)
    results = []
    for row in records:
        username = row.get("username")
        email = row.get("email")
        role = row.get("role")
        policy = row.get("policy")

        if not username or not email or not policy:
            print(f"Skipping row missing data: {row}")
            continue

        if not user_exists(username):
            create_user(username)
            # attach policy
            try:
                attach_policy_to_user(username, policy)
            except ClientError as e:
                print(f"Failed to attach policy: {e}")
            # optional: add user to role via inline policy or groups (not shown)
            # send email to the user and admin
            subject = f"[IAM Automation] New user created: {username}"
            body_html = (f"<b>User:</b> {username}<br>"
                         f"<b>Role:</b> {role}<br>"
                         f"<b>Policy:</b> {policy}<br>")
            send_email(email, subject, body_html)
            results.append({"username": username, "status": "created", "policy": policy})
        else:
            print(f"User {username} already exists; skipping creation.")
            results.append({"username": username, "status": "exists"})

    return {"results": results}