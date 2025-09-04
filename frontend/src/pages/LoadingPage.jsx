import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";

const LoadingPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const email = localStorage.getItem("userEmail"); // ✅ Fetch from localStorage
    const userFormData = localStorage.getItem("user_form_data");

    if (!email || !userFormData) {
      toast.error("Missing user data. Please restart the process.");
      navigate("/");
      return;
    }

    const initialAnswers = []; // Can prefill or keep empty initially

    const fetchCrossExam = async () => {
      try {
        const res = await fetch("http://localhost:8000/submit-answers", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, answers: initialAnswers }),
        });

        if (!res.ok) throw new Error("Error generating cross exam");

        const data = await res.json();
        console.log("✅ Received cross-exam data:", data);

        localStorage.setItem("crossExamQs", JSON.stringify(data.followupQuestions));
        navigate("/cross-exam");
      } catch (error) {
        console.error("❌ Error loading cross-exam:", error);
        toast.error("Failed to generate cross-exam questions.");
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
