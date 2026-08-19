// src/App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Flowbite } from "flowbite-react";
import Home from "./pages/Home";
import Agent from "./pages/Agent";
import "/public/assets/css/particles.css"; 



export default function App(){
  return (
    <Flowbite>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/agent" element={<Agent />} />
        </Routes>
      </Router>
    </Flowbite>
  );
}
