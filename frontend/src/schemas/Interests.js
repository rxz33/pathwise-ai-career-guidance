import { z } from "zod";

export const Interests = z.object({
  // Favorite Subjects
  favoriteSubjects: z.string().optional(),
  favoriteSubjectsOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.favoriteSubjects !== "Other" || (val && val.trim().length > 0);
    }, "Please specify your subject"),

  // Activities That Make You Lose Track of Time
  activitiesThatMakeYouLoseTime: z.string().optional(),
  activitiesOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.activitiesThatMakeYouLoseTime !== "Other" || (val && val.trim().length > 0);
    }, "Please specify your activity"),

  // Online Content
  onlineContent: z.string().optional(),
  onlineContentOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.onlineContent !== "Other" || (val && val.trim().length > 0);
    }, "Please specify online content"),

  // Areas to Explore
  exploreAreas: z.string().optional(),
  exploreAreasOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.exploreAreas !== "Other" || (val && val.trim().length > 0);
    }, "Please specify area to explore"),

  // Preferred Role
  preferredRole: z.string().optional(),
  preferredRoleOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.preferredRole !== "Other" || (val && val.trim().length > 0);
    }, "Please specify your preferred role"),

  // Preferred Company
  preferredCompany: z.string().optional(),
  preferredCompanyOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return parent.preferredCompany !== "Other" || (val && val.trim().length > 0);
    }, "Please specify your preferred company type"),

  // Job Priorities
  jobPriorities: z.array(z.string()).optional(),
  jobPrioritiesOther: z.string().optional()
    .refine((val, ctx) => {
      const parent = ctx.parent;
      return !parent.jobPriorities?.includes("Other") || (val && val.trim().length > 0);
    }, "Please specify your job priority"),
});
