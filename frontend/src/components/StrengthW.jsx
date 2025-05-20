import React from "react";
import { useFormContext } from "react-hook-form";

const StepSkillsProjects = () => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-800">Skills & Projects</h2>

      {/* Strengths */}
      <div>
        <label className="block mb-1">Your Strengths</label>
        <input
          type="text"
          placeholder="Comma-separated e.g. Communication, Leadership"
          {...register("strengths")}
          className="input"
        />
        {errors.strengths && <p className="text-red-500 text-sm">{errors.strengths.message}</p>}
      </div>

      {/* Struggle With */}
      <div>
        <label className="block mb-1">What do you struggle with?</label>
        <input
          type="text"
          placeholder="Comma-separated e.g. Public Speaking, Time Management"
          {...register("struggleWith")}
          className="input"
        />
        {errors.struggleWith && <p className="text-red-500 text-sm">{errors.struggleWith.message}</p>}
      </div>

      {/* Confidence Level */}
      <div>
        <label className="block mb-1">Overall Confidence Level (1–10)</label>
        <input
          type="range"
          min={1}
          max={10}
          {...register("confidenceLevel", { valueAsNumber: true })}
          className="w-full"
        />
        {errors.confidenceLevel && (
          <p className="text-red-500 text-sm">{errors.confidenceLevel.message}</p>
        )}
      </div>

      {/* Tools/Tech Used */}
      <div>
        <label className="block mb-1">Tools/Technologies You've Used</label>
        <input
          type="text"
          placeholder="Comma-separated e.g. React, Python, Figma"
          {...register("toolsTechUsed")}
          className="input"
        />
        {errors.toolsTechUsed && (
          <p className="text-red-500 text-sm">{errors.toolsTechUsed.message}</p>
        )}
      </div>

      {/* Internship or Project */}
      <div>
        <label className="block mb-1">Describe a Project or Internship</label>
        <textarea
          {...register("internshipOrProject")}
          rows={3}
          className="input"
          placeholder="Brief description of what you worked on..."
        />
        {errors.internshipOrProject && (
          <p className="text-red-500 text-sm">{errors.internshipOrProject.message}</p>
        )}
      </div>

      {/* What did you learn? */}
      <div>
        <label className="block mb-1">What did you learn from it?</label>
        <textarea
          {...register("whatDidYouLearn")}
          rows={2}
          className="input"
          placeholder="Key skills or insights gained"
        />
        {errors.whatDidYouLearn && (
          <p className="text-red-500 text-sm">{errors.whatDidYouLearn.message}</p>
        )}
      </div>

      {/* Related to Career? */}
      <div>
        <label className="block mb-1">Is this experience related to your career interests?</label>
        <select {...register("relatedToCareer")} className="input">
          <option value="">Select</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select>
        {errors.relatedToCareer && (
          <p className="text-red-500 text-sm">{errors.relatedToCareer.message}</p>
        )}
      </div>
    </div>
  );
};

export default StepSkillsProjects;
