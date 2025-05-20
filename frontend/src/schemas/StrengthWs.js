import { z } from "zod";

export const StrengthWs = z.object({
  strengths: z
    .string()
    .min(2, "Please list at least one strength")
    .optional(),

  struggleWith: z
    .string()
    .min(2, "Please mention at least one struggle area")
    .optional(),

  confidenceLevel: z
    .number()
    .min(1, "Minimum value is 1")
    .max(10, "Maximum value is 10")
    .optional(),

  toolsTechUsed: z
    .string()
    .min(2, "Please mention tools or technologies")
    .optional(),

  internshipOrProject: z
    .string()
    .min(3, "Please describe your internship/project")
    .optional(),

  whatDidYouLearn: z
    .string()
    .min(3, "Please describe what you learned")
    .optional(),

  relatedToCareer: z
    .enum(["Yes", "No"])
    .optional(),
});
