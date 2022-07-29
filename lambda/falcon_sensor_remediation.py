import boto3


def event_parser(event):
    compliance_state = event ['detail']['findings'][0]['Compliance']['Status']
    event_action = event ['detail']['actionName']
    if (event_action == "Install Falcon") and (compliance_state=="FAILED"):
        instance_id = event['detail']['findings'][0]['Resources'][0]['Id']
        print ("The instance that has", compliance_state, "compliance is", instance_id)
    return instance_id


def lambda_handler(event, context):
    instance_id = event_parser(event)
    ssm_client = boto3.client('ssm')
    response = ssm_client.send_command(
        InstanceIds = [instance_id],
        DocumentName = "AWS-ConfigureAWSPackage",
        Parameters = {"action":["Install"],"name":["FalconSensor"]}
            )
    command_id = response['Command']['CommandId']
    print (command_id)
