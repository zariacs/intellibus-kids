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
  triggers: z.array(z.string()).optional().default([]),
  concerns: z.array(z.string()).optional().default([]),
  patient_id: z.string().optional(),
  nutri_code: z.string().optional(),
});

// List options for multi-select fields
const allergyOptions = [
  { id: "dairy", label: "Dairy" },
  { id: "shellfish", label: "Shellfish" },
  { id: "nuts", label: "Nuts" },
  { id: "eggs", label: "Eggs" },
  { id: "wheat", label: "Wheat" },
  { id: "soy", label: "Soy" },
];

const symptomOptions = [
  { id: "frequent urination", label: "Frequent Urination" },
  { id: "increased thirst", label: "Increased Thirst" },
  { id: "fatigue", label: "Fatigue" },
  { id: "blurred vision", label: "Blurred Vision" },
  { id: "numbness", label: "Numbness or Tingling" },
  { id: "slow healing", label: "Slow Healing Sores" },
  { id: "headache", label: "Headache" },
  { id: "dizziness", label: "Dizziness" },
];

const dietaryOptions = [
  { id: "low-carb", label: "Low Carb" },
  { id: "gluten-free", label: "Gluten Free" },
  { id: "vegetarian", label: "Vegetarian" },
  { id: "vegan", label: "Vegan" },
  { id: "keto", label: "Keto" },
  { id: "paleo", label: "Paleo" },
  { id: "diabetic", label: "Diabetic Diet" },
];

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
      conditions: undefined, // Changed to undefined since it's an enum now
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
      
      // Check if user is authenticated
      if (!user || !user.id) {
        throw new Error("You must be signed in to submit this form");
      }
      
      // Handle triggers and concerns that might be entered as comma-separated text
      let triggersArray = values.triggers;
      if (!Array.isArray(triggersArray) && typeof triggersArray === 'string') {
        triggersArray = (triggersArray as string).split(',').map(item => item.trim()).filter(item => item.length > 0);
      }
      
      let concernsArray = values.concerns;
      if (!Array.isArray(concernsArray) && typeof concernsArray === 'string') {
        concernsArray = (concernsArray as string).split(',').map(item => item.trim()).filter(item => item.length > 0);
      }
      
      // Transform form data to match the required JSON structure
      const transformedData = {
        patient_id: String(user.id), // Ensure patient_id is a string
        nutri_code: values.nutri_code || "NT2025-42",
        conditions: [values.conditions], // Array of the selected condition
        symptoms: values.symptoms || [],
        diet_restriction: values.diet_restriction || [],
        allergies: values.allergies || [],
        medications: values.medications || [],
        dietary_preferences: values.dietary_preferences || [],
        triggers: triggersArray || [],
        concerns: concernsArray || [],
        demographics: {
          age: values.age,
          gender: values.gender,
          weight: values.weight,
          height: values.height
        },
        status: "pending"
      };
      
      console.log("Submitting transformed data:", transformedData);
      
      // // External API endpoint
      // const response = await fetch("http://127.0.0.1:8000/api/requests/create", {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      //   body: JSON.stringify(transformedData),
      // });
      
      // console.log("Response status:", response.status);
      
      // const responseData = await response.json().catch(() => ({}));
      // console.log("Response data:", responseData);
      
      // if (!response.ok) {
      //   let errorMsg = "Failed to submit patient information";
        
      //   // Try to extract specific error messages if available
      //   if (responseData.detail && Array.isArray(responseData.detail)) {
      //     errorMsg = responseData.detail.map(err => err.msg || err).join(', ');
      //   } else if (responseData.detail) {
      //     errorMsg = typeof responseData.detail === 'string' 
      //       ? responseData.detail 
      //       : JSON.stringify(responseData.detail);
      //   }
        
      //   throw new Error(errorMsg);
      // }
      
      setSubmitStatus("success");
      
      // Optional: Navigate after successful submission
      setTimeout(() => router.push("/patient/requests"), 2000);
    } catch (error) {
      console.error("Form submission error:", error);
      setSubmitStatus("error");
      setErrorMessage(error instanceof Error ? error.message : "An unknown error occurred");
    } finally {
      setIsSubmitting(false);
    }
  }

  // Custom component for the medications input
  const MedicationsInput = () => {
    const [medication, setMedication] = useState("");
    
    const addMedication = () => {
      if (medication.trim() === "") return;
      
      const currentMeds = form.getValues().medications || [];
      form.setValue("medications", [...currentMeds, medication]);
      setMedication("");
    };
    
    const removeMedication = (index: number) => {
      const currentMeds = form.getValues().medications || [];
      form.setValue(
        "medications",
        currentMeds.filter((_, i) => i !== index)
      );
    };

    console.log('Supabase URL:', process.env.NEXT_PUBLIC_SUPABASE_URL);
console.log('Supabase Key:', process.env.NEXT_PUBLIC_SUPABASE_KEY);    
    
    return (
      <div className="space-y-3">
        <div className="flex space-x-2">
          <Input
            placeholder="Enter medication and dosage"
            value={medication}
            onChange={(e) => setMedication(e.target.value)}
          />
          <Button type="button" onClick={addMedication}>Add</Button>
        </div>
        
        <div className="grid gap-2">
          {form.getValues().medications?.map((med, index) => (
            <div key={index} className="flex items-center justify-between bg-muted p-2 rounded-md">
              <span>{med}</span>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => removeMedication(index)}
              >
                Remove
              </Button>
            </div>
          ))}
        </div>
      </div>
    );
  };
  const id = user?.id;
  
  return (
    <div className="container mx-auto py-10">
      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle>Patient Information Form</CardTitle>
          <CardDescription>
            Please provide your medical information for our records.
            <div>ID: {id}</div>
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
              <AlertDescription>
                {errorMessage || "There was an error submitting your information. Please try again."}
              </AlertDescription>
            </Alert>
          )}
          
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Personal Information Section */}
                <FormField
                  control={form.control}
                  name="conditions"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Medical Condition</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select a condition" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="IBS">Irritable Bowel Syndrome (IBS)</SelectItem>
                          <SelectItem value="Celiac Disease">Celiac Disease</SelectItem>
                          <SelectItem value="Gastritis">Gastritis</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="age"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Age</FormLabel>
                      <FormControl>
                        <Input type="number" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="gender"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Gender</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select gender" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="Male">Male</SelectItem>
                          <SelectItem value="Female">Female</SelectItem>
                          <SelectItem value="Non-binary">Non-binary</SelectItem>
                          <SelectItem value="Other">Other</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="weight"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Weight (kg)</FormLabel>
                      <FormControl>
                        <Input type="number" step="0.1" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="height"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Height (cm)</FormLabel>
                      <FormControl>
                        <Input type="number" step="0.1" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              
              {/* Allergies Section */}
              <div>
                <FormField
                  control={form.control}
                  name="allergies"
                  render={() => (
                    <FormItem>
                      <div className="mb-4">
                        <FormLabel className="text-base">Allergies</FormLabel>
                        <FormDescription>
                          Select all allergies that apply to you.
                        </FormDescription>
                      </div>
                      {allergyOptions.map((option) => (
                        <FormField
                          key={option.id}
                          control={form.control}
                          name="allergies"
                          render={({ field }) => {
                            return (
                              <FormItem
                                key={option.id}
                                className="flex flex-row items-start space-x-3 space-y-0"
                              >
                                <FormControl>
                                  <Checkbox
                                    checked={field.value?.includes(option.id)}
                                    onCheckedChange={(checked) => {
                                      return checked
                                        ? field.onChange([...field.value || [], option.id])
                                        : field.onChange(
                                            field.value?.filter(
                                              (value) => value !== option.id
                                            )
                                          );
                                    }}
                                  />
                                </FormControl>
                                <FormLabel className="font-normal">
                                  {option.label}
                                </FormLabel>
                              </FormItem>
                            );
                          }}
                        />
                      ))}
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              
              {/* Medications Section */}
              <FormField
                control={form.control}
                name="medications"
                render={({  }) => (
                  <FormItem>
                    <FormLabel>Medications</FormLabel>
                    <FormDescription>
                      List all medications you are currently taking with dosage.
                    </FormDescription>
                    <FormControl>
                      <MedicationsInput />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              {/* Symptoms Section */}
              <div>
                <FormField
                  control={form.control}
                  name="symptoms"
                  render={() => (
                    <FormItem>
                      <div className="mb-4">
                        <FormLabel className="text-base">Symptoms</FormLabel>
                        <FormDescription>
                          Select all symptoms you are experiencing.
                        </FormDescription>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        {symptomOptions.map((option) => (
                          <FormField
                            key={option.id}
                            control={form.control}
                            name="symptoms"
                            render={({ field }) => {
                              return (
                                <FormItem
                                  key={option.id}
                                  className="flex flex-row items-start space-x-3 space-y-0"
                                >
                                  <FormControl>
                                    <Checkbox
                                      checked={field.value?.includes(option.id)}
                                      onCheckedChange={(checked) => {
                                        return checked
                                          ? field.onChange([...field.value || [], option.id])
                                          : field.onChange(
                                              field.value?.filter(
                                                (value) => value !== option.id
                                              )
                                            );
                                      }}
                                    />
                                  </FormControl>
                                  <FormLabel className="font-normal">
                                    {option.label}
                                  </FormLabel>
                                </FormItem>
                              );
                            }}
                          />
                        ))}
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              
              {/* Triggers Section */}
              <FormField
                control={form.control}
                name="triggers"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Triggers</FormLabel>
                    <FormDescription>
                      Please list any triggers that worsen your condition (e.g., foods, stress).
                    </FormDescription>
                    <FormControl>
                      <Textarea
                        placeholder="Enter triggers separated by commas (e.g., High stress levels, poor sleep)"
                        onChange={(e) => {
                          const triggersArray = e.target.value
                            .split(',')
                            .map(item => item.trim())
                            .filter(item => item.length > 0);
                          field.onChange(triggersArray);
                        }}
                        value={field.value?.join(', ')}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              {/* Concerns Section */}
              <FormField
                control={form.control}
                name="concerns"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Health Concerns</FormLabel>
                    <FormDescription>
                      Share any specific health concerns or goals you have.
                    </FormDescription>
                    <FormControl>
                      <Textarea
                        placeholder="Enter your health concerns separated by commas"
                        onChange={(e) => {
                          const concernsArray = e.target.value
                            .split(',')
                            .map(item => item.trim())
                            .filter(item => item.length > 0);
                          field.onChange(concernsArray);
                        }}
                        value={field.value?.join(', ')}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              {/* Dietary Preferences Section */}
              <div>
                <FormField
                  control={form.control}
                  name="dietary_preferences"
                  render={() => (
                    <FormItem>
                      <div className="mb-4">
                        <FormLabel className="text-base">Dietary Preferences</FormLabel>
                        <FormDescription>
                          Select any dietary preferences or restrictions you follow.
                        </FormDescription>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        {dietaryOptions.map((option) => (
                          <FormField
                            key={option.id}
                            control={form.control}
                            name="dietary_preferences"
                            render={({ field }) => {
                              return (
                                <FormItem
                                  key={option.id}
                                  className="flex flex-row items-start space-x-3 space-y-0"
                                >
                                  <FormControl>
                                    <Checkbox
                                      checked={field.value?.includes(option.id)}
                                      onCheckedChange={(checked) => {
                                        return checked
                                          ? field.onChange([...field.value || [], option.id])
                                          : field.onChange(
                                              field.value?.filter(
                                                (value) => value !== option.id
                                              )
                                            );
                                      }}
                                    />
                                  </FormControl>
                                  <FormLabel className="font-normal">
                                    {option.label}
                                  </FormLabel>
                                </FormItem>
                              );
                            }}
                          />
                        ))}
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              
              <div className="space-y-2">
                <Button 
                  type="submit" 
                  className="w-full"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "Submitting..." : "Submit Patient Information"}
                </Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}