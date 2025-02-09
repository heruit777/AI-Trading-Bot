"use client";
import React, { useState } from "react";
import { Button } from "./button";

type AccountType = "Demo Account" | "Real Account";

const AccountSelect: React.FC = () => {
  const [selected, setSelected] = useState<AccountType>("Demo Account");

  const handleChange = (account: AccountType) => {
    setSelected(account);
  };

  return (
    <div className="relative inline-block text-left">
      {/* Trigger Button */}
      <Button
        variant={"secondary"}
        onClick={() =>
          document.getElementById("dropdown-menu")?.classList.toggle("hidden")
        }
      >
        {selected}
        <svg
          className="ml-2 h-5 w-5"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.72-3.72a.75.75 0 011.06 1.06l-4 4a.75.75 0 01-1.06 0l-4-4a.75.75 0 01.02-1.06z"
            clipRule="evenodd"
          />
        </svg>
      </Button>

      {/* Dropdown Menu */}
      <div
        id="dropdown-menu"
        className="absolute right-0 z-10 mt-2 w-full origin-top-right rounded-md bg-secondary shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none hidden"
      >
        <ul className="py-1" role="menu" aria-orientation="vertical">
          <li>
            <button
              className="block w-full px-4 py-2 text-sm text-white hover:bg-secondary/80 hover:bg-[#232121]"
              onClick={() => {
                handleChange("Demo Account");
                document
                  .getElementById("dropdown-menu")
                  ?.classList.add("hidden");
              }}
            >
              Demo Account
            </button>
          </li>
          <li>
            <button
              className="block w-full px-4 py-2 text-sm text-white hover:bg-[#232121]"
              onClick={() => {
                handleChange("Real Account");
                document
                  .getElementById("dropdown-menu")
                  ?.classList.add("hidden");
              }}
            >
              Real Account
            </button>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default AccountSelect;