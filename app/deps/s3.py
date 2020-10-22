import boto3
from botocore.exceptions import NoCredentialsError
from conf import config


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=config.ACCESS_KEY,
                      aws_secret_access_key=config.SECRET_KEY,
                      region_name=config.REGION)

    try:
        data = s3.upload_file(local_file, bucket, s3_file, ExtraArgs={
            'ContentType':'application/pdf'
        })
        print("uploaded on s3", data)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


# uploaded = upload_to_aws('local_file', 'elevateweb', 's3_file_name')
