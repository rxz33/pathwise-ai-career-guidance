import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import SignUp from "./pages/SignUp";
import Login from "./pages/Login";
import MultiStepForm from "./pages/MultiStepForm";
import LoadingPage from "./pages/LoadingPage";
import CrossExamPage from "./pages/CrossExamPage";
import CareerResultPage from "./pages/CareerResultPage";
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <Router>
      <>
        <Toaster position="top-center" reverseOrder={false} />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/form"
            element={
              <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
                <div className="w-full max-w-3xl bg-white shadow-2xl rounded-2xl p-8">
                  <MultiStepForm />
                </div>
              </div>
            }
          />
          <Route path="/loading" element={<LoadingPage />} />
          <Route path="/cross-exam" element={<CrossExamPage />} />
          <Route path="/career-result" element={<CareerResultPage />} />
        </Routes>
      </>
    </Router>
  );
}

export default App;
