// pages/index.tsx (for Pages Router)
// or app/page.tsx (for App Router with client component)
"use client"; // Remove this line if using Pages Router

import { useUser } from "@clerk/nextjs";
import { useRouter } from "next/navigation"; // use "next/navigation" for App Router
import { useEffect } from "react";

export default function HomePage() {
  const { user, isLoaded, isSignedIn } = useUser();
  const router = useRouter();

  useEffect(() => {
    // Only proceed if Clerk has loaded and the user is signed in
    if (!isLoaded) return;

    if (isSignedIn && user) {
      // Get user role from publicMetadata
      const userRole = user.publicMetadata.role as string | undefined;
      
      // Redirect based on role
      if (userRole === "doctor") {
        router.push("/doctor");
      } else if (userRole === "patient") {
        router.push("/patient");
      } else {
        // If no role is set, redirect to role selection page
        router.push("/select-role");
      }
    }
    // No redirection if user is not signed in - show the homepage
  }, [isLoaded, isSignedIn, user, router]);

  // Loading state while Clerk loads
  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  // Show sign-in options if user is not signed in
  if (!isSignedIn) {
    return (
      <div className="flex items-center justify-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1 className="text-8xl font-bold">
        NutriLab
      </h1>
      <h1 className="text-5xl font-bold">
        Connect with your future dietician now
      </h1>
    </div>
    );
  }

  // This will briefly show before redirection happens
  return <div>Redirecting...</div>;
}