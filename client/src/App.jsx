// frontend/src/App.js
import React, { useState } from "react";
import { PiSDK } from "@pi-network/pi-sdk";  // Install Pi SDK

const App = () => {
  const [userData, setUserData] = useState(null);
  
  const authenticatePiUser = async () => {
    try {
      const authData = await PiSDK.auth({ permissions: ["payments", "username"] });
      setUserData(authData);
    } catch (error) {
      console.error("Pi Authentication Error:", error);
    }
  };

  return (
    <div>
      <h1>Pi Network Web3 App</h1>
      {userData ? (
        <div>
          <h2>Welcome, {userData.username}!</h2>
          <p>Pi Address: {userData.wallet_address}</p>
        </div>
      ) : (
        <button onClick={authenticatePiUser}>Login with Pi Network</button>
      )}
    </div>
  );
};

export default App;

import React, { Suspense, StrictMode } from 'react';
import './styles/globals.css';
import './fonts.css';

// Lazy load AppRoutes for performance optimization
const AppRoutes = React.lazy(() => import('./routes/AppRoutes'));

/**
 * ErrorBoundary class to gracefully handle runtime errors in the component tree.
 * Displays a fallback UI and logs error details.
 */
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    // Update state so next render shows fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    // Log error details for debugging/monitoring
    // You can integrate with external services here
    if (process.env.NODE_ENV !== 'production') {
      console.error('Uncaught error:', error, info);
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <section
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100vh',
            background: '#1a1a1a',
            color: '#fff',
            fontFamily: 'inherit',
          }}
        >
          <h1>Something went wrong.</h1>
          <p>
            An unexpected error occurred. Please refresh the page or contact support if the problem persists.
          </p>
        </section>
      );
    }
    return this.props.children;
  }
}

/**
 * App component - Root of the application.
 * Wraps the main routing logic with error and suspense boundaries for reliability and user experience.
 */
const App = () => (
  <StrictMode>
    <ErrorBoundary>
      <Suspense
        fallback={
          <div style={{
            width: '100vw',
            height: '100vh',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            background: '#0e0e0e'
          }}>
            <span style={{ color: '#8c8c8c', fontSize: 22 }}>Loading...</span>
          </div>
        }
      >
        <AppRoutes />
      </Suspense>
    </ErrorBoundary>
  </StrictMode>
);

export default App;
