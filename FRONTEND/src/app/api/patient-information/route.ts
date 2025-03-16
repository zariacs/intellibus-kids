// app/api/patient-information/route.ts (App Router)

import { NextRequest, NextResponse } from "next/server";
import { getAuth } from "@clerk/nextjs/server";

// Type definition matching the form data
type PatientInformation = {
  name: string;
  condition: "IBS" | "Celiac Disease" | "Gastritis";
  age: number;
  gender: string;
  weight: number;
  height: number;
  allergies?: string[];
  medications: string[];
  symptoms: string[];
  dietary_preferences?: string[];
};

// Debug endpoint to verify the route is registered
export async function GET() {
  console.log("GET request received on patient-information endpoint");
  return NextResponse.json({ message: "Patient information API is working" });
}

// App Router implementation
export async function POST(request: NextRequest) {
  console.log("POST request received on patient-information endpoint");
  
  try {
    // Authenticate the request
    const { userId } = getAuth(request);
    
    if (!userId) {
      return NextResponse.json(
        { error: "Unauthorized. Please sign in." },
        { status: 401 }
      );
    }
    
    // Parse the request body
    const patientInfo: PatientInformation = await request.json();
    
    // Here you would typically:
    // 1. Validate the data
    // 2. Save to your database
    // 3. Return appropriate response
    
    console.log("Received patient information:", patientInfo);
    
    // Example: Save to database
    // const result = await db.patientInformation.create({
    //   data: {
    //     ...patientInfo,
    //     userId,
    //   },
    // });
    
    return NextResponse.json(
      { 
        message: "Patient information saved successfully",
        // id: result.id, // If you're saving to a database
      },
      { status: 201 }
    );
  } catch (error) {
    console.error("Error processing patient information:", error);
    return NextResponse.json(
      { error: "Failed to save patient information" },
      { status: 500 }
    );
  }
}

// For Pages Router, uncomment this code instead:
/*
import type { NextApiRequest, NextApiResponse } from "next";
import { getAuth } from "@clerk/nextjs/server";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    // Authenticate the request
    const { userId } = getAuth(req);
    
    if (!userId) {
      return res.status(401).json({ error: "Unauthorized. Please sign in." });
    }
    
    // Parse the request body
    const patientInfo: PatientInformation = req.body;
    
    console.log("Received patient information:", patientInfo);
    
    // Example: Save to database
    // const result = await db.patientInformation.create({
    //   data: {
    //     ...patientInfo,
    //     userId,
    //   },
    // });
    
    return res.status(201).json({ 
      message: "Patient information saved successfully",
      // id: result.id, // If you're saving to a database
    });
  } catch (error) {
    console.error("Error processing patient information:", error);
    return res.status(500).json({ error: "Failed to save patient information" });
  }
}
*/