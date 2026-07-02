'use client'
import { useClerk } from '@clerk/nextjs'
import { useForm } from 'react-hook-form'
import React, { useEffect, useState } from 'react'
import { Agency } from '@/generated/prisma/client'
import { useRouter } from 'next/navigation'
import { zodResolver } from '@hookform/resolvers/zod'
import { NumberInput } from '@tremor/react'
import { toast } from 'sonner'
import { v4 } from 'uuid'

import * as z from 'zod'
import { Button } from '../ui/button'
import Loading from '../global/loading'
import { Input } from '../ui/input'
import { Switch } from '../ui/switch'
import FileUpload from '../global/file-upload'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '../ui/form'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '../ui/alert-dialog'

import {
  deleteAgency,
  saveActivityLogsNotification,
  updateAgencyDetails,
  initUser,
  upsertAgency,
} from '@/lib/queries'


type Props = {
  data?: Partial<Agency>
}

const E164_PHONE_REGEX = /^\+?[1-9]\d{1,14}$/

const requiredString = (requiredError: string) =>
  z.string({ required_error: requiredError }).trim().min(1, requiredError)

const FormSchema = z.object({
  name: requiredString('Agency name is required.').min(
    2,
    'Agency name must be at least 2 characters long.'
  ),
  companyEmail: requiredString('Company email is required.').email(
    'Invalid email address.'
  ),
  companyPhone: requiredString('Company phone number is required.').regex(
    E164_PHONE_REGEX,
    'Invalid phone number format.'
  ),
  whiteLabel: z.boolean(),
  address: requiredString('Provide an address for your agency.'),
  city: requiredString('Provide a city for your agency.'),
  zipCode: requiredString('Provide a postal or ZIP code for your agency.'),
  state: requiredString('Provide a state for your agency.'),
  country: requiredString('Provide a country for your agency.'),
  agencyLogo: requiredString('An agency logo is required.'),
})

