import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import Credentials from "next-auth/providers/credentials";
import { loginSchema } from "./lib/zod";
import { ZodError } from "zod";
import { PrismaClient } from "@prisma/client";
import { getUserFromDb, hashPassword } from "./lib/db";

const prisma = new PrismaClient();

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google,
    GitHub,
    Credentials({
      credentials: {
        email: { label: "Email", type: "email", placeholder: "Email" },
        password: {
          label: "Password",
          type: "password",
          placeholder: "Password",
        },
      },
      authorize: async (credentials) => {
        return true;
        try {
          //Server Side validation using Zod
          const { success, data } = loginSchema.safeParse(credentials);
          if (!success) {
            return false;
          }
          const { email, password } = data;
          // logic to verify if the user exists
          const user = await getUserFromDb(email);

          // const loginType = account?.loginType;

          // logic to salt and hash password
          const pwHash = await hashPassword(password);

          // demo purpose
          // user = {
          //   id: "1",
          //   email,
          //   password,
          // };

          if (!user) {
            // No user found, so this is their first attempt to login
            // Optionally, this is also the place you could do a user registration
            //   throw new Error("Invalid credentials.")
            return null;
          }
          // return user object with their profile data
          console.log(user);
          return user;
        } catch (error) {
          if (error instanceof ZodError) {
            return null;
          }
          throw new Error("Some error occured " + error);
        }
      },
    }),
  ],
  callbacks: {
    //SignIn for OAuth
    async signIn({ user, account }) {
      const loginType = account?.loginType;

      if (account?.provider !== "credentails") {
        // check if email already exists and check the validity of the email
        if (!user.email) {
          return false;
        }

        const existingUser = await getUserFromDb(user.email);

        if (loginType === "signup") {
          // user is registering for the first time
          if (existingUser) return false;
          // create the user
          await prisma.user.create({
            data: {
              email: user.email,
              provider: account?.provider,
            },
          });
        } else if (loginType === "login") {
          if (!existingUser) return false;
        }
      }

      return true;
    },
  },
});
