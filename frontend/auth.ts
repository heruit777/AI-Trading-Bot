import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import Credentials from "next-auth/providers/credentials";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [Google, GitHub, Credentials({
    credentials: {
        email: {label: "Email", type: "email", placeholder: "Email"},
        password: {label: "Password", type: "password", placeholder: "Password"},
    },
    authorize: async (credentials) => {
        let user = null;

        // logic to salt and hash password
        // const pwHash = saltAndHashPassword(credentials.password)
 
        // logic to verify if the user exists
        // user = await getUserFromDb(credentials.email, pwHash)
        
        // demo purpose
        // user = {
        //     id: '1',
        //     name: 'harsh nivande',
        //     email: 'harshnivande@gmail.com'
        // }

        if (!user) {
          // No user found, so this is their first attempt to login
          // Optionally, this is also the place you could do a user registration
        //   throw new Error("Invalid credentials.")
            return null
        }
        // return user object with their profile data
        return user
    }
  })],
  callbacks: {

  }
});
