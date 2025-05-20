import { z } from "zod";

export const Interests = z.object({
  favoriteSubjects: z
    .string()
    .min(2, "Please enter at least one subject")
    .optional(),

  activitiesThatMakeYouLoseTime: z
    .string()
    .min(3, "This field is required")
    .optional(),

  onlineContent: z
    .string()
    .min(3, "Please specify some online content")
    .optional(),

  exploreAreas: z
    .string()
    .min(3, "Please mention at least one area")
    .optional(),

  preferredRole: z
    .string()
    .min(2, "Please specify your preferred role")
    .optional(),

  preferredCompany: z
    .string()
    .min(2, "Please describe your preferred company type")
    .optional(),

  jobPriorities: z
    .array(z.string())
    .min(1, "Please select at least one job priority")
    .optional(),
});
