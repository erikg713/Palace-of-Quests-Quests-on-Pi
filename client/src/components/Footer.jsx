import React from 'react';
import './Footer.css'; // Assumes a CSS file for styling

const Footer = () => {
  return (
    <footer className="footer">
      <p>&copy; {new Date().getFullYear()} Palace of Quests. All rights reserved.</p>
      <nav>
        <ul>
          <li>
            <a href="/terms" target="_blank" rel="noopener noreferrer">
              Terms of Service
            </a>
          </li>
          <li>
            <a href="/privacy" target="_blank" rel="noopener noreferrer">
              Privacy Policy
            </a>
          </li>
        </ul>
      </nav>
    </footer>
  );
};

export default Footer;
