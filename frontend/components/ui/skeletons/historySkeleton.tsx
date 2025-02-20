import { Skeleton } from "../skeleton";

export default function HistorySkeleton() {
  return (
    <div className="w-full px-10 pt-10">
      <div className="h-[600px] rounded-md border p-4">
        {/* Table Header Skeleton */}
        <div className="flex space-x-4 mb-4">
          <Skeleton className="h-6 w-10 rounded" />
          <Skeleton className="h-6 w-1/2 rounded" />
          <Skeleton className="h-6 w-40 rounded" />
          <Skeleton className="h-6 w-40 rounded" />
          <Skeleton className="h-6 w-40 rounded" />
          <Skeleton className="h-6 w-40 rounded" />
          <Skeleton className="h-6 w-40 rounded" />
        </div>

        {/* Table Rows Skeleton */}
        <div className="space-y-3">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="flex space-x-4">
              <Skeleton className="h-6 w-10 rounded" />
              <Skeleton className="h-6 w-1/2 rounded" />
              <Skeleton className="h-6 w-40 rounded" />
              <Skeleton className="h-6 w-40 rounded" />
              <Skeleton className="h-6 w-40 rounded" />
              <Skeleton className="h-6 w-40 rounded" />
              <Skeleton className="h-6 w-40 rounded" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
