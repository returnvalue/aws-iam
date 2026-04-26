# Lab 4: Conditional Access

**Goal:** Enforce restrictions on the types of EC2 instances a user can provision by applying a Condition block to their policy.
```bash
# 1. Create a policy with an EC2 InstanceType condition
cat <<EOF > restrict-ec2.json
{
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
EOF

# 2. Create the policy
awslocal iam create-policy --policy-name RestrictEC2InstanceType --policy-document file://restrict-ec2.json
aws iam create-policy --policy-name RestrictEC2InstanceType --policy-document file://restrict-ec2.json
```

## 🧠 Key Concepts & Importance

- **Policy Conditions:** The `Condition` element (or `Condition` block) lets you specify conditions for when a policy is in effect.
- **ABAC (Attribute-Based Access Control):** An authorization strategy that defines permissions based on attributes, such as tags or properties of the resource or request.
- **Granular Control:** Conditions allow you to go beyond simple service-level permissions and enforce specific business rules (e.g., "only allow small instances" or "only allow access from a specific IP").
- **Condition Keys:** Service-specific keys (like `ec2:InstanceType`) and global keys (like `aws:SourceIp`) provide the data used for evaluation.

## 🛠️ Command Reference

- `iam create-policy`: Creates a new managed policy.
    - `--policy-name`: The name of the policy.
    - `--policy-document`: The JSON policy document containing conditions.

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
