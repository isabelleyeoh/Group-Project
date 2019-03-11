# Connect to AWS S3

import boto3, botocore
from app import app

# Authentication process
s3 = boto3.client(
"s3",
# We us app.config to make it dynamic - we can change config to go from dev to production environment, and this will amend the S3_KEY accordingly
aws_access_key_id=app.config['S3_KEY'],
aws_secret_access_key=app.config['S3_SECRET']
)

# Function to upload file to s3





def upload_file_to_s3(file, key, bucket_name, content_type):
    
    try:

        s3.put_object(ACL='public-read',Body=file.getvalue(),Key=key,Bucket=bucket_name, ContentType= content_type)

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return f'{app.config["S3_LOCATION"]}{key}'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


