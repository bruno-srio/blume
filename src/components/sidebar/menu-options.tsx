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



// defaultOpen = desktop sidebar (always visible). Without it, this is the mobile drawer.
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
  // Wait for the client so the drawer doesn't flash the wrong markup on first load.
  const [isMounted, setIsMounted] = useState(false)
  // Close the account switcher ourselves before opening the create-account modal (otherwise the menu covers it).
  const [popoverOpen, setPopoverOpen] = useState(false)

  // Desktop: force the sidebar open. Mobile: leave it alone so the burger can open/close it.
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
      {/* Hide the burger while a modal is open, otherwise it sits on top of the dialog. */}
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
        // Desktop stays open, so no X. Mobile drawer needs the close button.
        showX={!defaultOpen}
        side='left'
        className={clsx(
          'bg-background/80 backdrop-blur-xl fixed top-0 border-r-[1px] p-6',
          {
            // Two instances render (desktop + mobile); only one is visible at a time.
            'hidden md:inline-block z-0 w-[300px]': defaultOpen,
            'inline-block md:hidden z-[100] w-full': !defaultOpen,
          }
        )}
        >
        <div>
         {/* Keep the logo in a fixed box so a tall upload can't spill into the switcher. */}
         <AspectRatio ratio={16 / 5} className='overflow-hidden'>
          <Image 
            src={sidebarLogo} 
            alt='sidebar logo' 
            fill 
            className='object-contain' 
            sizes='300px'
          />
         </AspectRatio>
          {/* Account switcher: current agency/subaccount; click to pick another. */}
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
            {/* Sit above the mobile drawer so this menu isn't stuck behind it. */}
            <PopoverContent className="w-80 h-80 mt-4 z-[200]">
              <Command className="rounded-lg">
                <CommandInput placeholder="Search Accounts..." />
                <CommandList className="pb-16">
                  <CommandEmpty> No results found</CommandEmpty>
                  {/* Owners/admins also get a shortcut back to the agency. */}
                  {(user?.role === "AGENCY_OWNER" ||
                    user?.role === "AGENCY_ADMIN") &&
                    user?.Agency && (
                      <CommandGroup heading="Agency">
                        <CommandItem className="!bg-transparent my-2 text-primary border-[1px] border-border p-2 rounded-md hover:!bg-muted cursor-pointer transition-all">
                          {/* Mobile: close the drawer on navigate. Desktop sidebar stays put. */}
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
                  {/* Subaccounts this user can jump into. Same close-on-mobile trick as Agency above. */}
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
                {/* Owners/admins: close the switcher, then open the create-subaccount form. */}
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
          {/* Searchable menu: type in the box and the links below filter, same idea as the account switcher. */}
          <nav className="relative">
            <Command className="rounded-lg overflow-visible bg-transparent">
              <CommandInput placeholder="Search..." />
              <CommandList className="py-4 overflow-visible">
                <CommandEmpty>No Results Found</CommandEmpty>
                <CommandGroup className="overflow-visible">
                  {sidebarOptions.map((sidebarOption) => {
                    // Icon name comes from the DB as a string, match it to the actual icon component.
                    let val;
                    const result = icons.find(
                      (icon) => icon.value === sidebarOption.icon
                    );
                    if (result) {
                      const IconComponent = result.path;
                      val = <IconComponent />;
                    }
                    return (
                      // CommandItem is the row (hover/keyboard highlight). Link is what actually goes to the page.
                      // data-selected is how this list marks the highlighted row; hover is the regular mouse style.
                      <CommandItem
                        key={sidebarOption.id}
                        className="w-full cursor-pointer hover:bg-primary hover:text-primary-foreground hover:font-bold data-[selected=true]:bg-primary data-[selected=true]:text-primary-foreground data-[selected=true]:font-bold"
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
