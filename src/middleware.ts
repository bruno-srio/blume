import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

const isPublicRoute = createRouteMatcher([
  '/site',
  '/agency/sign-in(.*)',
  '/agency/sign-up(.*)',
  '/api/uploadthing',
]);

export default clerkMiddleware(
  async (auth, req) => {
    const url = req.nextUrl;
    const search = url.searchParams.toString();
    const pathWithSearch = `${url.pathname}${search ? `?${search}` : ''}`;

    // Root redirect to /site
    if (url.pathname === '/') {
      return NextResponse.redirect(new URL('/site', req.url));
    }

    // 
    if (url.pathname === '/sign-in' || url.pathname === '/sign-up') {
      return NextResponse.redirect(new URL('/agency/sign-in', req.url));
    }

    // Custom rewrite for subdomains
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

    // Protect private routes with auth
    if (!isPublicRoute(req)) {
      await auth.protect();
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
