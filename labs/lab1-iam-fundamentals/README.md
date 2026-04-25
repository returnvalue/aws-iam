# Lab 1: IAM Fundamentals (Users, Groups, & Identity Policies)

**Goal:** Create an IAM User, add them to a Group, and attach an identity-based AWS managed policy (AmazonS3ReadOnlyAccess).

```bash
# 1. Create a new IAM User
awslocal iam create-user --user-name DevUser
aws iam create-user --user-name DevUser

# 2. Create an IAM Group
awslocal iam create-group --group-name Developers
aws iam create-group --group-name Developers

# 3. Add the User to the Group
awslocal iam add-user-to-group --user-name DevUser --group-name Developers
aws iam add-user-to-group --user-name DevUser --group-name Developers

# 4. Attach a Managed Policy to the Group
awslocal iam attach-group-policy \
  --group-name Developers \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
aws iam attach-group-policy \
  --group-name Developers \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

## 🧠 Key Concepts & Importance

- **IAM User:** Represents a person or service that interacts with AWS.
- **IAM Group:** A collection of IAM users. Groups let you specify permissions for multiple users, which can make it easier to manage the permissions for those users.
- **Identity-Based Policies:** JSON permissions policy documents that you can attach to an identity, such as an IAM user, group, or role.
- **AWS Managed Policies:** Standalone policies that are created and managed by AWS.

## 🛠️ Command Reference

- `iam create-user`: Creates a new IAM user.
    - `--user-name`: The name of the user.
- `iam create-group`: Creates a new IAM group.
    - `--group-name`: The name of the group.
- `iam add-user-to-group`: Adds an IAM user to an IAM group.
    - `--user-name`: The name of the user.
    - `--group-name`: The name of the group.
- `iam attach-group-policy`: Attaches a managed policy to an IAM group.
    - `--group-name`: The name of the group.
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
