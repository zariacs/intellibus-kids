"use client";
import React from 'react';
// import { useRouter } from 'next/navigation'
// import { useUser } from '@clerk/clerk-react';

export default function WelcomeLayout(
    {
        children,
      }: Readonly<{
        children: React.ReactNode
      }>) {

    return (
        <div>
            <h1>Welcome</h1>
            {children}
        </div>
    );
};