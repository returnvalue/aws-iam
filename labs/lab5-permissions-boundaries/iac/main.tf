resource "aws_iam_policy" "boundary" {
  name = "S3OnlyBoundary"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "s3:*"
      Effect = "Allow"
      Resource = "*"
    }]
  })
}

resource "aws_iam_user" "boundary_user" {
  name                 = "BoundaryUser"
  permissions_boundary = aws_iam_policy.boundary.arn
}

resource "aws_iam_user_policy_attachment" "grant_admin" {
  user       = aws_iam_user.boundary_user.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}
