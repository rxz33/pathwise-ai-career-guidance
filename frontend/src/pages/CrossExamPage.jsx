import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";

const CrossExamPage = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [analysis, setAnalysis] = useState([]);
  const [loading, setLoading] = useState(false);
  const [round, setRound] = useState(
    Number(localStorage.getItem("crossExamRound") || 1)
  );
  const maxRounds = 2;
  const email = localStorage.getItem("user_email");

  useEffect(() => {
    const savedQs = localStorage.getItem("crossExamQs");
    if (!savedQs) {
      toast.error("No questions found. Redirecting...");
      navigate("/loading");
      return;
    }
    const parsedQs = JSON.parse(savedQs);
    setQuestions(parsedQs);
    setAnswers(new Array(parsedQs.length).fill(""));
  }, [navigate]);

  const handleChange = (index, value) => {
    const updated = [...answers];
    updated[index] = value;
    setAnswers(updated);
  };

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
        body: JSON.stringify({ email, answers, round_number: round }),
      });

      if (!res.ok) throw new Error("Server error");
      const data = await res.json();

      // Append incremental AI analysis
      if (data.analysis) setAnalysis((prev) => [...prev, data.analysis]);

      if (data.followupQuestions?.length > 0 && round < maxRounds) {
        // Save and display next round
        localStorage.setItem("crossExamQs", JSON.stringify(data.followupQuestions));
        setQuestions(data.followupQuestions);
        setAnswers(new Array(data.followupQuestions.length).fill(""));
        setRound(round + 1);
        localStorage.setItem("crossExamRound", round + 1);
        toast.success("Next set of questions loaded!");
      } else {
        // All rounds complete, save final analysis
        localStorage.setItem("evaluation", JSON.stringify(analysis.concat(data.analysis || [])));
        toast.success("Evaluation complete!");
        navigate("/career-result");
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
      <h1 className="text-3xl font-bold mb-6 text-center">Cross-Examination Questions</h1>

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

      {analysis.length > 0 && (
        <div className="mt-10 p-5 bg-gray-100 border border-gray-300 rounded-lg">
          <h2 className="text-xl font-semibold mb-3 text-gray-800">AI Analysis So Far</h2>
          {analysis.map((a, idx) => (
            <pre key={idx} className="text-gray-700 whitespace-pre-wrap">{a}</pre>
          ))}
        </div>
      )}
    </div>
  );
};

export default CrossExamPage;
