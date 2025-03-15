export {}

// Create a type for the roles
export type Roles = 'admin' | 'moderator' | 'doctor' | 'patient'

declare global {
  interface CustomJwtSessionClaims {
    metadata: {
      role?: Roles
    }
  }
}