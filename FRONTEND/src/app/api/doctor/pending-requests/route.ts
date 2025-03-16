// app/api/doctor/pending-requests/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getAuth } from "@clerk/nextjs/server";
import { createClient } from '@supabase/supabase-js';

// Server-side Supabase client (not exposed to the browser)
const supabase = createClient(
  process.env.SUPABASE_URL || '',
  process.env.SUPABASE_SERVICE_ROLE_KEY || ''
);

export async function GET(request: NextRequest) {
  try {
    // Verify the user is authorized as a doctor
    const { userId } = getAuth(request);
    
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    
    // You may want to add a check here to verify the user is a doctor
    // For example, by checking a 'role' field in your users table
    
    // Fetch all pending nutrition requests with joined patient details
    const { data, error } = await supabase
      .from('nutrition_requests')
      .select(`
        id,
        created_at,
        conditions,
        status,
        patient_id,
        dietary_preference,
        patients:patient_id (
          id,
          name,
          age,
          gender,
          email
        )
      `)
      .eq('status', 'pending')
      .order('created_at', { ascending: false });
    
    if (error) {
      console.error("Supabase error:", error);
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    
    // Process the data to ensure proper format
    const processedData = data.map(request => ({
      ...request,
      conditions: parseStringArray(request.conditions),
      // Ensure patients data is structured correctly
      patient: request.patients || { 
        id: request.patient_id,
        name: "Unknown",
        age: null,
        gender: null,
        email: null
      }
    }));
    
    return NextResponse.json(processedData);
  } catch (error) {
    console.error("Error fetching pending requests:", error);
    return NextResponse.json(
      { error: "Failed to fetch pending requests" },
      { status: 500 }
    );
  }
}

// Helper function to parse string arrays stored as JSON or comma-separated values
function parseStringArray(value: string | null): string[] {
  if (!value) return [];
  
  try {
    // First try to parse as JSON
    return JSON.parse(value);
  } catch (e) {
    // If not valid JSON, treat as comma-separated
    return value.split(',').map(item => item.trim());
  }
}