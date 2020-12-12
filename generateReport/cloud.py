import boto3
from personal_config import aws_config, aws_bucket

def upload_to_S3(file_name,extention):
    print("Cloud1")
    s3 = boto3.client('s3', **aws_config)
    bucket=aws_bucket["bucket_name"]
    print("Cloud2")
    try: 
        print("Cloud3")
        res = s3.upload_file(
            "{file}.{extention}".format(file=file_name,extention=extention), 
            bucket,  
            "{file}.{extention}".format(file=file_name,extention=extention), 
            ExtraArgs={'ACL': 'public-read'}
        )
        return {
                "success":True,
                "message":"https://{bucket}.s3.amazonaws.com/{file_name}.{extention}".format(
                    bucket=bucket,
                    file_name=file_name,
                    extention=extention
                )
        }
    except Exception as e:
        print("Cloud4")
        return {
                "success": False,
                "message": "Error while uploading to aws.\n{error}".format(error=str(e))
        }
    print("Cloud5")


