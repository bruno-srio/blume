# Blume

Blume is a multi-tenant agency management platform — "run your agency, in one place". An agency owns one or more sub-accounts (client workspaces), each with its own CRM pipelines, funnels, automations, media library, and team permissions. Stripe-based billing is planned but not yet wired up.

> **Status:** under active development. The marketing site, authentication, and agency onboarding are functional. The agency/sub-account dashboards, Stripe integration, and funnel subdomain pages are still in progress.

## Tech stack

- **Runtime / package manager:** [Bun](https://bun.sh)
- **Framework:** Next.js 14.2 (App Router) with TypeScript
- **Database:** MySQL via Prisma 6.9 (`relationMode = "prisma"`; client generated to `src/generated/prisma`)
- **Auth:** [Clerk](https://clerk.com)
- **File uploads:** [UploadThing](https://uploadthing.com) v7
- **UI:** shadcn/ui + Radix primitives, Tailwind CSS 3.4, lucide-react, sonner, next-themes
- **Forms:** react-hook-form + Zod
- **Charts:** Recharts / Tremor

## Prerequisites

- [Bun](https://bun.sh) installed
- A MySQL database (local or hosted, e.g. PlanetScale)
- A [Clerk](https://clerk.com) application
- An [UploadThing](https://uploadthing.com) app

## Environment variables

There is no `.env.example` yet — create a `.env` file in the project root with:

```bash
# MySQL connection string (used by prisma/schema.prisma)
DATABASE_URL="mysql://user:password@localhost:3306/blume"

# Clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="pk_test_..."
CLERK_SECRET_KEY="sk_test_..."

# UploadThing
UPLOADTHING_TOKEN="..."

# Base domain used by src/middleware.ts for subdomain -> tenant rewrites.
# Locally this is the dev host; in production, your apex domain.
NEXT_PUBLIC_DOMAIN="localhost:3000"
```

## Getting started

```bash
# Install dependencies
bun install

# Generate the Prisma client (output is gitignored, so this is required)
bunx prisma generate

# Push the schema to your MySQL database
bunx prisma db push

# Start the dev server
bun run dev
```

Open [http://localhost:3000](http://localhost:3000) — the root route redirects to the marketing site at `/site`. Sign up at `/agency/sign-up` to go through agency onboarding.

Other scripts:

```bash
bun run build   # production build
bun run start   # serve the production build
bun run lint    # ESLint
```

## Project structure

```
prisma/
└── schema.prisma        # Full domain model (Agency, SubAccount, Funnel, Pipeline, ...)
src/
├── app/
│   ├── site/            # Public marketing site (landing + pricing)
│   ├── (main)/agency/   # Authenticated area: onboarding, sign-in/sign-up (Clerk)
│   ├── [domain]/        # Tenant funnel pages served via subdomain rewrites (stubs)
│   └── api/uploadthing/ # UploadThing file router
├── components/
│   ├── ui/              # shadcn/ui components
│   ├── forms/           # e.g. agency-details
│   └── global/          # file upload, loading, theme toggle
├── lib/
│   ├── db.ts            # Prisma client singleton
│   ├── queries.ts       # Server actions (user init, invitations, agency CRUD)
│   └── constants.ts     # Pricing cards, icon map
└── middleware.ts        # Clerk auth + subdomain routing
```

## Architecture notes

**Multi-tenancy.** An `Agency` is the top-level tenant that owns billing and the team; `SubAccount`s are client workspaces holding CRM, funnels, media, and automations. Access is role-based (`AGENCY_OWNER`, `AGENCY_ADMIN`, `SUBACCOUNT_USER`, `SUBACCOUNT_GUEST`) with per-sub-account `Permissions`. New team members join via `Invitation`s, which are verified and accepted on first sign-in.

**Subdomain routing.** `src/middleware.ts` protects all routes with Clerk (except `/site`, the auth pages, and the upload API) and rewrites requests from `tenant.<NEXT_PUBLIC_DOMAIN>` to the `/[domain]` route, which is how published funnels will be served on their own subdomains.
