data "aws_iam_policy_document" "policy" {
  statement {
    sid       = "Statement1"
    effect    = "Allow"
    resources = ["*"]
    actions   = ["lambda:ListFunctions"]
  }

  statement {
    sid       = "Statement2"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "s3:CreateBucket",
      "s3:DeleteBucket",
    ]
  }
}
