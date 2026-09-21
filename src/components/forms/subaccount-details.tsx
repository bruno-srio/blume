'use client'

import { useForm } from 'react-hook-form'
import React, { useEffect } from 'react'
import { Agency, SubAccount } from '@/generated/prisma/client'
import { useRouter } from 'next/navigation'
import { zodResolver } from '@hookform/resolvers/zod'
import { toast } from 'sonner'
import { v4 } from 'uuid'

import * as z from 'zod'
import { Button } from '../ui/button'
import Loading from '../global/loading'
import { Input } from '../ui/input'
import FileUpload from '../global/file-upload'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '../ui/form'
import { saveActivityLogsNotification, upsertSubAccount } from '@/lib/queries'
import { useModal } from '@/providers/modal-provider'

// Create/edit a subaccount. Lives in a modal from the sidebar switcher.
type Props = {
  agencyDetails: Agency
  details?: Partial<SubAccount>
  userId: string
  userName: string
}

const E164_PHONE_REGEX = /^\+?[1-9]\d{1,14}$/

const requiredString = (requiredError: string) =>
  z.string({ required_error: requiredError }).trim().min(1, requiredError)

const FormSchema = z.object({
  name: requiredString('Account name is required.').min(
    2,
    'Account name must be at least 2 characters long.'
  ),
  companyEmail: requiredString('Company email is required.').email(
    'Invalid email address.'
  ),
  companyPhone: requiredString('Company phone number is required.').regex(
    E164_PHONE_REGEX,
    'Invalid phone number format.'
  ),
  address: requiredString('Provide an address for your sub account.'),
  city: requiredString('Provide a city for your sub account.'),
  zipCode: requiredString('Provide a postal or ZIP code for your sub account.'),
  state: requiredString('Provide a state for your sub account.'),
  country: requiredString('Provide a country for your sub account.'),
  subAccountLogo: requiredString('A sub account logo is required.'),
})

// TODO: Give access for Subaccount Guest — they should see a different view, maybe a form that allows them to create tickets.

// TODO: layout.tsx only runs once, so if you remove permissions for someone and they keep navigating, layout.tsx won't fire again. Solution: save the data inside metadata for the current user.

const SubAccountDetails = ({
  details,
  agencyDetails,
  userId,
  userName,
}: Props) => {
  const { setClose } = useModal()
  const router = useRouter()
  const form = useForm<z.infer<typeof FormSchema>>({
    mode: 'onChange',
    resolver: zodResolver(FormSchema),
    defaultValues: {
      name: details?.name,
      companyEmail: details?.companyEmail,
      companyPhone: details?.companyPhone,
      address: details?.address,
      city: details?.city,
      zipCode: details?.zipCode,
      state: details?.state,
      country: details?.country,
      subAccountLogo: details?.subAccountLogo,
    },
  })
  const isLoading = form.formState.isSubmitting

  useEffect(() => {
    if (details) {
      // Merge over current values since `details` may be partial;
      // a plain reset(details) would clear other fields.
      form.reset({ ...form.getValues(), ...details })
    }
  }, [details])

  const handleSubmit = async (values: z.infer<typeof FormSchema>) => {
    try {
      // New subaccount gets a fresh uuid; existing ones keep their id.
      const response = await upsertSubAccount({
        id: details?.id ? details.id : v4(),
        address: values.address,
        subAccountLogo: values.subAccountLogo,
        city: values.city,
        companyPhone: values.companyPhone,
        country: values.country,
        name: values.name,
        state: values.state,
        zipCode: values.zipCode,
        createdAt: new Date(),
        updatedAt: new Date(),
        companyEmail: values.companyEmail,
        agencyId: agencyDetails.id,
        connectAccountId: '',
        goal: 5000,
      })
      if (!response) throw new Error('No response from server')

      await saveActivityLogsNotification({
        agencyId: response.agencyId,
        description: `${userName} | updated sub account | ${response.name}`,
        subaccountId: response.id,
      })

      toast.success('Subaccount details saved', {
        description: 'Successfully saved your subaccount details.',
      })

      // Close the sidebar modal, then refresh so the switcher picks up the new account.
      setClose()
      return router.refresh()
    } catch (error) {
      console.log(error)
      toast.error('Oops!', {
        description: 'Could not save sub account details.',
      })
    }
  }

  return (
    <Card className='w-full'>
      <CardHeader>
        <CardTitle>Sub Account Information</CardTitle>
        <CardDescription>Please enter business details</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className='space-y-4'>
            <fieldset disabled={isLoading} className='space-y-4 border-0 p-0 m-0'>
              <FormField
                control={form.control}
                name='subAccountLogo'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Account Logo</FormLabel>
                    <FormControl>
                      <FileUpload
                        apiEndpoint='subaccountLogo'
                        onChange={field.onChange}
                        value={field.value}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <div className='flex md:flex-row gap-4'>
                <FormField
                  control={form.control}
                  name='name'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>Account Name</FormLabel>
                      <FormControl>
                        <Input placeholder='Your account name' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name='companyEmail'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>Account Email</FormLabel>
                      <FormControl>
                        <Input placeholder='your@email.com' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <div className='flex md:flex-row gap-4'>
                <FormField
                  control={form.control}
                  name='companyPhone'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>Account Phone</FormLabel>
                      <FormControl>
                        <Input placeholder='+1 (234) 567-8900' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <div className='flex md:flex-row gap-4'>
                <FormField
                  control={form.control}
                  name='address'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>Address</FormLabel>
                      <FormControl>
                        <Input placeholder='123 Main St' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <div className='flex md:flex-row gap-4'>
                <FormField
                  control={form.control}
                  name='city'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>City</FormLabel>
                      <FormControl>
                        <Input placeholder='City name' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name='zipCode'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>Zip Code</FormLabel>
                      <FormControl>
                        <Input placeholder='12345' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name='state'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>State</FormLabel>
                      <FormControl>
                        <Input placeholder='State name' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <div className='flex md:flex-row gap-4'>
                <FormField
                  control={form.control}
                  name='country'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>Country</FormLabel>
                      <FormControl>
                        <Input placeholder='Country name' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            </fieldset>

            <Button type='submit' disabled={isLoading}>
              {isLoading ? <Loading /> : 'Save Account Information'}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  )
}

export default SubAccountDetails
