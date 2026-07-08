'use client'
import React from 'react'
import { AgencySidebarOption, SubAccount, SubAccountSidebarOption } from '@/generated/prisma'

type Props = {
  defaultOpen?: boolean
  subAccounts: SubAccount[]
  sidebarOptions: AgencySidebarOption[] | SubAccountSidebarOption[]
  sidebarLogo: string
  details: any
  user: any
  id: string
}

const MenuOptions = ({ defaultOpen, subAccounts, sidebarOptions, sidebarLogo, details, user, id }: Props) => {
  return <div>MenuOptions</div>
}

export default MenuOptions