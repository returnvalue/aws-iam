import boto3

iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")

iam.create_user(UserName='DevUser')

iam.create_group(GroupName='Developers')

iam.add_user_to_group(UserName='DevUser', GroupName='Developers')

iam.attach_group_policy(
    GroupName='Developers',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)
