import asyncio
import httpx
import json
import shlex
import os
from datetime import datetime, timezone, timedelta

BASE_URL = "http://localhost:8000"
API_V1_URL = f"{BASE_URL}/api/v1"

async def test_api():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        report = []
        
        def to_curl(method, url, headers=None, json_data=None):
            command = ["curl", "-X", method, f"{BASE_URL}{url}"]
            if headers:
                for k, v in headers.items():
                    command.extend(["-H", f"{k}: {v}"])
            if json_data:
                command.extend(["-d", json.dumps(json_data)])
            return " ".join(shlex.quote(x) for x in command)

        async def perform_op(method, path, label, json_data=None, headers=None, expected_status=200):
            full_url = path if path.startswith("http") else path
            
            report.append(f"### {label}")
            report.append(f"**Request:** `{method} {path}`")
            if json_data:
                report.append("```json\n" + json.dumps(json_data, indent=2) + "\n```")
            
            # Generate Curl
            report.append("**Curl Command:**")
            report.append("```bash\n" + to_curl(method, path, headers, json_data) + "\n```")
            
            start_time = datetime.now()
            try:
                if method == "GET":
                    res = await client.get(path, headers=headers)
                elif method == "POST":
                    res = await client.post(path, json=json_data, headers=headers)
                elif method == "PATCH":
                    res = await client.patch(path, json=json_data, headers=headers)
                elif method == "DELETE":
                    res = await client.delete(path, headers=headers)
                
                status_match = res.status_code == expected_status
                status_icon = "✅" if status_match else "❌"
                
                report.append(f"**Response Status:** {res.status_code} {status_icon}")
                try:
                    resp_json = res.json()
                    report.append("```json\n" + json.dumps(resp_json, indent=2) + "\n```")
                except:
                    report.append("*[No JSON Body]*")
                
                report.append("-" * 20)
                print(f"{status_icon} {label}")
                return res if status_match else None
            except Exception as e:
                report.append(f"**Error:** {str(e)}")
                print(f"❌ {label}: {str(e)}")
                return None

        report.append("# Full API CRUD Detailed Trace")
        report.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
        report.append("=" * 40)

        # 1. AUTH & USER
        report.append("\n## 1. Authentication & User")
        ts = int(datetime.now().timestamp())
        test_email = f"trace_{ts}@example.com"
        test_username = f"trace_{ts}"
        test_password = "SecurePassword123!"

        reg_data = {"name": "Trace Tester", "username": test_username, "primary_email": test_email, "password": test_password}
        res = await perform_op("POST", "/api/auth/register", "User Registration", reg_data, expected_status=200)
        if not res: return
        
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        res = await perform_op("GET", "/api/v1/users/me", "Get Current User", headers=headers)
        if not res: return
        user_id = res.json()["id"]

        await perform_op("PATCH", f"/api/v1/users/{user_id}", "Update User", {"name": "Trace Pro"}, headers=headers)
        await perform_op("GET", f"/api/v1/users/{user_id}", "Get User by ID", headers=headers)

        # 2. CATEGORY
        report.append("\n## 2. Category CRUD")
        cat_data = {"name": f"Trace_Cat_{ts}", "type": "expense"}
        res = await perform_op("POST", "/api/v1/categories/", "Create Category", cat_data, headers, 201)
        if res:
            category_id = res.json()["id"]
            await perform_op("GET", "/api/v1/categories/", "List Categories", headers=headers)
            await perform_op("PATCH", f"/api/v1/categories/{category_id}", "Update Category", {"name": "Trace Modified"}, headers=headers)

        # 3. CONNECTED ACCOUNT
        report.append("\n## 3. Connected Account CRUD")
        acc_data = {
            "provider": "gmail",
            "email": f"trace_{ts}@gmail.com",
            "access_token": "tk_123",
            "refresh_token": "rf_123",
            "token_expiry": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
        }
        res = await perform_op("POST", "/api/v1/connected-accounts/", "Create Connected Account", acc_data, headers, 201)
        if res: account_id = res.json()["id"]

        # 4. EMAIL CONNECTION
        report.append("\n## 4. Email Connection CRUD")
        econn_data = {
            "user_id": user_id,
            "provider": "gmail",
            "access_token": "env_tk",
            "refresh_token": "env_rf",
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        }
        res = await perform_op("POST", "/api/v1/email-connections/", "Create Email Connection", econn_data, headers, 201)
        if res: email_conn_id = res.json()["id"]

        # 5. EMAIL
        report.append("\n## 5. Email CRUD")
        if email_conn_id:
            email_data = {
                "user_id": user_id,
                "email_connection_id": email_conn_id,
                "provider": "gmail",
                "provider_message_id": f"trace_msg_{ts}",
                "subject": "Trace Subject",
                "received_at": datetime.now(timezone.utc).isoformat()
            }
            res = await perform_op("POST", "/api/v1/emails/", "Create Email", email_data, headers, 201)
            if res: email_id = res.json()["id"]

        # 6. JOB
        report.append("\n## 6. Job CRUD")
        job_data = {"job_type": "EMAIL_FETCH", "triggered_by": "MANUAL"}
        res = await perform_op("POST", "/api/v1/jobs/", "Create Job", job_data, headers, 201)
        if res: job_id = res.json()["id"]

        # 7. LLM TRANSACTION
        report.append("\n## 7. LLM Transaction CRUD")
        if job_id:
            llm_data = {"job_id": job_id, "model_name": "gpt-4", "provider": "openai"}
            res = await perform_op("POST", "/api/v1/llm-transactions/", "Create LLM Transaction", llm_data, headers, 201)
            if res: llm_tx_id = res.json()["id"]

        # 8. EMAIL EXTRACTION
        report.append("\n## 8. Email Extraction CRUD")
        if email_id:
            ext_data = {"email_id": email_id, "status": "SUCCESS", "extracted_json": {"test": "data"}}
            res = await perform_op("POST", "/api/v1/email-extractions/", "Create Extraction", ext_data, headers, 201)
            if res: ext_id = res.json()["id"]

        # 9. FINANCIAL TRANSACTION
        report.append("\n## 9. Financial Transaction CRUD")
        if category_id:
            tx_data = {"user_id": user_id, "amount": 10.5, "type": "expense", "occurred_at": datetime.now(timezone.utc).isoformat(), "category_id": category_id}
            res = await perform_op("POST", "/api/v1/transactions/", "Create Transaction", tx_data, headers, 201)
            if res: tx_id = res.json()["id"]

        # 10. CLEANUP
        report.append("\n## 10. Cleanup")
        if tx_id: await perform_op("DELETE", f"/api/v1/transactions/{tx_id}", "Delete Transaction", None, headers, 204)
        if ext_id: await perform_op("DELETE", f"/api/v1/email-extractions/{ext_id}", "Delete Extraction", None, headers, 204)
        if llm_tx_id: await perform_op("DELETE", f"/api/v1/llm-transactions/{llm_tx_id}", "Delete LLM TX", None, headers, 204)
        if job_id: await perform_op("DELETE", f"/api/v1/jobs/{job_id}", "Delete Job", None, headers, 204)
        if email_id: await perform_op("DELETE", f"/api/v1/emails/{email_id}", "Delete Email", None, headers, 204)
        if email_conn_id: await perform_op("DELETE", f"/api/v1/email-connections/{email_conn_id}", "Delete Email Conn", None, headers, 204)
        if account_id: await perform_op("DELETE", f"/api/v1/connected-accounts/{account_id}", "Delete Account", None, headers, 204)
        if category_id: await perform_op("DELETE", f"/api/v1/categories/{category_id}", "Delete Cat", None, headers, 204)
        if user_id: await perform_op("DELETE", f"/api/v1/users/{user_id}", "Delete User", None, headers, 204)

        report.append("\n" + "=" * 40)
        report.append("Trace Complete.")
        
        report_text = "\n".join(report)
        
        # Save to main file
        with open("full_api_verification.md", "w") as f:
            f.write(report_text)
            
        # Save to history
        os.makedirs("test_results", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        history_file = f"test_results/test_result_{timestamp}.md"
        with open(history_file, "w") as f:
            f.write(report_text)
            
        print(f"\nDetailed report saved to: {history_file}")

if __name__ == "__main__":
    asyncio.run(test_api())
