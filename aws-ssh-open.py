import boto3
import logging

def lambda_handler(event, context):
    client = boto3.client('ec2')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    instance_id = event['detail']['instance-id']
    instance_dict = client.describe_instances(InstanceIds=[instance_id])
    sec_group_ids = [instance['GroupId'] for instance in instance_dict['Reservations'][0]['Instances'][0]['SecurityGroups']]

    for sec_id in sec_group_ids:
        sg = client.describe_security_groups(GroupIds=[sec_id])['SecurityGroups'][0]
        for ipPermission in sg['IpPermissions']:
            from_port = ipPermission['FromPort']
            to_port = ipPermission['ToPort']
            if (from_port <= 22 and to_port >= 22) and ('0.0.0.0/0' == ipPermission['IpRanges'][0]['CidrIp']):
                logger.info('Security Exception: SSH is open to the world.\n Terminating Instance.\n Event: {}'.format(event))
                client.stop_instances(InstanceIds=[instance_id])
                return
    return
