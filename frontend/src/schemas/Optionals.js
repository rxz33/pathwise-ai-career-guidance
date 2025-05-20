import { z } from "zod";

export const Optionals = z
  .object({
    currentRole: z.string().optional().or(z.literal("")),

    yearsOfExperience: z
      .union([
        z
          .string()
          .refine(
            (val) =>
              val === "" ||
              (!isNaN(Number(val)) && Number(val) >= 0 && Number(val) <= 50),
            { message: "Please enter a valid experience between 0 and 50" }
          )
          .transform((val) => (val === "" ? undefined : Number(val))),
        z.undefined(),
      ]),

    leadershipRole: z.enum(["Yes", "No"]).optional().or(z.literal("")),

    leadershipSkill: z.string().optional().or(z.literal("")),
  })
  .superRefine((data, ctx) => {
    if (data.leadershipRole === "Yes" && !data.leadershipSkill?.trim()) {
      ctx.addIssue({
        path: ["leadershipSkill"],
        code: z.ZodIssueCode.custom,
        message: "Please describe your leadership skill.",
      });
    }
  });
