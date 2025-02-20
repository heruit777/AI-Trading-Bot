"use server";
import { signIn, signOut } from "@/auth";
import { signinSchema } from "@/lib/zod";
import { prisma } from "@/prisma/prisma";
import bcryptjs from "bcryptjs";
import { AuthError } from "next-auth";

export async function handleGoogleSignin() {
  return await signIn("google", { redirectTo: "/dashboard" });
}

export async function handleGithubSignin() {
  return await signIn("github", { redirectTo: "/dashboard" });
}

export async function handleCredentialsSignin({
  email,
  password,
}: {
  email: string;
  password: string;
}) {
  try {
    return await signIn("credentials", {
      email,
      password,
      redirect: false,
    });
  } catch (error) {
    if (error instanceof AuthError) {
      switch (error.type) {
        case "CredentialsSignin":
          return {
            message: "Invalid credentials",
          };
        default:
          return {
            message: "Something went wrong.",
          };
      }
    }
    throw error;
  }
}

export async function handleSignout() {
  return await signOut({ redirectTo: "/" });
}

export async function handleSignUp({
  email,
  password,
}: {
  email: string;
  password: string;
}) {
  try {
    const parsedCredentials = signinSchema.safeParse({ email, password });
    if (!parsedCredentials.success) {
      return { success: false, message: "Invalid data." };
    }

    // check if the email is already taken
    const existingUser = await prisma.user.findUnique({
      where: {
        email,
      },
    });

    if (existingUser) {
      return {
        success: false,
        message: "Email already exists. Login to continue.",
      };
    }

    // hash the password
    const hashedPassword = await bcryptjs.hash(password, 10);
    await prisma.user.create({
      data: {
        email,
        password: hashedPassword,
      },
    });

    return { success: true, message: "Account created successfully." };
  } catch (error) {
    console.error("Error creating account:", error);
    return {
      success: false,
      message: "An unexpected error occurred. Please try again.",
    };
  }
}
