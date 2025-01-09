"use client";
import { signIn } from "next-auth/react";
import { Button } from "./button";
import SigninForm from "./signinForm";
import { handleGithubSignin, handleGoogleSignin } from "@/app/actions/authActions";

export default function LoginPage() {
  return (
    <div className="grid grid-cols-3 h-screen">
      <div className="flex items-center px-10">
        <div className="flex flex-col items-center justify-center text-4xl font-bold">
          Let's Automate Trading <span>🚀 🚀 🚀</span>
        </div>
      </div>
      <div className="border col-span-2 bg-[#191919] h-screen flex flex-col items-center justify-center">
        <div className="space-y-4">
          <div className="text-2xl font-bold">Login in to your Account</div>
          <div className="flex space-x-2">
            <Button
              className="grow"
              onClick={handleGoogleSignin} 
              >
              Google
            </Button>
            <Button
              className="grow"
              onClick={handleGithubSignin}
            >
              Github
            </Button>
          </div>
          <div className="flex items-center">
            <hr className="border-white border grow" />
            <div className="text-xs mx-2 text-gray-100">
              OR LOG IN WITH YOUR EMAIL
            </div>
            <hr className="border-white border grow" />
          </div>
          <div className="flex text-sm flex-col">
            <label className="mb-2 text-gray-400">Email</label>
            <input
              type="text"
              className="p-2 rounded-lg bg-[#1c1c1c] border-2"
            />
          </div>
          <div className="flex flex-col">
            <div className="flex justify-between items-end align-bottom mb-2 text-gray-400">
              <label className="text-sm">Password</label>
              <div className="text-blue-600 font-semibold text-xs">
                Forget Password?
              </div>
            </div>
            <input
              type="password"
              className="p-2 rounded-lg bg-[#1c1c1c] border-2"
            />
          </div>
          <Button className="w-full">Log in</Button>
          <div className="text-sm flex justify-between items-end">
            <div className="mr-2">New to AI Trading Bot?</div>
            <div className="text-blue-600 font-semibold">
              Sign up for an account
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
