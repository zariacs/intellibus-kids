// import React from 'react';
// import { useRouter } from 'next/navigation'
// import { useUser } from '@clerk/clerk-react';
"use client";
import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation'
import { useUser } from '@clerk/clerk-react';

export default function WelcomePage({
    children,
  }: Readonly<{
    children: React.ReactNode
  }>) {
    const { user } = useUser();
    const router = useRouter()
    const status: boolean = true;

    useEffect(() => {
        if (status) {
            router.push('/welcome/doctor');
        }
        // if (user) {
        //     const role = user.publicMetadata.role;
        //     if (role === 'doctor') {
        //         router.push('/doctor');
        //     } else if (role === 'patient') {
        //         router.push('/patient');
        //     }
        // }
    }, []);

    return (
        <div>
            <h1>Welcome</h1>
            {children}
        </div>
    );
};