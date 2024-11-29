import React from 'react';
import { Link } from 'react-router-dom';
import './styles/MobileNav.css';

const MobileNav = () => {
  return (
    <nav className="mobile-nav">
      <Link to="/">Home</Link>
      <Link to="/marketplace">Marketplace</Link>
      <Link to="/profile">Profile</Link>
    </nav>
  );
};

export default MobileNav;
