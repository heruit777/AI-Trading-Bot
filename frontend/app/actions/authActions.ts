"use server"
import { signIn } from "@/auth"

export async function handleGoogleSignin(){
    await signIn('google', {redirectTo: '/'})
}

export async function handleGithubSignin(){
    await signIn('github', {redirectTo: '/'})
}