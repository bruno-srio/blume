'use client'

import React, { useEffect, useMemo, useState } from 'react'
import { AgencySidebarOption, SubAccount, SubAccountSidebarOption } from '@/generated/prisma'
import { Menu } from 'lucide-react'
import { Button } from '../ui/button'
import { Sheet, SheetTrigger } from '../ui/sheet'

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
  
  // Prevents the sidebar from flashing on page load
  const [isMounted, setIsMounted] = useState(false)

  // Force open for the persistent desktop rail; omit for the mobile sheet so it stays uncontrolled.
  const openState = useMemo(
    () => (defaultOpen ? { open: true } : {}),
    [defaultOpen]
  )

  useEffect(() => {
    setIsMounted(true)
  }, [])

  if (!isMounted) return

  // modal={false}: keep page content interactive (sidebar is not a blocking dialog)
  return (
    <Sheet modal={false} {...openState}>
      {/* TODO: Menu button as SheetTrigger child for mobile */} 
      <SheetTrigger
        asChild
        className="absolute left-4 top-4 z-[100] md:!hidden flex"
      >
        <Button variant="outline" size="icon">
          <Menu className="h-4 w-4" />
        </Button>
      </SheetTrigger>
    </Sheet>
  )
}

export default MenuOptions
