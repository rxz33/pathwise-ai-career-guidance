import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import axios from "axios";
import jsPDF from "jspdf";

const stages = [
  "Analyzing your answers...",
  "Analyzing your resume / aptitude assessment...",
  "Detecting skill gaps...",
  "Generating career recommendations...",
  "Compiling final summary..."
];

function CareerResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [loadingStage, setLoadingStage] = useState(0);
  const email = location.state?.email || localStorage.getItem("user_email");

  useEffect(() => {
    if (!email) {
      toast.error("Missing user email.");
      navigate("/");
      return;
    }

    const fetchFinalResult = async () => {
      try {
        // Step-wise simulated loading
        for (let i = 0; i < stages.length; i++) {
          setLoadingStage(i);
          await new Promise((r) => setTimeout(r, 800));
        }

        const response = await axios.get("http://localhost:8000/get-final-analysis", {
          params: { email },
        });

        if (response.data.finalAnalysis) {
          setResult(response.data.finalAnalysis);
        } else {
          throw new Error("No finalAnalysis in response.");
        }
      } catch (err) {
        console.error(err);
        toast.error("Failed to load your final result.");
        navigate("/");
      }
    };

    fetchFinalResult();
  }, [email, navigate]);

  const downloadPDF = () => {
    if (!result) return;
    const doc = new jsPDF({ orientation: "portrait", unit: "pt", format: "a4" });
    const margin = 40;
    const pageWidth = doc.internal.pageSize.getWidth();

    doc.setFontSize(16);
    doc.text("Career Guidance Report", margin, 50);

    let y = 80;
    const addSection = (title, content) => {
      doc.setFontSize(14);
      doc.text(title, margin, y);
      y += 20;
      doc.setFontSize(12);

      if (Array.isArray(content)) {
        content.forEach((item) => {
          const lines = doc.splitTextToSize("• " + item, pageWidth - margin * 2);
          lines.forEach((line) => {
            doc.text(line, margin + 20, y);
            y += 16;
          });
        });
      } else if (content) {
        const lines = doc.splitTextToSize(content, pageWidth - margin * 2);
        lines.forEach((line) => {
          doc.text(line, margin, y);
          y += 16;
        });
      }

      y += 10;
    };

    addSection("Friendly Summary", result.friendly_summary);
    addSection("Strengths", result.strengths);
    addSection("Weaknesses", result.weaknesses);
    addSection("Skill Gaps", result.skill_gaps);
    addSection("Suggestions", result.suggestions);
    addSection("Next Steps", result.next_steps);

    doc.save("career-guidance-report.pdf");
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center p-6">
      {result ? (
        <div className="max-w-4xl bg-white shadow-lg rounded-lg p-6 space-y-6">
          <h1 className="text-3xl font-bold text-center">🎓 Your Career Guidance Summary</h1>

          {/* Summary */}
          <section>
            <h2 className="text-xl font-semibold">Friendly Summary</h2>
            <p className="text-gray-800">{result.friendly_summary}</p>
          </section>

          {/* Lists */}
          {["strengths", "weaknesses", "skill_gaps", "suggestions", "next_steps"].map((key) => (
            <section key={key}>
              <h2 className="text-xl font-semibold capitalize">{key.replace("_", " ")}</h2>
              <ul className="list-disc pl-6 text-gray-800">
                {result[key]?.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </section>
          ))}

          <div className="flex justify-center space-x-4 mt-6">
            <button
              onClick={() => navigate("/")}
              className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-lg"
            >
              Back to Home
            </button>
            <button
              onClick={downloadPDF}
              className="bg-green-600 hover:bg-green-700 text-white py-2 px-6 rounded-lg"
            >
              Download PDF
            </button>
          </div>
        </div>
      ) : (
        <div className="flex flex-col items-center">
          <div className="loader mb-4"></div>
          <p className="text-lg font-medium text-gray-700">{stages[loadingStage]}</p>
        </div>
      )}
    </div>
  );
}

export default CareerResultPage;
