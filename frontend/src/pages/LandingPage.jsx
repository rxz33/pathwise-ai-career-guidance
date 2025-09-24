// // src/pages/Landing.jsx
// import React from "react";
// import { Link } from "react-router-dom";

// const Landing = () => {
//   return (
//     <div className="min-h-screen bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white flex items-center justify-center">
//       <div className="text-center">
//         <h1 className="text-4xl font-bold mb-6">Welcome to PathWise</h1>
//         <p className="text-lg mb-6">AI-powered Career Guidance</p>
//         <Link to="/signup" className="bg-white text-gray-800 py-2 px-6 rounded-lg shadow-lg">
//           Get Started
//         </Link>
//       </div>
//     </div>
//   );
// };



// export default Landing;

// src/pages/Landing.jsx
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { ChevronDown, ChevronUp, Mail, Target, TrendingUp, UserCheck } from "lucide-react";

const Landing = () => {
  const [expandedFaq, setExpandedFaq] = useState(null);
  const [email, setEmail] = useState("");

  const faqs = [
    {
      question: "How does PathWise help me choose a career path?",
      answer: "We use advanced assessments and AI-driven insights to match your skills, interests, and goals with suitable career paths.",
    },
    {
      question: "Is PathWise free?",
      answer: "Yes! Basic guidance is free. Premium personalized coaching is optional for deeper insights.",
    },
    {
      question: "How often is career data updated?",
      answer: "We update career insights monthly to reflect the latest market trends and opportunities.",
    },
    {
      question: "Can I use PathWise if I'm already employed?",
      answer: "Absolutely! Our platform supports career growth, skill upgrades, and industry switches for working professionals.",
    },
  ];

  const toggleFaq = (index) => {
    setExpandedFaq(expandedFaq === index ? null : index);
  };

  const handleNewsletterSubmit = (e) => {
    e.preventDefault();
    alert(`Thank you for subscribing with ${email}!`);
    setEmail("");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 text-white py-28 text-center">
        <h1 className="text-5xl font-extrabold mb-6 drop-shadow-lg">
          Find Your Perfect <span className="text-yellow-300">Career Path</span>
        </h1>
        <p className="mb-8 max-w-xl mx-auto text-lg drop-shadow-md">
          Discover careers tailored to your skills, interests, and aspirations with AI-powered guidance.
        </p>
        <Link
          to="/signup"
          className="inline-block bg-yellow-300 text-gray-900 font-semibold px-8 py-3 rounded-lg shadow-lg hover:bg-yellow-400 transition"
        >
          Get Started
        </Link>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 grid gap-8 md:grid-cols-3 text-center">
          <div className="p-8 bg-white rounded-xl shadow-lg hover:shadow-2xl transition">
            <div className="mb-4 flex items-center justify-center h-16 w-16 mx-auto rounded-full bg-indigo-100">
              <Target className="h-6 w-6 text-indigo-600" />
            </div>
            <h3 className="font-bold text-lg mb-2">Career Assessment</h3>
            <p className="text-gray-600">Identify your strengths, interests, and values with AI-powered assessments.</p>
          </div>

          <div className="p-8 bg-white rounded-xl shadow-lg hover:shadow-2xl transition">
            <div className="mb-4 flex items-center justify-center h-16 w-16 mx-auto rounded-full bg-indigo-100">
              <TrendingUp className="h-6 w-6 text-indigo-600" />
            </div>
            <h3 className="font-bold text-lg mb-2">Explore Paths</h3>
            <p className="text-gray-600">Access hundreds of career options with insights on growth and opportunities.</p>
          </div>

          <div className="p-8 bg-white rounded-xl shadow-lg hover:shadow-2xl transition">
            <div className="mb-4 flex items-center justify-center h-16 w-16 mx-auto rounded-full bg-indigo-100">
              <UserCheck className="h-6 w-6 text-indigo-600" />
            </div>
            <h3 className="font-bold text-lg mb-2">Personalized Plan</h3>
            <p className="text-gray-600">Receive a roadmap with actionable steps to reach your career goals.</p>
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-20 bg-indigo-50 text-center">
        <div className="max-w-xl mx-auto px-4">
          <Mail className="mx-auto mb-4 h-12 w-12 text-indigo-600" />
          <h2 className="text-2xl font-bold mb-4">Get Career Insights</h2>
          <p className="mb-8 text-gray-600">Subscribe to receive tips, trends, and exclusive resources.</p>
          <form onSubmit={handleNewsletterSubmit} className="flex flex-col sm:flex-row gap-4 justify-center">
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="flex-1 px-4 py-2 rounded-lg border focus:outline-none focus:ring-2 focus:ring-indigo-300"
              required
            />
            <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition">
              Subscribe
            </button>
          </form>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20">
        <div className="max-w-3xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>
          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <div key={index} className="border rounded-xl shadow hover:shadow-lg transition">
                <div
                  className="flex justify-between items-center p-4 cursor-pointer bg-white rounded-t-xl"
                  onClick={() => toggleFaq(index)}
                >
                  <h3 className="font-semibold">{faq.question}</h3>
                  {expandedFaq === index ? <ChevronUp /> : <ChevronDown />}
                </div>
                {expandedFaq === index && (
                  <div className="p-4 bg-gray-50 rounded-b-xl text-gray-600">{faq.answer}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-100 py-12 text-center text-gray-600">
        © 2025 PathWise. All rights reserved.
      </footer>
    </div>
  );
};

export default Landing;


