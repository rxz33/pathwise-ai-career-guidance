import { z } from "zod";

export const PersonalInfos = z.object({
  fullName: z.string().min(1, "Full name is required").optional(),

  age: z
    .coerce
    .number({ invalid_type_error: "Age is required" })
    .min(14, "Minimum age is 14")
    .max(80, "Maximum age is 80")
    .optional(),

  currentStatus: z
    .enum(["Student", "Fresher", "Working Professional", "Career Break"], {
      required_error: "Current status is required",
    })
    .optional(),

  fieldOfStudy: z.string().min(1, "Field of study is required").optional(),

  educationLevel: z
    .enum(
      [
        "High School",
        "Diploma/Intermediate",
        "Undergraduate",
        "Postgraduate",
        "Doctorate",
        "Other",
      ],
      { required_error: "Education level is required" }
    )
    .optional(),

  mobility: z
    .enum(
      ["Willing to relocate", "Prefer hometown", "Depends on opportunity"],
      { required_error: "Relocation preference is required" }
    )
    .optional(),

  financialStatus: z
    .enum(["Lower Class", "Middle Class", "Upper Class"], {
      required_error: "Financial Status is required",
    })
    .optional(),

  // 🌍 Location
  country: z.string().min(1, "Country is required").optional(),
  state: z.string().min(1, "State is required").optional(),
  city: z.string().min(1, "City is required").optional(),
});

export const defaultPersonalInfo = {
  fullName: "",
  age: undefined,
  currentStatus: "",
  fieldOfStudy: "",
  educationLevel: "",
  mobility: "",
  financialStatus: "",
  country: "",
  state: "",
  city: "",
};
