import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function parseNumber(value: string): number {
  const num = parseFloat(value);
  return isNaN(num) ? 0 : num;
}