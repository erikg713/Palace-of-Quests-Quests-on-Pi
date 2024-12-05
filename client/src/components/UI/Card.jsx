import React from 'react';
import PropTypes from 'prop-types';
import './Card.css'; // Assuming you have a CSS file for styling

const Card = ({ children, className = '', style = {} }) => {
  return (
    <div className={`card ${className}`} style={style}>
      {children}
    </div>
  );
};

Card.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  style: PropTypes.object,
};

export default Card;
