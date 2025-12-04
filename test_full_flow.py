import requests
import time
import os

BASE_URL = "http://localhost:8000/api/v1"
ADMIN_USERNAME = "admin"
# Assuming the password was reset or is the one from .env.
# If login fails, I might need to check init_admin.py or reset it again.
# From .env: ADMIN_PASSWORD=your_admin_password
# But in previous session user might have reset it.
# I'll try "admin123" as a common reset, or the one from .env.
# Let's try "admin123" first as that's what I saw in previous turn summaries often.
# Wait, the .env says "your_admin_password".
ADMIN_PASSWORD = "your_admin_password"

FILE_PATH = "/Users/minglongsun/Downloads/app.apk"


def test_flow():
    session = requests.Session()
    session.trust_env = False  # Bypass proxy

    # 1. Login
    print("Logging in...")
    try:
        login_resp = session.post(
            f"{BASE_URL}/admin/login",
            data={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
        )
        if login_resp.status_code != 200:
            print(f"Login failed: {login_resp.text}")
            # Try with admin123 just in case
            print("Retrying with password 'admin123'...")
            login_resp = session.post(
                f"{BASE_URL}/admin/login",
                data={"username": ADMIN_USERNAME, "password": "admin123"},
            )
            if login_resp.status_code != 200:
                print(f"Login failed again: {login_resp.text}")
                return

        token = login_resp.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful.")
    except Exception as e:
        print(f"Login error: {e}")
        return

    # 2. Upload APK
    print(f"Uploading {FILE_PATH}...")
    if not os.path.exists(FILE_PATH):
        print(f"File not found: {FILE_PATH}")
        return

    with open(FILE_PATH, "rb") as f:
        files = {"file": ("app.apk", f, "application/vnd.android.package-archive")}
        data = {
            "name": "test_package_auto_r2",
            "version": "1.0.0",
            "description": "Test package for auto R2 upload",
        }
        upload_resp = session.post(
            f"{BASE_URL}/admin/packages/upload", headers=headers, files=files, data=data
        )

        if upload_resp.status_code != 200:
            print(f"Upload failed: {upload_resp.text}")
            return

        package_data = upload_resp.json()["data"]
        package_id = package_data["id"]
        print(f"Upload successful. Package ID: {package_id}")

    # 3. Poll status
    print("Polling status...")
    max_retries = 30
    for i in range(max_retries):
        # There is no direct GET /admin/packages/{id} in the code snippet I saw earlier.
        # But usually there is one. If not, I might need to check the code or use list and filter.
        # Let's try to find if there is a get package endpoint in admin.
        # The previous `Read` of admin.py didn't show it in the first 200 lines.
        # I will check client API /api/v1/package/query with API_KEY if admin API is missing.
        # But admin should have access.
        # Let's check if there is a GET /packages/{id} in admin.py.
        # Actually, I can just query the client API with API_KEY.

        # Using client API for polling status
        api_key = "your_api_key"  # from .env
        # api key in header
        headers_client = {"x-api-key": api_key}
        query_resp = session.get(
            f"{BASE_URL}/package/query",
            params={"package_name": "test_package_auto_r2"},
            headers=headers_client,
        )

        if query_resp.status_code == 200:
            data = query_resp.json()["data"]
            # client API returns latest package.
            # Check if it matches our version/id
            # Schema uses 'version' not 'current_version'
            if data.get("version") == "1.0.0":
                # Check status if exposed, but client API might not expose status directly if not ready?
                # The client API usually returns valid packages.
                # If it returns, it means it is distributing.
                # But we want to see the download URL.
                print(
                    f"Package found in client query! Download URL: {data.get('download_url')}"
                )
                if "dl.yourdomain.com" in data.get("download_url", ""):
                    print("Success! Download URL points to CDN.")
                    break
                else:
                    print(
                        f"Download URL is {data.get('download_url')}, waiting for R2 update..."
                    )
        else:
            print(f"Query status: {query_resp.status_code} - {query_resp.text}")

        time.sleep(2)
    else:
        print("Timeout waiting for processing.")


if __name__ == "__main__":
    test_flow()
