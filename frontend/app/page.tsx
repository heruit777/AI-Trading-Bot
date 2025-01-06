import { Button } from "@/components/ui/button";
import Navbar from "@/components/ui/navbar";

export default function Home() {
  return (
    <div className="h-screen flex flex-col">
      <Navbar />
      <div className="flex flex-col items-center h-full space-y-6 text-center">
        <div className="text-5xl font-extrabold w-1/2 mt-40">
          Automate Your Trading. Maximize Your Returns.
        </div>
        <div className="text-gray-400 w-1/2 px-8 text-xl">
          AI-powered trading bot that analyzes the market, executes trades and
          manages risk - so you don't have to 🎉🎉
        </div>
        <Button variant={"default"}>Get Started Now</Button>
      </div>
    </div>
  );
}
