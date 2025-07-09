import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// List of routes that do not require authentication
const PUBLIC_PATHS = ['/login', '/register', '/_next', '/api'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow public paths
  if (PUBLIC_PATHS.some((path) => pathname.startsWith(path))) {
    return NextResponse.next();
  }

  // Check for access token in cookies
  const accessToken = request.cookies.get('access_token');

  if (!accessToken) {
    // Redirect to login if not authenticated
    const loginUrl = request.nextUrl.clone();
    loginUrl.pathname = '/login';
    loginUrl.searchParams.set('from', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Allow request to proceed
  return NextResponse.next();
}

// Specify the paths the middleware should run on
export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}; 