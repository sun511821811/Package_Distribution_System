import requests
import os
import time
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"  # Assuming default reset password

def test_scheduled_task_flow():
    # Create session with trust_env=False to ignore proxy
    session = requests.Session()
    session.trust_env = False

    # 1. Login
    print("Logging in...")
    login_data = {"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
    response = session.post(f"{BASE_URL}/admin/login", data=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    
    token = response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful")

    # 2. Get Packages (to pick one)
    print("Fetching packages...")
    response = session.get(f"{BASE_URL}/admin/packages", headers=headers)
    if response.status_code != 200:
        print(f"Failed to list packages: {response.text}")
        return
    
    packages = response.json()["data"]
    if not packages:
        print("No packages found. Uploading one...")
        # Create dummy file
        with open("test_task.apk", "wb") as f:
            f.write(b"dummy apk content")
        
        files = {"file": open("test_task.apk", "rb")}
        data = {"name": "TaskTestPackage", "version": "1.0.0", "description": "For task test"}
        response = session.post(f"{BASE_URL}/admin/packages/upload", headers=headers, files=files, data=data)
        if response.status_code != 200:
            print(f"Upload failed: {response.text}")
            return
        package_id = response.json()["data"]["id"]
        os.remove("test_task.apk")
    else:
        package_id = packages[0]["id"]
    
    print(f"Using Package ID: {package_id}")

    # 3. Create Scheduled Task
    print("Creating scheduled task...")
    task_data = {
        "package_id": str(package_id),
        "interval_seconds": 3600,
        "is_active": True
    }
    response = session.post(f"{BASE_URL}/admin/tasks/scheduled", headers=headers, json=task_data)
    if response.status_code != 201:
        print(f"Failed to create task: {response.text}")
        return
    
    task = response.json()["data"]
    task_id = task["id"]
    print(f"Task created with ID: {task_id}")
    
    # 4. List Tasks
    print("Listing tasks...")
    response = session.get(f"{BASE_URL}/admin/tasks/scheduled", headers=headers)
    tasks = response.json()["data"]
    print(f"Found {len(tasks)} tasks")
    found = False
    for t in tasks:
        if t["id"] == task_id:
            found = True
            print(f"Verified task: {t}")
            break
    if not found:
        print("Task not found in list!")
        return

    # 5. Run Task Manually
    print("Running task manually...")
    response = session.post(f"{BASE_URL}/admin/tasks/scheduled/{task_id}/run", headers=headers)
    if response.status_code != 200:
        print(f"Failed to run task: {response.text}")
    else:
        print("Task triggered successfully")

    # 6. Delete Task
    print("Deleting task...")
    response = session.delete(f"{BASE_URL}/admin/tasks/scheduled/{task_id}", headers=headers)
    if response.status_code != 200:
        print(f"Failed to delete task: {response.text}")
    else:
        print("Task deleted successfully")

if __name__ == "__main__":
    try:
        test_scheduled_task_flow()
    except Exception as e:
        print(f"Test failed with exception: {e}")
