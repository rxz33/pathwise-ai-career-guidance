import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import axios from 'axios';
import jsPDF from 'jspdf';

function CareerResultPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  const email = location.state?.email || localStorage.getItem('user_email');

  useEffect(() => {
    if (!email) {
      toast.error('Missing user email.');
      navigate('/');
      return;
    }

    const fetchFinalResult = async () => {
      try {
        const response = await axios.get('http://localhost:8000/get-final-analysis', {
          params: { email },
        });

        const data = response.data;
        if (data.finalAnalysis) {
          setResult(data.finalAnalysis);
        } else {
          throw new Error('No finalAnalysis in response.');
        }
      } catch (error) {
        console.error('Error fetching final analysis:', error);
        toast.error('Failed to load your final result.');
        navigate('/');
      } finally {
        setLoading(false);
      }
    };

    fetchFinalResult();
  }, [email, navigate]);

  // ✅ Updated PDF Styling
const downloadPDF = () => {
  const doc = new jsPDF({ orientation: "portrait", unit: "pt", format: "a4" });
  const margin = 40;
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const lineHeight = 18;
  let cursorY = margin;

  // Title
  doc.setFont("helvetica", "bold");
  doc.setFontSize(20);
  doc.text("🎓 Career Guidance Report", pageWidth / 2, cursorY, { align: "center" });
  cursorY += 40;

  // Helper to render section with a table
  const addTableSection = (title, data) => {
    // Section heading
    if (cursorY + 2 * lineHeight > pageHeight - margin) {
      doc.addPage();
      cursorY = margin;
    }
    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.text(title, margin, cursorY);
    cursorY += lineHeight + 5;

    // Table headers
    doc.setFont("helvetica", "bold");
    doc.setFontSize(13);
    const headers = ["Trait", "Score"];
    const colWidths = [200, 100];
    let colX = margin;
    headers.forEach((h, i) => {
      doc.text(h, colX, cursorY);
      colX += colWidths[i];
    });
    cursorY += lineHeight;

    // Table content
    doc.setFont("times", "normal");
    Object.entries(data).forEach(([key, value]) => {
      if (cursorY + lineHeight > pageHeight - margin) {
        doc.addPage();
        cursorY = margin;
      }
      doc.text(key, margin, cursorY);
      doc.text(String(value), margin + colWidths[0], cursorY);
      cursorY += lineHeight;
    });

    cursorY += lineHeight; // extra spacing after section
  };

  const finalAnalysis = userData.finalAnalysis || "No final analysis available.";

  // Add each section
  addTableSection("🧠 Big Five Personality Test", bigFive);
  addTableSection("💼 RIASEC Test", riasec);
  addTableSection("📊 Aptitude Test", aptitude);

  // Final Analysis
  if (cursorY + 3 * lineHeight > pageHeight - margin) {
    doc.addPage();
    cursorY = margin;
  }
  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  doc.text("📌 Career Analysis Summary", margin, cursorY);
  cursorY += lineHeight + 5;

  doc.setFont("times", "normal");
  doc.setFontSize(13);
  const lines = doc.splitTextToSize(finalAnalysis, pageWidth - margin * 2);
  lines.forEach((line) => {
    if (cursorY + lineHeight > pageHeight - margin) {
      doc.addPage();
      cursorY = margin;
    }
    doc.text(line, margin, cursorY);
    cursorY += lineHeight;
  });

  // Footer with page numbers
  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFont("helvetica", "italic");
    doc.setFontSize(10);
    doc.text(`Page ${i} of ${pageCount}`, pageWidth - margin, pageHeight - 20, { align: "right" });
  }

  doc.save("career-guidance-report.pdf");
};



  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* ✅ Heading font: bold sans-serif (modern look) */}
      <h1 className="text-3xl font-bold mb-6 text-center font-sans text-gray-900">
        🎓 Your Career Guidance Summary
      </h1>

      {loading ? (
        <p className="text-center text-gray-600 font-sans">Loading your results...</p>
      ) : (
        <div className="bg-white shadow-lg rounded-lg p-6 space-y-4">
          {result ? (
            <>
              {/* ✅ Result text: serif (report style) */}
              <pre className="whitespace-pre-wrap text-gray-800 text-lg font-serif leading-relaxed">
                {result}
              </pre>

              <div className="text-center mt-8 space-x-4">
                <button
                  onClick={() => navigate('/')}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-sans font-semibold py-2 px-6 rounded-lg transition duration-300"
                >
                  Back to Home
                </button>
                <button
                  onClick={downloadPDF}
                  className="bg-green-600 hover:bg-green-700 text-white font-sans font-semibold py-2 px-6 rounded-lg transition duration-300"
                >
                  Download as PDF
                </button>
              </div>
            </>
          ) : (
            <p className="text-center text-gray-500 font-sans">No career summary available.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default CareerResultPage;
