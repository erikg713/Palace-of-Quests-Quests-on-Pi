// components/Layout/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/profile">Profile</Link></li>
        <li><Link to="/shop">Shop</Link></li>
        <li><Link to="/premium">Premium</Link></li>
        <li><Link to="/logout">Logout</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/shop">Shop</Link></li>
        <li><Link to="/subscription">Premium</Link></li>
        <li><Link to="/login">Login</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;