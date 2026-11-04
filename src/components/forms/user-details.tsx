

import { SubAccount, User } from '@/generated/prisma'
import React, { useState, useEffect } from 'react'
import { useModal } from '@/providers/modal-provider'
import { toast } from 'sonner'
import { useRouter } from 'next/navigation'
import { getAuthUserDetails, getUserPermissions } from '@/lib/queries'
import { z } from 'zod'
import { 
    UserWithPermissionsAndSubAccounts,
    AuthUserWithAgencySidebarOptionsSubAccounts 
} from '@/lib/types'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'

type Props = {
    id: string | null
    type: 'agency' | 'subAccount'
    userData?: Partial<User>
    subAccounts?: SubAccount[]
}

// userData on the settings page, modal data.user when opened via setOpen.
// FIXME: needs 'use client'.
function UserDetails({ id, type, userData, subAccounts }: Props) {
    const [subAccountPermissions, setSubAccountPermissions] = useState<UserWithPermissionsAndSubAccounts | null>(null)
    const { data, setClose } = useModal()
    const [roleState, setRoleState] = useState('')
    const [loadingPermissions, setLoadingPermissions] = useState(false)
    const [authUserData, setAuthUserData] = useState<AuthUserWithAgencySidebarOptionsSubAccounts | null>(null)
    const router = useRouter()
    

    // Modal only: the logged-in user's details decide what they can grant.
    useEffect(() => {
        if (data.user) {
            const fetchDetails = async () => {
                const response = await getAuthUserDetails()
                if (response) setAuthUserData(response)
            }
            fetchDetails()
        }
    }, [data])

    const userDataSchema = z.object({
        name: z.string().min(1),
        email: z.string().email(),
        avatarUrl: z.string(),
        role: z.enum(['AGENCY_OWNER', 'AGENCY_ADMIN', 'SUBACCOUNT_USER', 'SUBACCOUNT_GUEST']),
    })
    const form = useForm<z.infer<typeof userDataSchema>>({
        resolver: zodResolver(userDataSchema),
        mode: 'onChange',
        defaultValues: {
            name: userData ? userData.name : data?.user?.name,
            email: userData ? userData.email : data?.user?.email,
            avatarUrl: userData ? userData.avatarUrl : data?.user?.avatarUrl,
            role: userData ? userData.role : data?.user?.role,
        },
    })

    useEffect(() => {
        if (!data.user) return
        const getPermissions = async () => {
            if (!data.user) return
            const permission = await getUserPermissions(data.user.id)
            setSubAccountPermissions(permission)
        }
        getPermissions()
    }, [data, form])


    return (
    <div>UserDetails</div>
  )
}

export default UserDetails