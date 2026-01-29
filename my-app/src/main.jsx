/**
 * Application Entry Point
 * Initializes React application and renders root component.
 */

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

// Create React root and render application
ReactDOM.createRoot(document.getElementById("root")).render(
  // React.StrictMode helps identify potential problems
  <React.StrictMode>
    <App />  {/* Root application component */}
  </React.StrictMode>
);