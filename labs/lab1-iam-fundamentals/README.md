# Lab 1: IAM Fundamentals (Users, Groups, & Identity Policies)

**Goal:** Create an IAM User, add them to a Group, and attach an identity-based AWS managed policy (AmazonS3ReadOnlyAccess).

```bash
# 1. Create a new IAM User
awslocal iam create-user --user-name DevUser

# 2. Create an IAM Group
awslocal iam create-group --group-name Developers

# 3. Add the User to the Group
awslocal iam add-user-to-group --user-name DevUser --group-name Developers

# 4. Attach a Managed Policy to the Group
awslocal iam attach-group-policy \
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
