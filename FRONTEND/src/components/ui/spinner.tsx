// components/ui/spinner.tsx
import * as React from "react";
import { cn } from "@/lib/utils";

type SpinnerProps = React.HTMLAttributes<HTMLDivElement>;

export const Spinner = React.forwardRef<HTMLDivElement, SpinnerProps>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn("animate-spin rounded-full border-2 border-t-transparent", className)}
        {...props}
      />
    );
  }
);

Spinner.displayName = "Spinner";