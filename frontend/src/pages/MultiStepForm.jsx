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
    const formData = { ...rawData, personal: { ...rawData.personal, email } };

    try {
      setIsSubmitting(true);

      // Upload resume if available
      if (formData.hasResume === "Yes" && formData.resumeFile?.length > 0) {
        const formDataUpload = new FormData();
        formDataUpload.append("email", email);
        formDataUpload.append("resume", formData.resumeFile[0]);
        await fetch("http://localhost:8000/upload-resume", { method: "POST", body: formDataUpload });
      }

      // Submit other form info
      const response = await fetch("http://localhost:8000/submit-info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail);

      localStorage.setItem("user_form_data", JSON.stringify(formData));
      setIsSuccess(true);
      toast.success("Form submitted successfully!");

      // Navigate to Loading Page (triggering cross-exam)
      setTimeout(() => {
        navigate("/loading");
      }, 1000);

    } catch (error) {
      console.error(error);
      toast.error("Submission failed. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNext = async () => {
    const valid = await methods.trigger();
    if (!valid) return;

    if (step === 5) {
      // Step 5 → go to loading page for personality tests
      setStep(6); // Step 6 is loading page
    } else if (step < 8) {
      setStep((prev) => prev + 1);
    } else if (step === 8) {
      // Final submission after last test
      onSubmit();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f2f4f8] via-white to-[#e8edf5] flex justify-center items-start py-10 px-4">
      <div className="w-full max-w-4xl space-y-8">
        {/* Progress Bar */}
        <div className={`w-full ${flatStyle ? "h-1 bg-gray-300" : "bg-gray-200 rounded-full h-3"} mb-8 overflow-hidden`}>
          <div
            className={`${flatStyle ? "bg-indigo-600" : "bg-indigo-500 rounded-full"} h-full transition-all duration-500 ease-in-out`}
            style={{ width: `${(step / 8) * 100}%` }}
          ></div>
        </div>

        {/* Success Message */}
        {isSuccess && <div className="text-green-600 text-center font-medium text-lg mb-6">✅ Submitted successfully!</div>}

        <h2 className="text-2xl md:text-3xl font-semibold text-gray-800 text-center mb-4">
          Step {step} of 8
        </h2>

        <FormProvider {...methods}>
          <form onSubmit={(e) => e.preventDefault()} className="space-y-10">
            {/* Step Components */}
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
              {step > 1 && step !== 6 && (
                <button type="button" onClick={() => setStep((prev) => prev - 1)}
                  className={`px-6 py-2 font-medium transition ${flatStyle ? "bg-transparent border border-gray-400 text-gray-700 hover:bg-gray-100" : " bg-gray-100 text-gray-700 hover:bg-gray-200 rounded-md"}`}>
                  ← Back
                </button>
              )}

              {/* Next / Submit All Button */}
              {step !== 6 && (
                <button type="button" onClick={handleNext}
                  className={`px-6 py-2 font-semibold text-white transition ${flatStyle ? "bg-indigo-600 hover:bg-indigo-700" : " bg-indigo-600 hover:bg-indigo-700 rounded-md"}`}>
                  {step === 8 ? "Submit All" : "Next →"}
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
