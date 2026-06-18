# Restaurant Recommendation Service

This project was built as part of the Varonis DevOps take-home assignment.

The application provides a simple restaurant recommendation service that allows users to search for restaurants based on cuisine, vegetarian preferences, and delivery availability. The service also checks the current time and only recommends restaurants that are currently open.

## Architecture

The solution uses a serverless AWS architecture:

* API Gateway exposes the public API endpoint
* AWS Lambda contains the recommendation logic
* DynamoDB stores restaurant data and request logs
* CloudWatch provides application logging
* Terraform manages all infrastructure

## Features

* Search by cuisine type
* Filter by vegetarian options
* Filter by delivery availability
* Validate restaurant operating hours
* Return restaurant recommendations as JSON
* Log all requests for auditing and troubleshooting
* Simple web interface for testing the API

## Example API Request

GET

```text
/recommendation?style=Italian
```

Example response:

```json
{
  "restaurantRecommendation": {
    "id": "open-kitchen",
    "name": "Open Kitchen",
    "style": "Italian",
    "address": "100 Freedom Drive, Charlotte, NC",
    "openHour": "00:00",
    "closeHour": "23:59",
    "vegetarian": true,
    "delivery": true
  }
}
```

## Frontend

A lightweight frontend is included to demonstrate the API.

Users can:

* Select a cuisine
* Choose vegetarian options
* Choose delivery availability
* Receive a restaurant recommendation

The frontend communicates directly with the API Gateway endpoint.

## Infrastructure

All infrastructure is deployed using Terraform.

Resources created:

* API Gateway
* Lambda Function
* DynamoDB Restaurant Table
* DynamoDB Request Log Table
* IAM Roles and Policies
* CloudWatch Log Groups
* Secure S3 Bucket

## Security Considerations

* No secrets are stored in source code
* Request logs are stored separately from restaurant data
* DynamoDB encryption is enabled
* S3 public access is blocked
* IAM permissions follow least-privilege principles

## Running Locally

Frontend:

```bash
python -m http.server 8080
```

Open:

```text
http://localhost:8080
```

Terraform:

```bash
terraform init
terraform plan
terraform apply
```

## Future Improvements

If this project were expanded further, I would consider:

* Authentication and authorization
* Restaurant ratings and ranking logic
* Additional search criteria
* Frontend hosting through S3 and CloudFront
* Automated CI/CD deployment pipeline
