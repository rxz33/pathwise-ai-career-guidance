import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const LoadingPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const email = localStorage.getItem("userEmail"); // ✅ Fetch from localStorage

    const fetchCrossExam = async () => {
      try {
        const res = await fetch("http://localhost:8000/cross-examination", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        });

        if (!res.ok) throw new Error("Error generating cross exam");

        const data = await res.json();
        console.log("✅ Received cross-exam data:", data);

        localStorage.setItem("crossExamQs", JSON.stringify(data));
        navigate("/cross-exam");
      } catch (error) {
        console.error("❌ Error loading cross-exam:", error);
      }
    };

    if (email) {
      fetchCrossExam();
    } else {
      console.error("❌ Email not found in localStorage.");
    }
  }, [navigate]);

  return (
    <div className="min-h-screen flex justify-center items-center text-lg font-medium">
      Loading your personalized questions...
    </div>
  );
};

export default LoadingPage;
