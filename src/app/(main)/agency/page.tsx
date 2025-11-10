import { getAuthUserDetails } from '@/lib/queries'
import { verifyAndAcceptInvitation } from '@/lib/queries'
import { currentUser } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'
import React from 'react'

const Page = async () => {
  const authUser = await currentUser()
  if (!authUser) {
    redirect('/sign-in')
  }

  const agencyId = await verifyAndAcceptInvitation()

  const user = await getAuthUserDetails()
  return (
    <div>Agency</div>
  )
}

export default Page