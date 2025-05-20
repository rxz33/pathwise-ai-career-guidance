import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';

function CrossExamPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(false);

  // ✅ Define email only once and use fallback sources
  const [email, setEmail] = useState(() => {
    return location.state?.email || localStorage.getItem('user_email') || '';
  });

  useEffect(() => {
    const savedData = localStorage.getItem('crossExamQs');
    const formData = localStorage.getItem('user_form_data');

    console.log('✅ crossExamQs from localStorage:', savedData);
    console.log('✅ user_form_data from localStorage:', formData);

    if (!savedData || !formData) {
      toast.error('Missing data. Please restart the process.');
      navigate('/');
      return;
    }

    try {
      const parsedQuestions = JSON.parse(savedData);
      const parsedForm = JSON.parse(formData);

      console.log('✅ Parsed questions object:', parsedQuestions);
      console.log('✅ Parsed user email:', parsedForm?.personal?.email);

      setQuestions(parsedQuestions.questions || []);
      setAnswers(new Array(parsedQuestions.questions?.length || 0).fill(''));

      // ✅ Update email if not already set
      if (!email && parsedForm?.personal?.email) {
        setEmail(parsedForm.personal.email);
        localStorage.setItem('user_email', parsedForm.personal.email);
      }

      // Save user name for later use
      if (!localStorage.getItem('user_name') && parsedForm?.personal?.name) {
        localStorage.setItem('user_name', parsedForm.personal.name);
      }
    } catch (error) {
      console.error('❌ JSON parsing error:', error);
      toast.error('Corrupted data. Please restart.');
      navigate('/');
    }
  }, [navigate, email]);

  const handleChange = (index, value) => {
    const newAnswers = [...answers];
    newAnswers[index] = value;
    setAnswers(newAnswers);
  };

  const generateManualSummary = () => {
    const form = JSON.parse(localStorage.getItem('user_form_data'));
    const name = form?.personal?.name || 'The user';
    const hometown = form?.personal?.hometown || 'an unspecified location';
    const locationType = form?.personal?.current_location_type || 'unspecified';

    const parseField = (field) => {
      if (Array.isArray(field)) return field.join(', ');
      if (typeof field === 'string') return field;
      return 'not specified';
    };

    const interests = parseField(form?.interests);
    const strengths = parseField(form?.strengths);
    const weaknesses = parseField(form?.weaknesses);
    const goal = form?.learning?.goal || 'explore career options';

    return `
${name} is from ${hometown}, currently living in a ${locationType} area.
Interests: ${interests}.
Strengths: ${strengths}.
Weaknesses: ${weaknesses}.
Goal: ${goal}.
`.trim();
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  if (answers.some((ans) => ans.trim() === '')) {
    toast.error('Please answer all questions.');
    return;
  }

  if (!email) {
    toast.error('Missing email. Please restart the process.');
    return;
  }

  setLoading(true);
  window.scrollTo({ top: 0, behavior: 'smooth' });

  try {
    const manualSummary = generateManualSummary();

    const res = await fetch('http://localhost:8000/evaluate-cross-exam', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        user_summary: localStorage.getItem('evaluation') || manualSummary,
      }),
    });

    if (!res.ok) throw new Error('Server error');

    const data = await res.json();
    console.log('✅ Career evaluation response:', data);
    localStorage.setItem('careerEvaluation', JSON.stringify(data));


    toast.success('Evaluation complete! 🚀');
    // localStorage.setItem('careerEvaluationText', evaluation);
    localStorage.setItem('user_email', email);

    navigate('/career-result');
  } catch (err) {
    console.error(err);
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
