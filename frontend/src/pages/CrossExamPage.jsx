// export default CrossExamPage;
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import { fetchFromAPI } from "../api";

const CrossExamPage = ({ email: propEmail }) => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const email = propEmail || localStorage.getItem("userEmail");

  // Fetch questions
  useEffect(() => {
    if (!email) {
      setError("User email not found. Please start again.");
      setLoading(false);
      return;
    }

    const fetchQuestions = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await fetchFromAPI("generate-questions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        });

        if (data?.questions?.length > 0) {
          setQuestions(data.questions);
          setAnswers(Array(data.questions.length).fill(""));
        } else {
          setError("No questions available at this time.");
        }
      } catch (err) {
        console.error("Error fetching questions:", err);
        setError("Failed to fetch questions. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [email]);

  const handleAnswerChange = (index, value) => {
    const updated = [...answers];
    updated[index] = value;
    setAnswers(updated);
  };

  const handleSubmit = async () => {
    if (answers.some((a) => a.trim() === "")) {
      toast.error("Please answer all questions before submitting.");
      return;
    }

    try {
      setLoading(true);
      await fetchFromAPI("submit-answers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, answers }),
      });

      toast.success("Answers submitted successfully!");
      navigate("/career-result", { state: { email } }); // navigate to results
    } catch (err) {
      console.error(err);
      toast.error("Failed to submit answers. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // if (loading)
  //   return (
  //     <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 px-4">
  //       <div className="text-indigo-600 text-lg font-medium mb-4">
  //         Loading your personalized questions...
  //       </div>
  //       <div className="w-64 h-2 bg-gray-300 rounded-full overflow-hidden">
  //         <div className="h-2 bg-indigo-500 animate-pulse w-full"></div>
  //       </div>
  //     </div>
  //   );

  if (error)
    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-4">
        <p className="text-red-500 font-semibold text-lg mb-4">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition"
        >
          Retry
        </button>
      </div>
    );

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 flex flex-col items-center py-10 px-4">
      <div className="w-full max-w-2xl bg-white shadow-lg rounded-2xl p-8 space-y-6">
        <h2 className="text-2xl font-bold text-center text-indigo-700 mb-6">
          Quick Verification Questions
        </h2>

        {questions.map((q, i) => (
          <div key={i} className="flex flex-col space-y-2">
            <label className="font-medium text-gray-700">{q}</label>
            <input
              type="text"
              value={answers[i]}
              onChange={(e) => handleAnswerChange(i, e.target.value)}
              className="border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-indigo-400 focus:outline-none transition shadow-sm"
              placeholder="Your answer..."
            />
          </div>
        ))}

        <button
          onClick={handleSubmit}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl transition shadow-lg mt-4"
        >
          Submit Answers
        </button>
      </div>
    </div>
  );
};

export default CrossExamPage; 