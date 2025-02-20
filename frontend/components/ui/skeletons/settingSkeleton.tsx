import { Skeleton } from "../skeleton";

export default function SettingSkeleton() {
  return (
    <div className="mx-auto w-3/4 mt-10 min-h-52 px-10 py-5 rounded-lg border space-y-5">
      <Skeleton className="h-10 w-40 rounded" />
      <Skeleton className="h-10 w-full rounded" />
      <Skeleton className="h-10 w-40 rounded" />
      <Skeleton className="h-10 w-full rounded" />
    </div>
  );
}
