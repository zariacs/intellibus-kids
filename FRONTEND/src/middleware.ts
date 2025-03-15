import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

const isDoctorRoute = createRouteMatcher(['/welcome/doctor(.*)'])
const isPatientRoute = createRouteMatcher(['/welcome/patient(.*)'])

export default clerkMiddleware(async (auth, req) => {
  // Protect all routes starting with `/admin`
  if (isDoctorRoute(req) && (await auth()).sessionClaims?.metadata?.role !== 'doctor') {
    const url = new URL('/', req.url)
    return NextResponse.redirect(url)
  }
  if (isPatientRoute(req) && (await auth()).sessionClaims?.metadata?.role !== 'patient') {
    const url = new URL('/', req.url)
    return NextResponse.redirect(url)
  }
})

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
};