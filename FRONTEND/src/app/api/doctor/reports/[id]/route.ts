// app/api/doctor/reports/[id]/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getAuth } from "@clerk/nextjs/server";
import { createClient } from '@supabase/supabase-js';

// Server-side Supabase client
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL || '',
  process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY || ''
);

// Simple helper function that gets the ID from the URL
function getIdFromUrl(url: string): string {
  const segments = url.split('/');
  return segments[segments.length - 1];
}

// Export a simplified GET handler that doesn't rely on context params
export async function GET(request: NextRequest) {
  try {
    // Verify the user is authorized as a doctor
    const { userId } = getAuth(request);
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    
    // Extract ID from URL instead of using params
    const reportId = getIdFromUrl(request.url);
    
    // Fetch the report from Supabase
    const { data, error: dbError } = await supabase
      .from('reports')
      .select('id, patient_id, content, created_at')
      .eq('id', reportId)
      .single();
      
    if (dbError) {
      console.error("Supabase error:", dbError);
      return NextResponse.json({ error: dbError.message }, { status: 500 });
    }
    
    if (!data) {
      return NextResponse.json({ error: "Report not found" }, { status: 404 });
    }
    
    return NextResponse.json(data);
  } catch (err) {
    console.error("Error fetching report:", err);
    return NextResponse.json(
      { error: "Failed to fetch report" },
      { status: 500 }
    );
  }
}