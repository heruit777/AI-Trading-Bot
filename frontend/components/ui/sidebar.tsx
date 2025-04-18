"use client";
import { History, House, Settings } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <div className="flex flex-col border  w-64">
      <Link href="/dashboard">
        <div
          className={`flex items-center px-3 py-2 font-bold ${
            pathname === "/dashboard"
              ? "bg-secondary"
              : "hover:cursor-pointer hover:bg-secondary"
          } rounded-lg my-2 mx-3`}
        >
          <House className="mr-4" />
          DashBoard
        </div>
      </Link>
      <Link href="/dashboard/history">
        <div
          className={`flex items-center px-3 py-2 font-bold ${
            pathname === "/dashboard/history"
              ? "bg-secondary"
              : "hover:cursor-pointer hover:bg-secondary"
          } rounded-lg my-2 mx-3`}
        >
          <History className="mr-4" />
          History
        </div>
      </Link>
      <Link href="/dashboard/settings">
        <div
          className={`flex items-center px-3 py-2 font-bold ${
            pathname === "/dashboard/settings"
              ? "bg-secondary"
              : "hover:cursor-pointer hover:bg-secondary"
          } rounded-lg my-2 mx-3`}
        >
          <Settings className="mr-4" />
          Settings
        </div>
      </Link>
    </div>
  );
}
