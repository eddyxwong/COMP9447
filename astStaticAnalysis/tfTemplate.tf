data "aws_iam_policy_document" "policy" {
  statement {
    sid       = "Statement1"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "s3:ListAllMyBuckets",
      "s3:CreateBucket",
      "s3:DeleteBucket",
    ]
  }

  statement {
    sid       = "Statement2"
    effect    = "Allow"
    resources = ["arn:aws:lambda:us-east-1:221094580673:function:testFunction"]
    actions   = ["lambda:GetFunction"]
  }

  statement {
    sid       = "Statement3"
    effect    = "Allow"
    resources = ["*"]
    actions   = ["lambda:ListFunctions"]
  }
}
