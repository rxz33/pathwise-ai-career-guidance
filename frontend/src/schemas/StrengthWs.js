import { z } from "zod";

export const StrengthWs = z.object({
  // Strengths
  strengths: z.string().optional(),
  strengthsOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.strengths !== "Other" || (val && val.trim().length > 0);
    }, "Please specify your strength"),

  // Struggles
  struggleWith: z.string().optional(),
  struggleWithOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.struggleWith !== "Other" || (val && val.trim().length > 0);
    }, "Please specify your struggle area"),

  // Confidence
  confidenceLevel: z.number().min(1).max(10).optional(),

  // Tools / Tech
  toolsTechUsed: z.string().optional(),
  toolsTechOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.toolsTechUsed !== "Other" || (val && val.trim().length > 0);
    }, "Please specify the tool/technology"),

  // Internship / Project
  internshipOrProject: z.string().optional(),
  internshipOther: z.string().optional(),

  // Learnings
  whatDidYouLearn: z.string().optional(),
  learningOther: z.string().optional(),

  // Related to Career
  relatedToCareer: z.string().optional(),

  // Resume Section
  hasResume: z.string().optional(),
  resumeFile: z
    .any()
    .optional()
    .refine((file, ctx) => {
      const parent = ctx.parent;
      // Only require file if "Yes" is selected
      return parent.hasResume !== "Yes" || file;
    }, "Please upload your resume"),
});
