import boto3
import json

iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")

allow_policy = {
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]
}

with open('s3-allow-all.json', 'w') as f:
    json.dump(allow_policy, f)

allow_response = iam.create_policy(
    PolicyName='S3AllowAll',
    PolicyDocument=json.dumps(allow_policy)
)
allow_arn = allow_response['Policy']['Arn']

deny_policy = {
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Action": "s3:*",
    "Resource": [
      "arn:aws:s3:::production-data",
      "arn:aws:s3:::production-data/*"
    ]
  }]
}

with open('s3-explicit-deny.json', 'w') as f:
    json.dump(deny_policy, f)

deny_response = iam.create_policy(
    PolicyName='S3ExplicitDeny',
    PolicyDocument=json.dumps(deny_policy)
)
deny_arn = deny_response['Policy']['Arn']

iam.create_user(UserName='DataScientist')

iam.attach_user_policy(UserName='DataScientist', PolicyArn=allow_arn)
iam.attach_user_policy(UserName='DataScientist', PolicyArn=deny_arn)
