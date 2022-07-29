import os

import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

SECURITYHUB = boto3.client('securityhub')
CONFIG = boto3.client('config')
BUCKET_NAME = os.environ['S3Bucket']
FILE_NAME = os.environ['S3FileName']
LOCAL_FILE_NAME = '/tmp/test.txt'
# call s3 bucket
securityhub_client = boto3.client('securityhub')
config_client = boto3.client('config')
s3_client =  boto3.client('s3')
s3_resource = boto3.resource('s3')
s3 = boto3.resource('s3', region_name =  'eu-west-1')
bucket = s3.Bucket(BUCKET_NAME)  # Enter your bucket name, e.g 'Data'
# key path, e.g.'customer_profile/Reddit_Historical_Data.csv'
s3

# lambda function
def bucket_handler(event, context):
    details = event['detail']
    if 'oldEvaluationResult' not in event['detail']:
        old_recorded_time = (details['newEvaluationResult']['resultRecordedTime'])
    else:
        old_recorded_time = (details['oldEvaluationResult']['resultRecordedTime'])
    # download s3 csv file to lambda tmp folder
    try:
        # Check if remote exists
        result = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=FILE_NAME)
        if 'Contents' in result:
            s3.Bucket(BUCKET_NAME).download_file(FILE_NAME, LOCAL_FILE_NAME)
        else:
            print("Key doesn't exist in the bucket. Creating file")




    # write the data into '/tmp' folder
        with open(LOCAL_FILE_NAME, 'a+') as file_object:
            outstr = f"{old_recorded_time},{details['resourceId']},{details['awsAccountId']},{details['awsRegion']}\n"
            file_object.write(outstr)
    except Exception as error:
        logger.info("Got error {} writing to file".format(error))

    # upload file from tmp to s3 key
    bucket.upload_file(LOCAL_FILE_NAME, FILE_NAME)

    if os.path.exists(LOCAL_FILE_NAME):
        os.remove(LOCAL_FILE_NAME)
    else:
        print("The file does not exist")
    return {
        'message': 'success!!'
    }
def lambda_handler(event, context):
    """Begin Lambda execution."""
    if (event['detail']['messageType'] == 'ComplianceChangeNotification' and
            event['detail']['configRuleName'] == "ec2-managedinstance-applications-required"):
        logger.info("Got event of interest")
        bucket_handler(event, context)
    else:
        logger.info("Nothing to do")