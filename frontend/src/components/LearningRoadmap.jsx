import React, { useState } from "react";
import { useFormContext } from "react-hook-form";

const StepLearningRoadmap = () => {
  const { register, formState: { errors } } = useFormContext();

  const [studyPlanValue, setStudyPlanValue] = useState("");
  const [learningModeValue, setLearningModeValue] = useState("");
  const [openToExploreValue, setOpenToExploreValue] = useState("");
  const [riskTakingValue, setRiskTakingValue] = useState("");

  const studyPlanOptions = ["Masters", "Certifications", "MBA", "Diploma", "Other"];
  const learningModeOptions = ["Self-paced", "Classroom", "Online Courses", "Workshops", "Other"];
  const openToExploreOptions = ["Yes", "No", "Maybe", "Other"];
  const riskTakingOptions = ["Low", "Medium", "High", "Very High", "Other"];

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-800">Learning & Roadmap Insight</h2>

      {/* Study Plan */}
      <div>
        <label>Your Study Plan</label>
        <select {...register("studyPlan")} className="input" onChange={(e) => setStudyPlanValue(e.target.value)}>
          <option value="">Select</option>
          {studyPlanOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {studyPlanValue === "Other" && (
          <input type="text" {...register("studyPlanOther")} placeholder="Please specify" className="input mt-2" />
        )}
        {errors.studyPlan && <p className="text-red-500 text-sm">{errors.studyPlan.message}</p>}
      </div>

      {/* Preferred Learning Mode */}
      <div>
        <label>Preferred Learning Mode</label>
        <select {...register("preferredLearning")} className="input" onChange={(e) => setLearningModeValue(e.target.value)}>
          <option value="">Select</option>
          {learningModeOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {learningModeValue === "Other" && (
          <input type="text" {...register("preferredLearningOther")} placeholder="Please specify" className="input mt-2" />
        )}
        {errors.preferredLearning && <p className="text-red-500 text-sm">{errors.preferredLearning.message}</p>}
      </div>

      {/* Open to Explore */}
      <div>
        <label>Are you open to exploring new fields?</label>
        <select {...register("openToExplore")} className="input" onChange={(e) => setOpenToExploreValue(e.target.value)}>
          <option value="">Select</option>
          {openToExploreOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {openToExploreValue === "Other" && (
          <input type="text" {...register("openToExploreOther")} placeholder="Please specify" className="input mt-2" />
        )}
        {errors.openToExplore && <p className="text-red-500 text-sm">{errors.openToExplore.message}</p>}
      </div>

      {/* Risk Taking Level */}
      <div>
        <label>Your Risk Taking Level</label>
        <select {...register("riskTaking")} className="input" onChange={(e) => setRiskTakingValue(e.target.value)}>
          <option value="">Select</option>
          {riskTakingOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {riskTakingValue === "Other" && (
          <input type="text" {...register("riskTakingOther")} placeholder="Please specify" className="input mt-2" />
        )}
        {errors.riskTaking && <p className="text-red-500 text-sm">{errors.riskTaking.message}</p>}
      </div>
    </div>
  );
};

export default StepLearningRoadmap;
