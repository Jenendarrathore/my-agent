# API Testing Guide

This project includes a comprehensive API verification script that performs full CRUD (Create, Read, Update, Delete) lifecycles for all supported models.

## Test Script Implementation

The main test script is located at:
[`app/scripts/test_api_crud.py`](file:///opt/gitco/ai/my-agent/app/scripts/test_api_crud.py)

### What it Tests
The script verifies the following models in a realistic application sequence:
1. **Authentication & User**: Registration, Login (token generation), and profile updates.
2. **Category**: Management of transaction categories.
3. **Connected Account**: Banking/Provider account linking.
4. **Email Connection**: OAuth-style email provider connections.
5. **Email**: Ingestion of email metadata.
6. **Job**: Background task tracking.
7. **LLM Transaction**: AI usage logging linked to jobs.
8. **Email Extraction**: Results of AI processing on emails.
9. **Financial Transaction**: Spending/Income records linked to categories.

---

## Getting Started

### Prerequisites
Ensure you have the required dependencies installed:
```bash
pip install httpx asyncpg email-validator
```

### Running the Tests
1. **Start the Application Server**:
   The tests require the server to be running on your local machine.
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Execute the Test Script**:
   Run the script using Python. It will perform all operations and generate a report.
   ```bash
   python3 app/scripts/test_api_crud.py
   ```

---

## Configuration

### Updating the Base URL
By default, the script targets `http://localhost:8000`. If your server is running on a different port or host, update the `BASE_URL` constant at the top of the file:

```python
# app/scripts/test_api_crud.py

BASE_URL = "http://localhost:8000"  # Change this to your server URL
```

### Authentication Handling
The script automatically:
1. Generates a unique test user for every run.
2. Registers the user via `/api/auth/register`.
3. Extracts the `access_token`.
4. Attaches the `Authorization: Bearer <token>` header to all subsequent V1 API calls.

---

## Test Output

After running the script, the following outputs are generated:
1. **[`full_api_verification.md`](full_api_verification.md)**: The latest trace with full request/response details and curl commands.
2. **`test_results/`**: A historical record of all test runs, stored with timestamped filenames (e.g., `test_result_2026-02-28T10-32-33.md`).

The reports contain:
- **Request Payloads**: Exactly what was sent to the server.
- **Curl Commands**: Reproducible commands for manual debugging.
- **Response Status**: Including success/failure icons.
- **Response Bodies**: The JSON returned by the server.

> [!TIP]
> Check the `test_results/` folder periodically to track your API's performance and behavior over the course of development.
