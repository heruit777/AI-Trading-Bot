"use server"
import { signIn, signOut,  } from "@/auth"
import { AuthError } from "next-auth"

export async function handleGoogleSignin(loginType: "signup" | "login"){
    await signIn('google', {redirectTo: '/', loginType})
}

export async function handleGithubSignin(loginType: "signup" | "login"){
    await signIn('github', {redirectTo: '/', loginType})
}

export async function handleCredentialsSignin({ email, password, loginType }: {
    email: string,
    password: string,
    loginType: "signup" | "login"
}) {
    try {
        return await signIn("credentials", { email, password, redirectTo: "/", loginType });
    } catch (error) {
        if (error instanceof AuthError) {
            switch (error.type) {
                case 'CredentialsSignin':
                    return {
                        message: 'Invalid credentials',
                    }
                default:
                    return {
                        message: 'Something went wrong.',
                    }
            }
        }
        throw error;
    }
}

export async function handleSignout(){
    await signOut()
}