// app/api/doctor/reports/[id]/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getAuth } from "@clerk/nextjs/server";
import { createClient } from '@supabase/supabase-js';

// Server-side Supabase client
const supabase = createClient(
  process.env.SUPABASE_URL || '',
  process.env.SUPABASE_SERVICE_ROLE_KEY || ''
);

// Use this format instead for App Router
export const GET = async (
  request: NextRequest,
  context: { params: { id: string } }
) => {
  try {
    // Verify the user is authorized as a doctor
    const { userId } = getAuth(request);
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    
    const reportId = context.params.id;
    
    // Fetch the report from Supabase
    const { data, error } = await supabase
      .from('reports')
      .select('id, patient_id, content, created_at')
      .eq('id', reportId)
      .single();
      
    if (error) {
      console.error("Supabase error:", error);
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    
    if (!data) {
      return NextResponse.json({ error: "Report not found" }, { status: 404 });
    }
    
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error fetching report:", error);
    return NextResponse.json(
      { error: "Failed to fetch report" },
      { status: 500 }
    );
  }
};