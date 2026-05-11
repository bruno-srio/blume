'use client'
import React, { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { Agency } from '@/generated/prisma/client'
import { useRouter } from 'next/navigation'
import { AlertDialog } from '../ui/alert-dialog'
import { zodResolver } from '@hookform/resolvers/zod'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '../ui/form'
import FileUpload from '../global/file-upload';
import { toast } from 'sonner'


import * as z from 'zod'

type Props = {
  data?: Partial<Agency>
}

const FormSchema = z.object({
  name: z.string()
    .min(2, { message: "Agency name must be at least 2 characters long.",
    }),
  companyEmail: z.string()
    .min(1, { message: "Company email is required." })
    .email({ message: "Invalid email address." 
    }),
  companyPhone: z
    .string()
    .min(1, { message: "Company phone number is required." })
    // Only digits (optional + at the start), 2–15 digits total, and the number can't start with 0.
    .regex(/^\+?[1-9]\d{1,14}$/, { message: "Invalid phone number format.",
    }),
  whiteLabel: z.boolean(),
  address: z.string().min(1, { message: "Provide an address for your agency.",}),
  city: z.string().min(1, { message: "Provide a city for your agency." }),
  zipCode: z.string().min(1, { message: "Provide a postal or ZIP code for your agency.",}),
  state: z.string().min(1, { message: "Provide a state for your agency." }),
  country: z.string().min(1, { message: "Provide a country for your agency.",}),
  agencyLogo: z.string().min(1, { message: "An agency logo is required.",}),
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
                                          <FileUpload
                                              apiEndpoint='agencyLogo'
                                              onChange={field.onChange}
                                              value={field.value}
                                          />
                                      </FormControl>
                                      <FormMessage />
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