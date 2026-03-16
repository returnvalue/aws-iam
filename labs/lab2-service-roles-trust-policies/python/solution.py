import boto3
import json

iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")

trust_policy = {
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}

with open('trust-policy.json', 'w') as f:
    json.dump(trust_policy, f)

iam.create_role(
    RoleName='LambdaS3ReaderRole',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)

iam.attach_role_policy(
    RoleName='LambdaS3ReaderRole',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)
