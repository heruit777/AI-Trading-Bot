import { auth } from "@/auth";
import { AlignJustifyIcon } from "lucide-react";
import Link from "next/link";
import { Button } from "./button";
import { handleSignout } from "@/app/actions/authActions";
import { ModeToggle } from "./modeToggle";
import AccountSelect from "./accountSelect";

export default async function AuthenticatedNavbar() {
  const session = await auth();
  return (
    <div className="flex justify-between items-center border border-b-2 min-h-16 px-4 text-base">
      <div className="flex items-center space-x-5">
        <AlignJustifyIcon className="hover:cursor-pointer md:hidden" />
        <Link href="/dashboard">
          <div className="md:text-2xl font-extrabold">AI TRADING BOT</div>
        </Link>
      </div>
      <div className="flex justify-around items-center space-x-8">
        {/* Can add icons here for the mobile */}
        {/* <AccountSelect /> */}

        <div className="hidden sm:block sm:space-x-4">
          {session?.user ? (
            <Button variant={"default"} onClick={handleSignout}>
              Sign Out
            </Button>
          ) : (
            <>
              <Link href="/login">
                <Button variant={"secondary"}>Log in</Button>
              </Link>
              <Link href="/signup">
                <Button>Sign up</Button>
              </Link>
            </>
          )}
        </div>
        <div className="pr-2">
          <ModeToggle />
        </div>
      </div>
    </div>
  );
}
