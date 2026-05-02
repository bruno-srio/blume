'use client'
import React, { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { Agency } from '@/generated/prisma/client'
import { useRouter } from 'next/navigation'
import { AlertDialog } from '../ui/alert-dialog'
import { zodResolver } from '@hookform/resolvers/zod'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Form, FormControl, FormField, FormItem, FormLabel } from '../ui/form'
import { toast } from 'sonner'

import * as z from 'zod'

type Props = {
    data?:Partial<Agency>
}
// try this one out later in production
// const FormSchema = z.object({
//     name: z.string().min(2, 'Agency name must be at least 2 characters long'),
//     companyEmail: z.string().min(1, 'Company email is required').email('Invalid email address'),
//     companyPhone: z.string().min(1, 'Company phone number is required').regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number format'),
//     whiteLabel: z.boolean(),
//     address: z.string().min(1, 'Provide an address for your agency'),
//     city: z.string().min(1, 'Provide a city for your agency'),
//     state: z.string().min(1, 'Provide a state for your agency'),
//     country: z.string().min(1, 'Provide a country for your agency'),
//     agencyLogo: z.string().min(1),
// })

const FormSchema = z.object({
  name: z.string().min(2, { message: "Agency name must be of 2 characters." }),
  companyEmail: z.string().min(1),
  companyPhone: z.string().min(1),
  whiteLabel: z.boolean(),
  address: z.string().min(1),
  city: z.string().min(1),
  zipCode: z.string().min(1),
  state: z.string().min(1),
  country: z.string().min(1),
  agencyLogo: z.string().min(1),
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
    } catch {
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
                                disabled= {isLoading} 
                                control={form.control}
                                name='agencyLogo'
                                render={({field}) => (
                                <FormItem>
                                    <FormLabel>Agency Logo</FormLabel>
                                    <FormControl>
                                        {/* <FileUpload></FileUpload> */}
                                    </FormControl>
                                </FormItem>
                                )}

                            ></FormField>
                        </form>
                    </Form>
                </CardContent>
            </Card>
        </AlertDialog>
    )
}

export default AgencyDetails