const AgencyDetails = ({ data }: Props) => {
  const router = useRouter()
  const { signOut } = useClerk()
  const [deletingAgency, setDeletingAgency] = useState(false)
  const form = useForm<z.infer<typeof FormSchema>>({
    mode: 'onChange',
    resolver: zodResolver(FormSchema),
    defaultValues: {
      name: data?.name,
      companyEmail: data?.companyEmail,
      companyPhone: data?.companyPhone,
      whiteLabel: data?.whiteLabel || false,
      address: data?.address,
      city: data?.city,
      zipCode: data?.zipCode,
      state: data?.state,
      country: data?.country,
      agencyLogo: data?.agencyLogo,
    },
  })
  const isLoading = form.formState.isSubmitting

  useEffect(() => {
    if (data) {
      // Merge over current values since `data` may be partial;
      // a plain reset(data) would clear other fields and the `whiteLabel` boolean, breaking z.boolean().
      form.reset({ ...form.getValues(), ...data });
      // form.reset(data);
    }
  }, [data]);

  const handleSubmit = async (values: z.infer<typeof FormSchema>) => {
    try {
      let newUserData;
      let custId;
      if (!data?.id) {
        const bodyData = {
          email: values.companyEmail,
          name: values.name,
          shipping: {
            address: {
              city: values.city,
              country: values.country,
              line1: values.address,
              postal_code: values.zipCode,
              state: values.zipCode,
            },
            name: values.name,
          },
          address: {
            city: values.city,
            country: values.country,
            line1: values.address,
            postal_code: values.zipCode,
            state: values.zipCode,
          },
        }
      }
      newUserData = await initUser({ role: 'AGENCY_OWNER' })
      //WIP: custId for stripe customer creation is still in progress
      await upsertAgency({
        id: data?.id ? data.id : v4(),
        // customerId: data?.customerId || custId || "",
        address: values.address,
        agencyLogo: values.agencyLogo,
        city: values.city,
        companyPhone: values.companyPhone,
        country: values.country,
        name: values.name,
        state: values.state,
        whiteLabel: values.whiteLabel,
        zipCode: values.zipCode,
        createdAt: new Date(),
        updatedAt: new Date(),
        companyEmail: values.companyEmail,
        connectAccountId: "",
        goal: 5,
      });

      toast.success("Created Agency");
      //FIX: this is not working, I commented it out previous attempts
      // if (data?.id) return router.refresh();
      // if (response) {
      //   return router.refresh();
      // }
      return router.refresh();

    } catch (error) {
      console.log(error);
      toast.error("Oops!", {
        description: "Could not create your agency",
      });
    }
  }

  const handleDeleteAgency = async () => {
    if (!data?.id) return;
    setDeletingAgency(true);
    //TODO: discontinue the subscription
    try {
      await deleteAgency(data.id);
      toast.success('Agency deleted.');
      await signOut({ redirectUrl: '/agency/sign-in' });
    } catch {
      toast.error('Could not delete agency.');
      setDeletingAgency(false);
    }
  };

  return (
    <AlertDialog>
      <Card className='w-full'>
        <CardHeader>
          <CardTitle>Agency Information</CardTitle>
          <CardDescription>Lets create an agency for your business. You can edit agency settings
            later from the agency settings tab.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(handleSubmit)} className='space-y-4'>
              <fieldset disabled={isLoading} className='space-y-4 border-0 p-0 m-0'>
                <FormField
                  control={form.control}
                  name='agencyLogo'
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Agency Logo</FormLabel>
                      <FormControl>
                        <FileUpload
                          apiEndpoint='agencyLogo'
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
                        <FormLabel>Agency Name</FormLabel>
                        <FormControl>
                          <Input placeholder='Agency name' {...field} />
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
                        <FormLabel>Agency Email</FormLabel>
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
                        <FormLabel>Agency Phone</FormLabel>
                        <FormControl>
                          <Input placeholder='+1 (234) 567-8900' {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <FormField
                  control={form.control}
                  name='whiteLabel'
                  render={({ field }) => {
                    return (
                      <FormItem className='flex flex-row items-center justify-between rounded-lg border gap-4 p-4'>
                        <div>
                          <FormLabel>Whitelabel Agency</FormLabel>
                          <FormDescription>
                            Turning on whitelabel mode will show your agency logo
                            to all sub accounts by default. You can overwrite this
                            functionality through sub account settings.
                          </FormDescription>
                        </div>

                        <FormControl>
                          <Switch
                            checked={field.value}
                            onCheckedChange={field.onChange}
                          />
                        </FormControl>
                      </FormItem>
                    );
                  }}
                />
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
                {data?.id && (
                  <div className='flex flex-col gap-2'>
                    <FormLabel>Create a Goal</FormLabel>
                    <FormDescription>
                      Set a milestone for your agency growth. Track your progress and raise
                      the standard as your business evolves.
                    </FormDescription>
                    <NumberInput
                      defaultValue={data?.goal}
                      onValueChange={async (val: number) => {
                        if (!data?.id) return;
                        await updateAgencyDetails(data.id, { goal: val });
                        await saveActivityLogsNotification({
                          agencyId: data.id,
                          description: `Updated the agency goal to | ${val} Sub Account`,
                          subaccountId: undefined,
                        });
                        router.refresh();
                      }}
                      min={1}
                      className="bg-background !border !border-input rounded-md"
                      placeholder="Sub Account Goal"
                    />
                  </div>
                )}
              </fieldset>

              <Button type="submit" disabled={isLoading}>
                {isLoading ? <Loading /> : "Save Agency Information"}
              </Button>
            </form>
          </Form>
          {data?.id && (
            <div className="flex flex-row items-center justify-center rounded-lg border border-destructive gap-4 p-4 mt-4">
              <div>
                <div>Danger Zone</div>
              </div>
              <div className="text-muted-foreground">
                Deleting your agency cannot be undone. This will also delete all
                sub accounts and all data related to your sub accounts. Sub
                accounts will no longer have access to funnels, contacts etc.
              </div>
              <AlertDialogTrigger
                disabled={isLoading || deletingAgency}
                className="text-red-600 p-2 text-center mt-2 rounded-md hover:bg-red-600 hover:text-white whitespace-nowrap"
              >
                {deletingAgency ? "Deleting..." : "Delete Agency"}
              </AlertDialogTrigger>
            </div>
          )}

          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle className="text-left">
                Are you absolutely sure?
              </AlertDialogTitle>
              <AlertDialogDescription className="text-left">
                This action cannot be undone. This will permanently delete the
                Agency account and all related sub accounts.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter className="flex items-center">
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction
                disabled={deletingAgency}
                className="bg-destructive hover:bg-destructive/80"
                onClick={handleDeleteAgency}
              >
                Delete
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </CardContent>
      </Card>
    </AlertDialog>
  )
}

export default AgencyDetails
