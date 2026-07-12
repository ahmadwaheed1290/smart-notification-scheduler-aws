import json
import boto3
import uuid
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = dynamodb.Table('notifications')
scheduler = boto3.client('scheduler', region_name='ap-southeast-1')

ROLE_ARN = 'arn:aws:iam::781863586083:role/scheduler-lambda-role'
SES_LAMBDA_ARN = 'arn:aws:lambda:ap-southeast-1:781863586083:function:contact-form-handler'

def lambda_handler(event, context):

    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }

    body = json.loads(event['body'])
    message = body.get('message')
    email = body.get('email')
    date = body.get('date')
    time = body.get('time')

    notification_id = str(uuid.uuid4())

    table.put_item(
        Item={
            'id': notification_id,
            'message': message,
            'email': email,
            'date': date,
            'time': time,
            'created_at': datetime.now().isoformat()
        }
    )

    year, month, day = map(int, date.split('-'))
    hour, minute = map(int, time.split(':'))

    local_dt = datetime(year, month, day, hour, minute)
    utc_dt = local_dt - timedelta(hours=5)

    schedule_expression = f"at({utc_dt.strftime('%Y-%m-%dT%H:%M:%S')})"

    payload = {
        'name': email,
        'email': email,
        'message': message
    }

    try:
        scheduler.create_schedule(
            Name=f"notify-{notification_id}",
            ScheduleExpression=schedule_expression,
            Target={
                'Arn': SES_LAMBDA_ARN,
                'RoleArn': ROLE_ARN,
                'Input': json.dumps({'body': json.dumps(payload)})
            },
            FlexibleTimeWindow={'Mode': 'OFF'},
            ActionAfterCompletion='DELETE'
        )
    except Exception as e:
        print(f"Scheduler error: {str(e)}")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps({'message': 'Notification scheduled successfully', 'id': notification_id})
    }
