import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const [email, setEmail] = useState("");
  const [isSignedUp, setIsSignedUp] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
  e.preventDefault();
  console.log("User email:", email);

  // ✅ Store email globally
  localStorage.setItem("userEmail", email);

  setIsSignedUp(true);
};

  const goToForm = () => {
    navigate("/form");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-100 via-white to-pink-100 px-4">
      <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-2xl">
        <h2 className="text-3xl font-bold text-center text-indigo-600 mb-6">
          Join PathWise
        </h2>

        {!isSignedUp ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email address
              </label>
              <input
                type="email"
                id="email"
                required
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent transition"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition duration-200 shadow-md"
            >
              Sign Up
            </button>
          </form>
        ) : (
          <div className="text-center">
            <p className="text-green-600 text-lg font-semibold mb-4">
              ✅ Successfully signed up!
            </p>
            <button
              onClick={goToForm}
              className="w-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white py-3 rounded-lg font-semibold hover:from-indigo-600 hover:to-purple-600 transition duration-200 shadow-lg"
            >
              Continue to Career Form →
            </button>
          </div>
        )}

        <p className="mt-6 text-sm text-gray-500 text-center">
          Already have an account?{" "}
          <span className="text-indigo-600 font-medium cursor-pointer hover:underline">
            Log in
          </span>
        </p>
      </div>
    </div>
  );
};

export default Signup;
