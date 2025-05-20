import { z } from "zod";

export const LearningRoadmaps = z.object({
  studyPlan: z
    .string()
    .min(2, "Please specify your study plan")
    .optional(),

  preferredLearning: z
    .array(z.string())
    .optional(),

  openToExplore: z
    .enum(["Yes", "No"])
    .optional(),

  riskTaking: z
    .enum(["Low", "Medium", "High"])
    .optional(),
});
