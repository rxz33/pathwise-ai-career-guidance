import React, { useState, useEffect } from "react";
import { toast } from "react-hot-toast";
import { fetchFromAPI } from "../api";

const questions = [
  { trait: "extraversion", text: "I am the life of the party." },
  { trait: "extraversion", text: "I feel comfortable around people." },
  { trait: "openness", text: "I enjoy trying new things." },
  { trait: "agreeableness", text: "I am considerate of others." },
  { trait: "conscientiousness", text: "I follow a schedule." },
  { trait: "neuroticism", text: "I often feel anxious or stressed." },
  // Add all 25+ questions here...
];

const traitExplanations = {
  extraversion: {
    low: "You tend to be reserved and enjoy solitude.",
    medium: "You balance social interaction and alone time.",
    high: "You are outgoing and energized by social situations."
  },
  agreeableness: {
    low: "You are more competitive and question others’ intentions.",
    medium: "You are cooperative yet assertive when needed.",
    high: "You are considerate and value harmony with others."
  },
  conscientiousness: {
    low: "You may struggle with organization and planning.",
    medium: "You are reasonably organized and responsible.",
    high: "You are very organized, reliable, and goal-oriented."
  },
  neuroticism: {
    low: "You are emotionally stable and handle stress well.",
    medium: "You experience occasional stress but manage it.",
    high: "You may feel anxious or stressed easily."
  },
  openness: {
    low: "You prefer routine and familiar experiences.",
    medium: "You are open to new experiences sometimes.",
    high: "You enjoy exploring new ideas, creativity, and novelty."
  }
};

const BigFiveTest = ({ onComplete, onSkip }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [finished, setFinished] = useState(false);
  const [result, setResult] = useState(null);

  const options = [
    { label: "Disagree", value: 1 },
    { label: "Slightly disagree", value: 2 },
    { label: "Neutral", value: 3 },
    { label: "Slightly agree", value: 4 },
    { label: "Agree", value: 5 },
  ];

  const handleAnswer = (value) => {
    const q = questions[currentIndex];
    const newAnswers = { ...answers, [currentIndex]: { trait: q.trait, score: value } };
    setAnswers(newAnswers);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      toast.success("Test complete!");
      calculateResult(newAnswers);
    }
  };

  const handleSkip = () => {
    const q = questions[currentIndex];
    const newAnswers = { ...answers, [currentIndex]: { trait: q.trait, score: null } }; // skipped = null
    setAnswers(newAnswers);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      toast.success("Test complete!");
      calculateResult(newAnswers);
    }
  };

  const sendBigFiveResult = async (summaryData) => {
  const email = localStorage.getItem("userEmail");
  if (!email) return toast.error("Email not found");

  const payload = {
    email,
    test: "big_five",
    scores: summaryData.reduce((acc, r) => {
      acc[r.trait] = r.avg;
      return acc;
    }, {})
  };

  try {
    const res = await fetch(`${API_BASE_URL}/big-five`, {  // <- use correct endpoint
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Submission failed");
    toast.success("Big Five test result sent!");
  } catch (err) {
    console.error(err);
    toast.error("Failed to send test result.");
  }
};

  const calculateResult = (allAnswers) => {
    const scores = {};
    const counts = {};

    Object.values(allAnswers).forEach(({ trait, score }) => {
      if (score !== null) { // ignore skipped
        if (!scores[trait]) scores[trait] = 0;
        if (!counts[trait]) counts[trait] = 0;
        scores[trait] += score;
        counts[trait] += 1;
      }
    });

    const summary = Object.entries(scores).map(([trait, total]) => {
      const avg = total / counts[trait];
      let level = "medium";
      if (avg <= 2.4) level = "low";
      else if (avg >= 3.7) level = "high";

      return {
        trait: trait.charAt(0).toUpperCase() + trait.slice(1),
        avg: avg.toFixed(2),
        explanation: traitExplanations[trait][level]
      };
    });

    setResult(summary);
    setFinished(true);

    if (onComplete) {
      onComplete({
        test: "big_five",
        responses: allAnswers,
        scores: summary.reduce((acc, r) => {
          acc[r.trait] = r.avg;
          return acc;
        }, {})
      });
    }
  };

  const currentQuestion = questions[currentIndex];

useEffect(() => {
  if (result) {
    sendBigFiveResult(result);
  }
}, [result]);

 
  if (finished) {
    return (
      <div className="max-w-xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-4">
        <div className="space-y-3">
          {result.map((r, idx) => (
            <div key={idx} className="p-3 border-l-4 border-indigo-500 bg-indigo-50 rounded">
              <p><span className="font-bold">{r.trait}:</span> {r.avg}</p>
              <p className="text-gray-700 text-sm">{r.explanation}</p>
            </div>
          ))}
        </div>

        {/* <div className="mt-6 text-center">
          <button
            onClick={() => navigate("/riasec-test")}
            className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition"
          >
            Next: RIASEC Test
          </button>
        </div> */}
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-6">
      <h1 className="text-2xl font-bold text-center mb-4">Big Five Personality Test</h1>
      <h2 className="text-xl font-semibold">{currentQuestion.text}</h2>

      <div className="flex flex-col space-y-3">
        {options.map((opt) => (
          <button
            key={opt.value}
            onClick={() => handleAnswer(opt.value)}
            className="p-3 bg-yellow-50 border border-yellow-200 rounded hover:bg-yellow-100 text-left"
          >
            {opt.label}
          </button>
        ))}
      </div>

      <div className="flex justify-between items-center text-sm text-gray-500 mt-4">
        <button onClick={handleSkip} className="underline hover:text-gray-700">
          Skip
        </button>
        <span>{currentIndex + 1} / {questions.length}</span>

        <button
          onClick={onSkip} // skip entire test
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
        >
          Skip the Test
        </button>
      </div>
    </div>
  );
};

export default BigFiveTest; 
