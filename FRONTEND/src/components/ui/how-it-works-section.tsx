"use client";
import React from "react";
import { TextRevealCard, TextRevealCardTitle, TextRevealCardDescription } from "./text-reveal-card";
import { motion } from "framer-motion";

// Process steps for the app
const processSteps = [
  {
    title: "Secure Patient Registration",
    description: "Patients register with encrypted personal data, connecting with their healthcare providers in a HIPAA-compliant environment.",
    text: "Step 1: Registration",
    revealText: "Secure Onboarding"
  },
  {
    title: "Real-time Health Monitoring",
    description: "Continuous monitoring of vital signs through connected devices, with AI-powered analysis to detect anomalies.",
    text: "Step 2: Monitoring",
    revealText: "24/7 Tracking"
  },
  {
    title: "Doctor-Patient Collaboration",
    description: "Direct communication channels between patients and doctors, with secure video consultations and messaging.",
    text: "Step 3: Collaboration",
    revealText: "Virtual Care"
  },
  {
    title: "Personalized Treatment Plans",
    description: "AI-assisted treatment recommendations based on patient data and medical history, continuously refined over time.",
    text: "Step 4: Treatment",
    revealText: "Smart Healthcare"
  }
];

export function HowItWorksSection() {
  return (
    <section className="py-20 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-500 mb-4">
            How It Works
          </h2>
          <p className="text-gray-300 max-w-3xl mx-auto text-lg">
            Our platform connects patients and doctors through a seamless, secure digital experience
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-10 perspective-[1000px]">
          {processSteps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, rotateY: -10, z: -100 }}
              whileInView={{ opacity: 1, rotateY: 0, z: 0 }}
              transition={{ 
                duration: 0.8, 
                delay: index * 0.2,
                ease: [0.2, 0.65, 0.3, 0.9] 
              }}
              viewport={{ once: true, margin: "-100px" }}
              className="transform-gpu"
            >
              <TextRevealCard
                text={step.text}
                revealText={step.revealText}
                className="h-full w-full shadow-[0_0_20px_rgba(59,130,246,0.1)] backdrop-blur-sm bg-black/20 border-blue-500/5 hover:border-blue-500/20 transition-all duration-500"
              >
                <TextRevealCardTitle className="text-blue-300">{step.title}</TextRevealCardTitle>
                <TextRevealCardDescription className="text-gray-400">{step.description}</TextRevealCardDescription>
              </TextRevealCard>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Floating particles for depth effect */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {[...Array(15)].map((_, i) => (
          <motion.div
            key={`particle-${i}`}
            className="absolute w-2 h-2 rounded-full bg-blue-400/10"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
            }}
            animate={{
              x: [0, Math.random() * 100 - 50],
              y: [0, Math.random() * 100 - 50],
              scale: [0, Math.random() * 2 + 1, 0],
              opacity: [0, Math.random() * 0.3 + 0.05, 0],
            }}
            transition={{
              duration: Math.random() * 10 + 15,
              repeat: Infinity,
              ease: "linear",
            }}
          />
        ))}
      </div>
    </section>
  );
} 