// import { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { toast } from "react-hot-toast";

// const LoadingPage = () => {
//   const navigate = useNavigate();
//   const [progressText, setProgressText] = useState("Preparing your personalized questions...");
//   const [roundNumber, setRoundNumber] = useState(1);
//   const maxRounds = 2;

//   useEffect(() => {
//     const email = localStorage.getItem("userEmail");

//     if (!email) {
//       toast.error("Email not found. Please start again.");
//       navigate("/");
//       return;
//     }

//     const fetchQuestions = async () => {
//       try {
//         const res = await fetch("http://localhost:8000/generate-questions", {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({ email, round_number: roundNumber }),
//         });

//         if (!res.ok) throw new Error("Error generating cross-exam questions");

//         const data = await res.json();

//         if (!data.questions || data.questions.length === 0) {
//           toast.error("No questions generated.");
//           navigate("/");
//           return;
//         }

//         localStorage.setItem("crossExamQs", JSON.stringify(data.questions));
//         localStorage.setItem("crossExamRound", roundNumber);

//         navigate("/cross-exam");
//       } catch (err) {
//         console.error(err);
//         toast.error("Failed to load questions. Try again.");
//         navigate("/");
//       }
//     };

//     fetchQuestions();
//   }, [navigate, roundNumber]);

//   return (
//     <div className="min-h-screen flex flex-col justify-center items-center text-lg font-medium">
//       <p>{progressText}</p>
//       <div className="mt-4 w-64 h-2 bg-gray-300 rounded-full overflow-hidden">
//         <div
//           className="h-2 bg-blue-500 transition-all duration-500"
//           style={{ width: `${(roundNumber / maxRounds) * 100}%` }}
//         />
//       </div>
//       <p className="mt-2 text-gray-600">Round {roundNumber} of {maxRounds}</p>
//     </div>
//   );
// };

// export default LoadingPage;
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";

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
        const res = await fetch("http://localhost:8000/generate-questions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        });

        if (!res.ok) throw new Error("Error generating cross-exam questions");
        const data = await res.json();

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
