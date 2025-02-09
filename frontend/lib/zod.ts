import { object, string } from "zod";

export const signinSchema = object({
  email: string({ required_error: "Email is required" }).email("Invalid email"),
  password: string({ required_error: "Password is required" })
    .min(1, "Password is required")
    .min(8, "Password must be more than 8 characters")
    .max(32, "Password must be less than 32 characters"),
});

export const settingSchema = object({
  brokerType: string().min(1, "Select a broker type"),
  accessToken: string().optional(), 
  apiKey: string().optional(),
  apiSecret: string().optional(),
}).refine(
  (data) => {
    if (data.brokerType !== "dummy") {
      return data.apiKey && data.apiSecret && data.accessToken;
    }
    return true;
  },
  {
    message: "API Key, API Secret, and Access Token are required",
    path: ["apiKey"], // You can set this to a different path, like "brokerType", to show a general message
  }
);

export const loginSchema = signinSchema;
