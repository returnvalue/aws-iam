import boto3
import json

iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")

boundary_policy = {
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]
}

with open('boundary-policy.json', 'w') as f:
    json.dump(boundary_policy, f)

response = iam.create_policy(
    PolicyName='S3OnlyBoundary',
    PolicyDocument=json.dumps(boundary_policy)
)
boundary_arn = response['Policy']['Arn']

iam.create_user(
    UserName='BoundaryUser',
    PermissionsBoundary=boundary_arn
)

iam.attach_user_policy(
    UserName='BoundaryUser',
    PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
)
