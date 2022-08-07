data "aws_iam_policy_document" "policy" {
  statement {
    sid       = "Statement1"
    effect    = "Allow"
    resources = ["*"]
    actions   = ["s3:ListAllMyBuckets"]
  }

  statement {
    sid       = "Statement2"
    effect    = "Allow"
    resources = ["arn:aws:lambda:us-east-1:221094580673:function:testFunction"]
    actions   = ["lambda:GetFunction"]
  }
}
