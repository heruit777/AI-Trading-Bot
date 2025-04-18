import Link from "next/link";
import { Button } from "./button";
import LoginForm from "./loginForm";
import {
  handleGithubSignin,
  handleGoogleSignin,
} from "@/app/actions/authActions";
import { ArrowLeft } from "lucide-react";
import SigninForm from "./SigninForm";
import GithubButton from "./githubButton";

export default function SignupPage() {
  return (
    <div className="grid grid-cols-3 h-screen">
      <div className="flex items-center px-10">
        <div className="flex flex-col items-center justify-center text-4xl font-bold">
          Let's Automate Trading <span>🚀 🚀 🚀</span>
        </div>
      </div>
      <Link
        href="/"
        className="flex items-center px-3 py-1 absolute border border-gray-500 space-x-1 rounded-lg left-[35em] top-10"
      >
        <ArrowLeft className="w-5 text-primary" />
        <div className="text-primary text-sm">Home</div>
      </Link>
      <div className="border col-span-2 bg-primary-foreground h-screen flex flex-col items-center justify-center">
        <div className="space-y-4">
          <div className="text-2xl font-bold">Create your Account for free</div>
          <div className="flex space-x-2">
            <Button className="grow" onClick={handleGoogleSignin}>
              <svg
                enableBackground="new 0 0 128 128"
                id="Social_Icons"
                version="1.1"
                viewBox="0 0 128 128"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g id="_x31__stroke">
                  <g id="Google">
                    <rect
                      clipRule="evenodd"
                      fill="none"
                      fillRule="evenodd"
                      height="128"
                      width="128"
                    />
                    <path
                      clipRule="evenodd"
                      d="M27.585,64c0-4.157,0.69-8.143,1.923-11.881L7.938,35.648    C3.734,44.183,1.366,53.801,1.366,64c0,10.191,2.366,19.802,6.563,28.332l21.558-16.503C28.266,72.108,27.585,68.137,27.585,64"
                      fill="#FBBC05"
                      fillRule="evenodd"
                    />
                    <path
                      clipRule="evenodd"
                      d="M65.457,26.182c9.031,0,17.188,3.2,23.597,8.436L107.698,16    C96.337,6.109,81.771,0,65.457,0C40.129,0,18.361,14.484,7.938,35.648l21.569,16.471C34.477,37.033,48.644,26.182,65.457,26.182"
                      fill="#EA4335"
                      fillRule="evenodd"
                    />
                    <path
                      clipRule="evenodd"
                      d="M65.457,101.818c-16.812,0-30.979-10.851-35.949-25.937    L7.938,92.349C18.361,113.516,40.129,128,65.457,128c15.632,0,30.557-5.551,41.758-15.951L86.741,96.221    C80.964,99.86,73.689,101.818,65.457,101.818"
                      fill="#34A853"
                      fillRule="evenodd"
                    />
                    <path
                      clipRule="evenodd"
                      d="M126.634,64c0-3.782-0.583-7.855-1.457-11.636H65.457v24.727    h34.376c-1.719,8.431-6.397,14.912-13.092,19.13l20.474,15.828C118.981,101.129,126.634,84.861,126.634,64"
                      fill="#4285F4"
                      fillRule="evenodd"
                    />
                  </g>
                </g>
              </svg>
              Google
            </Button>
            <GithubButton />
          </div>
          <div className="flex items-center">
            <hr className="border-white border grow" />
            <div className="text-xs mx-2 text-gray-100">
              OR CONTINUE WITH EMAIL
            </div>
            <hr className="border-white border grow" />
          </div>
          <SigninForm />
          <div className="text-sm flex items-end">
            <div className="mr-2">Already have an account?</div>
            <Link href="/login">
              <div className="text-blue-600 font-semibold">Login in</div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
