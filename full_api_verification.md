# Full API CRUD Detailed Trace
Generated: 2026-02-28T05:04:35.376180+00:00
========================================

## 1. Authentication & User
### User Registration
**Request:** `POST /api/auth/register`
```json
{
  "name": "Trace Tester",
  "username": "trace_1772255075",
  "primary_email": "trace_1772255075@example.com",
  "password": "SecurePassword123!"
}
```
**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/auth/register -d '{"name": "Trace Tester", "username": "trace_1772255075", "primary_email": "trace_1772255075@example.com", "password": "SecurePassword123!"}'
```
**Response Status:** 200 ✅
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNzcyODU5ODc1fQ.WcsZqh0QZOcrJHmw9TvuORzBz5ZJdmvC3M3YUIQGlwg",
  "token_type": "bearer"
}
```
--------------------
### Get Current User
**Request:** `GET /api/v1/users/me`
**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/v1/users/me -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 200 ✅
```json
{
  "name": null,
  "username": "trace_1772255075",
  "primary_email": "trace_1772255075@example.com",
  "id": 13,
  "is_active": true,
  "created_at": "2026-02-28T05:04:35.667974Z"
}
```
--------------------
### Update User
**Request:** `PATCH /api/v1/users/13`
```json
{
  "name": "Trace Pro"
}
```
**Curl Command:**
```bash
curl -X PATCH http://localhost:8000/api/v1/users/13 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"name": "Trace Pro"}'
```
**Response Status:** 200 ✅
```json
{
  "name": "Trace Pro",
  "username": "trace_1772255075",
  "primary_email": "trace_1772255075@example.com",
  "id": 13,
  "is_active": true,
  "created_at": "2026-02-28T05:04:35.667974Z"
}
```
--------------------
### Get User by ID
**Request:** `GET /api/v1/users/13`
**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/v1/users/13 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 200 ✅
```json
{
  "name": "Trace Pro",
  "username": "trace_1772255075",
  "primary_email": "trace_1772255075@example.com",
  "id": 13,
  "is_active": true,
  "created_at": "2026-02-28T05:04:35.667974Z"
}
```
--------------------

## 2. Category CRUD
### Create Category
**Request:** `POST /api/v1/categories/`
```json
{
  "name": "Trace_Cat_1772255075",
  "type": "expense"
}
```
**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/v1/categories/ -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"name": "Trace_Cat_1772255075", "type": "expense"}'
```
**Response Status:** 201 ✅
```json
{
  "name": "Trace_Cat_1772255075",
  "type": "expense",
  "is_system": false,
  "id": 8,
  "user_id": 13,
  "created_at": "2026-02-28T05:04:35.919348Z"
}
```
--------------------
### List Categories
**Request:** `GET /api/v1/categories/`
**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/v1/categories/ -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 200 ✅
```json
[
  {
    "name": "Trace_Cat_1772255075",
    "type": "expense",
    "is_system": false,
    "id": 8,
    "user_id": 13,
    "created_at": "2026-02-28T05:04:35.919348Z"
  }
]
```
--------------------
### Update Category
**Request:** `PATCH /api/v1/categories/8`
```json
{
  "name": "Trace Modified"
}
```
**Curl Command:**
```bash
curl -X PATCH http://localhost:8000/api/v1/categories/8 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"name": "Trace Modified"}'
```
**Response Status:** 200 ✅
```json
{
  "name": "Trace Modified",
  "type": "expense",
  "is_system": false,
  "id": 8,
  "user_id": 13,
  "created_at": "2026-02-28T05:04:35.919348Z"
}
```
--------------------

## 3. Connected Account CRUD
### Create Connected Account
**Request:** `POST /api/v1/connected-accounts/`
```json
{
  "provider": "gmail",
  "email": "trace_1772255075@gmail.com",
  "access_token": "tk_123",
  "refresh_token": "rf_123",
  "token_expiry": "2026-03-30T05:04:35.966258+00:00"
}
```
**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/v1/connected-accounts/ -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"provider": "gmail", "email": "trace_1772255075@gmail.com", "access_token": "tk_123", "refresh_token": "rf_123", "token_expiry": "2026-03-30T05:04:35.966258+00:00"}'
```
**Response Status:** 201 ✅
```json
{
  "provider": "gmail",
  "email": "trace_1772255075@gmail.com",
  "is_active": true,
  "id": 6,
  "user_id": 13,
  "token_expiry": "2026-03-30T05:04:35.966258Z",
  "created_at": "2026-02-28T05:04:35.975496Z"
}
```
--------------------

