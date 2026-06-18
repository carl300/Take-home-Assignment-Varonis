output "api_endpoint" {
  description = "Public HTTP API endpoint."
  value       = aws_apigatewayv2_api.http.api_endpoint
}

output "recommendation_url_example" {
  description = "Example recommendation request."
  value       = "${aws_apigatewayv2_api.http.api_endpoint}/recommendation?style=Italian&vegetarian=true&delivery=true"
}

output "restaurants_table" {
  value = aws_dynamodb_table.restaurants.name
}

output "request_logs_table" {
  value = aws_dynamodb_table.request_logs.name
}

output "secure_logs_bucket" {
  value = aws_s3_bucket.secure_logs.bucket
}
