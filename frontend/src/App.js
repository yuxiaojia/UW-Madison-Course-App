/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/12/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

import React from "react";
import "./App.css";
import "react-bootstrap-typeahead/css/Typeahead.css";
import "react-bootstrap-typeahead/css/Typeahead.bs5.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./components/Home";
import Course from "./components/Course";
import Instructor from "./components/Instructor";

/**
 * App: stores the router logic of the web application
 * @returns App React element
 */
function App() {
  return (
    // Router enables navigation between different React components
    <Router>
      <Routes>
        {/* Routes to Home component when path is / */}
        <Route exact path="/" element={<Home />} />
        {/* Routes to Course component when path is /course */}
        <Route path="/course/:id" element={<Course />} />
        {/* Routes to Instructor component when path is /instructor */}
        <Route path="/instructor/:id" element={<Instructor />} />
      </Routes>
    </Router>
  );
}

export default App;
