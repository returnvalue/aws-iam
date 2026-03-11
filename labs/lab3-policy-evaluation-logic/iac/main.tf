resource "aws_iam_policy" "allow_all" {
  name        = "S3AllowAll"
  description = "Allow all S3 actions"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "s3:*"
      Effect = "Allow"
      Resource = "*"
    }]
  })
}

resource "aws_iam_policy" "explicit_deny" {
  name        = "S3ExplicitDeny"
  description = "Deny production bucket"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "s3:*"
      Effect = "Deny"
      Resource = ["arn:aws:s3:::production-data", "arn:aws:s3:::production-data/*"]
    }]
  })
}

resource "aws_iam_user" "data_scientist" {
  name = "DataScientist"
}

resource "aws_iam_user_policy_attachment" "attach_allow" {
  user       = aws_iam_user.data_scientist.name
  policy_arn = aws_iam_policy.allow_all.arn
}

resource "aws_iam_user_policy_attachment" "attach_deny" {
  user       = aws_iam_user.data_scientist.name
  policy_arn = aws_iam_policy.explicit_deny.arn
}
