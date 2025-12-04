import boto3
from app.core.config import settings


class StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name=settings.R2_REGION,
        )
        self.bucket = settings.R2_BUCKET_NAME

    def upload_file(self, file_path, object_name):
        """
        Upload a file to R2
        :param file_path: Local file path
        :param object_name: Object name in R2 bucket
        :return: Public URL of the uploaded file
        """
        try:
            # Use put_object for better compatibility with R2 in some cases,
            # or ensure we don't have issues with seeking.
            # upload_file is generally preferred but let's try put_object if upload_file fails with rewinding.
            # Actually, let's try to just open and put.
            with open(file_path, "rb") as f:
                self.s3.put_object(Bucket=self.bucket, Key=object_name, Body=f)
            return self.get_public_url(object_name)
        except Exception as e:
            print(f"Failed to upload file to R2: {e}")
            raise e

    def get_public_url(self, object_name):
        """
        Get public URL for an object
        :param object_name: Object name
        :return: Public URL
        """
        # If CDN_DOMAIN is configured, use it
        if hasattr(settings, "CDN_DOMAIN") and settings.CDN_DOMAIN:
            return f"https://{settings.CDN_DOMAIN}/{object_name}"
        # Fallback or other logic if needed
        return f"{settings.R2_ENDPOINT_URL}/{self.bucket}/{object_name}"

    def download_file(self, object_name, dest_path):
        """
        Download a file from R2
        :param object_name: Object name in R2 bucket
        :param dest_path: Local destination path
        """
        try:
            # Ensure directory exists
            import os

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            self.s3.download_file(self.bucket, object_name, dest_path)
        except Exception as e:
            print(f"Failed to download file from R2: {e}")
            raise e

    def delete_folder(self, folder_prefix: str):
        """
        Delete all objects with the given prefix (simulating folder deletion)
        :param folder_prefix: Folder prefix (e.g., "12345/")
        """
        try:
            # List all objects with the prefix
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket, Prefix=folder_prefix)

            delete_us = []
            for page in pages:
                if "Contents" in page:
                    for obj in page["Contents"]:
                        delete_us.append({"Key": obj["Key"]})
                        # S3 delete_objects allows max 1000 keys
                        if len(delete_us) >= 1000:
                            self.s3.delete_objects(
                                Bucket=self.bucket, Delete={"Objects": delete_us}
                            )
                            delete_us = []

            if delete_us:
                self.s3.delete_objects(
                    Bucket=self.bucket, Delete={"Objects": delete_us}
                )
        except Exception as e:
            print(f"Failed to delete folder from R2: {e}")
            # We log but might not want to crash if cleanup fails
            pass


storage_service = StorageService()
