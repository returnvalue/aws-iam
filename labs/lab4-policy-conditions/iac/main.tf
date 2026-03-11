resource "aws_iam_policy" "restrict_ec2" {
  name = "RestrictEC2InstanceType"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "ec2:RunInstances"
      Effect = "Allow"
      Resource = "arn:aws:ec2:*:*:instance/*"
      Condition = {
        StringEquals = { "ec2:InstanceType" = ["t3.micro", "t3.small"] }
      }
    }]
  })
}
