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

  // if not white label, use subaccount logo if available
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

  const subaccounts = user.Agency.SubAccount.filter((subaccount) =>
    user.Permissions.find(
      (permission) =>
        permission.subAccountId === subaccount.id && permission.access
    )
  )

  return (
    <>
    <MenuOptions
      defaultOpen={true}
      subAccounts={subaccounts}
      sidebarOptions={sidebarOpt}
      sidebarLogo={sidebarLogo}
      details={details}
      user={user}
      id={id}
    />
    <MenuOptions
      defaultOpen={true}
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