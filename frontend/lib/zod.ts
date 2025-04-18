import { number, object, string } from "zod";

export const signinSchema = object({
  email: string({ required_error: "Email is required" }).email("Invalid email"),
  password: string({ required_error: "Password is required" })
    .min(1, "Password is required")
    .min(8, "Password must be >=8 characters")
    .max(32, "Password must be less than 32 characters"),
});

export const settingSchema = object({
  brokerType: string().min(1, "Select a broker type"),
  accessToken: string().optional(),
  apiKey: string().optional(),
  apiSecret: string().optional(),
  balance: number().min(0, "Balance cannot be negative").optional(),
}).superRefine((data, ctx) => {
  if (data.brokerType === "dummy" && data.balance === undefined) {
    ctx.addIssue({
      code: "custom",
      message: "Please provide balance amount for your demo account",
      path: ["balance"],
    });
  }

  if (data.brokerType !== "dummy") {
    if (!data.accessToken?.trim()) {
      ctx.addIssue({
        code: "custom",
        message:
          "Please provide an Access token. Click on the button to get it.",
        path: ["accessToken"],
      });
    }

    if (!data.apiKey?.trim()) {
      ctx.addIssue({
        code: "custom",
        message: "Please provide an API Key",
        path: ["apiKey"],
      });
    }

    if (!data.apiSecret?.trim()) {
      ctx.addIssue({
        code: "custom",
        message: "Please provide an API Secret",
        path: ["apiSecret"],
      });
    }
  }
});

export const loginSchema = signinSchema;
