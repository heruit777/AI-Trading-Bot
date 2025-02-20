import MoonLoader from "react-spinners/MoonLoader";
import { Button } from "./button";

export default function LoadingButton({
  loading,
  text,
  loadingText,
  type,
  className
}: {
  loading: boolean;
  text: string;
  loadingText: string;
  type: "submit" | "reset" | "button" | undefined;
  className?: string;
}) {
  return (
    <Button
      type={type}
      className={`${className} ${loading && "bg-primary/90"}`}
    >
      {loading ? (
        <>
          <MoonLoader
            size={20}
            aria-label="Loading Spinner"
            data-testid="loader"
          />
          {loadingText}
        </>
      ) : (
        text
      )}
    </Button>
  );
}
