'use client'

import React, { useEffect, useMemo, useState } from 'react'
import { AgencySidebarOption, SubAccount, SubAccountSidebarOption } from '@/generated/prisma'
import { Menu } from 'lucide-react'
import { Button } from '../ui/button'
import { Sheet, SheetContent, SheetTrigger, SheetClose } from '../ui/sheet'
import Image from 'next/image'
import clsx from 'clsx'
import { AspectRatio } from '../ui/aspect-ratio'
import { Popover, PopoverContent, PopoverTrigger } from '../ui/popover'
import { ChevronsUpDown, Compass } from 'lucide-react'
import { Command, CommandInput, CommandList, CommandEmpty, CommandGroup, CommandItem } from '../ui/command'
import Link from 'next/link'


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

  // Only when the component is mounted, set the state to true
  useEffect(() => {
    setIsMounted(true)
  }, [])

  if (!isMounted) return

  // modal={false}: keep page content interactive (sidebar is not a blocking dialog)
  return (
    <Sheet 
      modal={false}
      open={true}
      // {...openState}
      >
      <SheetTrigger
        asChild
        className="absolute left-4 top-4 z-[100] md:!hidden flex"
      >
        <Button variant='outline' size='icon'>
          <Menu className='h-4 w-4' />
        </Button>
      </SheetTrigger>
      <SheetContent 
        showX={!defaultOpen}
        side='left'
        className={clsx(
          'bg-background/80 backdrop-blur-xl fixed top-0 border-r-[1px] p-6',
          {
            'hidden md:inline-block z-0 w-[300px]': defaultOpen,
            'inline-block md:hidden z-[100] w-full': !defaultOpen,
          }
        )}
        >
        <div>
         <AspectRatio ratio={16 / 5}>
          <Image 
            src={sidebarLogo} 
            alt='sidebar logo' 
            fill 
            className='object-contain' 
          />
          <Popover>
            <PopoverTrigger asChild>
              <Button 
                className='w-full my-4 flex items-center justify-between py-8' 
                variant='ghost'
              >
                <div className='flex items-center gap-2 text-left'>
                  <Compass />
                  <div className='flex flex-col'>
                    {details.name}
                    <span className='text-muted-foreground'>
                      {details.address}
                    </span>
                  </div>
                </div>
                <div>
                  <ChevronsUpDown
                    size={16}
                    className='text-muted-foreground'
                  />
                </div>
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-80 h-80 mt-4 z-[200]">
              <Command className="rounded-lg">
                <CommandInput placeholder="Search Accounts..." />
                <CommandList className="pb-16">
                  <CommandEmpty> No results found</CommandEmpty>
                  {(user?.role === "AGENCY_OWNER" ||
                    user?.role === "AGENCY_ADMIN") &&
                    user?.Agency && (
                      <CommandGroup heading="Agency">
                        <CommandItem className="!bg-transparent my-2 text-primary border-[1px] border-border p-2 rounded-md hover:!bg-muted cursor-pointer transition-all">
                          {defaultOpen ? (
                            <Link
                              href={`/agency/${user?.Agency?.id}`}
                              className="flex gap-4 w-full h-full"
                            >
                              <div className="relative w-16">
                                <Image
                                  src={user?.Agency?.agencyLogo}
                                  alt="Agency Logo"
                                  fill
                                  className="rounded-md object-contain"
                                />
                              </div>
                              <div className="flex flex-col flex-1">
                                {user?.Agency?.name}
                                <span className="text-muted-foreground">
                                  {user?.Agency?.address}
                                </span>
                              </div>
                            </Link>
                          ) : (
                            <SheetClose asChild>
                              <Link
                                href={`/agency/${user?.Agency?.id}`}
                                className="flex gap-4 w-full h-full"
                              >
                                <div className="relative w-16">
                                  <Image
                                    src={user?.Agency?.agencyLogo}
                                    alt="Agency Logo"
                                    fill
                                    className="rounded-md object-contain"
                                  />
                                </div>
                                <div className="flex flex-col flex-1">
                                  {user?.Agency?.name}
                                  <span className="text-muted-foreground">
                                    {user?.Agency?.address}
                                  </span>
                                </div>
                              </Link>
                            </SheetClose>
                          )}
                        </CommandItem>
                      </CommandGroup>
                    )}
                  <CommandGroup heading="Accounts">
                    {!!subAccounts
                      ? subAccounts.map((subaccount) => (
                          <CommandItem
                            className="!bg-transparent my-2 text-primary border-[1px] border-border p-2 rounded-md hover:!bg-muted cursor-pointer transition-all"
                            key={subaccount.id}
                          >
                            {defaultOpen ? (
                              <Link
                                href={`/subaccount/${subaccount.id}`}
                                className="flex gap-4 w-full h-full"
                              >
                                <div className="relative w-16">
                                  <Image
                                    src={subaccount.subAccountLogo}
                                    alt="subaccount Logo"
                                    fill
                                    className="rounded-md object-contain"
                                  />
                                </div>
                                <div className="flex flex-col flex-1">
                                  {subaccount.name}
                                  <span className="text-muted-foreground">
                                    {subaccount.address}
                                  </span>
                                </div>
                              </Link>
                            ) : (
                              <SheetClose asChild>
                                <Link
                                  href={`/subaccount/${subaccount.id}`}
                                  className="flex gap-4 w-full h-full"
                                >
                                  <div className="relative w-16">
                                    <Image
                                      src={subaccount.subAccountLogo}
                                      alt="subaccount Logo"
                                      fill
                                      className="rounded-md object-contain"
                                    />
                                  </div>
                                  <div className="flex flex-col flex-1">
                                    {subaccount.name}
                                    <span className="text-muted-foreground">
                                      {subaccount.address}
                                    </span>
                                  </div>
                                </Link>
                              </SheetClose>
                            )}
                          </CommandItem>
                        ))
                      : "No Accounts"}
                  </CommandGroup>
                </CommandList>
              </Command>
            </PopoverContent>
          </Popover>
         </AspectRatio>
        </div>

      </SheetContent>
    </Sheet>
  )
}

export default MenuOptions
