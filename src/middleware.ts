import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

// Marketing + auth + uploads can be hit without being signed in.
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

    if (url.pathname === '/') {
      return NextResponse.redirect(new URL('/site', req.url));
    }

    // Already signed in? Don't dump them on the Clerk sign-in/up screens again.
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

    // Bare /sign-in and /sign-up aren't mounted — send everyone to the agency Clerk pages.
    if (url.pathname === '/sign-in' || url.pathname === '/sign-up') {
      return NextResponse.redirect(new URL('/agency/sign-in', req.url));
    }

    if (!isPublicRoute(req)) {
      await auth.protect();
    }

    // Custom subdomain (`tenant.yourdomain`) is rewritten to `/tenant/path`
    // so one Next app can serve every agency/subaccount site.
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
  { debug: false } // flip to true if Clerk auth redirects are acting up
);

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/',
    '/(api|trpc)(.*)',
  ],
};
