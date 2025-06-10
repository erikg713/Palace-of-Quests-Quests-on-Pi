import React, { useState, useCallback } from "react";
import { PiSDK } from "@pi-network/pi-sdk";
import "./App.css";

const App = () => {
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState("");

  const authenticatePiUser = useCallback(async () => {
    setAuthLoading(true);
    setAuthError("");
    try {
      const authData = await PiSDK.auth({ permissions: ["payments", "username"] });
      setUser(authData);
    } catch (error) {
      // Ideally, replace console.error with a logging service in production
      console.error("Pi Authentication Error:", error);
      setAuthError("Authentication failed. Please try again.");
    } finally {
      setAuthLoading(false);
    }
  }, []);

  return (
    <main className="app-container" role="main" tabIndex={-1}>
      <header className="app-header">
        <h1>Palace of Quests</h1>
        <p className="app-subtitle">Enter the Pi-powered metaverse and begin your journey.</p>
      </header>
      <section className="auth-section">
        {!user ? (
          <>
            <button
              className="auth-btn"
              onClick={authenticatePiUser}
              disabled={authLoading}
              aria-busy={authLoading}
            >
              {authLoading ? "Signing in..." : "Sign in with Pi Network"}
            </button>
            {authError && (
              <div className="auth-error" role="alert">
                {authError}
              </div>
            )}
          </>
        ) : (
          <div className="user-info">
            <p>
              <strong>Welcome,</strong> {user.username}
            </p>
            {/* Add additional user info or actions here */}
          </div>
        )}
      </section>
    </main>
  );
};

export default App;
