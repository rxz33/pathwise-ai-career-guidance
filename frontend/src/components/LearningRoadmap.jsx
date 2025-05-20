import React from "react";
import { useFormContext } from "react-hook-form";

const StepLearningRoadmap = () => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-800">Learning & Roadmap Insight</h2>

      {/* Study Plan */}
      <div>
        <label className="block mb-1">Your Study Plan</label>
        <input
          type="text"
          placeholder="e.g. Masters, Certifications, MBA"
          {...register("studyPlan")}
          className="input"
        />
        {errors.studyPlan && <p className="text-red-500 text-sm">{errors.studyPlan.message}</p>}
      </div>

      {/* Preferred Learning Mode */}
      <div>
        <label className="block mb-1">Preferred Learning Mode</label>
        <div className="space-y-1">
          <label className="block">
            <input type="checkbox" value="Self-paced" {...register("preferredLearning")} />
            <span className="ml-2">Self-paced</span>
          </label>
          <label className="block">
            <input type="checkbox" value="Classroom" {...register("preferredLearning")} />
            <span className="ml-2">Classroom</span>
          </label>
          <label className="block">
            <input type="checkbox" value="Online Courses" {...register("preferredLearning")} />
            <span className="ml-2">Online Courses</span>
          </label>
        </div>
        {errors.preferredLearning && (
          <p className="text-red-500 text-sm">{errors.preferredLearning.message}</p>
        )}
      </div>

      {/* Open to Explore New Fields */}
      <div>
        <label className="block mb-1">Are you open to exploring new fields?</label>
        <select {...register("openToExplore")} className="input">
          <option value="">Select</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select>
        {errors.openToExplore && (
          <p className="text-red-500 text-sm">{errors.openToExplore.message}</p>
        )}
      </div>

      {/* Risk Taking Level */}
      <div>
        <label className="block mb-1">Your Risk Taking Level</label>
        <select {...register("riskTaking")} className="input">
          <option value="">Select</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
        {errors.riskTaking && (
          <p className="text-red-500 text-sm">{errors.riskTaking.message}</p>
        )}
      </div>
    </div>
  );
};

export default StepLearningRoadmap;
