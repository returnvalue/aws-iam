# Lab 5: Privilege Escalation Mitigation (Permissions Boundaries)

**Goal:** A permissions boundary sets the maximum permissions an entity can have. Even if a user is granted AdministratorAccess, the boundary will block them if it only allows S3 access.
```bash
# 1. Create a Permissions Boundary Policy (Max permissions: S3 only)
cat <<EOF > boundary-policy.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]
}
EOF
BOUNDARY_ARN=$(awslocal iam create-policy --policy-name S3OnlyBoundary --policy-document file://boundary-policy.json --query 'Policy.Arn' --output text)
BOUNDARY_ARN=$(aws iam create-policy --policy-name S3OnlyBoundary --policy-document file://boundary-policy.json --query 'Policy.Arn' --output text)

# 2. Apply the boundary to a user upon creation
awslocal iam create-user --user-name BoundaryUser --permissions-boundary $BOUNDARY_ARN
aws iam create-user --user-name BoundaryUser --permissions-boundary $BOUNDARY_ARN

# 3. Grant the user Admin access (The boundary will throttle this to S3 ONLY)
awslocal iam attach-user-policy --user-name BoundaryUser --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
aws iam attach-user-policy --user-name BoundaryUser --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

## 🧠 Key Concepts & Importance

- **Permissions Boundary:** A managed policy that sets the absolute maximum permissions an IAM entity (user or role) can have. It does not grant permissions on its own.
- **Effective Permissions:** The permissions that an entity actually has, which is the intersection of its identity-based policies and its permissions boundary.
- **Privilege Escalation Mitigation:** Boundaries are used to prevent users from gaining more permissions than they should, even if they have the ability to create new policies or roles.
- **Delegated Administration:** Commonly used when allowing developers to create roles for services (like Lambda) while ensuring those roles cannot exceed a predefined security "sandbox".

## 🛠️ Command Reference

- `iam create-policy`: Creates a new managed policy.
    - `--policy-name`: The name of the policy.
    - `--policy-document`: The JSON policy document.
- `iam create-user`: Creates a new IAM user.
    - `--user-name`: The name of the user.
    - `--permissions-boundary`: The ARN of the policy to use as a permissions boundary.
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
