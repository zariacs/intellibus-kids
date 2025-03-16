"use client";

import { useState, useEffect } from "react";
import { useUser } from "@clerk/nextjs";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Spinner } from "@/components/ui/spinner";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

type NutritionRequest = {
  id: number;
  patient_id: string;
  conditions: string[];
  allergies: string[];
  diet_restrictions: string[];
  dietary_preference: string;
  status: string;
  created_at: string;
};

// Dummy data for Jane Doe
const DUMMY_REQUESTS: NutritionRequest[] = [
  {
    id: 3,
    patient_id: "user_123abc",
    conditions: ["Type 2 Diabetes", "Hypertension", "High Cholesterol"],
    allergies: ["Dairy", "Shellfish", "Peanuts"],
    diet_restrictions: ["Low-carb", "Gluten-free"],
    dietary_preference: "Mediterranean-inspired",
    status: "processing",
    created_at: "2025-03-14T09:42:18Z"
  }
];

export default function NutritionRequestsPage() {
  const { user, isLoaded } = useUser();
  const [requests, setRequests] = useState<NutritionRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Flag to use dummy data (set to false when backend is ready)
  const useDummyData = true;

  useEffect(() => {
    async function fetchRequests() {
      if (!isLoaded || !user) return;

      try {
        setLoading(true);
        
        if (useDummyData) {
          // Use dummy data for testing
          // Simulate network delay
          setTimeout(() => {
            setRequests(DUMMY_REQUESTS);
            setLoading(false);
          }, 800);
          
          return;
        }
        
        // Real API call for when backend is ready
        const response = await fetch(`/api/nutrition-requests?userId=${user.id}&status=pending,processing,rejected`);
        
        if (!response.ok) {
          throw new Error("Failed to fetch nutrition requests");
        }
        
        const data = await response.json();
        setRequests(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        if (!useDummyData) {
          setLoading(false);
        }
      }
    }

    fetchRequests();
  }, [user, isLoaded, useDummyData]);
  
  const handleViewReport = () => {
    // For demo purposes, always route to report/3
    window.location.href = '/report/3';
    
    // When backend is ready, uncomment this:
    // window.location.href = `/report/${requestId}`;
  };

  if (!isLoaded || loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spinner className="h-8 w-8" />
        <span className="ml-2">Loading requests...</span>
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
        <h1 className="text-2xl font-bold">Your Nutrition Requests</h1>
        <Button onClick={() => window.location.href = '/patient'}>
          New Request
        </Button>
      </div>
      
      {requests.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">You don&apos;t have any pending nutrition requests.</p>
          <Button onClick={() => window.location.href = '/patient'}>
            Create Your First Request
          </Button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {requests.map((request) => (
            <Card key={request.id} className="overflow-hidden">
              <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                  <CardTitle className="text-lg">Request #{request.id}</CardTitle>
                  <StatusBadge status={request.status} />
                </div>
                <p className="text-sm text-gray-500">
                  Created: {new Date(request.created_at).toLocaleDateString()}
                </p>
              </CardHeader>
              
              <CardContent className="pb-4">
                {request.conditions && request.conditions.length > 0 && (
                  <div className="mb-3">
                    <h3 className="text-sm font-semibold mb-1">Conditions</h3>
                    <div className="flex flex-wrap gap-1">
                      {request.conditions.map((condition, i) => (
                        <Badge key={i} variant="outline" className="bg-blue-50">
                          {condition}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {request.allergies && request.allergies.length > 0 && (
                  <div className="mb-3">
                    <h3 className="text-sm font-semibold mb-1">Allergies</h3>
                    <div className="flex flex-wrap gap-1">
                      {request.allergies.map((allergy, i) => (
                        <Badge key={i} variant="outline" className="bg-red-50">
                          {allergy}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {request.dietary_preference && (
                  <div>
                    <h3 className="text-sm font-semibold mb-1">Dietary Preferences</h3>
                    <p className="text-sm">{request.dietary_preference}</p>
                  </div>
                )}
              </CardContent>
              
              <CardFooter className="bg-gray-50 border-t">
                <div className="w-full flex justify-between items-center">
                  <span className="text-sm">
                    {request.status === "processing" && (
                      <span className="flex items-center text-amber-600">
                        <Spinner className="h-3 w-3 mr-2" />
                        Processing
                      </span>
                    )}
                    {request.status === "pending" && (
                      <span className="text-gray-600">Awaiting review</span>
                    )}
                    {request.status === "rejected" && (
                      <span className="text-red-600">Request declined</span>
                    )}
                  </span>
                  
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    className="text-blue-600 hover:text-blue-800"
                    onClick={() => handleViewReport()}
                  >
                    View Report
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

function StatusBadge({ status }: { status: string }) {
  switch (status.toLowerCase()) {
    case "approved":
      return <Badge className="bg-green-100 text-green-800 hover:bg-green-200">Approved</Badge>;
    case "rejected":
      return <Badge className="bg-red-100 text-red-800 hover:bg-red-200">Rejected</Badge>;
    case "processing":
      return <Badge className="bg-amber-100 text-amber-800 hover:bg-amber-200">Processing</Badge>;
    case "pending":
      return <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-200">Pending</Badge>;
    default:
      return <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-200">{status}</Badge>;
  }
}