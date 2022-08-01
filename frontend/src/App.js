import React from "react";
import logo from './logo.svg';
import './css/App.css';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from './pages/Home';
import Upload from './pages/Upload';
import Sessions from './pages/Sessions';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Home />}/>
          <Route path ="/upload" element={<Upload />}/>
          <Route path ="/sessions" element={<Sessions />}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
