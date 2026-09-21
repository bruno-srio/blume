import { ClerkProvider } from '@clerk/nextjs'
import { dark } from '@clerk/themes'
import React from 'react'

const Layout = ({children}: {children: React.ReactNode}) => {
  // Logged-in app (agency/subaccount). Marketing site has its own ClerkProvider in site/layout.
  return (
    <ClerkProvider appearance={{baseTheme: dark}}>
        {children}
    </ClerkProvider>
  )
}

export default Layout