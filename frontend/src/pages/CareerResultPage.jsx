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

export default function CareerResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [taskId, setTaskId] = useState(null);
  const [loadingStage, setLoadingStage] = useState(0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const email = location.state?.email || localStorage.getItem("userEmail");

  useEffect(() => {
    if (!email) {
      toast.error("Missing user email.");
      navigate("/");
      return;
    }

    const startFinalization = async () => {
      try {
        setLoading(true);
        const response = await axios.post(
          "http://localhost:8000/finalize-career-path",
          { email }
        );
        setTaskId(response.data.task_id);
      } catch (err) {
        console.error(err);
        toast.error("Failed to start finalization.");
        navigate("/");
      }
    };

    startFinalization();
  }, [email, navigate]);

  // Poll backend for status
  useEffect(() => {
    if (!taskId) return;

    const interval = setInterval(async () => {
      try {
        const res = await axios.get(
          `http://localhost:8000/finalize-career-path/status/${taskId}`
        );
        const data = res.data;

        setLoadingStage(data.current_stage);
        if (data.partial_report) {
          setResult(data.partial_report.final_report || data.partial_report);
        }

        if (data.status === "completed") {
          clearInterval(interval);
          toast.success("Career report generated!");
        } else if (data.status === "failed") {
          clearInterval(interval);
          toast.error("Failed to generate career report.");
        }
      } catch (err) {
        console.error(err);
        clearInterval(interval);
        toast.error("Error fetching report status.");
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [taskId]);

  const downloadPDF = () => {
    if (!result) return;
    const doc = new jsPDF({ orientation: "portrait", unit: "pt", format: "a4" });
    const margin = 40;
    const pageWidth = doc.internal.pageSize.getWidth();
    let y = 50;

    doc.setFontSize(16);
    doc.text("Career Guidance Report", margin, y);
    y += 30;

    const addSection = (title, content) => {
      doc.setFontSize(14);
      doc.text(title, margin, y);
      y += 20;
      doc.setFontSize(12);

      if (Array.isArray(content)) {
        content.forEach((item) => {
          const lines = doc.splitTextToSize("• " + String(item), pageWidth - margin * 2);
          lines.forEach((line) => {
            doc.text(line, margin + 20, y);
            y += 16;
          });
        });
      } else if (content) {
        const lines = doc.splitTextToSize(String(content), pageWidth - margin * 2);
        lines.forEach((line) => {
          doc.text(line, margin, y);
          y += 16;
        });
      }
      y += 10;
    };

    addSection("Friendly Summary", result.friendly_summary);

    if (result.top_careers) {
      result.top_careers.forEach((career, idx) => {
        addSection(`Top Career #${idx + 1}: ${career.name}`, [
          `Merits: ${career.merits.join(", ")}`,
          `Demerits: ${career.demerits.join(", ")}`,
          `Market Trends: ${career.trends.join(", ")}`
        ]);
      });
    }

    ["strengths", "weaknesses", "skill_gaps", "suggestions", "next_steps"].forEach((key) => {
      addSection(key.replace("_", " ").toUpperCase(), result[key]);
    });

    doc.save("career-guidance-report.pdf");
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-6 bg-gradient-to-br from-indigo-50 to-purple-50">
      {loading && !result ? (
        <div className="flex flex-col items-center justify-center mt-20">
          <div className="loader mb-4 w-12 h-12 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-lg font-medium text-gray-700">{stages[loadingStage]}</p>
        </div>
      ) : result ? (
        <div className="max-w-5xl bg-white shadow-2xl rounded-3xl p-8 space-y-8 mt-10">
          <h1 className="text-3xl font-bold text-center text-indigo-700">🎓 Your Career Guidance Summary</h1>

          <section className="bg-indigo-50 p-4 rounded-lg shadow-inner">
            <h2 className="text-xl font-semibold">Friendly Summary</h2>
            <p className="text-gray-800">{result.friendly_summary}</p>
          </section>

          {result.top_careers?.map((career, idx) => (
            <section key={idx} className="bg-green-50 p-4 rounded-lg shadow-md">
              <h2 className="text-xl font-bold">{`Top Career #${idx + 1}: ${career.name}`}</h2>
              <ul className="list-disc pl-6 text-gray-800 mt-2">
                <li><strong>Merits:</strong> {career.merits.join(", ")}</li>
                <li><strong>Demerits:</strong> {career.demerits.join(", ")}</li>
                <li><strong>Market Trends:</strong> {career.trends.join(", ")}</li>
              </ul>
            </section>
          ))}

          {["strengths", "weaknesses", "skill_gaps", "suggestions", "next_steps"].map(key => (
            <section key={key} className="bg-gray-50 p-4 rounded-lg shadow-inner">
              <h2 className="text-xl font-semibold capitalize">{key.replace("_", " ")}</h2>
              <ul className="list-disc pl-6 text-gray-800">
                {Array.isArray(result[key]) && result[key].length > 0
                  ? result[key].map((item, i) => <li key={i}>{item}</li>)
                  : <li className="text-gray-500">No data available</li>}
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
        <p>Initializing...</p>
      )}
    </div>
  );
}
