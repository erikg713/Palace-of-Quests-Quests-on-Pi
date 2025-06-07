import React, { useEffect } from "react";
import PropTypes from "prop-types";

/**
 * Home Page – Palace of Quests
 * --------------------------------------------
 * The main landing page for the Palace of Quests metaverse game.
 * Welcomes users and introduces the platform.
 *
 * @component
 */
const Home = ({ title, subtitle }) => {
  // Set the document title dynamically for SEO
  useEffect(() => {
    document.title = title ? `${title} | Palace of Quests` : "Palace of Quests";
    
    // Analytics tracking for page view (if applicable)
    if (window.analytics) {
      window.analytics.pageView("Home");
    }
    
    return () => {
      // Cleanup any listeners or side effects if needed
    };
  }, [title]);

  return (
    <main className="home" role="main" aria-label="Home Page">
      <section className="home__hero">
        <h1 tabIndex={0} className="home__title">
          {title}
        </h1>
        <p tabIndex={0} className="home__subtitle">
          {subtitle}
        </p>
        <div className="home__cta-container">
          <button 
            className="home__cta-button primary"
            onClick={() => window.location.href = '/quests'}
          >
            Explore Quests
          </button>
        </div>
      </section>
    </main>
  );
};

Home.propTypes = {
  title: PropTypes.string,
  subtitle: PropTypes.string,
};

Home.defaultProps = {
  title: "Welcome to Palace of Quests",
  subtitle: "Embark on your journey in the metaverse.",
};

export default Home;
