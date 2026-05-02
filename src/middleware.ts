import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

const isPublicRoute = createRouteMatcher([
  '/site',
  '/agency/sign-in(.*)',
  '/agency/sign-up(.*)',
  '/api/uploadthing',
]);

export default clerkMiddleware(async (auth, req) => {
    const url = req.nextUrl;
    const search = url.searchParams.toString();
    const pathWithSearch = `${url.pathname}${search ? `?${search}` : ''}`;
    // Root redirect to /site
    if (url.pathname === '/') {
      return NextResponse.redirect(new URL('/site', req.url));
    }

    // Signed-in users should not land on auth UI (Clerk redirects; avoids <SignIn/> error + wrong afterSignIn targets)
    {
      const { userId } = await auth();
      if (userId) {
        if (
          url.pathname === '/agency/sign-in' ||
          url.pathname.startsWith('/agency/sign-in/')
        ) {
          return NextResponse.redirect(new URL('/agency', req.url));
        }
        if (
          url.pathname === '/agency/sign-up' ||
          url.pathname.startsWith('/agency/sign-up/')
        ) {
          return NextResponse.redirect(new URL('/agency', req.url));
        }
      }
    }

    // Legacy/un-scoped auth paths — funnel everyone into the agency-scoped flow,
    // which is the only Clerk <SignIn/> mount in the app.
    if (url.pathname === '/sign-in' || url.pathname === '/sign-up') {
      return NextResponse.redirect(new URL('/agency/sign-in', req.url));
    }

    if (!isPublicRoute(req)) {
      await auth.protect();
    }

    // Multi-tenant routing: a request to `<tenant>.<NEXT_PUBLIC_DOMAIN>` is
    // rewritten to `/<tenant>/<path>` so a single Next.js app can serve every
    // agency/subaccount on its own subdomain without duplicating routes.
    const host = req.headers.get('host') || '';
    const customSubdomain = host
      .split(`${process.env.NEXT_PUBLIC_DOMAIN}`)
      .filter(Boolean)[0];

    if (customSubdomain) {
      return NextResponse.rewrite(new URL(`/${customSubdomain}${pathWithSearch}`, req.url));
    }

    if (
      url.pathname.startsWith('/agency') ||
      url.pathname.startsWith('/subaccount')
    ){
      return NextResponse.rewrite(new URL(pathWithSearch, req.url));
    }

    return NextResponse.next();
  },
  { debug: false } // Set true to see detailed logs during dev
);

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/',
    '/(api|trpc)(.*)',
  ],
};
