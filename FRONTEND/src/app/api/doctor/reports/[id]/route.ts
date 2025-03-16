import { NextRequest, NextResponse } from "next/server";
import { getAuth } from "@clerk/nextjs/server";
import { createClient } from '@supabase/supabase-js';

// Server-side Supabase client (not exposed to the browser)
const supabase = createClient(
  process.env.SUPABASE_URL || '',  // Note: no NEXT_PUBLIC_ prefix
  process.env.SUPABASE_SERVICE_ROLE_KEY || ''  // Using service role key
);

// Rewritten to fix the build error
export async function GET(request: NextRequest,  context: any) {
  try {
    const { userId } = getAuth(request);
    
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const reportId = context?.params?.id;
    
    const { data, error } = await supabase
      .from('reports')
      .select('*')
      .eq('id', reportId)
      .eq('patient_id', userId)
      .single();
    
    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    
    if (!data) {
      return NextResponse.json({ error: "Report not found" }, { status: 404 });
    }
    
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error fetching report:", error);
    return NextResponse.json(
      { error: "An error occurred" },
      { status: 500 }
    );
  }
}