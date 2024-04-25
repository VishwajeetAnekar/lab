import boto3
import os

# Initialize the S3 client with credentials
s3 = boto3.client(
    's3',
    aws_access_key_id='your_access_key_id',
    aws_secret_access_key='your_secret_access_key'
)

bucket_name = 'my-unique-bucket-name'

def create_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except Exception as e:
        print(f"Error creating bucket {bucket_name}: {e}")

def upload_file(bucket_name, file_path, object_name):
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File {object_name} uploaded successfully to {bucket_name}.")
    except Exception as e:
        print(f"Error uploading file {file_path} to {bucket_name}: {e}")

def download_file(bucket_name, object_name, file_path):
    try:
        s3.download_file(bucket_name, object_name, file_path)
        print(f"File {object_name} downloaded successfully to {file_path}.")
    except Exception as e:
        print(f"Error downloading file {object_name} from {bucket_name}: {e}")

def list_objects(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"Object: {obj['Key']}, Size: {obj['Size']}")
        else:
            print(f"No objects found in bucket {bucket_name}.")
    except Exception as e:
        print(f"Error listing objects in bucket {bucket_name}: {e}")

def delete_object(bucket_name, object_name):
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        print(f"Object {object_name} deleted successfully from {bucket_name}.")
    except Exception as e:
        print(f"Error deleting object {object_name} from {bucket_name}: {e}")

def delete_bucket(bucket_name):
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting bucket {bucket_name}: {e}")

if __name__ == '__main__':
    create_bucket(bucket_name)

    file_path = 'sample.txt'
    object_name = os.path.basename(file_path)
    upload_file(bucket_name, file_path, object_name)

    list_objects(bucket_name)

    download_file(bucket_name, object_name, f"downloaded_{object_name}")

    delete_object(bucket_name, object_name)

    delete_bucket(bucket_name)
