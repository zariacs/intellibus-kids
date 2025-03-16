"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useUser } from "@clerk/nextjs";
import { useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle, CheckCircle2 } from "lucide-react";

// Define the form schema using Zod
const formSchema = z.object({
  conditions: z.enum(["IBS", "Celiac Disease", "Gastritis"], { 
    required_error: "Please select a medical condition." 
  }),
  age: z.coerce.number().int().positive({ message: "Age must be a positive number." }),
  gender: z.string().min(1, { message: "Gender selection is required." }),
  weight: z.coerce.number().positive({ message: "Weight must be a positive number." }),
  height: z.coerce.number().positive({ message: "Height must be a positive number." }),
  allergies: z.array(z.string()).optional(),
  medications: z.array(z.string()),
  symptoms: z.array(z.string()),
  dietary_preferences: z.array(z.string()).optional(),
  diet_restriction: z.array(z.string()).optional(),
  triggers: z.union([z.string(), z.array(z.string())]).optional().default([]),
  concerns: z.union([z.string(), z.array(z.string())]).optional().default([]),
  patient_id: z.string().optional(),
  nutri_code: z.string().optional(),
});

export default function PatientInformationForm() {
  const { user } = useUser();
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");
  
  // Initialize the form with default values
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      conditions: undefined,
      age: 0,
      gender: "",
      weight: 0,
      height: 0,
      allergies: [],
      medications: [],
      symptoms: [],
      dietary_preferences: [],
      diet_restriction: [],
      triggers: [],
      concerns: [],
      patient_id: '2',
      nutri_code: "NT2025-42",
    },
  });

  // Function to handle form submission
  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsSubmitting(true);
    setSubmitStatus("idle");
    
    try {
      console.log("Form values:", values);
      
      if (!user || !user.id) {
        throw new Error("You must be signed in to submit this form");
      }

      // Ensure triggers and concerns are always arrays before applying .split()
      const triggersArray: string[] = Array.isArray(values.triggers)
        ? values.triggers
        : typeof values.triggers === "string"
          ? values.triggers.split(",").map(item => item.trim()).filter(item => item.length > 0)
          : [];

      const concernsArray: string[] = Array.isArray(values.concerns)
        ? values.concerns
        : typeof values.concerns === "string"
          ? values.concerns.split(",").map(item => item.trim()).filter(item => item.length > 0)
          : [];

      const transformedData = {
        patient_id: String(user.id),
        nutri_code: values.nutri_code || "NT2025-42",
        conditions: [values.conditions],
        symptoms: values.symptoms || [],
        diet_restriction: values.diet_restriction || [],
        allergies: values.allergies || [],
        medications: values.medications || [],
        dietary_preferences: values.dietary_preferences || [],
        triggers: triggersArray,
        concerns: concernsArray,
        demographics: {
          age: values.age,
          gender: values.gender,
          weight: values.weight,
          height: values.height
        },
        status: "pending"
      };
      
      console.log("Submitting transformed data:", transformedData);
      
      setSubmitStatus("success");
      setTimeout(() => router.push("/patient/requests"), 2000);
    } catch (error) {
      console.error("Form submission error:", error);
      setSubmitStatus("error");
      setErrorMessage(error instanceof Error ? error.message : "An unknown error occurred");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="container mx-auto py-10">
      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle>Patient Information Form</CardTitle>
          <CardDescription>
            Please provide your medical information for our records.
            <div>ID: {user?.id}</div>
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          {submitStatus === "success" && (
            <Alert className="mb-6 bg-green-50 text-green-800 border-green-200">
              <CheckCircle2 className="h-4 w-4" />
              <AlertTitle>Success!</AlertTitle>
              <AlertDescription>
                Your information has been successfully submitted.
              </AlertDescription>
            </Alert>
          )}
          
          {submitStatus === "error" && (
            <Alert className="mb-6 bg-red-50 text-red-800 border-red-200">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{errorMessage}</AlertDescription>
            </Alert>
          )}
