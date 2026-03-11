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

# 3. Attach both policies to a new user
awslocal iam create-user --user-name DataScientist
awslocal iam attach-user-policy --user-name DataScientist --policy-arn $ALLOW_POLICY_ARN
awslocal iam attach-user-policy --user-name DataScientist --policy-arn $DENY_POLICY_ARN
```

## 🧠 Key Concepts & Importance

- **Implicit Deny:** By default, all requests are denied.
- **Explicit Allow:** A policy that allows a specific action on a specific resource.
- **Explicit Deny:** A policy that explicitly denies a specific action on a specific resource. This always overrides any Allow.
- **Policy Evaluation Order:** AWS evaluates all policies that apply to the request. If an explicit deny is found in any of those policies, the request is denied.
