import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import { fetchFromAPI } from "../api";

const LoadingPage = () => {
  const navigate = useNavigate();
  const [progressText, setProgressText] = useState("Preparing your personalized questions...");
  const [dotCount, setDotCount] = useState(0);

  useEffect(() => {
    const email = localStorage.getItem("userEmail");
    if (!email) {
      toast.error("Email not found. Please start again.");
      navigate("/");
      return;
    }

    // Animate dots for effect
    const dotInterval = setInterval(() => {
      setDotCount((prev) => (prev + 1) % 4); // cycles 0-3 dots
    }, 500);

    // Poll backend until questions appear
    const fetchQuestions = async () => {
      try {
        const data = await fetchFromAPI("/generate-questions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        });

        if (!data.questions || data.questions.length === 0) {
          toast.error("No questions generated. Please try again.");
          navigate("/");
          return;
        }

        localStorage.setItem("crossExamQs", JSON.stringify(data.questions));
        navigate("/cross-exam");
      } catch (err) {
        console.error(err);
        toast.error("Failed to generate questions. Please try again.");
        navigate("/");
      } finally {
        clearInterval(dotInterval);
      }
    };

    fetchQuestions();

    // Cleanup interval on unmount
    return () => clearInterval(dotInterval);
  }, [navigate]);

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-indigo-50 to-purple-50 px-4">
      <p className="text-lg font-medium text-indigo-700">
        {progressText + ".".repeat(dotCount)}
      </p>
      <div className="mt-6 w-64 h-2 bg-gray-300 rounded-full overflow-hidden">
        <div className="h-2 w-full bg-indigo-500 animate-pulse"></div>
      </div>
    </div>
  );
};

export default LoadingPage;
