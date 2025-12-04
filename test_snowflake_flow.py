import requests
import os
from app.core.config import settings
from app.core.snowflake import snowflake
import boto3
import time

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
ADMIN_USERNAME = settings.ADMIN_USERNAME
ADMIN_PASSWORD = "admin123"  # Reset to this
API_KEY = settings.API_KEY
TEST_FILE = "/Users/minglongsun/Downloads/app.apk"

def test_full_flow():
    # 1. Login
    print("Logging in...")
    session = requests.Session()
    # Bypass proxy for local
    session.trust_env = False
    
    login_data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    resp = session.post(f"{BASE_URL}/admin/login", data=login_data)
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    
    token = resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful")

    # 2. Upload Package
    print(f"Uploading package {TEST_FILE}...")
    if not os.path.exists(TEST_FILE):
        print(f"Test file not found: {TEST_FILE}")
        return

    with open(TEST_FILE, "rb") as f:
        files = {"file": ("app.apk", f, "application/vnd.android.package-archive")}
        data = {
            "name": f"test_snowflake_{int(time.time())}",
            "version": "1.0.0",
            "description": "Test snowflake ID"
        }
        upload_resp = session.post(
            f"{BASE_URL}/admin/packages/upload", 
            headers=headers, 
            files=files, 
            data=data
        )

    if upload_resp.status_code != 200:
        print(f"Upload failed: {upload_resp.text}")
        return

    package_data = upload_resp.json()["data"]
    package_id = package_data["id"]
    print(f"Upload successful. Package ID: {package_id}")
    
    # Verify Snowflake ID format (should be large int as string)
    if not isinstance(package_id, str) or len(package_id) < 10:
        print(f"WARNING: Package ID {package_id} does not look like a Snowflake ID")
    else:
        print("Package ID format looks correct (Snowflake)")

    # 3. Verify Original File in R2
    print("Verifying original file in R2...")
    s3 = boto3.client(
        "s3",
        endpoint_url=settings.R2_ENDPOINT_URL,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name=settings.R2_REGION,
    )
    
    original_key = f"{package_id}/original/app.apk"
    try:
        s3.head_object(Bucket=settings.R2_BUCKET_NAME, Key=original_key)
        print(f"Original file found in R2 at {original_key}")
    except Exception as e:
        print(f"Original file NOT found in R2 at {original_key}: {e}")
        return

    # 4. Poll for Processing Completion
    print("Waiting for processing...")
    processed = False
    client_session = requests.Session()
    client_session.trust_env = False
    
    for i in range(30):
        # Use client query API to check status
        headers_client = {"x-api-key": API_KEY}
        # Bypass proxy
        try:
            query_resp = client_session.get(
                f"{BASE_URL}/package/query",
                params={"package_id": package_id},
                headers=headers_client
            )
            
            if query_resp.status_code == 200:
                data = query_resp.json()["data"]
                status = data["status"]
                if status == "processed_success":
                    processed = True
                    print(f"Status: {status}")
                    print(f"Processing complete. Download URL: {data['download_url']}")
                    break
                elif status == "processed_failed":
                    print("Processing failed")
                    break
                else:
                    # Still processing or pending
                    if i % 5 == 0:
                        print(f"Status: {status}...")
            elif query_resp.status_code == 403:
                # Might be 403 if distributing is not enabled yet (processing)
                # or strictly if not distributing.
                # Our API returns 403 if is_distributing is False.
                # So this means still processing.
                if i % 5 == 0:
                    print(f"Client query returned 403, likely still processing...")
            else:
                print(f"Query failed: {query_resp.status_code} {query_resp.text}")
        except Exception as e:
            print(f"Request error: {e}")
            
        time.sleep(2)
    
    if processed:
        # 5. Verify Processed File in R2
        print("Verifying processed file in R2...")
        # Assuming filename is processed_app.apk based on logic
        processed_key = f"{package_id}/processed/processed_app.apk"
        try:
            s3.head_object(Bucket=settings.R2_BUCKET_NAME, Key=processed_key)
            print(f"Processed file found in R2 at {processed_key}")
        except Exception as e:
            print(f"Processed file NOT found in R2 at {processed_key}: {e}")

if __name__ == "__main__":
    test_full_flow()
