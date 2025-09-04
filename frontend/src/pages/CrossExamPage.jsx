import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';

function CrossExamPage() {
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState('');

  useEffect(() => {
    // Fetch saved data from localStorage
    const savedQuestions = localStorage.getItem('crossExamQs');
    const userFormData = localStorage.getItem('user_form_data');
    const userEmail = localStorage.getItem('userEmail');

    if (!savedQuestions || !userFormData || !userEmail) {
      toast.error('Missing data. Please restart the process.');
      navigate('/');
      return;
    }

    setEmail(userEmail);

    const parsedQuestions = JSON.parse(savedQuestions);
    setQuestions(parsedQuestions || []);
    setAnswers(new Array(parsedQuestions?.length || 0).fill(''));
  }, [navigate]);

  const handleChange = (index, value) => {
    const updatedAnswers = [...answers];
    updatedAnswers[index] = value;
    setAnswers(updatedAnswers);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (answers.some(ans => ans.trim() === '')) {
      toast.error('Please answer all questions.');
      return;
    }

    if (!email) {
      toast.error('Missing email. Please restart.');
      return;
    }

    setLoading(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });

    try {
      // Prepare payload for the backend
      const payload = {
        email,
        answers,
      };

      const res = await fetch('http://localhost:8000/submit-answers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error('Server error');

      const data = await res.json();
      console.log('✅ Cross-exam response:', data);

      // Save evaluation & next questions (if any)
      localStorage.setItem('careerEvaluation', JSON.stringify(data.evaluation || {}));
      if (data.followupQuestions?.length > 0) {
        localStorage.setItem('crossExamQs', JSON.stringify(data.followupQuestions));
        setQuestions(data.followupQuestions);
        setAnswers(new Array(data.followupQuestions.length).fill(''));
        toast.success('Next set of questions loaded!');
      } else {
        toast.success('Evaluation complete! 🚀');
        navigate('/career-result');
      }
    } catch (err) {
      console.error('❌', err);
      toast.error('Something went wrong!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">Cross-Examination Questions</h1>

      {questions.length > 0 ? (
        <form className="space-y-6" onSubmit={handleSubmit}>
          {questions.map((q, idx) => (
            <div key={idx}>
              <p className="font-medium text-gray-800">{idx + 1}. {q}</p>
              <textarea
                className="w-full mt-2 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows="3"
                value={answers[idx]}
                onChange={(e) => handleChange(idx, e.target.value)}
                placeholder="Type your answer here..."
              />
            </div>
          ))}

          <button
            type="submit"
            disabled={loading}
            className={`mt-6 w-full bg-blue-600 text-white py-3 rounded-lg font-semibold transition duration-300 hover:bg-blue-700 ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
          >
            {loading ? 'Submitting...' : 'Submit Answers'}
          </button>
        </form>
      ) : (
        <p className="text-center text-gray-500">Loading questions...</p>
      )}
    </div>
  );
}

export default CrossExamPage;
