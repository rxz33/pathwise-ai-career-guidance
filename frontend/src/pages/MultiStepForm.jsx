// MultiStepForm.jsx
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

import { PersonalInfos } from "../schemas/PersonalInfos";
import { Interests } from "../schemas/Interests";
import { StrengthWs } from "../schemas/StrengthWs";
import { LearningRoadmaps } from "../schemas/LearningRoadmaps";
import { Optionals } from "../schemas/Optionals";

const MultiStepForm = () => {
  const navigate = useNavigate();

  // Initialize form methods early so we can use reset immediately
  const methods = useForm({
    resolver: zodResolver(PersonalInfos), // default schema, will be updated below
    mode: "onTouched",
  });

  // 🔄 Reset form and localStorage on page refresh
  useEffect(() => {
    localStorage.removeItem("multiStepFormStep");
    localStorage.removeItem("multiStepFormData");
    methods.reset();
  }, []);

  const [step, setStep] = useState(1); // no longer reading from localStorage
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  useEffect(() => {
    localStorage.setItem("multiStepFormStep", step.toString());
  }, [step]);

  const currentSchema =
    step === 1 ? PersonalInfos :
    step === 2 ? Interests :
    step === 3 ? StrengthWs :
    step === 4 ? LearningRoadmaps :
    Optionals;

  // Dynamically update resolver based on current step
  useEffect(() => {
    methods.reset(methods.getValues(), {
      keepErrors: true,
      keepDirty: true,
      keepValues: true,
      keepDefaultValues: true,
    });
    methods.resetField; // ensure updates on schema change
  }, [currentSchema]);

  // 🧠 Save form data to localStorage when any field changes
  useEffect(() => {
    const subscription = methods.watch(() => {
      const allValues = methods.getValues();
      localStorage.setItem("multiStepFormData", JSON.stringify(allValues));
    });
    return () => subscription.unsubscribe();
  }, [methods]);

  const onSubmit = async () => {
    const email = localStorage.getItem("userEmail");
    if (!email) {
      console.error("❌ Email not found in localStorage");
      toast.error("Email missing. Please log in again.");
      return;
    }

    const rawData = methods.getValues();
    const formData = {
      ...rawData,
      personal: {
        ...rawData.personal,
        email,
      },
    };

    console.log("✅ Submitting Form Data:", formData);

    try {
      setIsSubmitting(true);
      const response = await fetch("http://localhost:8000/submit-info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(`❌ API Error: ${data.detail}`);
      }

      console.log("✅ Submission Success:", data);
      setIsSuccess(true);
      toast.success("Submitted successfully! 🎉");

      // ✅ Store form data for cross-examination
      localStorage.setItem("user_form_data", JSON.stringify(formData));


      // 🧼 Clear localStorage and form
      methods.reset();
      localStorage.removeItem("multiStepFormStep");
      localStorage.removeItem("multiStepFormData");

      // 🔁 Navigate to loading screen
      setTimeout(() => {
        navigate("/loading");
      }, 1500);
    } catch (error) {
      console.error("❌ Submission Error:", error);
      toast.error("Submission failed. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNext = async () => {
    const valid = await methods.trigger();
    if (valid) setStep((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f2f4f8] via-white to-[#e8edf5] flex justify-center items-center py-10 px-4">
      <div className="w-full max-w-4xl bg-white/60 backdrop-blur-md rounded-3xl shadow-xl p-8 md:p-12 transition-all duration-300 border border-gray-200">

        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-3 mb-8 overflow-hidden">
          <div
            className="bg-indigo-500 h-full transition-all duration-500 ease-in-out"
            style={{ width: `${(step / 5) * 100}%` }}
          ></div>
        </div>

        {/* Success Message */}
        {isSuccess && (
          <div className="text-green-600 text-center font-medium text-lg flex items-center justify-center gap-2 mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-500" fill="none"
              viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
            Submitted successfully!
          </div>
        )}

        <h2 className="text-2xl md:text-3xl font-semibold text-gray-800 text-center mb-4">
          Step {step} of 5
        </h2>

        <FormProvider {...methods}>
          <form
            onSubmit={async (e) => {
              e.preventDefault();
              if (step === 5) {
                await methods.handleSubmit(onSubmit)(e);
              } else {
                await handleNext();
              }
            }}
            className="space-y-10"
          >
            {step === 1 && <PersonalInfo />}
            {step === 2 && <Interest />}
            {step === 3 && <StrengthW />}
            {step === 4 && <LearningRoadmap />}
            {step === 5 && <Optional />}

            {/* Navigation Buttons */}
            <div className="flex justify-between items-center pt-6">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={() => setStep((prev) => prev - 1)}
                  className="px-6 py-2 rounded-lg bg-gray-100 text-gray-700 font-medium hover:bg-gray-200 transition"
                >
                  ← Back
                </button>
              ) : <div></div>}

              <button
                type="submit"
                disabled={isSubmitting}
                className={`px-6 py-2 rounded-lg text-white font-semibold transition ${
                  step === 5
                    ? "bg-green-600 hover:bg-green-700 flex items-center gap-2"
                    : "bg-indigo-600 hover:bg-indigo-700"
                }`}
              >
                {step === 5 ? (
                  <>
                    {isSubmitting && (
                      <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10"
                          stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor"
                          d="M4 12a8 8 0 018-8v8H4z" />
                      </svg>
                    )}
                    {isSubmitting ? "Submitting..." : "Submit"}
                  </>
                ) : (
                  "Next →"
                )}
              </button>
            </div>
          </form>
        </FormProvider>
      </div>
    </div>
  );
};

export default MultiStepForm;
