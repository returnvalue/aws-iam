# Lab 2: Service Roles & Trust Policies

**Goal:** Compute services like Lambda should never use hardcoded access keys. Instead, create a Service Role with a Trust Policy that allows the Lambda service to assume the role.

```bash
# 1. Create a Trust Policy document allowing Lambda to assume the role
cat <<EOF > trust-policy.json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF

# 2. Create the IAM Role using the Trust Policy
awslocal iam create-role \
  --role-name LambdaS3ReaderRole \
  --assume-role-policy-document file://trust-policy.json

# 3. Attach a Permissions Policy defining what the role can do
awslocal iam attach-role-policy \
  --role-name LambdaS3ReaderRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

## 🧠 Key Concepts & Importance

- **Trust Policy:** A JSON policy document in which you define the principals that you trust to assume the role.
- **Permissions Policy:** Defines what actions the role can perform and on which resources.
- **IAM Role:** An IAM identity that you can create in your account that has specific permissions. An IAM role is similar to an IAM user, but it is not uniquely associated with one person.
- **STS (Security Token Service):** The service that issues temporary security credentials when a role is assumed.
