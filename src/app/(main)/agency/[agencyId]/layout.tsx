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

    let allNotifications: any = []
    const notifications = await getNotifications(agencyId)
    if (notifications) {
      allNotifications = notifications
    }

    return (
      <div className='h-screen overflow-hidden'>
        <Sidebar id={params.agencyId} type='agency'/>
        <div className='md:pl-[300px]'>{children}</div>
      </div>
    )
}

export default layout