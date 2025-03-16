// // app/actions/user-management.ts
// "use server";

// import { clerkClient } from "@clerk/nextjs/server";
// import { auth, currentUser } from "@clerk/nextjs";
// import { redirect } from "next/navigation";

// export async function updateUserRole(userId: string, role: string) {
//   // Security check: ensure current user is admin
//   const user = await currentUser();
  
//   if (user?.publicMetadata?.role !== "admin") {
//     throw new Error("Unauthorized");
//   }
  
//   try {
//     await clerkClient.users.updateUser(userId, {
//       publicMetadata: { role }
//     });
//     return { success: true };
//   } catch (error) {
//     console.error("Failed to update user role:", error);
//     throw new Error("Failed to update user role");
//   }
// }