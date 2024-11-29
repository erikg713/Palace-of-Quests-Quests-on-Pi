import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

const HomeContainer = styled.div`
  text-align: center;
  padding: 50px;
`;

const Home = () => {
  return (
    <HomeContainer>
      <h1>Welcome to Palace of Quests</h1>
      <p>Embark on an adventure from Level 1 to 250!</p>
      <Link to="/dashboard">Start Your Quest</Link>
    </HomeContainer>
  );
};

export default Home;
import React from 'react';

const Home = () => {
  return (
    <div>
      <h1>Welcome to PiQuest</h1>
      <p>Start your adventure and earn Pi by completing quests!</p>
    </div>
  );
};

export default Home;
