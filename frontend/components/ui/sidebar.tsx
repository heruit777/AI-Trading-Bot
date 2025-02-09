import { History, House, Settings } from "lucide-react";
import Link from "next/link";

export default function Sidebar() {
  return (
    <div className="flex flex-col border border-l w-64">
      <Link href="/dashboard">
        <div className="flex items-center px-3 py-2 hover:cursor-pointer hover:bg-secondary rounded-lg my-2 mx-3">
          <House className="mr-2" />
          DashBoard
        </div>
      </Link>
      <Link href="/dashboard/history">
        <div className="flex items-center px-3 py-2 hover:cursor-pointer hover:bg-secondary rounded-lg my-2 mx-3">
          <History className="mr-2" />
          History
        </div>
      </Link>
      <Link href="/dashboard/settings">
        <div className="flex items-center px-3 py-2 hover:cursor-pointer hover:bg-secondary rounded-lg my-2 mx-3">
          <Settings className="mr-2" />
          Settings
        </div>
      </Link>
    </div>
  );
}
