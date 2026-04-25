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
aws iam create-role \
  --role-name LambdaS3ReaderRole \
  --assume-role-policy-document file://trust-policy.json

# 3. Attach a Permissions Policy defining what the role can do
awslocal iam attach-role-policy \
  --role-name LambdaS3ReaderRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
aws iam attach-role-policy \
  --role-name LambdaS3ReaderRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

## 🧠 Key Concepts & Importance

- **Trust Policy:** A JSON policy document in which you define the principals that you trust to assume the role.
- **Permissions Policy:** Defines what actions the role can perform and on which resources.
- **IAM Role:** An IAM identity that you can create in your account that has specific permissions. An IAM role is similar to an IAM user, but it is not uniquely associated with one person.
- **STS (Security Token Service):** The service that issues temporary security credentials when a role is assumed.

## 🛠️ Command Reference

- `iam create-role`: Creates a new IAM role.
    - `--role-name`: The name of the role.
    - `--assume-role-policy-document`: The trust policy that allows an entity (like a service) to assume the role.
- `iam attach-role-policy`: Attaches a managed policy to an IAM role.
    - `--role-name`: The name of the role.
    - `--policy-arn`: The ARN of the policy to attach.

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.
