import React from 'react';
import PropTypes from 'prop-types';
import './AuthLayout.css'; // Optional CSS file for styling

const AuthLayout = ({ children }) => {
  return (
    <div className="auth-layout">
      <div className="auth-container">
        <div className="auth-header">
          <h1>Welcome to Our App</h1>
          <p>Please sign in or register to continue</p>
        </div>
        <div className="auth-body">{children}</div>
      </div>
    </div>
  );
};

AuthLayout.propTypes = {
  children: PropTypes.node.isRequired,
};

export default AuthLayout;
