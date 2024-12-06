import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css'; // Assumes a CSS file for styling

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">
        <h1>
          <Link to="/">Palace of Quests</Link>
        </h1>
      </div>
      <nav className="header-nav">
        <ul>
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li>
            <Link to="/quests">Quests</Link>
          </li>
          <li>
            <Link to="/profile">Profile</Link>
          </li>
          <li>
            <Link to="/logout">Logout</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
