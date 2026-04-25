# Lab 3: Policy Evaluation Logic (Explicit Deny vs. Allow)

**Goal:** IAM defaults to Implicit Deny. If a policy has an Allow, the action is permitted. However, if any policy evaluates to an Explicit Deny, it will completely override the Allow.

```bash
# 1. Create an Allow policy for all S3 buckets
cat <<EOF > s3-allow-all.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]
}
EOF
ALLOW_POLICY_ARN=$(awslocal iam create-policy --policy-name S3AllowAll --policy-document file://s3-allow-all.json --query 'Policy.Arn' --output text)
ALLOW_POLICY_ARN=$(aws iam create-policy --policy-name S3AllowAll --policy-document file://s3-allow-all.json --query 'Policy.Arn' --output text)

# 2. Create an Explicit Deny policy for a specific "production" bucket
cat <<EOF > s3-explicit-deny.json
{
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
EOF
DENY_POLICY_ARN=$(awslocal iam create-policy --policy-name S3ExplicitDeny --policy-document file://s3-explicit-deny.json --query 'Policy.Arn' --output text)
DENY_POLICY_ARN=$(aws iam create-policy --policy-name S3ExplicitDeny --policy-document file://s3-explicit-deny.json --query 'Policy.Arn' --output text)

# 3. Attach both policies to a new user
awslocal iam create-user --user-name DataScientist
aws iam create-user --user-name DataScientist
awslocal iam attach-user-policy --user-name DataScientist --policy-arn $ALLOW_POLICY_ARN
aws iam attach-user-policy --user-name DataScientist --policy-arn $ALLOW_POLICY_ARN
awslocal iam attach-user-policy --user-name DataScientist --policy-arn $DENY_POLICY_ARN
aws iam attach-user-policy --user-name DataScientist --policy-arn $DENY_POLICY_ARN
```

## 🧠 Key Concepts & Importance

- **Implicit Deny:** By default, all requests are denied.
- **Explicit Allow:** A policy that allows a specific action on a specific resource.
- **Explicit Deny:** A policy that explicitly denies a specific action on a specific resource. This always overrides any Allow.
- **Policy Evaluation Order:** AWS evaluates all policies that apply to the request. If an explicit deny is found in any of those policies, the request is denied.

## 🛠️ Command Reference

- `iam create-policy`: Creates a new managed policy.
    - `--policy-name`: The name of the policy.
    - `--policy-document`: The JSON policy document.
- `iam create-user`: Creates a new IAM user.
    - `--user-name`: The name of the user.
- `iam attach-user-policy`: Attaches a managed policy to an IAM user.
    - `--user-name`: The name of the user.
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
