import { PrismaClient } from '@/generated/prisma'

// Cache the client on `globalThis` so Next.js HMR in dev doesn't spawn a new
// PrismaClient on every reload and exhaust the database connection pool.
// In production each Lambda/Function instance creates exactly one client.
declare global {
  var prisma: PrismaClient | undefined
}

export const db = globalThis.prisma || new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalThis.prisma = db