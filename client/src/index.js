import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import store from './store'; // Adjust the path as necessary
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Provider store={store}>
    <App />
  </Provider>
);

import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux"; // Redux Provider
import store from "./store"; // Redux store
import App from "./App"; // Root App component
import "./styles/globals.css"; // Global styles (optional)

// Initialize the React application and wrap it with the Redux provider
const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
    <React.StrictMode>
        <Provider store={store}>
            <App />
        </Provider>
    </React.StrictMode>
);
