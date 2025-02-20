import Credentials from "next-auth/providers/credentials";
import Github, { GitHubProfile } from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import { signinSchema } from "./lib/zod";
import { prisma } from "./prisma/prisma";

import bcryptjs from "bcryptjs";
import { NextAuthConfig } from "next-auth";

export default {
  providers: [
    Google({
      allowDangerousEmailAccountLinking: true,
    }),
    Github({
      allowDangerousEmailAccountLinking: true,
      profile: (profile: GitHubProfile) => {
        const name = profile.name?.split(" ");
        return {
          id: profile.id.toString(), // Ensure the 'id' is returned
          firstName: name?.[0] ?? "unknown",
          lastName: name?.[1],
          email: profile.email,
          image: profile.avatar_url,
          username: profile.login,
        };
      },
    }),
    Credentials({
      credentials: {
        email: { label: "Email", type: "email", placeholder: "Email" },
        password: {
          label: "Password",
          type: "password",
          placeholder: "Password",
        },
      },
      async authorize(credentials) {
        let user = null;

        // validate credentials
        const parsedCredentials = signinSchema.safeParse(credentials);
        if (!parsedCredentials.success) {
          console.error("Invalid credentials:", parsedCredentials.error.errors);
          return null;
        }
        // get user

        user = await prisma.user.findUnique({
          where: {
            email: credentials.email as string,
          },
        });

        if (!user) {
          console.log("Invalid credentials");
          return null;
        }

        if (!user.password) {
          console.log(
            "User has no password. They probably signed up with an oauth provider."
          );
          return null;
        }

        const isPasswordValid = await bcryptjs.compare(
          credentials.password as string,
          user.password
        );
        if (!isPasswordValid) {
          console.log("Invalid password");
          return null;
        }

        const { password, ...userWithoutPassword } = user;
        return userWithoutPassword;
      },
    }),
  ],
  callbacks: {
    jwt({ token, user, trigger, session }) {
      if (user) {
        token.id = user.id as string;
      }
      if (trigger === "update" && session) {
        token = { ...token, ...session };
      }
      return token;
    },
    session({ session, token }) {
      session.user.id = token.id as string;
      return session;
    },
  },
  pages: {
    signIn: "/signup",
  },
} satisfies NextAuthConfig;
