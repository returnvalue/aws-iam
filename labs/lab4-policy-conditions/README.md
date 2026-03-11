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
```

## 🧠 Key Concepts & Importance

- **Policy Conditions:** The `Condition` element (or `Condition` block) lets you specify conditions for when a policy is in effect.
- **ABAC (Attribute-Based Access Control):** An authorization strategy that defines permissions based on attributes, such as tags or properties of the resource or request.
- **Granular Control:** Conditions allow you to go beyond simple service-level permissions and enforce specific business rules (e.g., "only allow small instances" or "only allow access from a specific IP").
- **Condition Keys:** Service-specific keys (like `ec2:InstanceType`) and global keys (like `aws:SourceIp`) provide the data used for evaluation.

## 🛠️ Command Reference

- `awslocal iam create-policy`: Creates a new managed policy.
    - `--policy-name`: The name of the policy.
    - `--policy-document`: The JSON policy document containing conditions.
