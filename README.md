# aws-serverless-image-moderator
An AI-powered image moderation workflow using AWS Lambda, S3, and Rekognition.
# AWS Serverless Image Moderator

A fully automated, event-driven image moderation pipeline built on AWS. This project automatically analyzes images upon upload to an S3 bucket and quarantines any content flagged as inappropriate by Amazon Rekognition AI.

---

## Architecture Diagram

This diagram shows how the AWS services are connected.

[User Uploads Image]
       |
       v
[S3 Upload Bucket] --(triggers)--> [AWS Lambda Function]
                                           |
                                           v
                                [Calls Amazon Rekognition AI]
                                           |
                                           v
                              [Receives Moderation Labels]
                                           |
                                           v
                                 [Decision: Is it clean?]
                                         /       \
                                (Yes)   /         \ (No)
                                     /             \
                                    v               v
                             [Do Nothing]      [Move Image to Quarantine S3 Bucket]
<img width="1024" height="1024" alt="unnamed" src="https://github.com/user-attachments/assets/7162b927-2cbe-46e6-9515-6e994a463441" />


                      
       
