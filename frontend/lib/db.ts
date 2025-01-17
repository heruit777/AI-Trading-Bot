import { prisma } from "@/prisma/prisma";
import bcryptjs from "bcryptjs";
// logic to verify if the user exists
export async function getUserFromDb(email: string, password: string) {
  try {
    const existedUser = await prisma.user.findFirst({
      where: { email: email },
    });

    if (!existedUser) {
      return {
        success: false,
        message: "User not found.",
      };
    }

    if (!existedUser.password) {
      return {
        success: false,
        message: "Password is required.",
      };
    }

    const isPasswordMatches = await bcryptjs.compare(
      password,
      existedUser.password
    );

    if (!isPasswordMatches) {
      return {
        success: false,
        message: "Password is incorrect.",
      };
    }

    return {
      success: true,
      data: existedUser,
    };
  } catch (error: any) {
    return {
      success: false,
      message: error.message,
    };
  }
}

// export async function hashPassword(password: string): Promise<string> {
//   try {
//     const hashedPassword = await hash(password);
//     return hashedPassword;
//   } catch (err) {
//     console.error("Error hashing password:", err);
//     throw new Error("Could not hash the password");
//   }
// }

// export async function verifyPassword(
//   hashedPassword: string,
//   plainPassword: string
// ): Promise<Boolean> {
//   try {
//     const isMatch = await verify(hashedPassword, plainPassword);
//     return isMatch;
//   } catch (err) {
//     console.error("Error verifying password:", err);
//     throw new Error("Could not verify the password");
//   }
// }
