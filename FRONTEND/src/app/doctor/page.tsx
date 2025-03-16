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

// Dummy data for testing until backend is connected
const DUMMY_REQUESTS: PendingRequest[] = [
  {
    id: 1,
    created_at: "2025-03-10T10:23:45Z",
    conditions: ["Type 2 Diabetes", "Hypertension", "High Cholesterol"],
    status: "pending",
    patient_id: "user_123abc",
    dietary_preference: "Low-carb, Mediterranean-inspired",
    patient: {
      id: "user_123abc",
      name: "Jane Doe",
      age: 42,
      gender: "Female",
      email: "jane.doe@example.com"
    }
  },
  {
    id: 2,
    created_at: "2025-03-12T14:17:32Z",
    conditions: ["Gluten Intolerance", "IBS", "Vitamin D Deficiency"],
    status: "pending",
    patient_id: "user_456def",
    dietary_preference: "Gluten-free, High fiber",
    patient: {
      id: "user_456def",
      name: "Michael Johnson",
      age: 35,
      gender: "Male",
      email: "michael.j@example.com"
    }
  },
  {
    id: 3,
    created_at: "2025-03-14T09:42:18Z",
    conditions: ["GERD", "Lactose Intolerance"],
    status: "pending",
    patient_id: "user_789ghi",
    dietary_preference: "Dairy-free, Low acid",
    patient: {
      id: "user_789ghi",
      name: "Sarah Williams",
      age: 29,
      gender: "Female",
      email: "sarah.w@example.com"
    }
  },
  {
    id: 4,
    created_at: "2025-03-15T16:05:51Z",
    conditions: ["Pre-diabetes", "Obesity", "Sleep Apnea"],
    status: "pending",
    patient_id: "user_101jkl",
    dietary_preference: "Calorie restricted, High protein",
    patient: {
      id: "user_101jkl",
      name: "Robert Chen",
      age: 47,
      gender: "Male",
      email: "robert.c@example.com"
    }
  },
  {
    id: 5,
    created_at: "2025-03-15T18:33:27Z",
    conditions: ["Anemia", "Hypothyroidism"],
    status: "pending",
    patient_id: "user_202mno",
    dietary_preference: "Iron-rich, Balanced macros",
    patient: {
      id: "user_202mno",
      name: "Emily Rodriguez",
      age: 31,
      gender: "Female",
      email: "emily.r@example.com"
    }
  }
];

export default function DoctorDashboardPage() {
  const { user, isLoaded } = useUser();
  const [pendingRequests, setPendingRequests] = useState<PendingRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Flag to use dummy data (set to false when backend is ready)
  const useDummyData = true;

  useEffect(() => {
    async function fetchPendingRequests() {
      if (!isLoaded || !user) return;

      try {
        setLoading(true);
        
        if (useDummyData) {
          // Use dummy data for testing
          // Simulate a network delay
          setTimeout(() => {
            setPendingRequests(DUMMY_REQUESTS);
            setLoading(false);
          }, 800);
          
          return;
        }
        
        // Real API call for when backend is ready
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
        if (!useDummyData) {
          setLoading(false);
        }
      }
    }

    fetchPendingRequests();
  }, [user, isLoaded, useDummyData]);

  const handleReviewRequest = () => {
    // For demo purposes, always route to report/3
    // In production, this would use the actual requestId
    window.location.href = '/report/3';
    
    // When backend is ready, uncomment this:
    // window.location.href = `/report/${requestId}`;
  };

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
                    onClick={() => handleReviewRequest()}
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