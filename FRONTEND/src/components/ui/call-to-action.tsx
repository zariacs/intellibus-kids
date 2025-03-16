"use client";
import React from "react";
import { motion } from "framer-motion";
import { MoveRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { SignUpButton } from "@clerk/nextjs";

export function CallToAction() {
  return (
    <section className="relative py-24 overflow-hidden">
      {/* Gradient background */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-900/20 to-indigo-900/20 opacity-50" />

      {/* Animated particles */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(15)].map((_, i) => (
          <motion.div
            key={`cta-particle-${i}`}
            className="absolute w-2 h-2 rounded-full bg-blue-400/10"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, Math.random() * 50 - 25],
              x: [0, Math.random() * 50 - 25],
              scale: [0, Math.random() * 1.5 + 0.5, 0],
              opacity: [0, Math.random() * 0.3 + 0.1, 0],
            }}
            transition={{
              duration: Math.random() * 8 + 10,
              repeat: Infinity,
              ease: "linear",
            }}
          />
        ))}
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-300 via-indigo-400 to-purple-400">
              Transform Your Health Journey Today
            </h2>
            <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
              Join thousands who've already discovered the power of 
              personalized nutritional guidance. Start your path to better health now.
            </p>

            <div className="flex flex-wrap gap-4 justify-center">
              <SignUpButton mode="modal">
                <Button size="lg" className="gap-2 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 border-0 text-lg px-8 py-6">
                  Get Started <MoveRight className="w-5 h-5" />
                </Button>
              </SignUpButton>
              
              <motion.div 
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
              >
                <Button 
                  variant="outline" 
                  size="lg" 
                  className="gap-2 border border-blue-500/20 hover:border-blue-500/40 bg-black/20 text-white hover:bg-black/30 text-lg px-8 py-6"
                >
                  Schedule a Demo
                </Button>
              </motion.div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            viewport={{ once: true }}
            className="mt-16 pt-8 border-t border-blue-500/10"
          >
            <p className="text-gray-400 italic">
              "This platform literally changed my life. After years of struggling with dietary issues, 
              I finally have a solution that works for me." — Alex, Patient
            </p>
          </motion.div>
        </div>
      </div>
    </section>
  );
} 