import NextAuth, { NextAuthConfig, User } from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import Credentials from "next-auth/providers/credentials";
import { encode as defaultEncode } from "next-auth/jwt";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "./prisma/prisma";
import { v4 as uuid } from "uuid";
import { getUserFromDb } from "./lib/db";
import authConfig from "./auth.config";


export const { handlers, signIn, signOut, auth } = NextAuth({
    adapter: PrismaAdapter(prisma),
    session: {
        strategy: "jwt",
    },
    ...authConfig
})

// const adapter = PrismaAdapter(prisma);

// const authConfig: NextAuthConfig = {
//   adapter,
//   session: {
//     strategy: "jwt",
//   },
//   providers: [
//     Google,
//     GitHub,
//     Credentials({
//       credentials: {
//         email: {},
//         password: {},
//       },
//       async authorize(credentials) {
//         console.log("Authorize callback called --------");
//         const { email, password } = credentials;

//         const res = await getUserFromDb(email as string, password as string);
//         if (res.success) {
//           return res.data as User;
//         }
//         return null;
//       },
//     }),
//   ],
//   callbacks: {
//     async jwt({ token, user, account }) {
//       console.log("jwt callback called --------");
//       if (account?.provider === "credentials") {
//         token.credentials = true;
//       }
//       return token;
//     },
//   },
//   jwt: {
//     encode: async function (params) {
//       console.log("jwt encode callback called --------");
//       if (params.token?.credentials) {
//         const sessionToken = uuid();

//         if (!params.token.sub) {
//           throw new Error("No user ID found in token");
//         }

//         const createdSession = await adapter?.createSession?.({
//           sessionToken: sessionToken,
//           userId: params.token.sub,
//           expires: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
//         });

//         if (!createdSession) {
//           throw new Error("Failed to create session");
//         }

//         return sessionToken;
//       }
//       return defaultEncode(params);
//     },
//   },
//   secret: process.env.AUTH_SECRET!,
// };

// export const { handlers, signIn, signOut, auth } = NextAuth(authConfig);

// export const { handlers, signIn, signOut, auth } = NextAuth({
//   providers: [
//     Google,
//     GitHub,
//     Credentials({
//       credentials: {
//         email: { label: "Email", type: "email", placeholder: "Email" },
//         password: {
//           label: "Password",
//           type: "password",
//           placeholder: "Password",
//         },
//       },
//       authorize: async (credentials) => {
//         return true;
//         try {
//           //Server Side validation using Zod
//           const { success, data } = loginSchema.safeParse(credentials);
//           if (!success) {
//             return false;
//           }
//           const { email, password } = data;
//           // logic to verify if the user exists
//           const user = await getUserFromDb(email);

//           // const loginType = account?.loginType;

//           // logic to salt and hash password
//           const pwHash = await hashPassword(password);

//           // demo purpose
//           // user = {
//           //   id: "1",
//           //   email,
//           //   password,
//           // };

//           if (!user) {
//             // No user found, so this is their first attempt to login
//             // Optionally, this is also the place you could do a user registration
//             //   throw new Error("Invalid credentials.")
//             return null;
//           }
//           // return user object with their profile data
//           console.log(user);
//           return user;
//         } catch (error) {
//           if (error instanceof ZodError) {
//             return null;
//           }
//           throw new Error("Some error occured " + error);
//         }
//       },
//     }),
//   ],
//   callbacks: {
//     //SignIn for OAuth
//     async signIn({ user, account }) {
//       const loginType = account?.loginType;

//       if (account?.provider !== "credentails") {
//         // check if email already exists and check the validity of the email
//         if (!user.email) {
//           return false;
//         }

//         const existingUser = await getUserFromDb(user.email);

//         if (loginType === "signup") {
//           // user is registering for the first time
//           if (existingUser) return false;
//           // create the user
//           await prisma.user.create({
//             data: {
//               email: user.email,
//               provider: account?.provider,
//             },
//           });
//         } else if (loginType === "login") {
//           if (!existingUser) return false;
//         }
//       }

//       return true;
//     },
//   },
// });
