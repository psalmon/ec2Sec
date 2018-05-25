import boto3
import logging

def lambda_handler(event, context):
    client = boto3.client('ec2')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    instance_id = event['detail']['instance-id']
    instance_dict = client.describe_instances(Filters =
        [
            {
                'Name': 'instance.group-name',
                'Values': ['default']
            }
        ],
        InstanceIds=[instance_id])
    
    if len(instance_dict) > 0:
        logger.info('Security Exception: Instance has default security group.\n Terminating Instance.\n Event: {}'.format(event))
        client.stop_instances(InstanceIds=[instance_id])
        return
    