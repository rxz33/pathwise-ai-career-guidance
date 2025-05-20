// src/pages/Landing.jsx
import React from "react";
import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <div className="min-h-screen bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-6">Welcome to PathWise</h1>
        <p className="text-lg mb-6">AI-powered Career Guidance</p>
        <Link to="/signup" className="bg-white text-gray-800 py-2 px-6 rounded-lg shadow-lg">
          Get Started
        </Link>
      </div>
    </div>
  );
};

export default Landing;
