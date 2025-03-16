"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { useUser } from "@clerk/nextjs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { Alert, AlertDescription } from "@/components/ui/alert";

type Report = {
  id: string;
  patient_id: string;
  created_at: string;
  title: string;
  content: string;
  status: string;
  // Add other report fields as needed
};

export default function PatientReportPage() {
  const params = useParams();
  const { user, isLoaded } = useUser();
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const reportId = params.id as string;

  useEffect(() => {
    async function fetchReport() {
      if (!isLoaded || !user) return;

      try {
        setLoading(true);
        
        // Fetch from your API route instead of Supabase directly
        const response = await fetch(`/api/reports/${reportId}`);
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Failed to fetch report");
        }
        
        const data = await response.json();
        setReport(data);
      } catch (err) {
        console.error("Error fetching report:", err);
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    }

    fetchReport();
  }, [reportId, user, isLoaded]);

  if (!isLoaded || loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spinner className="h-8 w-8" />
        <span className="ml-2">Loading report...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive" className="max-w-2xl mx-auto mt-8">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (!report) {
    return (
      <Alert className="max-w-2xl mx-auto mt-8">
        <AlertDescription>Report not found</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="container mx-auto py-8">
      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle>{report.title}</CardTitle>
          <p className="text-sm text-gray-500">
            Created: {new Date(report.created_at).toLocaleDateString()}
          </p>
        </CardHeader>
        <CardContent>
          <div className="prose max-w-none">
            {/* Display report content - you might want to parse this if it's stored as JSON or Markdown */}
            <div dangerouslySetInnerHTML={{ __html: report.content }} />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}