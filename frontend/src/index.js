import React from "react";
import ReactDOM from "react-dom";
import PalaceOfQuests from "./App";

ReactDOM.render(
  <React.StrictMode>
    <PalaceOfQuests />
  </React.StrictMode>,
  document.getElementById("root")
);

import React from 'react';
import ReactDOM from 'react-dom';
import './assets/styles/styles.css';
import App from './App';

ReactDOM.render(<App />, document.getElementById('root'));
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './styles/global.css';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
