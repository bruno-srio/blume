import { getAuthUserDetails } from '@/lib/queries'
import React from 'react'
import MenuOptions from './menu-options'

type Props = {
  id: string
  type: 'agency' | 'subaccount'
}

const Sidebar = async ({ id, type }: Props) => {
  const user = await getAuthUserDetails()
  if (!user) return null

  if (!user.Agency) return
  // ?: path by type; ?. safe user access (Agency already guarded above)
  const details =
    type === 'agency'
      ? user?.Agency
      : user?.Agency.SubAccount.find((subaccount) => subaccount.id === id)

  const isWhiteLabel = user.Agency.whiteLabel
  if (!details) return 

  let sidebarLogo = user.Agency.agencyLogo || 'assets/plura-logo.svg'

  // White-label on: subaccounts show the agency logo. Off: they get their own.
  if (!isWhiteLabel) {
    if (type === "subaccount") {
      sidebarLogo =
        user?.Agency.SubAccount.find((subaccount) => subaccount.id === id)
          ?.subAccountLogo || user.Agency.agencyLogo;
    }
  }

  const sidebarOpt =
    type === 'agency'
      ? user.Agency.SidebarOption || []
      : user.Agency.SubAccount.find((subaccount) => subaccount.id === id)
          ?.SidebarOption || []

  // Switcher only lists subaccounts this user actually has access to.
  const subaccounts = user.Agency.SubAccount.filter((subaccount) =>
    user.Permissions.find(
      (permission) =>
        permission.subAccountId === subaccount.id && permission.access
    )
  )

  return (
    <>
    {/* Desktop: always-open rail. Mobile: drawer the burger can toggle. */}
    <MenuOptions
      defaultOpen={true}
      subAccounts={subaccounts}
      sidebarOptions={sidebarOpt}
      sidebarLogo={sidebarLogo}
      details={details}
      user={user}
      id={id}
    />
    {/* Same sidebar, but without defaultOpen — that's the mobile drawer. */}
    <MenuOptions
      subAccounts={subaccounts}
      sidebarOptions={sidebarOpt}
      sidebarLogo={sidebarLogo}
      details={details}
      user={user}
      id={id}
    />
    </>
  )
    
}

export default Sidebar