"use client";

import { useState } from "react";
import StrategyStatsSkeleton from "./skeletons/strategyStatsSkeleton";

export default function StrategyStats() {
  const [isLoading, setIsLoading] = useState<Boolean>(true);

  return (
    <>
      {isLoading ? (
        <StrategyStatsSkeleton />
      ) : (
        <div className="grid grid-rows-3 grid-cols-2 text-gray-300 font-semibold gap-4">
          <div>Win Rate: 53.36%</div>
          <div>Profit factor: 2.0</div>
          <div>Average Winner: 500</div>
          <div>Average Loser: 100</div>
          <div>Winning Streak: 5</div>
          <div>Losing Streak: 2</div>
        </div>
      )}
    </>
  );
}
