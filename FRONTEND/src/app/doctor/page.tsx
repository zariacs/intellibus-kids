"use client";

import { useState, useEffect } from "react";
import { useUser } from "@clerk/nextjs";
import { 
  Card, 
  CardContent, 
  CardFooter, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { UserRound, Calendar, Hourglass } from "lucide-react";

type Patient = {
  id: string;
  name: string;
  age: number | null;
  gender: string | null;
  email: string | null;
};

type PendingRequest = {
  id: number;
  created_at: string;
  conditions: string[];
  status: string;
  patient_id: string;
  dietary_preference: string | null;
  patient: Patient;
};

export default function DoctorDashboardPage() {
  const { user, isLoaded } = useUser();
  const [pendingRequests, setPendingRequests] = useState<PendingRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchPendingRequests() {
      if (!isLoaded || !user) return;

      try {
        setLoading(true);
        const response = await fetch('/api/doctor/pending-requests');
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Failed to fetch pending requests");
        }
        
        const data = await response.json();
        setPendingRequests(data);
      } catch (err) {
        console.error("Error fetching pending requests:", err);
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    }

    fetchPendingRequests();
  }, [user, isLoaded]);

  if (!isLoaded || loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spinner className="h-8 w-8" />
        <span className="ml-2">Loading pending requests...</span>
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

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Pending Nutrition Requests</h1>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="bg-blue-50">
            {pendingRequests.length} pending
          </Badge>
        </div>
      </div>
      
      {pendingRequests.length === 0 ? (
        <div className="bg-gray-50 rounded-lg p-8 text-center">
          <h3 className="text-lg font-medium text-gray-700 mb-2">No pending requests</h3>
          <p className="text-gray-500">All nutrition requests have been processed.</p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {pendingRequests.map((request) => (
            <Card key={request.patient_id} className="overflow-hidden">
              <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                  <CardTitle className="text-lg">{request.patient.name || "Unknown Patient"}</CardTitle>
                  <Badge className="bg-amber-100 text-amber-800">Pending</Badge>
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <Calendar className="h-4 w-4 mr-1" />
                  <span>
                    {new Date(request.created_at).toLocaleDateString()}
                  </span>
                </div>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center gap-2">
                    <UserRound className="h-4 w-4 text-gray-400" />
                    <span className="text-sm">
                      {request.patient.age ? `${request.patient.age} years old` : "Age not specified"}
                      {request.patient.gender ? `, ${request.patient.gender}` : ""}
                    </span>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-semibold mb-1">Health Conditions</h3>
                    {request.conditions && request.conditions.length > 0 ? (
                      <div className="flex flex-wrap gap-1">
                        {request.conditions.map((condition, i) => (
                          <Badge key={i} variant="outline" className="bg-blue-50">
                            {condition}
                          </Badge>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500">No conditions specified</p>
                    )}
                  </div>
                  
                  {request.dietary_preference && (
                    <div>
                      <h3 className="text-sm font-semibold mb-1">Dietary Preference</h3>
                      <p className="text-sm">{request.dietary_preference}</p>
                    </div>
                  )}
                  
                  <div className="flex items-center text-xs text-gray-500">
                    <Hourglass className="h-3 w-3 mr-1" />
                    <span>Waiting for review</span>
                  </div>
                </div>
              </CardContent>
              
              <CardFooter className="bg-gray-50 border-t pt-3">
                <div className="w-full">
                  <Button 
                    className="w-full" 
                    onClick={() => window.location.href = `/doctor/request/${request.id}`}
                  >
                    Review Request
                  </Button>
                </div>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}