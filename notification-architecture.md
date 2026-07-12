# Architecture

## Request Flow

```
User sets message, date, time and email
       |
       v
CloudFront CDN (HTTPS)
       |
       v
API Gateway — POST /schedule
       |
       v
AWS Lambda (Python 3.12)
       |
       v
DynamoDB — saves notification data
       |
       v
EventBridge Scheduler — alarm set for exact time
       |
       v
[Waiting until scheduled time]
       |
       v
Lambda triggered automatically
       |
       v
Amazon SES — email delivered
       |
       v
Schedule deleted automatically
```

## AWS Services Used

| Service | Purpose |
|---------|---------|
| AWS Lambda | Serverless function to process requests |
| Amazon DynamoDB | NoSQL database to store notifications |
| EventBridge Scheduler | Time-based trigger for automation |
| Amazon SES | Email delivery service |
| API Gateway | REST API endpoint |
| Amazon S3 | Frontend hosting |
| CloudFront | Global CDN delivery |
| IAM | Permissions management |

## Cost

Near-zero monthly cost — Lambda runs only when triggered.
Free tier covers 14 million EventBridge invocations per month.
