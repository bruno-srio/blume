import React from 'react'

const AuthLayout = ({ children }: { children: React.ReactNode }) => {
  // Just centers the Clerk sign-in/up widgets.
  return (
    <div className="h-full flex items-center justify-center" >{children}</div>
  )
}

export default AuthLayout