import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";

const LoadingPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const email = localStorage.getItem("user_email");

    if (!email) {
      toast.error("Email not found. Please start again.");
      navigate("/");
      return;
    }

    const fetchCrossExam = async () => {
      try {
        const res = await fetch("http://localhost:8000/generate-questions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }), // ✅ matches backend Pydantic model
        });

        if (!res.ok) throw new Error("Error generating cross exam");

        const data = await res.json();

        // Clear old questions before saving
        localStorage.removeItem("crossExamQs");
        localStorage.setItem("crossExamQs", JSON.stringify(data.questions));

        navigate("/cross-exam");
      } catch (err) {
        console.error(err);
        toast.error("Failed to load questions. Try again.");
        navigate("/");
      }
    };

    fetchCrossExam();
  }, [navigate]);

  return (
    <div className="min-h-screen flex justify-center items-center text-lg font-medium">
      Loading your personalized questions...
    </div>
  );
};

export default LoadingPage;
