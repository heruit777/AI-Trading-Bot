import { PrismaClient } from "@prisma/client";
import {hash, verify} from "argon2";

const prisma = new PrismaClient();

// logic to verify if the user exists
export async function getUserFromDb(email: string) {
  const existingUser = await prisma.user.findUnique({
    where: {
      email
    },
  });
  return existingUser;
}

export async function hashPassword(password: string): Promise<string> {
  try {
    const hashedPassword = await hash(password);
    return hashedPassword;
  } catch (err) {
    console.error("Error hashing password:", err);
    throw new Error("Could not hash the password");
  }
}

export async function verifyPassword(
  hashedPassword: string,
  plainPassword: string
): Promise<Boolean> {
  try {
    const isMatch = await verify(hashedPassword, plainPassword);
    return isMatch;
  } catch (err) {
    console.error("Error verifying password:", err);
    throw new Error("Could not verify the password");
  }
}
