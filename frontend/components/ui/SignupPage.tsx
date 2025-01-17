import Link from "next/link";
import { Button } from "./button";
import LoginForm from "./loginForm";
import {
  handleGithubSignin,
  handleGoogleSignin,
} from "@/app/actions/authActions";
import { ArrowLeft } from "lucide-react";
import SigninForm from "./SigninForm";

export default function SignupPage() {
  const handleGoogleSignup = handleGoogleSignin.bind(null, "signup")
  const handleGithubSignup = handleGithubSignin.bind(null, "signup")
  return (
    <div className="grid grid-cols-3 h-screen">
      <div className="flex items-center px-10">
        <div className="flex flex-col items-center justify-center text-4xl font-bold">
          Let's Automate Trading <span>🚀 🚀 🚀</span>
        </div>
      </div>
      <Link
        href="/"
        className="flex items-center px-3 py-1 absolute border border-gray-500 space-x-1 rounded-lg left-[35em] top-10 hover:bg-[#2e2e2e]"
      >
        <ArrowLeft className="w-5 text-gray-300" />
        <div className="text-gray-200 text-sm">Home</div>
      </Link>
      <div className="border col-span-2 bg-[#191919] h-screen flex flex-col items-center justify-center">
        <div className="space-y-4">
          <div className="text-2xl font-bold">Create your Account for free</div>
          <div className="flex space-x-2">
            <Button className="grow" onClick={handleGoogleSignup}>
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
            <Button className="grow" onClick={handleGithubSignup}>
              <svg
                enableBackground="new -1163 1657.697 56.693 56.693"
                height="56.693px"
                id="Layer_1"
                version="1.1"
                viewBox="-1163 1657.697 56.693 56.693"
                width="56.693px"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g>
                  <path
                    clipRule="evenodd"
                    d="M-1134.6598,1662.9163c-13.601,0-24.63,11.0267-24.63,24.6299   c0,10.8821,7.0573,20.1144,16.8435,23.3713c1.2308,0.2279,1.6829-0.5345,1.6829-1.1849c0-0.587-0.0227-2.5276-0.0334-4.5857   c-6.8521,1.4901-8.2979-2.906-8.2979-2.906c-1.1205-2.8467-2.7347-3.6039-2.7347-3.6039   c-2.2349-1.5287,0.1685-1.4972,0.1685-1.4972c2.473,0.1737,3.7755,2.5385,3.7755,2.5385c2.1967,3.7651,5.7618,2.6765,7.1675,2.0472   c0.2211-1.5917,0.8591-2.6786,1.5637-3.2936c-5.4707-0.6226-11.2218-2.7347-11.2218-12.1722c0-2.6888,0.9623-4.8861,2.538-6.611   c-0.2557-0.6206-1.0989-3.1255,0.2386-6.5183c0,0,2.0684-0.6616,6.7747,2.525c1.9648-0.5458,4.0719-0.8195,6.165-0.829   c2.093,0.0095,4.2017,0.2832,6.17,0.829c4.7012-3.1866,6.7665-2.525,6.7665-2.525c1.3406,3.3928,0.4974,5.8977,0.2417,6.5183   c1.5793,1.7249,2.5348,3.9221,2.5348,6.611c0,9.4602-5.7618,11.5428-11.2465,12.1527c0.8834,0.7644,1.6704,2.2632,1.6704,4.561   c0,3.2955-0.0282,5.9479-0.0282,6.7592c0,0.6556,0.4432,1.4236,1.6915,1.1818c9.7812-3.2605,16.8296-12.4896,16.8296-23.3682   C-1110.0299,1673.943-1121.0574,1662.9163-1134.6598,1662.9163z"
                    fillRule="evenodd"
                  />
                  <path d="M-1149.9611,1698.2793c-0.0542,0.1227-0.2469,0.1593-0.4222,0.0753c-0.1788-0.0804-0.2788-0.2473-0.2211-0.37   c0.053-0.126,0.2457-0.161,0.4242-0.0769C-1150.0013,1697.9882-1149.8993,1698.1566-1149.9611,1698.2793L-1149.9611,1698.2793z    M-1150.2642,1698.0547" />
                  <path d="M-1148.9634,1699.3922c-0.1174,0.1086-0.3473,0.0581-0.5031-0.1139c-0.1613-0.1718-0.1912-0.4016-0.072-0.5118   c0.1211-0.1088,0.3438-0.0579,0.505,0.1139C-1148.8721,1699.0541-1148.8407,1699.2819-1148.9634,1699.3922L-1148.9634,1699.3922z    M-1149.1984,1699.14" />
                  <path d="M-1147.9922,1700.8105c-0.151,0.1051-0.3979,0.0067-0.5505-0.2123c-0.151-0.2191-0.151-0.4819,0.0035-0.5872   c0.1526-0.1051,0.396-0.0104,0.5505,0.2068C-1147.8381,1700.4406-1147.8381,1700.7034-1147.9922,1700.8105L-1147.9922,1700.8105z    M-1147.9922,1700.8105" />
                  <path d="M-1146.6619,1702.1812c-0.1351,0.1489-0.4227,0.1086-0.6329-0.0945c-0.2155-0.1984-0.2753-0.4803-0.1403-0.6293   c0.1371-0.149,0.4263-0.1072,0.6381,0.0944C-1146.5831,1701.7501-1146.5182,1702.0337-1146.6619,1702.1812L-1146.6619,1702.1812z    M-1146.6619,1702.1812" />
                  <path d="M-1144.8265,1702.9769c-0.0597,0.1927-0.3365,0.2804-0.6154,0.1984c-0.2788-0.0845-0.4608-0.3103-0.4047-0.5051   c0.0577-0.1943,0.3361-0.2855,0.6169-0.1979C-1144.9512,1702.5563-1144.7688,1702.7805-1144.8265,1702.9769L-1144.8265,1702.9769z    M-1144.8265,1702.9769" />
                  <path d="M-1142.8107,1703.1243c0.0067,0.2031-0.2299,0.3716-0.5226,0.3752c-0.2944,0.0067-0.533-0.1577-0.5361-0.3577   c0-0.2052,0.2313-0.3717,0.5258-0.3768C-1143.0509,1702.7594-1142.8107,1702.9227-1142.8107,1703.1243L-1142.8107,1703.1243z    M-1142.8107,1703.1243" />
                  <path d="M-1140.9351,1702.8052c0.035,0.198-0.1686,0.4015-0.4594,0.4557c-0.2859,0.0526-0.5504-0.0701-0.587-0.2665   c-0.0354-0.2031,0.1716-0.4066,0.4573-0.4592C-1141.233,1702.4846-1140.9722,1702.6036-1140.9351,1702.8052L-1140.9351,1702.8052z    M-1140.9351,1702.8052" />
                </g>
              </svg>
              Github
            </Button>
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
