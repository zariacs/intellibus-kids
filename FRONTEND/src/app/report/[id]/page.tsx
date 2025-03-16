"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { useUser } from "@clerk/nextjs";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Spinner } from "@/components/ui/spinner";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Printer, ArrowLeft, Download, CheckCircle } from "lucide-react";

// Dummy report in markdown format for testing
const DUMMY_REPORT = `# Medical Report for Jane Doe

## Patient Details
•⁠  ⁠Name: Jane Doe
•⁠  ⁠Age: 42 years
•⁠  ⁠Gender: Female
•⁠  ⁠Weight: 78.5 kg
•⁠  ⁠Height: 165.3 cm
•⁠  ⁠Condition: Type 2 Diabetes
•⁠  ⁠Allergies: dairy, shellfish, peanuts

## Definition of Type 2 Diabetes

Type 2 diabetes is a chronic metabolic disorder characterized by high blood sugar (glucose) levels. This occurs when the body either doesn't produce enough insulin or doesn't use insulin effectively, a condition called insulin resistance.  Insulin is a hormone produced by the pancreas that regulates the movement of glucose from the bloodstream into cells for energy.  Over time, high blood sugar can damage various organs, including the heart, kidneys, eyes, and nerves.

## Challenges Faced By Patient

Based on Jane Doe's profile, she might face the following challenges:

1.⁠ ⁠*Managing Blood Sugar Levels:*  Fluctuations in blood glucose can lead to the symptoms she's experiencing, such as frequent urination, increased thirst, fatigue, and blurred vision.  Maintaining stable blood sugar through diet, medication, and exercise is crucial.
2.⁠ ⁠*Dietary Restrictions:*  Balancing her low-carb, gluten-free, and Mediterranean-inspired dietary preferences with the need for diabetic-friendly meals can be complex.  Careful meal planning and ingredient selection are essential.
3.⁠ ⁠*Medication Management:*  Adhering to her prescribed medications (Metformin, Lisinopril, and Atorvastatin) while also managing potential side effects and drug interactions requires attention.
4.⁠ ⁠*Potential Complications:*  Long-term uncontrolled diabetes can increase the risk of developing complications like cardiovascular disease, kidney disease, neuropathy, and retinopathy.  Proactive management is crucial to minimize these risks.
5.⁠ ⁠*Lifestyle Changes:*  Adopting and maintaining a healthy lifestyle, including regular exercise and stress management, is essential for managing type 2 diabetes effectively.


## Recommended Meal Plan

| Day | Breakfast (kcal) | Lunch (kcal) | Dinner (kcal) |
|-----|------------------|--------------|---------------|
| Monday | Almond Flour Pancakes with Berries and Sugar-Free Syrup (350 kcal) | Grilled Chicken Salad with Mixed Greens, Avocado, and Olive Oil Dressing (400 kcal) | Salmon with Roasted Asparagus and Quinoa (450 kcal) |
| Tuesday | Scrambled Eggs with Spinach and Tomatoes (300 kcal) | Leftover Salmon with a Side Salad (400 kcal) | Chicken Stir-Fry with Brown Rice and Mixed Vegetables (450 kcal) |
| Wednesday | Chia Seed Pudding with Almond Milk and Berries (350 kcal) | Tuna Salad Lettuce Wraps (350 kcal) | Ground Turkey and Vegetable Skewers with Brown Rice (450 kcal) |
| Thursday | Smoothie with Almond Milk, Spinach, Berries, and Protein Powder (300 kcal) | Leftover Ground Turkey Skewers with a Side Salad (400 kcal) | Baked Chicken Breast with Roasted Sweet Potatoes and Green Beans (450 kcal) |
| Friday | Almond Flour Waffles with Sugar-Free Syrup and Berries (350 kcal) | Shrimp Salad with Avocado and Mixed Greens (400 kcal) | Grilled Salmon with Roasted Broccoli and Quinoa (450 kcal) |
| Saturday | Omelette with Mushrooms, Onions, and Peppers (300 kcal) | Leftover Grilled Salmon with a Side Salad (400 kcal) | Chicken and Vegetable Curry with Brown Rice (450 kcal)|
| Sunday |  Breakfast Burrito with Scrambled Eggs, Black Beans, Salsa, and Avocado (350 kcal) | Leftover Chicken Curry (400 kcal) |  Steak with Roasted Asparagus and Sweet Potato Fries (500 kcal) |


## Ingredients

### Produce

•⁠  ⁠Spinach
•⁠  ⁠Tomatoes
•⁠  ⁠Berries (strawberries, blueberries, raspberries)
•⁠  ⁠Avocado
•⁠  ⁠Mixed Greens
•⁠  ⁠Asparagus
•⁠  ⁠Broccoli
•⁠  ⁠Mushrooms
•⁠  ⁠Onions
•⁠  ⁠Peppers
•⁠  ⁠Sweet Potatoes


### Groceries

•⁠  ⁠Chicken Breast
•⁠  ⁠Ground Turkey
•⁠  ⁠Salmon
•⁠  ⁠Tuna
•⁠  ⁠Eggs
•⁠  ⁠Almond Milk
•⁠  ⁠Sugar-Free Syrup
•⁠  ⁠Olive Oil
•⁠  ⁠Shrimp
•⁠  ⁠Steak


### Dry Goods

•⁠  ⁠Almond Flour
•⁠  ⁠Chia Seeds
•⁠  ⁠Quinoa
•⁠  ⁠Brown Rice
•⁠  ⁠Protein Powder
•⁠  ⁠Spices (for curry, etc.)
•⁠  ⁠Salsa
•⁠  ⁠Black Beans`;

