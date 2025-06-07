import React from "react";
import { NavLink } from "react-router-dom";
import "./Sidebar.css";

const SIDEBAR_LINKS = [
  { path: "/dashboard", label: "Dashboard" },
  { path: "/quests", label: "Quests" },
  { path: "/profile", label: "Profile" },
  { path: "/settings", label: "Settings" }
];

function Sidebar() {
  return (
    <aside className="sidebar" aria-label="Sidebar">
      <nav aria-label="Primary">
        <ul className="sidebar__list">
          {SIDEBAR_LINKS.map(({ path, label }) => (
            <li className="sidebar__item" key={path}>
              <NavLink
                to={path}
                className={({ isActive }) =>
                  `sidebar__link${isActive ? " sidebar__link--active" : ""}`
                }
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
}

export default Sidebar;
