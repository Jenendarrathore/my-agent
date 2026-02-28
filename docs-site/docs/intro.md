---
slug: /
sidebar_position: 1
sidebar_label: "🏠 Home"
title: "Financial Agent — System Documentation"
---

# 📚 Financial Agent — System Documentation

> **Comprehensive documentation for the Financial Agent application** — a full-stack FinTech platform built with FastAPI, SQLAlchemy, ARQ, and React.

---

## Quick Reference

```bash
# Start everything locally
uvicorn app.main:app --reload                                    # API Server
./venv/bin/arq app.core.worker.base_settings.WorkerSettings      # Base Worker
./venv/bin/arq app.core.worker.email_settings.WorkerSettings     # Email Worker
cd frontend && npm run dev                                       # Frontend

# Database Migrations
alembic revision --autogenerate -m "description"                 # Generate
alembic upgrade head                                             # Apply
```

## What's Inside

| Section | What You'll Find |
|---------|-----------------|
| **🏗️ Architecture** | System overview, tech stack, data flows, database schema |
| **🚀 Getting Started** | Setup, running, environment configuration |
| **⚙️ Backend** | Project structure, auth, API reference, models, services, jobs, email, migrations |
| **🎨 Frontend** | React app architecture, routing, pages |
| **📋 SOPs** | Step-by-step guides for adding features, models, jobs, workers, and providers |
| **🛠️ Scripts** | All available scripts documented |
