# AWS Identity and Access Management (IAM) Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-IAM_Security-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating advanced AWS Identity and Access Management (IAM) security concepts. Using [LocalStack Pro](https://localstack.cloud/), we simulate a localized AWS cloud environment to practice identity federation, policy evaluation logic, conditional access, and cross-account role assumption without risking real-world cloud environments.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS security best practices (SAA-C03), these labs demonstrate:
* **IAM Fundamentals:** Creating Users, Groups, and attaching Identity-Based Managed Policies.
* **Service Roles & Trust Policies:** Instead of embedding access keys, we use IAM Roles (Trust Policies + Permissions Policies) to securely grant compute services (like Lambda or EC2) access to other AWS resources.
* **Policy Evaluation Logic:** Proving that an `Explicit Deny` always overrides an `Allow`.
* **Policy Conditions:** Restricting the exact types of EC2 instances a user can provision using the `Condition` block (e.g., `ec2:InstanceType`).
* **Permissions Boundaries:** Defining the absolute maximum permissions an IAM entity can have, mitigating the risk of privilege escalation.
* **Cross-Account Access & STS:** Generating temporary security credentials using `AssumeRole` while preventing the "Confused Deputy" problem via the `ExternalId` condition.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/awslabs/iam.git
   cd iam
   
```

2. Configure your LocalStack Auth Token:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   
```

3. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   
```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative, end-to-end scenario rather than isolated tasks. You are building one evolving architecture as you progress.
>
> **Session Persistence:** You must run all commands sequentially within the **same terminal session**. The labs rely on bash variables (like `$USER_NAME`, `$ROLE_ARN`, etc.) created in earlier steps. If you close your terminal, these variables will be lost and subsequent labs will fail.

## 📚 Labs Index
1. [Lab 1: IAM Fundamentals (Users, Groups, & Policies)](./labs/lab1-iam-fundamentals/README.md)
2. [Lab 2: Service Roles & Trust Policies](./labs/lab2-service-roles-trust-policies/README.md)
3. [Lab 3: Policy Evaluation Logic (Explicit Deny)](./labs/lab3-policy-evaluation-logic/README.md)
4. [Lab 4: Policy Conditions (Attribute-Based Access Control)](./labs/lab4-policy-conditions/README.md)
5. [Lab 5: Permissions Boundaries](./labs/lab5-permissions-boundaries/README.md)
6. [Lab 6: Cross-Account Access & STS AssumeRole](./labs/lab6-cross-account-sts/README.md)

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
