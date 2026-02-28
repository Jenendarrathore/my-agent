# 🎨 Frontend Overview

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18 | UI framework |
| TypeScript | 5.2 | Type safety |
| Vite | 5.1 | Build tool & dev server |
| React Router | 7.x | Client-side routing |
| TailwindCSS | 3.4 | Utility-first CSS |
| Axios | 1.x | HTTP client |
| Lucide React | Latest | Icon library |
| clsx + tailwind-merge | Latest | Class name utilities |
| date-fns | 4.1 | Date formatting |

---

## Project Structure

```
frontend/
├── src/
│   ├── main.tsx              # React DOM entry point
│   ├── App.tsx               # Root component + routing
│   ├── App.css               # Global app styles
│   ├── index.css             # TailwindCSS imports + base styles
│   ├── components/
│   │   ├── MainLayout.tsx    # Sidebar navigation layout
│   │   └── ui/               # Shared UI primitives (Button, cn)
│   └── pages/
│       ├── Login.tsx         # Login page
│       ├── Register.tsx      # Registration page
│       ├── Dashboard.tsx     # Dashboard home
│       ├── ConnectedAccounts.tsx  # OAuth account management
│       ├── Jobs.tsx          # Job monitoring + triggers
│       └── Emails.tsx        # Email viewer
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
└── postcss.config.js
```

---

## Routing

Defined in `App.tsx` using React Router v7:

| Path | Component | Auth | Description |
|------|-----------|------|-------------|
| `/login` | `Login` | Public | Login page (redirects to dashboard if logged in) |
| `/register` | `Register` | Public | Registration page |
| `/dashboard` | `Dashboard` | Protected | Main dashboard |
| `/connected-accounts` | `ConnectedAccounts` | Protected | OAuth accounts |
| `/jobs` | `Jobs` | Protected | Job monitoring |
| `/emails` | `Emails` | Protected | Email viewer |
| `/` | — | — | Redirects to `/dashboard` |
| `*` | — | — | Redirects to `/dashboard` |

### Route Protection

- **`ProtectedRoute`**: Checks `localStorage.getItem("access_token")`. If missing → redirect to `/login`.
- **`PublicRoute`**: Checks token. If present → redirect to `/dashboard`.
- Protected routes are wrapped in `MainLayout` (shared sidebar).

---

## Layout

### MainLayout (`components/MainLayout.tsx`)

Collapsible sidebar navigation with:
- App branding ("Financial Agent") with admin badge
- Navigation links: Dashboard, Emails, Connections, Jobs, Transactions, Activity Log, Settings
- Active route highlighting
- Collapse/expand toggle
- Logout button

**Admin detection**:
```tsx
// Loads user from localStorage
const user = JSON.parse(localStorage.getItem("user"));
// Shows "Admin Level" badge if user.role.name === "admin"
```

---

## Pages

### Login
- OAuth2 form (username/email + password)
- POST to `/api/auth/login`
- Stores `access_token` and `user` (full object) in localStorage
- Link to register page

### Register
- Name, username, email, password form
- POST to `/api/auth/register`
- Stores token and navigates to dashboard

### Dashboard
- Main landing page after login

### Connected Accounts
- Lists user's connected email accounts
- Create new connections (provider + email)
- Authorize via Google OAuth (opens redirect)
- Trigger email fetch per account

### Jobs
- Lists all background jobs with status, type, timestamps
- Filters by status and job type
- Admin users see a "User" column showing who triggered each job
- Trigger buttons for email fetch and extraction

### Emails
- Lists fetched emails with subject, provider, status
- Admin sees all emails across users
- Regular users see only their own

---

## Authentication Flow

```
1. Login/Register → API returns { access_token, user }
2. Store in localStorage:
   - access_token → used for API calls
   - user → used for UI (role badge, permissions)
3. Protected routes check token existence
4. API calls include Bearer token in headers
5. Logout → clear localStorage → redirect to /login
```

---

## Running

```bash
cd frontend

# Development
npm run dev          # Starts Vite dev server on port 5174

# Production build
npm run build        # TypeScript check + Vite build → dist/

# Preview production build
npm run preview

# Lint
npm run lint
```
