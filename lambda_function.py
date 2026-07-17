import json
import boto3
import os

sns = boto3.client("sns")
TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
THRESHOLD = 30  # water the plant below this %

def lambda_handler(event, context):
    moisture = event.get("moisture_pct")
    device = event.get("device_id", "your plant")

    if moisture is not None and moisture < THRESHOLD:
        message = f"{device} needs water! Soil moisture is {moisture}%, below the {THRESHOLD}% threshold."
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Plant watering reminder",
            Message=message
        )
        return {"statusCode": 200, "body": json.dumps(f"Alert sent: {message}")}

    return {"statusCode": 200, "body": json.dumps(f"Moisture OK ({moisture}%), no alert needed.")}