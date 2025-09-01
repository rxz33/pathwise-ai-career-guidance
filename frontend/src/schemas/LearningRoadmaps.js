import { z } from "zod";

export const LearningRoadmaps = z.object({
  // Study Plan
  studyPlan: z.string().optional(),
  studyPlanOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.studyPlan !== "Other" || (val && val.trim().length > 0);
    }, "Please specify your study plan"),

  // Preferred Learning Mode
  preferredLearning: z.string().optional(),
  preferredLearningOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.preferredLearning !== "Other" || (val && val.trim().length > 0);
    }, "Please specify your preferred learning mode"),

  // Open to Explore New Fields
  openToExplore: z.string().optional(),
  openToExploreOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.openToExplore !== "Other" || (val && val.trim().length > 0);
    }, "Please specify"),

  // Risk Taking Level
  riskTaking: z.string().optional(),
  riskTakingOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.riskTaking !== "Other" || (val && val.trim().length > 0);
    }, "Please specify your risk level"),
});
