// app/api/nutrition-requests/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getAuth } from "@clerk/nextjs/server";
import { supabase } from "@/lib/supabase";

export async function GET(request: NextRequest) {
  try {
    const { userId } = getAuth(request);
    
    // If user is not authenticated, return 401
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Get query parameters
    const url = new URL(request.url);
    const statusParam = url.searchParams.get("status");
    
    // Parse status filter - if provided, split by comma
    const statusFilter = statusParam ? statusParam.split(",") : null;
    
    // Query Supabase for nutrition requests
    let query = supabase
      .from('nutrition_requests')
      .select('*')
      .eq('patient_id', userId)
      .order('created_at', { ascending: false });
    
    // Add status filter if provided
    if (statusFilter && statusFilter.length > 0) {
      query = query.in('status', statusFilter);
    }
    
    const { data, error } = await query;
    
    if (error) {
      console.error("Supabase error:", error);
      return NextResponse.json(
        { error: "Database error occurred" },
        { status: 500 }
      );
    }
    
    // Process the results - parse string arrays stored as JSON
    const processedRequests = data.map(request => ({
      ...request,
      conditions: parseStringArray(request.conditions),
      allergies: parseStringArray(request.allergies),
      diet_restrictions: parseStringArray(request.diet_restrictions),
    }));

    return NextResponse.json(processedRequests);
  } catch (error) {
    console.error("Error fetching nutrition requests:", error);
    return NextResponse.json(
      { error: "Failed to fetch nutrition requests" },
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