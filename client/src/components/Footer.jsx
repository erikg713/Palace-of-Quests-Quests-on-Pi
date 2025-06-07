import React from "react";
import "./Footer.css";

const year = new Date().getFullYear();

function Footer() {
  return (
    <footer className="footer" aria-label="Site Footer">
      <div className="footer__content">
        <p className="footer__copyright">
          &copy; {year} Palace of Quests. All rights reserved.
        </p>
        <nav aria-label="Footer Navigation">
          <ul className="footer__links">
            <li>
              <a
                href="/terms"
                target="_blank"
                rel="noopener noreferrer"
              >
                Terms of Service
              </a>
            </li>
            <li>
              <a
                href="/privacy"
                target="_blank"
                rel="noopener noreferrer"
              >
                Privacy Policy
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </footer>
  );
}

export default Footer;
