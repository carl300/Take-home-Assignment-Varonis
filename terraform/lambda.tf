data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/../api/app.py"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${local.name_prefix}-api"
  retention_in_days = var.log_retention_days
  # kms_key_id        = aws_kms_key.app.arn
  tags = local.common_tags
}

resource "aws_lambda_function" "api" {
  function_name    = "${local.name_prefix}-api"
  role             = aws_iam_role.lambda.arn
  handler          = "app.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  timeout          = 10
  memory_size      = 256

  environment {
    variables = {
      RESTAURANTS_TABLE  = aws_dynamodb_table.restaurants.name
      REQUEST_LOGS_TABLE = aws_dynamodb_table.request_logs.name
    }
  }

  tracing_config {
    mode = "Active"
  }

  depends_on = [aws_cloudwatch_log_group.lambda]
  tags       = local.common_tags
}
