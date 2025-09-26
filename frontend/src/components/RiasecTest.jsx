import React, { useState, useEffect } from "react";
import { toast } from "react-hot-toast";

const questions = [
  { type: "Realistic", text: "I enjoy working with tools, machines, or computers." },
  { type: "Investigative", text: "I like researching and analyzing information." },
  { type: "Artistic", text: "I enjoy creative activities like painting or writing." },
  { type: "Social", text: "I like helping others with practical tasks." },
  { type: "Enterprising", text: "I enjoy leading and persuading people." },
  { type: "Conventional", text: "I like organizing data and keeping things in order." },
];

const RiasecTest = ({ onComplete, onSkip }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [scores, setScores] = useState({});
  const [summary, setSummary] = useState("");
  const [finished, setFinished] = useState(false);

  const options = [
    { label: "Disagree", value: 1 },
    { label: "Slightly disagree", value: 2 },
    { label: "Neutral", value: 3 },
    { label: "Slightly agree", value: 4 },
    { label: "Agree", value: 5 },
  ];

  const handleAnswer = (value) => {
    const q = questions[currentIndex];
    const newAnswers = { ...answers, [currentIndex]: { type: q.type, score: value } };
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

  const calculateSummary = (allAnswers) => {
    const tempScores = {};
    const counts = {};

    Object.values(allAnswers).forEach(({ type, score }) => {
      if (score !== null) {
        if (!tempScores[type]) tempScores[type] = 0;
        if (!counts[type]) counts[type] = 0;
        tempScores[type] += score;
        counts[type] += 1;
      }
    });

    const avgScores = {};
    Object.entries(tempScores).forEach(([type, total]) => {
      avgScores[type] = parseFloat((total / counts[type]).toFixed(2));
    });

    setScores(avgScores);

    const summaryText = Object.entries(avgScores)
      .map(([type, avg]) => `${type}: ${avg}`)
      .join("\n");
    setSummary(summaryText);

    if (onComplete) {
      onComplete({
        test: "riasec",
        responses: allAnswers,
        scores: avgScores
      });
    }

    setFinished(true);
    toast.success("RIASEC Test complete!");
  };

  const sendRiasecResult = async (scores) => {
    const email = localStorage.getItem("userEmail");
    if (!email) return toast.error("Email not found");

    const payload = { email, test: "riasec", scores };

    try {
      const res = await fetch("https://pathwise-ai-career-guidance-pgtg.onrender.com", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Submission failed");
      toast.success("RIASEC test result sent!");
    } catch (err) {
      console.error(err);
      toast.error("Failed to send RIASEC test result.");
    }
  };

  useEffect(() => {
    if (finished) {
      sendRiasecResult(scores);
    }
  }, [finished]);

  const currentQuestion = questions[currentIndex];

  if (finished) {
    return (
      <div className="max-w-xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-4">
        <div className="space-y-3">
          {summary.split("\n").map((line, idx) => {
            const [type, avg] = line.split(": ");
            return (
              <div key={idx} className="p-3 border-l-4 border-indigo-500 bg-indigo-50 rounded">
                <p><span className="font-bold">{type}:</span> {avg}</p>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto bg-white p-6 rounded-xl shadow-md space-y-6">
      <h1 className="text-3xl font-bold text-center mb-4">RIASEC Career Test</h1>
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
        <button onClick={handleSkip} className="underline hover:text-gray-700">Skip</button>
        <span>{currentIndex + 1} / {questions.length}</span>
        <button
          onClick={onSkip}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
        >
          Skip the Test
        </button>
      </div>
    </div>
  );
};

export default RiasecTest;
