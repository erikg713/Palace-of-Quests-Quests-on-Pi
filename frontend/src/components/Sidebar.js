import React from "react";
import { Link } from "react-router-dom";
import "./Sidebar.css";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <ul>
        <li><Link to="/quests">Quests</Link></li>
        <li><Link to="/inventory">Inventory</Link></li>
        <li><Link to="/achievements">Achievements</Link></li>
        <li><Link to="/profile">Profile</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;
