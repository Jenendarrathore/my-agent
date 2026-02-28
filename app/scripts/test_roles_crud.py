import asyncio
import httpx
import sys

# Using the base API URL to allow access to both /v1 and /auth
BASE_URL = "http://localhost:8000/api"

async def test_roles_crud():
    print("🚀 Starting Role CRUD Verification...")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Try to Register a test user (in case DB was cleaned)
        print("--- Registering Test User ---")
        reg_res = await client.post("/auth/register", json={
            "username": "testuser_role",
            "primary_email": "test_role@example.com",
            "password": "Password123!"
        })
        
        if reg_res.status_code == 200:
            print("✅ Registration successful.")
            token = reg_res.json()["access_token"]
        else:
            print(f"⚠️ Registration status: {reg_res.status_code}. Trying to login instead...")
            login_res = await client.post("/auth/login", data={
                "username": "testuser_role",
                "password": "Password123!"
            })
            if login_res.status_code == 200:
                print("✅ Login successful.")
                token = login_res.json()["access_token"]
            else:
                print(f"❌ Auth failed: {login_res.status_code} - {login_res.text}")
                return
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. List Roles
        print("\n--- Listing Roles ---")
        res = await client.get("/v1/roles/", headers=headers)
        print(f"Status: {res.status_code}")
        roles = res.json()
        print(f"Roles found: {[r['name'] for r in roles]}")
        
        # 3. Create a New Role
        print("\n--- Creating Role 'manager' ---")
        res = await client.post("/v1/roles/", json={"name": "manager"}, headers=headers)
        print(f"Status: {res.status_code}")
        manager_role = res.json()
        print(f"Created: {manager_role}")
        manager_id = manager_role["id"]
        
        # 4. Get Role by ID
        print(f"\n--- Getting Role ID {manager_id} ---")
        res = await client.get(f"/v1/roles/{manager_id}", headers=headers)
        print(f"Status: {res.status_code}")
        print(f"Result: {res.json()}")
        
        # 5. Update Role
        print(f"\n--- Updating Role ID {manager_id} to 'admin_lite' ---")
        res = await client.patch(f"/v1/roles/{manager_id}", json={"name": "admin_lite"}, headers=headers)
        print(f"Status: {res.status_code}")
        print(f"Updated: {res.json()}")
        
        # 6. Delete Role
        print(f"\n--- Deleting Role ID {manager_id} ---")
        res = await client.delete(f"/v1/roles/{manager_id}", headers=headers)
        print(f"Status: {res.status_code}")
        
        # 7. Verify Deletion
        print("\n--- Verifying Deletion ---")
        res = await client.get(f"/v1/roles/{manager_id}", headers=headers)
        print(f"Status (Expected 404): {res.status_code}")
        
        if res.status_code == 404:
            print("\n✅ Role CRUD verification successful!")
        else:
            print("\n❌ Role verification failed.")

if __name__ == "__main__":
    asyncio.run(test_roles_crud())
