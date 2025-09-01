import React from "react";
import { useFormContext } from "react-hook-form";
import { Country, State, City } from "country-state-city";

const Step1 = () => {
  const {
    register,
    setValue,
    watch,
    formState: { errors },
  } = useFormContext();

  const countryCode = watch("country");
  const stateCode = watch("state");

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-800">
        Basic Identity & Context
      </h2>

      {/* Full Name */}
      <div>
        <label className="block mb-1">Full Name</label>
        <input type="text" {...register("fullName")} className="input" />
        {errors.fullName && (
          <p className="text-red-500 text-sm">
            {errors.fullName.message}
          </p>
        )}
      </div>

      {/* Age */}
      <div>
        <label className="block mb-1">Age</label>
        <input
          type="number"
          {...register("age", { valueAsNumber: true })}
          className="input"
        />
        {errors.age && (
          <p className="text-red-500 text-sm">{errors.age.message}</p>
        )}
      </div>

      {/* Current Status */}
      <div>
        <label className="block mb-1">Current Status</label>
        <select {...register("currentStatus")} className="input">
          <option value="">Select</option>
          <option value="Student">Student</option>
          <option value="Fresher">Fresher</option>
          <option value="Working Professional">
            Working Professional
          </option>
          <option value="Career Break">Career Break</option>
        </select>
        {errors.currentStatus && (
          <p className="text-red-500 text-sm">
            {errors.currentStatus.message}
          </p>
        )}
      </div>

      {/* Field of Study */}
      <div>
        <label className="block mb-1">Field of Study / Major</label>
        <input type="text" {...register("fieldOfStudy")} className="input" />
        {errors.fieldOfStudy && (
          <p className="text-red-500 text-sm">
            {errors.fieldOfStudy.message}
          </p>
        )}
      </div>

      {/* Education Level */}
      <div>
        <label className="block mb-1">Current Education Level</label>
        <select {...register("educationLevel")} className="input">
          <option value="">Select</option>
          <option value="High School">High School</option>
          <option value="Diploma/Intermediate">
            Diploma/Intermediate
          </option>
          <option value="Undergraduate">Undergraduate</option>
          <option value="Postgraduate">Postgraduate</option>
          <option value="Doctorate">Doctorate</option>
          <option value="Other">Other</option>
        </select>
        {errors.educationLevel && (
          <p className="text-red-500 text-sm">
            {errors.educationLevel.message}
          </p>
        )}
      </div>

      {/* Willingness to Relocate */}
      <div>
        <label className="block mb-1">Willingness to Relocate</label>
        <select {...register("mobility")} className="input">
          <option value="">Select</option>
          <option value="Willing to relocate">Willing to relocate</option>
          <option value="Prefer hometown">Prefer hometown</option>
          <option value="Depends on opportunity">
            Depends on opportunity
          </option>
        </select>
        {errors.mobility && (
          <p className="text-red-500 text-sm">
            {errors.mobility.message}
          </p>
        )}
      </div>

      {/* Financial Status */}
      <div>
        <label className="block mb-1">Financial Status</label>
        <select {...register("financialStatus")} className="input">
          <option value="">Select</option>
          <option value="Lower Class">Lower Class</option>
          <option value="Middle Class">Middle Class</option>
          <option value="Upper Class">Upper Class</option>
        </select>
        {errors.financialStatus && (
          <p className="text-red-500 text-sm">
            {errors.financialStatus.message}
          </p>
        )}
      </div>

      {/* 🌍 Location Section */}
      <div>
        <label className="block mb-1">Country</label>
        <select
          {...register("country")}
          className="input"
          onChange={(e) => {
            setValue("country", e.target.value);
            setValue("state", "");
            setValue("city", "");
          }}
        >
          <option value="">Select Country</option>
          {Country.getAllCountries().map((c) => (
            <option key={c.isoCode} value={c.isoCode}>
              {c.name}
            </option>
          ))}
        </select>
        {errors.country && (
          <p className="text-red-500 text-sm">
            {errors.country.message}
          </p>
        )}
      </div>

      <div>
        <label className="block mb-1">State</label>
        <select
          {...register("state")}
          className="input"
          disabled={!countryCode}
          onChange={(e) => {
            setValue("state", e.target.value);
            setValue("city", "");
          }}
        >
          <option value="">Select State</option>
          {countryCode &&
            State.getStatesOfCountry(countryCode).map((s) => (
              <option key={s.isoCode} value={s.isoCode}>
                {s.name}
              </option>
            ))}
        </select>
        {errors.state && (
          <p className="text-red-500 text-sm">{errors.state.message}</p>
        )}
      </div>

      <div>
        <label className="block mb-1">City</label>
        <select
          {...register("city")}
          className="input"
          disabled={!stateCode}
        >
          <option value="">Select City</option>
          {countryCode &&
            stateCode &&
            City.getCitiesOfState(countryCode, stateCode).map((city) => (
              <option key={city.name} value={city.name}>
                {city.name}
              </option>
            ))}
        </select>
        {errors.city && (
          <p className="text-red-500 text-sm">{errors.city.message}</p>
        )}
      </div>
    </div>
  );
};

export default Step1;
