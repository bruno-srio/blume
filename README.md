# Blume

Blume is a multi-tenant agency management platform — "run your agency, in one place". An agency owns one or more sub-accounts (client workspaces), each with its own CRM pipelines, funnels, automations, media library, and team permissions. Stripe-based billing is planned but not yet wired up.

> **Status:** under active development. Auth, agency onboarding, the agency sidebar shell, and creating sub-accounts from the switcher are in place. Dashboard widgets, sub-account pages, Stripe billing, and funnel subdomain sites are still stubs or unbuilt.

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

Open [http://localhost:3000](http://localhost:3000) — the root route redirects to the marketing site at `/site`. Sign up at `/agency/sign-up` to create an agency; after that you land on `/agency/[agencyId]` with the sidebar.

Other scripts:

```bash
bun run build   # production build
bun run start   # serve the production build
bun run lint    # ESLint
```

## Current progress

**Working**
- Marketing landing + pricing at `/site` (Stripe “Get Started” plan IDs are placeholders)
- Clerk sign-in / sign-up at `/agency/sign-in` and `/agency/sign-up`
- Agency create/edit form, logo upload (16:5 preview), delete (signs out after), optional growth goal
- Agency layout: invite accept, role gate (owner/admin), unauthorized page
- Dual sidebar — always-open desktop rail + mobile drawer, searchable menu links, white-label logos
- Account switcher: jump to the agency or a sub-account you have access to; owners/admins can create a sub-account from a modal
- Sub-account upsert seeds default sidebar links and grants the agency owner access
- Global modal provider (sidebar “Create Sub Account” uses this)

**In progress / stubbed**
- Agency dashboard page currently just prints the `agencyId`
- Notifications are fetched in the agency layout but not shown
- Custom-domain funnel routes (`/[domain]`) are empty placeholders; middleware already rewrites subdomains there
- Stripe billing, Connect, and customer IDs are sketched in forms/queries but not wired

**Not started (schema exists, no UI yet)**
- Sub-account app shell (`/subaccount/[id]`) and its pages: dashboard, funnels, pipelines, media, automations, contacts, launchpad, settings
- Agency pages behind the menu: team, billing, launchpad, all sub-accounts, settings
- Team invitations UI (accept-on-sign-in already exists in `verifyAndAcceptInvitation`)

## Project structure

```
prisma/
└── schema.prisma          # Full domain model (Agency, SubAccount, Funnel, Pipeline, ...)
src/
├── app/
│   ├── site/              # Public marketing site (landing + pricing)
│   ├── (main)/agency/     # Auth, onboarding, agency shell + sidebar
│   ├── [domain]/          # Tenant funnel pages via subdomain rewrites (stubs)
│   └── api/uploadthing/   # UploadThing file router
├── components/
│   ├── sidebar/           # Agency/sub-account rail + account switcher
│   ├── forms/             # agency-details, subaccount-details
│   ├── global/            # file upload, custom modal, loading, theme toggle
│   └── ui/                # shadcn/ui components
├── providers/             # Theme + modal context
├── lib/
│   ├── db.ts              # Prisma client singleton
│   ├── queries.ts         # Server actions (user, invitations, agency/sub-account CRUD)
│   └── constants.ts       # Pricing cards, sidebar icon map
└── middleware.ts          # Clerk auth + subdomain routing
```

## Architecture notes

**Multi-tenancy.** An `Agency` is the top-level tenant that owns billing and the team; `SubAccount`s are client workspaces holding CRM, funnels, media, and automations. Access is role-based (`AGENCY_OWNER`, `AGENCY_ADMIN`, `SUBACCOUNT_USER`, `SUBACCOUNT_GUEST`) with per-sub-account `Permissions`. New team members join via `Invitation`s, which are verified and accepted on first sign-in.

**Sidebar.** `Sidebar` renders `MenuOptions` twice: `defaultOpen` for the desktop rail, uncontrolled for the mobile drawer. Menu link names/icons live in the DB (`AgencySidebarOption` / `SubAccountSidebarOption`); the icon string is mapped in `src/lib/constants.ts`. Creating a sub-account from the switcher closes the popover first so it doesn't cover the modal.

**Subdomain routing.** `src/middleware.ts` protects all routes with Clerk (except `/site`, the auth pages, and the upload API) and rewrites requests from `tenant.<NEXT_PUBLIC_DOMAIN>` to the `/[domain]` route, which is how published funnels will be served on their own subdomains.
