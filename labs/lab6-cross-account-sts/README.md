# Lab 6: Temporary Access via STS (Confused Deputy Prevention)

**Goal:** Grant a third-party vendor temporary access to your account using `sts:AssumeRole`. Implement an `ExternalId` condition to protect against the "Confused Deputy" vulnerability.
```bash
# 1. Dynamically get your LocalStack Account ID
ACCOUNT_ID=$(awslocal sts get-caller-identity --query 'Account' --output text)
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

# 2. Create a Trust Policy requiring a unique External ID
cat <<EOF > cross-account-trust.json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"AWS": "arn:aws:iam::\${ACCOUNT_ID}:root"},
    "Action": "sts:AssumeRole",
    "Condition": {
      "StringEquals": {
        "sts:ExternalId": "SuperSecretVendorID-123"
      }
    }
  }]
}
EOF

# 3. Create the Cross-Account Role
awslocal iam create-role --role-name VendorCrossAccountRole --assume-role-policy-document file://cross-account-trust.json
aws iam create-role --role-name VendorCrossAccountRole --assume-role-policy-document file://cross-account-trust.json

# 4. Have the "Vendor" assume the role (Generates temporary AccessKey, SecretKey, and SessionToken)
awslocal sts assume-role \
  --role-arn arn:aws:iam::\${ACCOUNT_ID}:role/VendorCrossAccountRole \
  --role-session-name VendorAuditSession \
  --external-id "SuperSecretVendorID-123" \
  --duration-seconds 3600
aws sts assume-role \
  --role-arn arn:aws:iam::\${ACCOUNT_ID}:role/VendorCrossAccountRole \
  --role-session-name VendorAuditSession \
  --external-id "SuperSecretVendorID-123" \
  --duration-seconds 3600
```

## 🧠 Key Concepts & Importance

- **STS (Security Token Service):** A web service that enables you to request temporary, limited-privilege credentials for IAM users or for users that you authenticate (federated users).
- **AssumeRole:** An STS action that returns a set of temporary security credentials that you can use to access AWS resources that you might not normally have access to.
- **External ID:** A unique identifier that a third party must include when assuming a role. It is a security best practice to prevent the "Confused Deputy" problem in cross-account scenarios.
- **Confused Deputy Problem:** A security issue where an entity that doesn't have permission to perform a certain action can coerce a more-privileged entity to perform the action for them.
- **Temporary Credentials:** These consist of an Access Key ID, a Secret Access Key, and a Security Token. They expire after a specified duration (default is 1 hour).

## 🛠️ Command Reference

- `sts get-caller-identity`: Returns details about the IAM user or role whose credentials are used to call the operation.
    - `--query`: Filters the output to return specific fields (e.g., `Account`).
- `iam create-role`: Creates a new IAM role.
    - `--role-name`: The name of the role.
    - `--assume-role-policy-document`: The trust policy that allows an entity to assume the role.
- `sts assume-role`: Returns a set of temporary security credentials that you can use to access AWS resources.
    - `--role-arn`: The Amazon Resource Name (ARN) of the role to assume.
    - `--role-session-name`: An identifier for the assumed role session.
    - `--external-id`: A unique identifier that might be required by a role trust policy.
    - `--duration-seconds`: The duration, in seconds, of the role session.

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
