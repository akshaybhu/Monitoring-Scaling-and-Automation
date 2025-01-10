import boto3
import json

# Initialize the boto3 client for SNS and Lambda
sns_client = boto3.client('sns')
lambda_client = boto3.client('lambda')

# Define the SNS topics for different alerts
sns_topics = {
    "aks-Alert",
    "aks-Traffic-Alert"
}

# Lambda function for processing notifications (example Lambda ARN)
lambda_function_arn = 'arn:aws:lambda:us-east-1:975050024946:function:aks_boto3'

# Function to invoke Lambda for processing notifications
def invoke_lambda(topic_name, message):
    payload = {
        'topic': topic_name,
        'message': message
    }
    response = lambda_client.invoke(
        FunctionName=lambda_function_arn,
        InvocationType='Event',  # Asynchronous invocation
        Payload=json.dumps(payload)
    )
    print(f"Lambda invocation response for {topic_name}: {response}")

#Simulating event that triggers a notification
def trigger_alert(topic_name, topic_arn, message):
    sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=f"Alert: {topic_name.capitalize()} Notification"
    )
    print(f"Alert triggered for {topic_name}: {message}")
    invoke_lambda(topic_name, message)

#triggering an alert (traffic)
trigger_alert('aks-Traffic-Alert', 'arn:aws:sns:us-east-1:975050024946:aks_boto3', 'Website traffic has exceeded the threshold.')

#triggering an alert (health issue)
trigger_alert('aks-Alert', 'arn:aws:sns:us-east-1:975050024946:aks_boto3', 'A server in the ASG is unhealthy.')