import boto3
import json

iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")

restrict_ec2_policy = {
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "ec2:RunInstances",
    "Resource": "arn:aws:ec2:*:*:instance/*",
    "Condition": {
      "StringEquals": {
        "ec2:InstanceType": ["t3.micro", "t3.small"]
      }
    }
  }]
}

with open('restrict-ec2.json', 'w') as f:
    json.dump(restrict_ec2_policy, f)

iam.create_policy(
    PolicyName='RestrictEC2InstanceType',
    PolicyDocument=json.dumps(restrict_ec2_policy)
)
