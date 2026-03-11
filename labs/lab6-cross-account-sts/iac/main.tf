resource "aws_iam_role" "vendor_role" {
  name = "VendorCrossAccountRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { AWS = "arn:aws:iam::${var.account_id}:root" }
      Condition = {
        StringEquals = { "sts:ExternalId" = "SuperSecretVendorID-123" }
      }
    }]
  })
}
