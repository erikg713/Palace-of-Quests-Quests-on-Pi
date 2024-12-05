import React from 'react';
import PropTypes from 'prop-types';
import './Button.css'; // Assuming you have a CSS file for styling

const Button = ({ onClick, label, type = 'button', className = '', disabled = false }) => {
  return (
    <button
      type={type}
      className={`btn ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
};

Button.propTypes = {
  onClick: PropTypes.func,
  label: PropTypes.string.isRequired,
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
  className: PropTypes.string,
  disabled: PropTypes.bool,
};

export default Button;
