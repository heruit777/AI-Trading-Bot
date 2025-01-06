import Link from "next/link";
import { ModeToggle } from "./modeToggle";
import { AlignJustifyIcon } from "lucide-react";
import { Button } from "./button";

export default function Navbar() {
  return (
    <div className="flex justify-between items-center boder border-b-2 h-16 px-4 text-base">
      <div className="flex items-center space-x-5">
        <AlignJustifyIcon
          className="hover:cursor-pointer md:hidden"
        />
        <div className="md:text-2xl">AI Trading Bot</div>
      </div>
      <div className="flex justify-around items-center space-x-8">
        {/* Can add icons here for the mobile */}
        <div className="hidden md:text-base md:text-gray-300 md:flex md:justify-around md:space-x-2">
          <Link href="/docs1" className="hover:underline">About</Link>
          <Link href="/docs1" className="hover:underline">Broker Support</Link>
        </div>
        <div className="hidden sm:block sm:space-x-4">
            <Button>Log in</Button>
            <Button variant={"secondary"}>Sign up</Button>
        </div>
        <div className="pr-2">
          <ModeToggle />
        </div>
      </div>
    </div>
  );
}
