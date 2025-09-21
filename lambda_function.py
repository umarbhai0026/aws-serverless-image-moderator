import json
import os
import boto3

# Initialize the AWS clients
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

# Get the name of the bucket for flagged images from the environment variable
FLAGGED_BUCKET_NAME = os.environ.get('FLAGGED_BUCKET_NAME')

def lambda_handler(event, context):
    """
    This function is triggered by an S3 upload. It uses Amazon Rekognition
    to detect moderation labels in the uploaded image. If unsafe content
    is found, it moves the image to a separate 'flagged' S3 bucket.
    """
    
    # 1. Get the bucket and file name from the S3 event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    print(f"Processing image: {object_key} from bucket: {source_bucket}")

    try:
        # 2. Call Amazon Rekognition to detect unsafe content
        # MinConfidence can be adjusted. 70 means we're 70% sure or more.
        response = rekognition.detect_moderation_labels(
            Image={
                'S3Object': {
                    'Bucket': source_bucket,
                    'Name': object_key
                }
            },
            MinConfidence=70 
        )

        moderation_labels = response['ModerationLabels']

        # 3. Check if any moderation labels were returned
        if moderation_labels:
            print(f"!! MODERATION LABELS DETECTED for '{object_key}' !!")
            for label in moderation_labels:
                print(f"  - Label: {label['Name']}, Confidence: {label['Confidence']:.2f}%")

            # 4. If labels are found, move the image to the flagged bucket
            if FLAGGED_BUCKET_NAME:
                print(f"Moving '{object_key}' to quarantine bucket: '{FLAGGED_BUCKET_NAME}'")
                s3.copy_object(
                    CopySource={'Bucket': source_bucket, 'Key': object_key},
                    Bucket=FLAGGED_BUCKET_NAME,
                    Key=object_key
                )
                s3.delete_object(Bucket=source_bucket, Key=object_key)
                print("Move complete.")
            
        else:
            print(f"Image '{object_key}' is clean. No action taken.")

    except Exception as e:
        print(f"Error processing image '{object_key}': {str(e)}")
        # You might want to add error handling here, like moving the file to an 'error' bucket

    return {
        'statusCode': 200,
        'body': json.dumps('Image processing complete.')
    }