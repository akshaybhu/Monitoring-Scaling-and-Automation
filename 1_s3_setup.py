import boto3

def create_s3_bucket(bucket_name, region='us-east-1'):
    """
    Creates an S3 bucket and configures it for static website hosting
    """
    s3_client = boto3.client('s3', region_name=region)
    
    # Create bucket with appropriate region configuration
    if region == 'us-east-1':
        s3_client.create_bucket(Bucket=bucket_name)

    # Upload static files to S3
    s3_client.upload_file('students.html', bucket_name, 'index.html')

create_s3_bucket('akshay-s3-webstorage')