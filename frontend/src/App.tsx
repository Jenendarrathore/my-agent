import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Login } from "./pages/Login";
import { Dashboard } from "./pages/Dashboard";
import { Register } from "./pages/Register";
import { ConnectedAccounts } from "./pages/ConnectedAccounts";
import { Jobs } from "./pages/Jobs";
import { Emails } from "./pages/Emails";
import { MainLayout } from "./components/MainLayout";

// Protected Route Wrapper
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = !!localStorage.getItem("access_token");

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

// Public Route Wrapper (Redirects to dashboard if already logged in)
function PublicRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = !!localStorage.getItem("access_token");

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />

        {/* Protected Routes */}
        <Route element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/connected-accounts" element={<ConnectedAccounts />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/emails" element={<Emails />} />
          {/* Add more protected routes here */}
        </Route>

        {/* Default Redirects */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
