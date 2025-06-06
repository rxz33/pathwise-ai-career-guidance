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

  const downloadPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(11);
    const lines = doc.splitTextToSize(result || 'No data available.', 400);
    doc.text(lines, 40, 40);
    doc.save('career-guidance-result.pdf');
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">🎓 Your Career Guidance Summary</h1>

      {loading ? (
        <p className="text-center text-gray-600">Loading your results...</p>
      ) : (
        <div className="bg-white shadow-lg rounded-lg p-6 space-y-4">
          {result ? (
            <>
              <pre className="whitespace-pre-wrap text-gray-800 text-lg">{result}</pre>

              <div className="text-center mt-8 space-x-4">
                <button
                  onClick={() => navigate('/')}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition duration-300"
                >
                  Back to Home
                </button>
                <button
                  onClick={downloadPDF}
                  className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-6 rounded-lg transition duration-300"
                >
                  Download as PDF
                </button>
              </div>
            </>
          ) : (
            <p className="text-center text-gray-500">No career summary available.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default CareerResultPage;
