import React from "react";
import { useFormContext } from "react-hook-form";

const StepProfessionalDetails = () => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-800">
        Professional Experience (Optional)
      </h2>

      {/* Current Role */}
      <div>
        <label className="block mb-1">Current Role</label>
        <input
          type="text"
          placeholder="e.g. Software Developer, Analyst"
          {...register("currentRole")}
          className="input"
        />
        {errors.currentRole && (
          <p className="text-red-500 text-sm">{errors.currentRole.message}</p>
        )}
      </div>

      {/* Years of Experience */}
      <div>
        <label className="block mb-1">Years of Experience</label>
        <input
          type="number"
          placeholder="e.g. 2"
          {...register("yearsOfExperience")}
          className="input"
        />
        {errors.yearsOfExperience && (
          <p className="text-red-500 text-sm">{errors.yearsOfExperience.message}</p>
        )}
      </div>

      {/* Leadership Role */}
      <div>
        <label className="block mb-1">Have You Held a Leadership Role?</label>
        <select {...register("leadershipRole")} className="input">
          <option value="">Select</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select>
        {errors.leadershipRole && (
          <p className="text-red-500 text-sm">{errors.leadershipRole.message}</p>
        )}
      </div>

      {/* Leadership Skill */}
      <div>
        <label className="block mb-1">What Leadership Skills Have You Demonstrated?</label>
        <input
          type="text"
          placeholder="e.g. Team Management, Decision Making"
          {...register("leadershipSkill")}
          className="input"
        />
        {errors.leadershipSkill && (
          <p className="text-red-500 text-sm">{errors.leadershipSkill.message}</p>
        )}
      </div>
    </div>
  );
};

export default StepProfessionalDetails;
