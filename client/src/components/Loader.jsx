import React from 'react';
import PropTypes from 'prop-types';
import './Loader.css';

/**
 * Loader Spinner Component
 * @param {Object} props
 * @param {string} props.size - Loader size (e.g., "48px", "3rem")
 * @param {string} props.color - Spinner color (CSS color value)
 */
function Loader({ size = '48px', color = '#4caf50' }) {
  return (
    <span
      className="loader"
      role="status"
      aria-live="polite"
      aria-label="Loading"
      style={{
        width: size,
        height: size,
        borderColor: `${color} transparent ${color} transparent`,
      }}
      data-testid="loader"
    />
  );
}

Loader.propTypes = {
  size: PropTypes.string,
  color: PropTypes.string,
};

export default Loader;
