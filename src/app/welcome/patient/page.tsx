import React from 'react';
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const patients = [
    { id: 1, name: 'John Doe', age: 30, condition: 'Flu' },
    { id: 2, name: 'Jane Smith', age: 25, condition: 'Cold' },
    { id: 3, name: 'Sam Johnson', age: 40, condition: 'Asthma' },
];

export default function Doctor() {
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Patient List I am a patient</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {patients.map((patient) => (
                    <Card key={patient.id} className="shadow-lg">
                        <CardHeader>
                            <h2 className="text-xl font-semibold">{patient.name}</h2>
                        </CardHeader>
                        <CardContent>
                            <p>Age: {patient.age}</p>
                            <p>Condition: {patient.condition}</p>
                        </CardContent>
                        <CardFooter>
                            <Button className="">View Details</Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>
        </div>
    );
};