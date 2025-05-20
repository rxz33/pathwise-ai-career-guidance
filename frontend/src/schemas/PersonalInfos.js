import { z } from "zod";

export const PersonalInfos = z.object({
  fullName: z.string().min(1, "Full name is required"),

  age: z
    .number({ invalid_type_error: "Age is required" })
    .min(14, "Minimum age is 14")
    .max(80, "Maximum age is 80"),

  currentStatus: z.enum(
    ["Student", "Fresher", "Working Professional", "Career Break"],
    { required_error: "Current status is required" }
  ),

  fieldOfStudy: z.string().min(1, "Field of study is required"),

  educationLevel: z.enum(
    [
      "High School",
      "Diploma/Intermediate",
      "Undergraduate",
      "Postgraduate",
      "Doctorate",
      "Other",
    ],
    { required_error: "Education level is required" }
  ),

  mobility: z.enum(
    [
      "Willing to relocate",
      "Prefer hometown",
      "Depends on opportunity",
    ],
    { required_error: "Relocation preference is required" }
  ),

  financialStatus: z
    .number({ invalid_type_error: "Financial status must be a number" })
    .min(1, "Minimum value is 1")
    .max(10, "Maximum value is 10"),
});

export const defaultPersonalInfo = {
  fullName: "",
  age: undefined,
  currentStatus: "",
  fieldOfStudy: "",
  educationLevel: "",
  mobility: "",
  financialStatus: 5,
};
