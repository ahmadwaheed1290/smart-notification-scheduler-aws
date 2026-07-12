# Smart Notification Scheduler — AWS Lambda + DynamoDB + EventBridge

A serverless notification system that schedules and delivers automated emails at any future date and time — running entirely on AWS with zero idle cost.

## Live Demo
https://d2uko7csallknv.cloudfront.net/notify.html

## Tech Stack
- AWS Lambda
- Amazon DynamoDB
- Amazon EventBridge Scheduler
- Amazon SES
- API Gateway
- Python
- Amazon S3 + CloudFront

## How It Works
1. User sets a message, date, time and email
2. API Gateway receives the POST request
3. Lambda saves data to DynamoDB
4. EventBridge Scheduler creates an alarm for the exact time
5. At scheduled time, Lambda triggers and SES delivers the email
6. Schedule automatically deletes after completion

## Author
Ahmad Waheed — https://www.linkedin.com/in/ahmadwaheed2002/
