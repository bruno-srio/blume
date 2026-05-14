'use client'
import React, { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { Agency } from '@/generated/prisma/client'
import { useRouter } from 'next/navigation'
import { AlertDialog } from '../ui/alert-dialog'
import { zodResolver } from '@hookform/resolvers/zod'
import { NumberInput } from '@tremor/react'
import { toast } from 'sonner'



import * as z from 'zod'
import { Button } from '../ui/button'
import Loading from '../global/loading'
import { Input } from '../ui/input'
import { Switch } from '../ui/switch'
import FileUpload from '../global/file-upload';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '../ui/form'
import { updateAgencyDetails, saveActivityLogsNotification } from '@/lib/queries'

type Props = {
  data?: Partial<Agency>
}

const FormSchema = z.object({
  name: z.string()
    .min(2, {
      message: "Agency name must be at least 2 characters long.",
    }),
  companyEmail: z.string()
    .min(1, { message: "Company email is required." })
    .email({
      message: "Invalid email address."
    }),
  companyPhone: z
    .string()
    .min(1, { message: "Company phone number is required." })
    // Only digits (optional + at the start), 2–15 digits total, and the number can't start with 0.
    .regex(/^\+?[1-9]\d{1,14}$/, {
      message: "Invalid phone number format.",
    }),
  whiteLabel: z.boolean(),
  address: z.string().min(1, { message: "Provide an address for your agency.", }),
  city: z.string().min(1, { message: "Provide a city for your agency." }),
  zipCode: z.string().min(1, { message: "Provide a postal or ZIP code for your agency.", }),
  state: z.string().min(1, { message: "Provide a state for your agency." }),
  country: z.string().min(1, { message: "Provide a country for your agency.", }),
  agencyLogo: z.string().min(1, { message: "An agency logo is required.", }),
});

const AgencyDetails = ({ data }: Props) => {
  const router = useRouter();
  const [deletingAgency, setDeletingAgency] = useState(false);
  const form = useForm<z.infer<typeof FormSchema>>({
    mode: "onChange",
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
  });
  const isLoading = form.formState.isSubmitting;

  useEffect(() => {
    if (data) {
      form.reset(data);
    }
  }, [data]);

  const handleSubmit = async (values: z.infer<typeof FormSchema>) => {
    try {
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
    } 
    catch {
      toast.error('Could not save agency details.')
    }
  }

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
              <FormField
                disabled={isLoading}
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
                  disabled={isLoading}
                  control={form.control}
                  name='name'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>Agency Name</FormLabel>
                      <FormControl>
                        <Input placeholder='Agency name' {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
                <FormField
                  disabled={isLoading}
                  control={form.control}
                  name='companyEmail'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>Agency Email</FormLabel>
                      <FormControl>
                        <Input placeholder='your@email.com' {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
              </div>
              <div className='flex md:flex-row gap-4'>
                <FormField
                  disabled={isLoading}
                  control={form.control}
                  name='companyPhone'
                  render={({ field }) => (
                    <FormItem className='flex-1'>
                      <FormLabel>Agency Phone</FormLabel>
                      <FormControl>
                        <Input placeholder='+1 (234) 567-8900' {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
              </div>
              <FormField
                disabled={isLoading}
                control={form.control}
                name="whiteLabel"
                render={({ field }) => {
                  return (
                    <FormItem className="flex flex-row items-center justify-between rounded-lg border gap-4 p-4">
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
                  disabled={isLoading}
                  control={form.control}
                  name="address"
                  render={({ field }) => (
                    <FormItem className="flex-1">
                      <FormLabel>Address</FormLabel>
                      <FormControl>
                        <Input placeholder='123 Main St' {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
              </div>
              <div className='flex md:flex-row gap-4'>
                <FormField
                  disabled={isLoading}
                  control={form.control}
                  name="city"
                  render={({ field }) => (
                    <FormItem className="flex-1">
                      <FormLabel>City</FormLabel>
                      <FormControl>
                        <Input placeholder='City name' {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
                <FormField
                  disabled={isLoading}
                  control={form.control}
                  name="zipCode"
                  render={({ field }) => (
                    <FormItem className="flex-1">
                      <FormLabel>Zip Code</FormLabel>
                      <FormControl>
                        <Input placeholder='12345' {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
                <FormField
                  disabled={isLoading}
                  control={form.control}
                  name="state"
                  render={({ field }) => (
                    <FormItem className="flex-1">
                      <FormLabel>State</FormLabel>
                      <FormControl>
                        <Input placeholder='State name' {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
              </div>
              <div className='flex md:flex-row gap-4'>
                <FormField
                  disabled={isLoading}
                  control={form.control}
                  name="country"
                  render={({ field }) => (
                    <FormItem className="flex-1">
                      <FormLabel>Country</FormLabel>
                      <FormControl>
                        <Input placeholder='Country name' {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
              </div>
              {data?.id && (
                <div className='flex flex-col gap-2'>
                  <FormLabel>Create a Goal</FormLabel>
                  <FormDescription>
                    ✨ Create a goal for your agency. As your business grows
                    your goals grow too so dont forget to set the bar higher!
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
              <Button type="submit" disabled={isLoading}>
                {isLoading ? <Loading /> : "Save Agency Information"}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </AlertDialog>
  )
}

export default AgencyDetails
