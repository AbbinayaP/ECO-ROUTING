import * as React from "react";
import { cn } from "../../utils/cn";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "rounded-xl border border-cardBorder bg-card/80 shadow-glass backdrop-blur-glass",
        className
      )}
      {...props}
    />
  )
);
Card.displayName = "Card";

