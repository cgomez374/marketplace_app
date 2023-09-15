import boto3
from flask_login import current_user

# AWS CREDENTIALS
AWS_ACCESS_KEY = '#'
AWS_SECRET_KEY = '#'
S3_CLIENT = boto3.client("s3",
                         aws_access_key_id=AWS_ACCESS_KEY,
                         aws_secret_access_key=AWS_SECRET_KEY)


# UPLOAD TO S3 BUCKET
def upload_to_s3(file, update_object=False):
    bucket_name = "marketplace-product-images-bucket"
    object_key = f'{current_user.name}/{file.filename}'
    if not update_object:
        try:
            response = S3_CLIENT.head_object(Bucket=bucket_name, Key=object_key)
            # If the object exists, handle the scenario as needed (e.g., show an error message)
            return None
        except Exception as e:
            # Upload the file to S3
            S3_CLIENT.upload_fileobj(file, bucket_name, object_key)
    elif update_object:
        S3_CLIENT.upload_fileobj(file, bucket_name, object_key)
    # Construct the URL of the uploaded file
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
    return s3_url


def delete_object_s3(object_key):
    bucket_name = "marketplace-product-images-bucket"
    try:
        S3_CLIENT.delete_object(Bucket=bucket_name, Key=object_key)
        return True
    except Exception as e:
        return False