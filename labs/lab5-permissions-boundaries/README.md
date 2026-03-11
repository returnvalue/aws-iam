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

# 2. Apply the boundary to a user upon creation
awslocal iam create-user --user-name BoundaryUser --permissions-boundary $BOUNDARY_ARN

# 3. Grant the user Admin access (The boundary will throttle this to S3 ONLY)
awslocal iam attach-user-policy --user-name BoundaryUser --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
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
