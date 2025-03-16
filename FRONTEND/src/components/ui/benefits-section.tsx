import { CalendarClock, Award, Sparkles, Salad } from "lucide-react";
import { Badge } from "@/components/ui/badge";

function BenefitsSection() {
  return (
    <div className="w-full py-20">
      <div className="container mx-auto">
        <div className="flex flex-col gap-10">
          <div className="flex gap-4 flex-col items-start">
            <div>
              <Badge className="bg-blue-500/20 text-blue-300 hover:bg-blue-500/30">Benefits</Badge>
            </div>
            <div className="flex gap-2 flex-col">
              <h2 className="text-3xl md:text-5xl tracking-tighter max-w-xl font-regular text-left text-white">
                Why choose our solution?
              </h2>
              <p className="text-lg max-w-xl lg:max-w-lg leading-relaxed tracking-tight text-gray-400 text-left">
                Traditional dietary consultations take months. We deliver personalized advice in minutes.
              </p>
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-black/20 backdrop-blur-sm rounded-md h-full lg:col-span-2 p-6 aspect-square lg:aspect-auto flex justify-between flex-col border border-blue-500/5 hover:border-blue-500/20 transition-all shadow-[0_0_15px_rgba(59,130,246,0.05)]">
              <CalendarClock className="w-8 h-8 stroke-1 text-blue-300" />
              <div className="flex flex-col">
                <h3 className="text-xl tracking-tight text-white">Save Months of Waiting</h3>
                <p className="text-gray-400 max-w-xs text-base">
                  Skip the long waitlists for specialist appointments and get dietary recommendations immediately.
                </p>
              </div>
            </div>
            <div className="bg-black/20 backdrop-blur-sm rounded-md aspect-square p-6 flex justify-between flex-col border border-blue-500/5 hover:border-blue-500/20 transition-all shadow-[0_0_15px_rgba(59,130,246,0.05)]">
              <Award className="w-8 h-8 stroke-1 text-blue-300" />
              <div className="flex flex-col">
                <h3 className="text-xl tracking-tight text-white">Doctor Verified</h3>
                <p className="text-gray-400 max-w-xs text-base">
                  All recommendations are reviewed by qualified healthcare professionals for safety and efficacy.
                </p>
              </div>
            </div>

            <div className="bg-black/20 backdrop-blur-sm rounded-md aspect-square p-6 flex justify-between flex-col border border-blue-500/5 hover:border-blue-500/20 transition-all shadow-[0_0_15px_rgba(59,130,246,0.05)]">
              <Sparkles className="w-8 h-8 stroke-1 text-blue-300" />
              <div className="flex flex-col">
                <h3 className="text-xl tracking-tight text-white">AI-Powered Personalization</h3>
                <p className="text-gray-400 max-w-xs text-base">
                  Get meal plans tailored to your specific condition, preferences, and dietary restrictions.
                </p>
              </div>
            </div>
            <div className="bg-black/20 backdrop-blur-sm rounded-md h-full lg:col-span-2 p-6 aspect-square lg:aspect-auto flex justify-between flex-col border border-blue-500/5 hover:border-blue-500/20 transition-all shadow-[0_0_15px_rgba(59,130,246,0.05)]">
              <Salad className="w-8 h-8 stroke-1 text-blue-300" />
              <div className="flex flex-col">
                <h3 className="text-xl tracking-tight text-white">Specialized Diets Made Easy</h3>
                <p className="text-gray-400 max-w-xs text-base">
                  From low-FODMAP to gluten-free, we make specialized dietary management simple and accessible.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export { BenefitsSection }; 