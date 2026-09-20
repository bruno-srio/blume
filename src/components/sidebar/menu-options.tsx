'use client'

import React, { useEffect, useMemo, useState } from 'react'
import { Agency, AgencySidebarOption, SubAccount, SubAccountSidebarOption } from '@/generated/prisma'
import { Menu, PlusCircleIcon } from 'lucide-react'
import { icons } from '@/lib/constants'
import { Button } from '../ui/button'
import { Sheet, SheetContent, SheetTrigger, SheetClose } from '../ui/sheet'
import Image from 'next/image'
import clsx from 'clsx'
import { AspectRatio } from '../ui/aspect-ratio'
import { Popover, PopoverContent, PopoverTrigger } from '../ui/popover'
import { ChevronsUpDown, Compass } from 'lucide-react'
import { Command, CommandInput, CommandList, CommandEmpty, CommandGroup, CommandItem } from '../ui/command'
import Link from 'next/link'
import CustomModal from '../global/custom-modal'
import { useModal } from '@/providers/modal-provider'
import SubAccountDetails from '../forms/subaccount-details'
import { Separator } from '../ui/separator'



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
  
  const { setOpen, isOpen: isModalOpen } = useModal()
  // Avoid hydration mismatch / flash: Sheet markup only after client mount.
  const [isMounted, setIsMounted] = useState(false)
  // Controlled so Create Sub Account can dismiss the switcher before the modal opens (avoids z-[200] popover over the dialog).
  const [popoverOpen, setPopoverOpen] = useState(false)

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
    <Sheet 
      modal={false}
      {...openState}
      >
      {/* Hide burger while a global modal is open — it sits at z-100 above Dialog (z-50). */}
      {!isModalOpen && (
        <SheetTrigger
          asChild
          className="absolute left-4 top-4 z-[100] md:!hidden flex"
        >
          <Button variant='outline' size='icon'>
            <Menu className='h-4 w-4' />
          </Button>
        </SheetTrigger>
      )}
      <SheetContent 
        // Desktop rail stays open — hide the close (X); mobile sheet needs it.
        showX={!defaultOpen}
        side='left'
        className={clsx(
          'bg-background/80 backdrop-blur-xl fixed top-0 border-r-[1px] p-6',
          {
            // Two instances render (desktop + mobile); only one is visible per breakpoint.
            'hidden md:inline-block z-0 w-[300px]': defaultOpen,
            'inline-block md:hidden z-[100] w-full': !defaultOpen,
          }
        )}
        >
        <div>
         {/* Logo alone in AspectRatio so odd-sized uploads can't overflow into the switcher below. */}
         <AspectRatio ratio={16 / 5} className='overflow-hidden'>
          <Image 
            src={sidebarLogo} 
            alt='sidebar logo' 
            fill 
            className='object-contain' 
            sizes='300px'
          />
         </AspectRatio>
          <Popover open={popoverOpen} onOpenChange={setPopoverOpen}>
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
            {/* z above mobile Sheet (z-[100]) so the account menu isn't trapped under the sheet overlay. */}
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
                          {/* Mobile: SheetClose dismisses the drawer on navigate; desktop rail stays open. */}
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
                {(user?.role === "AGENCY_OWNER" ||
                  user?.role === "AGENCY_ADMIN") && (
                  <SheetClose>
                    <Button
                      className="w-full flex gap-2"
                      onClick={() => {
                        setPopoverOpen(false)
                        setOpen(
                          <CustomModal
                            title='Create Sub Account'
                            subheading='Enter the details below to create a new sub account'
                          >
                            <SubAccountDetails
                              agencyDetails={user?.Agency as Agency}
                              userId={user?.id as string}
                              userName={user?.name}
                            />
                          </CustomModal>
                        )
                      }}
                    >
                      <PlusCircleIcon size={15} />
                      Create Sub Account
                    </Button>
                  </SheetClose>
                )}
              </Command>
            </PopoverContent>
          </Popover>
          <p className="text-muted-foreground text-xs mb-2">MENU LINKS</p>
          <Separator className="mb-4" />
          <nav className="relative">
            <Command className="rounded-lg overflow-visible bg-transparent">
              <CommandInput placeholder="Search..." />
              <CommandList className="p-2 overflow-visible">
                <CommandEmpty>No Results Found</CommandEmpty>
                <CommandGroup className="overflow-visible">
                  {sidebarOptions.map((sidebarOption) => {
                    let val;
                    const result = icons.find(
                      (icon) => icon.value === sidebarOption.icon
                    );
                    if (result) {
                      const IconComponent = result.path;
                      val = <IconComponent />;
                    }
                    return (
                      <CommandItem
                        key={sidebarOption.id}
                        className="md:w-[340px] w-full"
                      >
                        <Link
                          href={sidebarOption.link}
                          className="flex items-center gap-2 hover:bg-transparent rounded-md transition-all md:w-full"
                        >
                          {val}
                          <span>{sidebarOption.name}</span>
                        </Link>
                      </CommandItem>
                    );
                  })}
                </CommandGroup>
              </CommandList>
            </Command>
          </nav>
        </div>

      </SheetContent>
    </Sheet>
  )
}

export default MenuOptions
