import React, { useState } from "react";
import { useFormContext } from "react-hook-form";

const StepInterests = () => {
  const { register, formState: { errors } } = useFormContext();

  const [showOther, setShowOther] = useState({
    subjects: false,
    activities: false,
    onlineContent: false,
    exploreAreas: false,
    preferredRole: false,
    preferredCompany: false,
    jobPriorities: false,
  });

  const subjectsOptions = ["Mathematics", "Biology", "History", "Computer Science", "Economics", "Other"];
  const activitiesOptions = ["Solving puzzles", "Designing", "Writing blogs", "Gaming", "Volunteering", "Other"];
  const onlineContentOptions = ["Tech YouTube videos", "Podcast interviews", "TED talks", "Blogs", "Online Courses", "Other"];
  const exploreAreasOptions = ["AI", "Entrepreneurship", "UI/UX", "Robotics", "Cybersecurity", "Other"];
  const preferredRoleOptions = ["Developer", "Researcher", "Designer", "Data Analyst", "Product Manager", "Other"];
  const preferredCompanyOptions = ["Startup", "MNC", "NGO", "Remote-first", "Government", "Other"];
  const jobPrioritiesOptions = ["Salary", "Learning", "Stability", "Work-life balance", "Social Impact", "Leadership", "Other"];

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-800">Interests & Preferences</h2>

      {/* Favorite Subjects */}
      <div>
        <label>Favorite Subjects</label>
        <select
          {...register("favoriteSubjects")}
          className="input"
          onChange={(e) => setShowOther(prev => ({ ...prev, subjects: e.target.value === "Other" }))}
        >
          <option value="">Select</option>
          {subjectsOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {showOther.subjects && (
          <input type="text" {...register("favoriteSubjectsOther")} placeholder="Your subject" className="input mt-2" />
        )}
        {errors.favoriteSubjects && <p className="text-red-500 text-sm">{errors.favoriteSubjects.message}</p>}
      </div>

      {/* Activities That Make You Lose Track of Time */}
      <div>
        <label>Activities That Make You Lose Track of Time</label>
        <select
          {...register("activitiesThatMakeYouLoseTime")}
          className="input"
          onChange={(e) => setShowOther(prev => ({ ...prev, activities: e.target.value === "Other" }))}
        >
          <option value="">Select</option>
          {activitiesOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {showOther.activities && (
          <input type="text" {...register("activitiesOther")} placeholder="Your activity" className="input mt-2" />
        )}
        {errors.activitiesThatMakeYouLoseTime && (
          <p className="text-red-500 text-sm">{errors.activitiesThatMakeYouLoseTime.message}</p>
        )}
      </div>

      {/* Online Content */}
      <div>
        <label>Online Content You Enjoy</label>
        <select
          {...register("onlineContent")}
          className="input"
          onChange={(e) => setShowOther(prev => ({ ...prev, onlineContent: e.target.value === "Other" }))}
        >
          <option value="">Select</option>
          {onlineContentOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {showOther.onlineContent && (
          <input type="text" {...register("onlineContentOther")} placeholder="Your content" className="input mt-2" />
        )}
        {errors.onlineContent && <p className="text-red-500 text-sm">{errors.onlineContent.message}</p>}
      </div>

      {/* Areas You’d Like to Explore */}
      <div>
        <label>Areas You’d Like to Explore</label>
        <select
          {...register("exploreAreas")}
          className="input"
          onChange={(e) => setShowOther(prev => ({ ...prev, exploreAreas: e.target.value === "Other" }))}
        >
          <option value="">Select</option>
          {exploreAreasOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {showOther.exploreAreas && (
          <input type="text" {...register("exploreAreasOther")} placeholder="Your area" className="input mt-2" />
        )}
        {errors.exploreAreas && <p className="text-red-500 text-sm">{errors.exploreAreas.message}</p>}
      </div>

      {/* Preferred Role */}
      <div>
        <label>Preferred Role</label>
        <select
          {...register("preferredRole")}
          className="input"
          onChange={(e) => setShowOther(prev => ({ ...prev, preferredRole: e.target.value === "Other" }))}
        >
          <option value="">Select</option>
          {preferredRoleOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {showOther.preferredRole && (
          <input type="text" {...register("preferredRoleOther")} placeholder="Your role" className="input mt-2" />
        )}
        {errors.preferredRole && <p className="text-red-500 text-sm">{errors.preferredRole.message}</p>}
      </div>

      {/* Preferred Company */}
      <div>
        <label>Preferred Company Type</label>
        <select
          {...register("preferredCompany")}
          className="input"
          onChange={(e) => setShowOther(prev => ({ ...prev, preferredCompany: e.target.value === "Other" }))}
        >
          <option value="">Select</option>
          {preferredCompanyOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        {showOther.preferredCompany && (
          <input type="text" {...register("preferredCompanyOther")} placeholder="Your company type" className="input mt-2" />
        )}
        {errors.preferredCompany && <p className="text-red-500 text-sm">{errors.preferredCompany.message}</p>}
      </div>

      {/* Job Priorities */}
      <div>
        <label>Job Priorities</label>
        <div className="grid grid-cols-2 gap-2">
          {jobPrioritiesOptions.map(priority => (
            <label key={priority} className="flex items-center space-x-2">
              <input
                type="checkbox"
                value={priority}
                {...register("jobPriorities")}
                onChange={(e) =>
                  priority === "Other" ? setShowOther(prev => ({ ...prev, jobPriorities: e.target.checked })) : null
                }
                className="accent-indigo-600"
              />
              <span>{priority}</span>
            </label>
          ))}
        </div>
        {showOther.jobPriorities && (
          <input type="text" {...register("jobPrioritiesOther")} placeholder="Your priority" className="input mt-2" />
        )}
        {errors.jobPriorities && <p className="text-red-500 text-sm">{errors.jobPriorities.message}</p>}
      </div>
    </div>
  );
};

export default StepInterests;
