# 🔑 Environment Variables Reference

All environment variables are loaded via **Pydantic Settings** from the `.env` file located at the project root.

**Config class**: `app/core/config.py` → `Settings`

---

## Required Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db` | Async PostgreSQL connection string. **Must** use `asyncpg` driver. |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string. DB 0 is used for general cache/OTP. ARQ workers use DB 1 and DB 2. |

---

## Authentication & Security

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `your-super-secret-key-change-it` | JWT signing key. **Must be changed in production.** |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Access token TTL (minutes) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token TTL (days) |

---

## Application URLs

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | `http://localhost:8000` | Backend API base URL |
| `FRONTEND_URL` | `http://localhost:5174` | Frontend app URL (used for OAuth redirect) |

---

## Google OAuth2 (Gmail Integration)

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_CLIENT_ID` | `GOOGLE_CLIENT_ID` | Google OAuth2 client ID |
| `GOOGLE_CLIENT_SECRET` | `GOOGLE_CLIENT_SECRET` | Google OAuth2 client secret |
| `GOOGLE_REDIRECT_URI` | `http://localhost:8000/api/v1/auth/google/callback` | OAuth redirect URI (must match Google Console) |

---

## `.env.example`

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-key-change-it
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```

---

## Redis Database Allocation

The application uses logical Redis databases for isolation:

| Redis DB | Purpose | Used By |
|----------|---------|---------|
| `0` | General cache, OTP storage | API Server (`app.core.redis`) |
| `1` | Base worker queue | Base Worker (ARQ) |
| `2` | Email worker queue | Email Worker (ARQ) |
