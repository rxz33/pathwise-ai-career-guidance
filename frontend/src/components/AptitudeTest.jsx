import React, { useState, useEffect } from "react";
import { toast } from "react-hot-toast";

const questions = [
  {
    type: "Logical",
    text: "If all cats are animals and some animals are dogs, are all cats dogs?",
    options: [
      { label: "Yes", score: 0 },
      { label: "No", score: 5 },
      { label: "Maybe", score: 2 },
      { label: "Cannot say", score: 1 },
    ],
  },
  {
    type: "Numerical",
    text: "What is 25% of 200?",
    options: [
      { label: "25", score: 0 },
      { label: "50", score: 5 },
      { label: "100", score: 0 },
      { label: "75", score: 2 },
    ],
  },
  {
    type: "Verbal",
    text: "Choose the word most similar to 'Happy':",
    options: [
      { label: "Joyful", score: 5 },
      { label: "Sad", score: 0 },
      { label: "Angry", score: 0 },
      { label: "Tired", score: 1 },
    ],
  },
  {
    type: "Logical",
    text: "Which number comes next: 2, 4, 8, 16, ?",
    options: [
      { label: "20", score: 0 },
      { label: "32", score: 5 },
      { label: "24", score: 1 },
      { label: "30", score: 0 },
    ],
  },
  {
    type: "Numerical",
    text: "If a train travels 60 km in 1.5 hours, what is its speed?",
    options: [
      { label: "30 km/h", score: 0 },
      { label: "40 km/h", score: 5 },
      { label: "45 km/h", score: 0 },
      { label: "50 km/h", score: 2 },
    ],
  },
];

const categorizeScore = (avg) => {
  if (avg >= 4) return "High";
  if (avg >= 2.5) return "Medium";
  return "Low";
};

const AptitudeTest = ({ email: propEmail, onComplete, onSkip }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [finished, setFinished] = useState(false);
  const [summary, setSummary] = useState(null);
  const [email, setEmail] = useState(propEmail || "");

  useEffect(() => {
    if (!propEmail) {
      const storedEmail = localStorage.getItem("userEmail");
      if (storedEmail) setEmail(storedEmail);
    }
  }, [propEmail]);

  const handleAnswer = (score) => {
    const q = questions[currentIndex];
    const newAnswers = { ...answers, [currentIndex]: { type: q.type, score } };
    setAnswers(newAnswers);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      calculateSummary(newAnswers);
    }
  };

  const handleSkip = () => {
    const q = questions[currentIndex];
    const newAnswers = { ...answers, [currentIndex]: { type: q.type, score: null } };
    setAnswers(newAnswers);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      calculateSummary(newAnswers);
    }
  };

  const calculateSummary = async (allAnswers) => {
    if (!email) {
      toast.error("User email not found!");
      return;
    }

    const scores = {};
    const counts = {};

    Object.values(allAnswers).forEach(({ type, score }) => {
      if (score !== null) {
        if (!scores[type]) scores[type] = 0;
        if (!counts[type]) counts[type] = 0;
        scores[type] += score;
        counts[type] += 1;
      }
    });

    const summaryData = Object.entries(scores).map(([type, total]) => {
      const avg = total / counts[type];
      const level = categorizeScore(avg);
      return { type, avg: parseFloat(avg.toFixed(2)), level };
    });

    setSummary(summaryData);
    setFinished(true);

    const payload = {
      email,
      test: "aptitude",
      scores: summaryData.reduce((acc, r) => {
        acc[r.type] = { avg: r.avg, level: r.level };
        return acc;
      }, {}),
    };

    console.log("Payload sending:", payload);

    try {
      const res = await fetch("http://localhost:8000/apti", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to save Aptitude results");

      toast.success("Aptitude Test results saved!");
    } catch (err) {
      console.error(err);
      toast.error("Error saving Aptitude results");
    }

    if (onComplete) {
      onComplete({
        test: "aptitude",
        responses: allAnswers,
        scores: payload.scores,
      });
    }
  };

  const currentQuestion = questions[currentIndex];

  if (finished) {
    return (
      <div className="max-w-xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-4">
        <h1 className="text-2xl font-bold text-center mb-6">Aptitude Test Summary</h1>
        <div className="space-y-3">
          {summary.map((r, idx) => (
            <div key={idx} className="p-3 border-l-4 border-indigo-500 bg-indigo-50 rounded">
              <p>
                <span className="font-bold">{r.type}:</span> {r.avg} ({r.level})
              </p>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-6">
      <h1 className="text-3xl font-bold text-center mb-6">Aptitude Test</h1>
      <h2 className="text-xl font-semibold">{currentQuestion.text}</h2>

      <div className="flex flex-col space-y-3">
        {currentQuestion.options.map((opt, idx) => (
          <button
            key={idx}
            onClick={() => handleAnswer(opt.score)}
            className="p-3 bg-yellow-50 border border-yellow-200 rounded hover:bg-yellow-100 text-left"
          >
            {opt.label}
          </button>
        ))}
        <button
          onClick={handleSkip}
          className="p-2 mt-4 bg-gray-100 border rounded hover:bg-gray-200"
        >
          Skip
        </button>
      </div>
    </div>
  );
};

export default AptitudeTest;
