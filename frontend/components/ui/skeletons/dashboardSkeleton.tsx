import { Skeleton } from "../skeleton";

export default function DashBoardSkeleton() {
  return (
    <div className="flex flex-col h-full p-10">
      {/* Trade Count & PnL Loader */}
      <div className="h-10 mb-5 flex items-center space-x-10">
        <div className="border rounded-lg p-2 space-x-2 flex items-center">
          <span className="font-bold text-sm">Trade Count:</span>
          <Skeleton className="h-4 w-10 rounded" />
        </div>
        <div className="border rounded-lg p-2 space-x-2 flex items-center">
          <span className="font-bold text-sm">Today's PnL:</span>
          <Skeleton className="h-4 w-16 rounded" />
        </div>
      </div>

      {/* Chart & Card Loader */}
      <div className="flex h-full items-center space-x-5">
        <Skeleton className="w-full h-80 rounded-lg" />
        <Skeleton className="w-80 h-96 rounded-lg" />
      </div>
    </div>
  );
}
