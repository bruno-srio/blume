import Unauthorized from '@/components/unauthorized'
import Sidebar from '@/components/sidebar'
import { getNotifications } from '@/lib/queries'
import { verifyAndAcceptInvitation } from '@/lib/queries'
import { currentUser } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'
import React from 'react'

type Props = {
  children: React.ReactNode
  params: {
    agencyId: string
  }
}

const layout = async ({ children, params }: Props) => {
  // Accept a pending invite if there is one, then verify: signed in, has an agency, owner/admin only.
  const agencyId = await verifyAndAcceptInvitation()
  const user = await currentUser()

  if (!user) {
    return redirect('/')
  }

  if (!agencyId) {
    return redirect('/agency')
  }

  if (
    user.privateMetadata.role !== "AGENCY_OWNER" &&
    user.privateMetadata.role !== "AGENCY_ADMIN"
  )
    return <Unauthorized/>

    // Pulled here so a notification bell can hang on this layout later — not rendered yet.
    let allNotifications: any = []
    const notifications = await getNotifications(agencyId)
    if (notifications) {
      allNotifications = notifications
    }

    return (
      <div className='h-screen overflow-hidden'>
        <Sidebar id={params.agencyId} type='agency'/>
        {/* 300px = sidebar width — don't let page content slide under the rail. */}
        <div className='md:pl-[300px]'>{children}</div>
      </div>
    )
}

export default layout