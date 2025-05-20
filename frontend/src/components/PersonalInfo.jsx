import React from "react";
import { useFormContext } from "react-hook-form";

const Step1 = () => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-800">Basic Identity & Context</h2>

      {/* Full Name */}
      <div>
        <label className="block mb-1">Full Name</label>
        <input type="text" {...register("fullName")} className="input" />
        {errors.fullName && <p className="text-red-500 text-sm">{errors.fullName.message}</p>}
      </div>

      {/* Age */}
      <div>
        <label className="block mb-1">Age</label>
        <input
          type="number"
          {...register("age", { valueAsNumber: true })}
          className="input"
        />
        {errors.age && <p className="text-red-500 text-sm">{errors.age.message}</p>}
      </div>

      {/* Current Status */}
      <div>
        <label className="block mb-1">Current Status</label>
        <select {...register("currentStatus")} className="input">
          <option value="">Select</option>
          <option value="Student">Student</option>
          <option value="Fresher">Fresher</option>
          <option value="Working Professional">Working Professional</option>
          <option value="Career Break">Career Break</option>
        </select>
        {errors.currentStatus && (
          <p className="text-red-500 text-sm">{errors.currentStatus.message}</p>
        )}
      </div>

      {/* Field of Study */}
      <div>
        <label className="block mb-1">Field of Study / Major</label>
        <input type="text" {...register("fieldOfStudy")} className="input" />
        {errors.fieldOfStudy && (
          <p className="text-red-500 text-sm">{errors.fieldOfStudy.message}</p>
        )}
      </div>

      {/* Education Level */}
      <div>
        <label className="block mb-1">Current Education Level</label>
        <select {...register("educationLevel")} className="input">
          <option value="">Select</option>
          <option value="High School">High School</option>
          <option value="Diploma/Intermediate">Diploma/Intermediate</option>
          <option value="Undergraduate">Undergraduate</option>
          <option value="Postgraduate">Postgraduate</option>
          <option value="Doctorate">Doctorate</option>
          <option value="Other">Other</option>
        </select>
        {errors.educationLevel && (
          <p className="text-red-500 text-sm">{errors.educationLevel.message}</p>
        )}
      </div>

      {/* Willingness to Relocate */}
      <div>
        <label className="block mb-1">Willingness to Relocate</label>
        <select {...register("mobility")} className="input">
          <option value="">Select</option>
          <option value="Willing to relocate">Willing to relocate</option>
          <option value="Prefer hometown">Prefer hometown</option>
          <option value="Depends on opportunity">Depends on opportunity</option>
        </select>
        {errors.mobility && (
          <p className="text-red-500 text-sm">{errors.mobility.message}</p>
        )}
      </div>

      {/* Financial Status (1–10) */}
      <div>
        <label className="block mb-1">Financial Status (1–10)</label>
        <input
          type="range"
          min={1}
          max={10}
          {...register("financialStatus", { valueAsNumber: true })}
          className="w-full"
        />
        {errors.financialStatus && (
          <p className="text-red-500 text-sm">{errors.financialStatus.message}</p>
        )}
      </div>
    </div>
  );
};

export default Step1;
