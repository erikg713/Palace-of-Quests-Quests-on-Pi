import React from "react";
import { NavLink } from "react-router-dom";
import "./Sidebar.css";

const links = [
  { path: "/dashboard", label: "Dashboard" },
  { path: "/quests", label: "Quests" },
  { path: "/profile", label: "Profile" },
  { path: "/settings", label: "Settings" }
];

const Sidebar = () => (
  <aside className="sidebar" aria-label="Main sidebar">
    <nav>
      <ul>
        {links.map(({ path, label }) => (
          <li key={path}>
            <NavLink
              to={path}
              className={({ isActive }) => isActive ? "active" : ""}
              end
            >
              {label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  </aside>
);

export default Sidebar;
