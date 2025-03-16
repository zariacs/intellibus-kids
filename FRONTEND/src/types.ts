// types.ts
import '@clerk/nextjs';

declare module '@clerk/nextjs' {
  interface PublicMetadata {
    role?: string;
  }
}