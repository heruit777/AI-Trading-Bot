"use client";

import { useState } from "react";
import AccountOverviewSkeleton from "./skeletons/accountOverviewSkeleton";

export default function AccountOverview() {
  const [isLoading, setIsLoading] = useState<Boolean>(true);

  return (
    <>
      {isLoading ? (
        <AccountOverviewSkeleton />
      ) : (
        <div className="grid grid-rows-3 grid-cols-2 text-gray-300 font-semibold gap-4">
          <div>Balance: 10,000</div>
          <div>Number of trades: 5</div>
          <div>Daily P&L: 100</div>
          <div>Monthly P&L: 5000</div>
        </div>
      )}
    </>
  );
}
