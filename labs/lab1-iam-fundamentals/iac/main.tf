resource "aws_iam_user" "dev_user" {
  name = "DevUser"
}

resource "aws_iam_group" "developers" {
  name = "Developers"
}

resource "aws_iam_group_membership" "add_user" {
  name = "add-user-to-developers"
  users = [aws_iam_user.dev_user.name]
  group = aws_iam_group.developers.name
}

resource "aws_iam_group_policy_attachment" "s3_readonly" {
  group      = aws_iam_group.developers.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}
