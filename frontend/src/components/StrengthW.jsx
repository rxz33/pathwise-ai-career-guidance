import React, { useState } from "react";
import { useFormContext } from "react-hook-form";

const StepSkillsProjects = () => {
  const { register, handleSubmit, formState: { errors } } = useFormContext();

  const [strengthsValue, setStrengthsValue] = useState("");
  const [struggleValue, setStruggleValue] = useState("");
  const [toolsValue, setToolsValue] = useState("");
  const [relatedCareerValue, setRelatedCareerValue] = useState("");
  const [resumeValue, setResumeValue] = useState("");

  const strengthsOptions = ["Communication", "Leadership", "Problem Solving", "Creativity", "Other"];
  const strugglesOptions = ["Time Management", "Public Speaking", "Technical Skills", "Confidence", "Other"];
  const toolsOptions = ["React", "Python", "Figma", "Excel", "Photoshop", "Other"];
  const relatedCareerOptions = ["Yes", "No"];
  const resumeOptions = ["Yes", "No"];

  // 🚀 No API calls here — parent handles submit
  const onSubmit = (data) => {
    console.log("📥 StepSkillsProjects Data:", data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-800">Skills, Projects & Experiences</h2>

      {/* Strengths */}
      <div>
        <label>Your Strengths</label>
        <select
          {...register("strengths")}
          className="input"
          onChange={(e) => setStrengthsValue(e.target.value)}
        >
          <option value="">Select</option>
          {strengthsOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {strengthsValue === "Other" && (
          <input type="text" {...register("strengthsOther")} placeholder="Please specify" className="input mt-2" />
        )}
        {errors.strengths && <p className="text-red-500 text-sm">{errors.strengths.message}</p>}
      </div>

      {/* Struggles */}
      <div>
        <label>Areas You Struggle With</label>
        <select
          {...register("struggleWith")}
          className="input"
          onChange={(e) => setStruggleValue(e.target.value)}
        >
          <option value="">Select</option>
          {strugglesOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {struggleValue === "Other" && (
          <input type="text" {...register("struggleWithOther")} placeholder="Please specify" className="input mt-2" />
        )}
        {errors.struggleWith && <p className="text-red-500 text-sm">{errors.struggleWith.message}</p>}
      </div>

      {/* Confidence */}
      <div>
        <label>Overall Confidence Level (1–10)</label>
        <input
          type="range"
          min={1}
          max={10}
          {...register("confidenceLevel", { valueAsNumber: true })}
          className="w-full"
        />
        {errors.confidenceLevel && <p className="text-red-500 text-sm">{errors.confidenceLevel.message}</p>}
      </div>

      {/* Tools / Tech */}
      <div>
        <label>Tools / Technologies You’ve Used</label>
        <select
          {...register("toolsTechUsed")}
          className="input"
          onChange={(e) => setToolsValue(e.target.value)}
        >
          <option value="">Select</option>
          {toolsOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {toolsValue === "Other" && (
          <input type="text" {...register("toolsTechOther")} placeholder="Please specify" className="input mt-2" />
        )}
        {errors.toolsTechUsed && <p className="text-red-500 text-sm">{errors.toolsTechUsed.message}</p>}
      </div>

      {/* Project / Internship */}
      <div>
        <label>Describe a Project or Internship</label>
        <textarea
          {...register("internshipOrProject")}
          rows={3}
          className="input"
          placeholder="Brief description of what you worked on..."
        />
        {errors.internshipOrProject && <p className="text-red-500 text-sm">{errors.internshipOrProject.message}</p>}
      </div>

      {/* Learnings */}
      <div>
        <label>What did you learn from it?</label>
        <textarea
          {...register("whatDidYouLearn")}
          rows={2}
          className="input"
          placeholder="Key skills or insights gained"
        />
        {errors.whatDidYouLearn && <p className="text-red-500 text-sm">{errors.whatDidYouLearn.message}</p>}
      </div>

      {/* Related to Career */}
      <div>
        <label>Is this related to your career interests?</label>
        <select
          {...register("relatedToCareer")}
          className="input"
          onChange={(e) => setRelatedCareerValue(e.target.value)}
        >
          <option value="">Select</option>
          {relatedCareerOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {relatedCareerValue === "Other" && (
          <input type="text" {...register("relatedToCareerOther")} placeholder="Please specify" className="input mt-2" />
        )}
        {errors.relatedToCareer && <p className="text-red-500 text-sm">{errors.relatedToCareer.message}</p>}
      </div>

      {/* Resume Section */}
      <div>
        <label>Do you have a resume?</label>
        <select
          {...register("hasResume")}
          className="input"
          onChange={(e) => setResumeValue(e.target.value)}
        >
          <option value="">Select</option>
          {resumeOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {errors.hasResume && <p className="text-red-500 text-sm">{errors.hasResume.message}</p>}
      </div>

      {/* Conditional Resume Upload */}
      {resumeValue === "Yes" && (
        <div>
          <label>Upload Resume</label>
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            {...register("resumeFile")}
            className="input"
          />
          {errors.resumeFile && <p className="text-red-500 text-sm">{errors.resumeFile.message}</p>}
        </div>
      )}
    </form>
  );
};

export default StepSkillsProjects;
