import boto3
import json

sts = boto3.client('sts', endpoint_url="http://localhost:4566", region_name="us-east-1")
iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")

account_id = sts.get_caller_identity()['Account']

trust_policy = {
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
    "Action": "sts:AssumeRole",
    "Condition": {
      "StringEquals": {
        "sts:ExternalId": "SuperSecretVendorID-123"
      }
    }
  }]
}

with open('cross-account-trust.json', 'w') as f:
    json.dump(trust_policy, f)

iam.create_role(
    RoleName='VendorCrossAccountRole',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)

sts.assume_role(
    RoleArn=f"arn:aws:iam::{account_id}:role/VendorCrossAccountRole",
    RoleSessionName='VendorAuditSession',
    ExternalId='SuperSecretVendorID-123',
    DurationSeconds=3600
)
