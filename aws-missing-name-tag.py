import boto3
import logging

def lambda_handler(event, context):
    client = boto3.client('ec2')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    instance_id = event['detail']['instance-id']
    instance_tags = client.describe_tags(
        Filters=[
            {
                'Name': 'resource-id',
                'Values': [instance_id]
            }
        ]
    )
    
    for tag in instance_tags['Tags']:
        if tag['Key'] == 'Name':
            return
    
    logger.info('Security Exception: No name tag.\n Terminating Instance.\n Event: {}'.format(event))
    client.stop_instances(InstanceIds=[instance_id])
    return
    