// app/api/doctor/reports/[id]/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getAuth } from "@clerk/nextjs/server";
import { createClient } from "@supabase/supabase-js";

// Server-side Supabase client
const supabase = createClient(
  process.env.SUPABASE_URL || "",
  process.env.SUPABASE_SERVICE_ROLE_KEY || ""
);

// Define a more explicit type for the context
type RouteContext = {
  params: {
    id: string;
  };
};

// Use the route handler approach from Next.js documentation
export async function GET(request: NextRequest, context: RouteContext) {
  // Get the report ID from the URL params
  const reportId = context.params.id;
  
  try {
    // Auth check
    const { userId } = getAuth(request);
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    
    // Fetch report
    const { data, error } = await supabase
      .from("reports")
      .select("id, patient_id, content, created_at")
      .eq("id", reportId)
      .single();
    
    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    
    if (!data) {
      return NextResponse.json({ error: "Report not found" }, { status: 404 });
    }
    
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error:", error);
    return NextResponse.json({ error: "Server error" }, { status: 500 });
  }
}