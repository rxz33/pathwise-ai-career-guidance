import React from "react";
import { useFormContext } from "react-hook-form";

const StepInterests = () => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-800">Interest & Preferences</h2>

      {/* Favorite Subjects */}
      <div>
        <label className="block mb-1">Favorite Subjects</label>
        <input
          type="text"
          {...register("favoriteSubjects")}
          placeholder="e.g. Mathematics, Biology, History"
          className="input"
        />
        {errors.favoriteSubjects && (
          <p className="text-red-500 text-sm">{errors.favoriteSubjects.message}</p>
        )}
      </div>

      {/* Activities That Make You Lose Track of Time */}
      <div>
        <label className="block mb-1">Activities That Make You Lose Track of Time</label>
        <textarea
          {...register("activitiesThatMakeYouLoseTime")}
          placeholder="e.g. Solving puzzles, Designing, Writing blogs"
          className="input"
          rows={3}
        />
        {errors.activitiesThatMakeYouLoseTime && (
          <p className="text-red-500 text-sm">{errors.activitiesThatMakeYouLoseTime.message}</p>
        )}
      </div>

      {/* Online Content You Enjoy */}
      <div>
        <label className="block mb-1">Online Content You Enjoy</label>
        <input
          type="text"
          {...register("onlineContent")}
          placeholder="e.g. Tech YouTube videos, Podcast interviews, TED talks"
          className="input"
        />
        {errors.onlineContent && (
          <p className="text-red-500 text-sm">{errors.onlineContent.message}</p>
        )}
      </div>

      {/* Areas You’d Like to Explore */}
      <div>
        <label className="block mb-1">Areas You’d Like to Explore</label>
        <input
          type="text"
          {...register("exploreAreas")}
          placeholder="e.g. AI, Entrepreneurship, UI/UX"
          className="input"
        />
        {errors.exploreAreas && (
          <p className="text-red-500 text-sm">{errors.exploreAreas.message}</p>
        )}
      </div>

      {/* Preferred Role */}
      <div>
        <label className="block mb-1">Preferred Role</label>
        <input
          type="text"
          {...register("preferredRole")}
          placeholder="e.g. Developer, Researcher, Designer"
          className="input"
        />
        {errors.preferredRole && (
          <p className="text-red-500 text-sm">{errors.preferredRole.message}</p>
        )}
      </div>

      {/* Preferred Company Type */}
      <div>
        <label className="block mb-1">Preferred Company Type</label>
        <input
          type="text"
          {...register("preferredCompany")}
          placeholder="e.g. Startup, MNC, NGO, Remote-first"
          className="input"
        />
        {errors.preferredCompany && (
          <p className="text-red-500 text-sm">{errors.preferredCompany.message}</p>
        )}
      </div>

      {/* Job Priorities */}
      <div>
        <label className="block mb-1">Job Priorities</label>
        <div className="grid grid-cols-2 gap-2">
          {["Salary", "Learning", "Stability", "Work-life balance", "Social Impact", "Leadership"].map((priority) => (
            <label key={priority} className="flex items-center space-x-2">
              <input
                type="checkbox"
                value={priority}
                {...register("jobPriorities")}
                className="accent-indigo-600"
              />
              <span>{priority}</span>
            </label>
          ))}
        </div>
        {errors.jobPriorities && (
          <p className="text-red-500 text-sm">{errors.jobPriorities.message}</p>
        )}
      </div>
    </div>
  );
};

export default StepInterests;