export default function PatientReportViewer() {
  const params = useParams();
  const { user, isLoaded } = useUser();
  const [markdownContent, setMarkdownContent] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [patientName, setPatientName] = useState<string>("");
  const [isApproving, setIsApproving] = useState(false);
  const [isApproved, setIsApproved] = useState(false);
  
  // Flag to use dummy data (set to false when backend is ready)
  const useDummyData = true;

  const reportId = params.id as string;
  
  // Get user role from Clerk public metadata
  const userRole = user?.publicMetadata?.role as string | undefined;
  const isDoctor = userRole === 'doctor';
  const isPatient = userRole === 'patient';

  useEffect(() => {
    async function fetchReportContent() {
      if (!isLoaded || !user) return;

      try {
        setLoading(true);
        
        if (useDummyData) {
          // Use dummy data for testing
          setMarkdownContent(DUMMY_REPORT);
          
          // Extract patient name from the dummy report
          const nameMatch = DUMMY_REPORT.match(/Name:\s*([^\n•]*)/);
          if (nameMatch && nameMatch[1]) {
            setPatientName(nameMatch[1].trim());
          }
          
          // Simulate network delay for testing loading state
          setTimeout(() => {
            setLoading(false);
          }, 800);
          
          return;
        }
        
        // Real API call for when backend is ready
        const response = await fetch(`/api/reports/${reportId}`);
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Failed to fetch report");
        }
        
        const data = await response.json();
        setMarkdownContent(data.content);
        
        // Extract patient name from markdown if possible
        const nameMatch = data.content.match(/Name:\s*([^\n•]*)/);
        if (nameMatch && nameMatch[1]) {
          setPatientName(nameMatch[1].trim());
        }
      } catch (err) {
        console.error("Error fetching report:", err);
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        if (!useDummyData) {
          setLoading(false);
        }
      }
    }

    fetchReportContent();
  }, [reportId, user, isLoaded, useDummyData]);

  const handlePrint = () => {
    window.print();
  };

  const handleDownload = () => {
    const blob = new Blob([markdownContent], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `medical_report_${patientName.replace(/\s+/g, "_") || reportId}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
  
  const handleApprove = async () => {
    setIsApproving(true);
    
    try {
      if (useDummyData) {
        // Simulate API call for approving the report
        await new Promise(resolve => setTimeout(resolve, 1000));
        setIsApproved(true);
      } else {
        // Real API call for when backend is ready
        const response = await fetch(`/api/reports/${reportId}/approve`, {
          method: 'POST',
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Failed to approve report");
        }
        
        setIsApproved(true);
      }
    } catch (err) {
      console.error("Error approving report:", err);
      setError(err instanceof Error ? err.message : "Failed to approve report");
    } finally {
      setIsApproving(false);
    }
  };

  // Get the appropriate return URL based on user role
  const getReturnUrl = () => {
    if (isDoctor) return '/doctor';
    if (isPatient) return '/patient';
    return '/';
  };

  if (!isLoaded || loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spinner className="h-8 w-8" />
        <span className="ml-2">Loading medical report...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8">
        <Button 
          variant="ghost" 
          className="mb-4" 
          onClick={() => window.location.href = getReturnUrl()}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back
        </Button>
        
        <Alert variant="destructive" className="max-w-4xl mx-auto">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 print:py-0">
      {/* Header with actions - hidden when printing */}
      <div className="flex justify-between items-center mb-6 print:hidden">
        <Button 
          variant="ghost" 
          onClick={() => window.location.href = getReturnUrl()}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back
        </Button>
        
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            onClick={handleDownload}
          >
            <Download className="mr-2 h-4 w-4" />
            Download
          </Button>
          <Button 
            variant="default" 
            onClick={handlePrint}
          >
            <Printer className="mr-2 h-4 w-4" />
            Print
          </Button>
        </div>
      </div>
      
      {/* Report content */}
      <Card className="max-w-4xl mx-auto shadow-sm print:shadow-none print:border-none">
        <CardContent className="p-8 print:p-0">
          <div className="markdown-content prose prose-slate max-w-none">
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({...props}) => <h1 className="text-3xl font-bold mt-6 mb-4 text-blue-800" {...props} />,
                h2: ({...props}) => <h2 className="text-2xl font-bold mt-6 mb-3 text-blue-700 border-b pb-1" {...props} />,
                h3: ({...props}) => <h3 className="text-xl font-semibold mt-4 mb-2 text-blue-600" {...props} />,
                p: ({...props}) => <p className="my-3 leading-relaxed" {...props} />,
                ul: ({...props}) => <ul className="my-3 list-disc pl-6" {...props} />,
                ol: ({...props}) => <ol className="my-3 list-decimal pl-6" {...props} />,
                li: ({...props}) => <li className="my-1" {...props} />,
                table: ({...props}) => (
                  <div className="overflow-x-auto my-4">
                    <table className="min-w-full border-collapse border border-gray-300" {...props} />
                  </div>
                ),
                thead: ({...props}) => <thead className="bg-gray-100" {...props} />,
                th: ({...props}) => <th className="border border-gray-300 px-4 py-2 text-left font-semibold" {...props} />,
                td: ({...props}) => <td className="border border-gray-300 px-4 py-2" {...props} />,
                tr: ({...props}) => <tr className="even:bg-gray-50" {...props} />,
                a: ({...props}) => <a className="text-blue-600 hover:underline" {...props} />,
                strong: ({...props}) => <strong className="font-bold" {...props} />,
                em: ({...props}) => <em className="italic" {...props} />,
                blockquote: ({...props}) => <blockquote className="border-l-4 border-gray-300 pl-4 italic my-4" {...props} />,
                code: ({...props}) => <code className="bg-gray-100 rounded px-1 py-0.5 font-mono text-sm" {...props} />,
              }}
            >
              {markdownContent}
            </ReactMarkdown>
          </div>
        </CardContent>
        
        {/* Only show approval button for doctors - hidden when printing */}
        {isDoctor && (
          <CardFooter className="px-8 py-4 bg-gray-50 print:hidden">
            {isApproved ? (
              <div className="w-full flex items-center justify-center p-2 bg-green-50 text-green-700 rounded-md">
                <CheckCircle className="mr-2 h-5 w-5" />
                Report approved successfully
              </div>
            ) : (
              <Button 
                className="w-full" 
                size="lg"
                disabled={isApproving}
                onClick={handleApprove}
              >
                {isApproving ? (
                  <>
                    <Spinner className="mr-2 h-4 w-4" />
                    Approving...
                  </>
                ) : (
                  <>
                    <CheckCircle className="mr-2 h-5 w-5" />
                    Approve Report
                  </>
                )}
              </Button>
            )}
          </CardFooter>
        )}
      </Card>
      
      {/* Print-specific styles */}
      <style jsx global>{`
        @media print {
          body {
            color: black;
            background: white;
          }
          .markdown-content {
            font-size: 12pt;
          }
          .markdown-content h1 {
            font-size: 18pt;
          }
          .markdown-content h2 {
            font-size: 16pt;
          }
          .markdown-content h3 {
            font-size: 14pt;
          }
          @page {
            margin: 2cm;
          }
        }
      `}</style>
    </div>
  );
}