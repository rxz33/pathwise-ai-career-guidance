import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";

const CrossExamPage = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [analysis, setAnalysis] = useState(""); // ✅ NEW: store AI analysis
  const [loading, setLoading] = useState(false);
  const email = localStorage.getItem("user_email") || "";

  // ✅ Fetch questions on mount
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        if (!email) {
          toast.error("Missing user email.");
          navigate("/");
          return;
        }

        // Check localStorage first
        let savedQs = localStorage.getItem("crossExamQs");
        if (savedQs) {
          const parsedQs = JSON.parse(savedQs);
          setQuestions(parsedQs);
          setAnswers(new Array(parsedQs.length).fill(""));
          return;
        }

        // Fetch from backend
        const res = await fetch("http://localhost:8000/generate-questions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        });

        if (!res.ok) throw new Error("Failed to generate questions");
        const data = await res.json();

        if (!data.questions || data.questions.length === 0) {
          toast.error("No questions generated.");
          return;
        }

        localStorage.setItem("crossExamQs", JSON.stringify(data.questions));
        setQuestions(data.questions);
        setAnswers(new Array(data.questions.length).fill(""));
      } catch (err) {
        console.error(err);
        toast.error("Error generating questions. Please try again.");
      }
    };

    fetchQuestions();
  }, [email, navigate]);

  // ✅ Handle input change
  const handleChange = (index, value) => {
    const updated = [...answers];
    updated[index] = value;
    setAnswers(updated);
  };

  // ✅ Submit answers
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (answers.some((a) => !a.trim())) {
      toast.error("Please answer all questions.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/submit-answers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, answers }),
      });

      if (!res.ok) throw new Error("Server error");

      const data = await res.json();

      if (data.followupQuestions?.length > 0) {
        // Save and show follow-up questions
        localStorage.setItem(
          "crossExamQs",
          JSON.stringify(data.followupQuestions)
        );
        setQuestions(data.followupQuestions);
        setAnswers(new Array(data.followupQuestions.length).fill(""));
        setAnalysis(data.analysis || ""); // show partial analysis too
        toast.success("Next set of questions loaded!");
      } else if (data.analysis) {
        // Save final analysis
        localStorage.setItem("evaluation", data.analysis);
        setAnalysis(data.analysis);
        toast.success("Evaluation complete!");
        // Optionally navigate to results
        navigate("/career-result");
      } else {
        toast.error("Unexpected response from server.");
      }
    } catch (err) {
      console.error(err);
      toast.error("Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Cross-Examination Questions
      </h1>

      {questions.length > 0 ? (
        <form onSubmit={handleSubmit} className="space-y-6">
          {questions.map((q, i) => (
            <div key={i}>
              <p className="font-medium text-gray-800">
                {i + 1}. {q}
              </p>
              <textarea
                className="w-full mt-2 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
                value={answers[i]}
                onChange={(e) => handleChange(i, e.target.value)}
                placeholder="Type your answer here..."
              />
            </div>
          ))}

          <button
            type="submit"
            disabled={loading}
            className={`mt-6 w-full bg-blue-600 text-white py-3 rounded-lg font-semibold transition duration-300 hover:bg-blue-700 ${
              loading ? "opacity-70 cursor-not-allowed" : ""
            }`}
          >
            {loading ? "Submitting..." : "Submit Answers"}
          </button>
        </form>
      ) : (
        <p className="text-center text-gray-500">Loading questions...</p>
      )}

      {/* ✅ Show AI analysis if available */}
      {analysis && (
        <div className="mt-10 p-5 bg-gray-100 border border-gray-300 rounded-lg">
          <h2 className="text-xl font-semibold mb-3 text-gray-800">
            AI Analysis
          </h2>
          <p className="text-gray-700 whitespace-pre-line">{analysis}</p>
        </div>
      )}
    </div>
  );
};

export default CrossExamPage;