## 4. Email Connection CRUD
### Create Email Connection
**Request:** `POST /api/v1/email-connections/`
```json
{
  "user_id": 13,
  "provider": "gmail",
  "access_token": "env_tk",
  "refresh_token": "env_rf",
  "expires_at": "2026-02-28T06:04:35.988562+00:00"
}
```
**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/v1/email-connections/ -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"user_id": 13, "provider": "gmail", "access_token": "env_tk", "refresh_token": "env_rf", "expires_at": "2026-02-28T06:04:35.988562+00:00"}'
```
**Response Status:** 201 ✅
```json
{
  "provider": "gmail",
  "access_token": "env_tk",
  "refresh_token": "env_rf",
  "scopes": null,
  "expires_at": "2026-02-28T06:04:35.988562Z",
  "id": 5,
  "user_id": 13,
  "revoked_at": null,
  "created_at": "2026-02-28T05:04:35.998349Z",
  "updated_at": "2026-02-28T05:04:35.998356Z"
}
```
--------------------

## 5. Email CRUD
### Create Email
**Request:** `POST /api/v1/emails/`
```json
{
  "user_id": 13,
  "email_connection_id": 5,
  "provider": "gmail",
  "provider_message_id": "trace_msg_1772255075",
  "subject": "Trace Subject",
  "received_at": "2026-02-28T05:04:36.011269+00:00"
}
```
**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/v1/emails/ -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"user_id": 13, "email_connection_id": 5, "provider": "gmail", "provider_message_id": "trace_msg_1772255075", "subject": "Trace Subject", "received_at": "2026-02-28T05:04:36.011269+00:00"}'
```
**Response Status:** 201 ✅
```json
{
  "provider": "gmail",
  "provider_message_id": "trace_msg_1772255075",
  "thread_id": null,
  "subject": "Trace Subject",
  "body_text": null,
  "body_html": null,
  "received_at": "2026-02-28T05:04:36.011269Z",
  "checksum": null,
  "extraction_status": "PENDING",
  "extraction_version": null,
  "id": 5,
  "user_id": 13,
  "email_connection_id": 5,
  "fetched_at": "2026-02-28T05:04:36.020139Z",
  "created_at": "2026-02-28T05:04:36.020143Z"
}
```
--------------------

## 6. Job CRUD
### Create Job
**Request:** `POST /api/v1/jobs/`
```json
{
  "job_type": "EMAIL_FETCH",
  "triggered_by": "MANUAL"
}
```
**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/v1/jobs/ -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"job_type": "EMAIL_FETCH", "triggered_by": "MANUAL"}'
```
**Response Status:** 201 ✅
```json
{
  "job_type": "EMAIL_FETCH",
  "status": "QUEUED",
  "triggered_by": "MANUAL",
  "input_payload": null,
  "output_payload": null,
  "error_payload": null,
  "retry_count": 0,
  "id": 5,
  "started_at": null,
  "finished_at": null,
  "created_at": "2026-02-28T05:04:36.036790Z"
}
```
--------------------

## 7. LLM Transaction CRUD
### Create LLM Transaction
**Request:** `POST /api/v1/llm-transactions/`
```json
{
  "job_id": 5,
  "model_name": "gpt-4",
  "provider": "openai"
}
```
**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/v1/llm-transactions/ -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"job_id": 5, "model_name": "gpt-4", "provider": "openai"}'
```
**Response Status:** 201 ✅
```json
{
  "model_name": "gpt-4",
  "provider": "openai",
  "prompt_version": null,
  "prompt_hash": null,
  "input_tokens": 0,
  "output_tokens": 0,
  "total_tokens": 0,
  "estimated_cost": 0.0,
  "latency_ms": 0,
  "id": 5,
  "job_id": 5,
  "created_at": "2026-02-28T05:04:36.051475Z"
}
```
--------------------

