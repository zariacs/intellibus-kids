// pages/index.tsx (for Pages Router)
// or app/page.tsx (for App Router with client component)
"use client"; // Remove this line if using Pages Router

import { useUser } from "@clerk/nextjs";
import { useRouter } from "next/navigation"; // use "next/navigation" for App Router
import { useEffect } from "react";
import { Hero } from "@/components/ui/animated-hero";
import { BenefitsSection } from "@/components/ui/benefits-section";
import { Testimonials } from "@/components/ui/testimonials";
import { HowItWorksSection } from "@/components/ui/how-it-works-section";
import { CallToAction } from "@/components/ui/call-to-action";

// Sample testimonial data focusing on success stories
const testimonialData = [
  {
    image: "/testimonials/doctor1.jpg",
    name: "Dr. Sarah Johnson",
    username: "Cardiologist",
    text: "This platform has transformed my practice. I can now monitor my patients remotely and intervene earlier when needed. Patient outcomes have improved by 30% since I started using it.",
    social: "https://twitter.com/example"
  },
  {
    image: "/testimonials/patient1.jpg",
    name: "Michael Rodriguez",
    username: "Heart Patient",
    text: "As someone managing a chronic condition, this platform has given me peace of mind. My doctor can check my vitals daily without requiring office visits, and I've avoided two hospitalizations this year alone.",
    social: "https://twitter.com/example"
  },
  {
    image: "/testimonials/doctor2.jpg",
    name: "Dr. Emily Chen",
    username: "Pediatrician",
    text: "The child-friendly interface makes it easy to engage young patients in their healthcare journey. Parents love the easy appointment scheduling and medication reminders.",
    social: "https://twitter.com/example"
  },
  {
    image: "/testimonials/patient2.jpg",
    name: "Robert Taylor",
    username: "Diabetes Patient",
    text: "Since using this platform, my A1C levels have stabilized for the first time in years. The medication tracking and glucose monitoring features have been life-changing.",
    social: "https://twitter.com/example"
  },
  {
    image: "/testimonials/doctor3.jpg",
    name: "Dr. James Wilson",
    username: "Family Physician",
    text: "I can now serve 40% more patients while providing better care. The secure messaging and automated follow-ups have streamlined my practice enormously.",
    social: "https://twitter.com/example"
  },
  {
    image: "/testimonials/patient3.jpg",
    name: "Lisa Washington",
    username: "Elderly Patient",
    text: "At 78, I was worried about technology, but this platform is so simple to use. I no longer need my daughter to drive me to appointments for routine check-ins.",
    social: "https://twitter.com/example"
  }
];

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
    return <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-black via-gray-950 to-gray-900">Loading...</div>;
  }

  // Show sign-in options if user is not signed in
  if (!isSignedIn) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-950 to-gray-900 text-white">
        <Hero />
        <BenefitsSection />
        <HowItWorksSection />
        <Testimonials 
          testimonials={testimonialData}
          title="Success Stories from Our Community" 
          description="See how our platform is helping doctors provide better care<br />and patients achieve better health outcomes."
          className="py-16 px-4 md:px-8 max-w-7xl mx-auto"
        />
        <CallToAction />
      </div>
    );
  }

  // This will briefly show before redirection happens
  return <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-black via-gray-950 to-gray-900">Redirecting...</div>;
}