import React, { Suspense } from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import store from "store";
import ErrorBoundary from "components/ErrorBoundary";
import "styles/globals.css";

const App = React.lazy(() => import("App"));

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <Provider store={store}>
        <Suspense fallback={<div>Loading...</div>}>
          <App />
        </Suspense>
      </Provider>
    </ErrorBoundary>
  </React.StrictMode>
);

// For debugging in development only
if (process.env.NODE_ENV === "development") {
  store.subscribe(() => {
    console.debug("Redux state:", store.getState());
  });
}
