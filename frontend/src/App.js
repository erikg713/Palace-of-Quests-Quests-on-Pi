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
