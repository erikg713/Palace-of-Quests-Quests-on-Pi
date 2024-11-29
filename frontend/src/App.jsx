import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";

const App = () => {
  const userToken = "your-auth-token"; // Replace with actual JWT logic

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard userToken={userToken} />} />
      </Routes>
    </Router>
  );
};

export default App;
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Marketplace from './pages/Marketplace';
import Profile from './pages/Profile';
import MobileNav from './components/MobileNav';

function App() {
  return (
    <Router>
      <div className="container">
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/marketplace" component={Marketplace} />
          <Route path="/profile" component={Profile} />
        </Switch>
        <MobileNav /> {/* Persistent bottom navigation for mobile */}
      </div>
    </Router>
  );
}

export default App;
