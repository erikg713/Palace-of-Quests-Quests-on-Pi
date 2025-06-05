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
  }, [title]);

  return (
    <main className="home" role="main" aria-label="Home Page">
      <section>
        <h1 tabIndex={0} className="home__title">
          {title}
        </h1>
        <p tabIndex={0} className="home__subtitle">
          {subtitle}
        </p>
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
