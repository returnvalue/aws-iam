# Lab 6: Temporary Access via STS (Confused Deputy Prevention)

**Goal:** Grant a third-party vendor temporary access to your account using `sts:AssumeRole`. Implement an `ExternalId` condition to protect against the "Confused Deputy" vulnerability.

```bash
# 1. Dynamically get your LocalStack Account ID
ACCOUNT_ID=$(awslocal sts get-caller-identity --query 'Account' --output text)

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

# 4. Have the "Vendor" assume the role (Generates temporary AccessKey, SecretKey, and SessionToken)
awslocal sts assume-role \
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
