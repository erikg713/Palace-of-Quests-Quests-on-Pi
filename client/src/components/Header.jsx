import React from "react";
import { Link } from "react-router-dom";
import "./Header.css";

const navLinks = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/quests", label: "Quests" },
  { to: "/profile", label: "Profile" },
  { to: "/logout", label: "Logout" }
];

function Header() {
  return (
    <header className="header" aria-label="Site Header">
      <div className="header__logo">
        <h1>
          <Link to="/" tabIndex={0} aria-label="Go to homepage">
            Palace of Quests
          </Link>
        </h1>
      </div>
      <nav className="header__nav" aria-label="Main Navigation">
        <ul className="header__nav-list">
          {navLinks.map(({ to, label }) => (
            <li key={to} className="header__nav-item">
              <Link to={to} className="header__nav-link">
                {label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}

export default Header;
