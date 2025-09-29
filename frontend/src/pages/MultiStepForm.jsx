import React, { useState, useEffect } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "react-hot-toast";
import { useNavigate } from "react-router-dom";

import PersonalInfo from "../components/PersonalInfo";
import Interest from "../components/Interest";
import StrengthW from "../components/StrengthW";
import LearningRoadmap from "../components/LearningRoadmap";
import Optional from "../components/Optional";
import TestPage from "../components/TestPage";       // Big Five
import RiasecTest from "../components/RiasecTest"; // RIASEC
import AptitudeTest from "../components/AptitudeTest";

import { PersonalInfos } from "../schemas/PersonalInfos";
import { Interests } from "../schemas/Interests";
import { StrengthWs } from "../schemas/StrengthWs";
import { LearningRoadmaps } from "../schemas/LearningRoadmaps";
import { Optionals } from "../schemas/Optionals";

import { fetchFromAPI } from "../api";

const MultiStepForm = ({ flatStyle = false }) => {
  const navigate = useNavigate();
  const methods = useForm({ resolver: zodResolver(PersonalInfos), mode: "onTouched" });

  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  // Reset form and localStorage on mount
  useEffect(() => {
    localStorage.removeItem("multiStepFormStep");
    methods.reset();
  }, []);

  useEffect(() => {
    localStorage.setItem("multiStepFormStep", step.toString());
  }, [step]);

  const currentSchema =
    step === 1 ? PersonalInfos :
    step === 2 ? Interests :
    step === 3 ? StrengthWs :
    step === 4 ? LearningRoadmaps :
    step === 5 ? Optionals :
    null;

  useEffect(() => {
    methods.reset(methods.getValues(), {
      keepErrors: true,
      keepDirty: true,
      keepValues: true,
      keepDefaultValues: true,
    });
  }, [currentSchema]);

  useEffect(() => {
    const subscription = methods.watch(() => {
      localStorage.setItem("multiStepFormData", JSON.stringify(methods.getValues()));
    });
    return () => subscription.unsubscribe();
  }, [methods]);

  const onSubmit = async () => {
  const email = localStorage.getItem("userEmail");
  if (!email) return toast.error("Email missing. Please log in again.");

  const rawData = methods.getValues();
  const formData = {
    personal: { ...rawData.personal, email },
    interests: rawData.interests,
    strengthsAndWeaknesses: rawData.strengthsAndWeaknesses,
    learningRoadmap: rawData.learningRoadmap,
    optionalFields: rawData.optionalFields,
  };


  try {
    setIsSubmitting(true);

    // Upload resume if available
    if (formData.hasResume === "Yes" && formData.resumeFile?.length > 0) {
      const formDataUpload = new FormData();
      formDataUpload.append("email", email);
      formDataUpload.append("resume", formData.resumeFile[0]);

      // For FormData, call fetch directly without 'Content-Type' header
      const uploadRes = await fetch(`${import.meta.env.VITE_API_URL}/upload-resume`, {
        method: "POST",
        body: formDataUpload,
      });

      if (!uploadRes.ok) {
        const errData = await uploadRes.json();
        throw new Error(errData.detail || "Resume upload failed");
      }
    }

    // Submit form JSON data
    await fetchFromAPI("/submit-info", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    localStorage.setItem("user_form_data", JSON.stringify(formData));
    setIsSuccess(true);
    toast.success("Form submitted successfully!");

    // Navigate to loading page for cross-exam
    setTimeout(() => navigate("/loading"), 1000);

  } catch (error) {
    console.error(error);
    toast.error(error.message || "Submission failed. Please try again.");
  } finally {
    setIsSubmitting(false);
  }
};


  const handleNext = async () => {
    const valid = await methods.trigger();
    if (!valid) return;

    if (step === 5) {
      setStep(6); // Loading personality tests
    } else if (step < 9) {
      setStep((prev) => prev + 1);
    } else if (step === 9) {
      onSubmit(); // Submit All on last test
    }
  };

  // Auto-advance Step 6 → Step 7
  useEffect(() => {
    if (step === 6) {
      const timer = setTimeout(() => setStep(7), 2000); // 2 seconds loading
      return () => clearTimeout(timer);
    }
  }, [step]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f2f4f8] via-white to-[#e8edf5] flex justify-center items-start py-10 px-4">
      <div className="w-full max-w-4xl space-y-8">

        {/* Progress Bar & Step Count only for Steps 1–5 */}
        {step <= 5 && (
          <>
            <div className={`w-full ${flatStyle ? "h-1 bg-gray-300" : "bg-gray-200 rounded-full h-3"} mb-8 overflow-hidden`}>
              <div
                className={`${flatStyle ? "bg-indigo-600" : "bg-indigo-500 rounded-full"} h-full transition-all duration-500 ease-in-out`}
                style={{ width: `${(step / 5) * 100}%` }}
              ></div>
            </div>
            <h2 className="text-2xl md:text-3xl font-semibold text-gray-800 text-center mb-4">
              Step {step} of 5
            </h2>
          </>
        )}

        {isSuccess && <div className="text-green-600 text-center font-medium text-lg mb-6">✅ Submitted successfully!</div>}

        <FormProvider {...methods}>
          <form onSubmit={(e) => e.preventDefault()} className="space-y-10">

            {step === 1 && <PersonalInfo />}
            {step === 2 && <Interest />}
            {step === 3 && <StrengthW />}
            {step === 4 && <LearningRoadmap />}
            {step === 5 && <Optional />}
            {step === 6 && (
              <div className="text-center text-lg font-medium py-20">
                Loading personality tests...
              </div>
            )}
            {step === 7 && <TestPage />}
            {step === 8 && <RiasecTest />}
            {step === 9 && <AptitudeTest />}

            {/* Navigation Buttons */}
            <div className="flex justify-between items-center pt-6">
              {/* Back button (not on Step 6) */}
              {step > 1 && step !== 6 && (
                <button type="button" onClick={() => setStep((prev) => prev - 1)}
                  className={`px-6 py-2 font-medium transition ${flatStyle ? "bg-transparent border border-gray-400 text-gray-700 hover:bg-gray-100" : " bg-gray-100 text-gray-700 hover:bg-gray-200 rounded-md"}`}>
                  ← Back
                </button>
              )}

              {/* Next / Submit All */}
              {step !== 6 && (
                <button type="button" onClick={handleNext}
                  className={`px-6 py-2 font-semibold text-white transition ${flatStyle ? "bg-indigo-600 hover:bg-indigo-700" : " bg-indigo-600 hover:bg-indigo-700 rounded-md"}`}>
                  {step === 9 ? "Submit All" : "Next →"}
                </button>
              )}
            </div>

          </form>
        </FormProvider>
      </div>
    </div>
  );
};

export default MultiStepForm;
