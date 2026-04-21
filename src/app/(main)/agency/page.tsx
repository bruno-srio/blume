import { getAuthUserDetails } from '@/lib/queries'
import { verifyAndAcceptInvitation } from '@/lib/queries'
import { currentUser } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'
import React from 'react'

const Page = async () => {
  const agencyId = await verifyAndAcceptInvitation()
  console.log('AGENCY ID', agencyId)

  const user = await getAuthUserDetails()
  return (
    <div>Agency</div>
  )
}

export default Page