## 8. Email Extraction CRUD
### Create Extraction
**Request:** `POST /api/v1/email-extractions/`
```json
{
  "email_id": 5,
  "status": "SUCCESS",
  "extracted_json": {
    "test": "data"
  }
}
```
**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/v1/email-extractions/ -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"email_id": 5, "status": "SUCCESS", "extracted_json": {"test": "data"}}'
```
**Response Status:** 201 ✅
```json
{
  "extraction_version": null,
  "status": "SUCCESS",
  "extracted_json": {
    "test": "data"
  },
  "model_used": null,
  "prompt_hash": null,
  "id": 5,
  "email_id": 5,
  "created_at": "2026-02-28T05:04:36.067819Z"
}
```
--------------------

## 9. Financial Transaction CRUD
### Create Transaction
**Request:** `POST /api/v1/transactions/`
```json
{
  "user_id": 13,
  "amount": 10.5,
  "type": "expense",
  "occurred_at": "2026-02-28T05:04:36.078263+00:00",
  "category_id": 8
}
```
**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/v1/transactions/ -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns' -d '{"user_id": 13, "amount": 10.5, "type": "expense", "occurred_at": "2026-02-28T05:04:36.078263+00:00", "category_id": 8}'
```
**Response Status:** 201 ✅
```json
{
  "amount": 10.5,
  "type": "expense",
  "occurred_at": "2026-02-28T05:04:36.078263Z",
  "category_id": 8,
  "source": "manual",
  "external_id": null,
  "notes": null,
  "id": 8,
  "user_id": 13,
  "created_at": "2026-02-28T05:04:36.085274Z"
}
```
--------------------

## 10. Cleanup
### Delete Transaction
**Request:** `DELETE /api/v1/transactions/8`
**Curl Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/transactions/8 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 204 ✅
*[No JSON Body]*
--------------------
### Delete Extraction
**Request:** `DELETE /api/v1/email-extractions/5`
**Curl Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/email-extractions/5 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 204 ✅
*[No JSON Body]*
--------------------
### Delete LLM TX
**Request:** `DELETE /api/v1/llm-transactions/5`
**Curl Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/llm-transactions/5 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 204 ✅
*[No JSON Body]*
--------------------
### Delete Job
**Request:** `DELETE /api/v1/jobs/5`
**Curl Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/jobs/5 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 204 ✅
*[No JSON Body]*
--------------------
### Delete Email
**Request:** `DELETE /api/v1/emails/5`
**Curl Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/emails/5 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 204 ✅
*[No JSON Body]*
--------------------
### Delete Email Conn
**Request:** `DELETE /api/v1/email-connections/5`
**Curl Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/email-connections/5 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 204 ✅
*[No JSON Body]*
--------------------
### Delete Account
**Request:** `DELETE /api/v1/connected-accounts/6`
**Curl Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/connected-accounts/6 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 204 ✅
*[No JSON Body]*
--------------------
### Delete Cat
**Request:** `DELETE /api/v1/categories/8`
**Curl Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/categories/8 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 204 ✅
*[No JSON Body]*
--------------------
### Delete User
**Request:** `DELETE /api/v1/users/13`
**Curl Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/users/13 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc3MjI1ODY3NX0.r-jV5DMJfeNEqa6Vmth7IIt1FfYgfE0OYVJkVOki5ns'
```
**Response Status:** 204 ✅
*[No JSON Body]*
--------------------

========================================
Trace Complete.