"use server";

import { clerkClient, currentUser } from '@clerk/nextjs/server'
import { db } from './db'
import { redirect } from 'next/navigation';
import { User } from '../generated/prisma/client'
import { SubAccount, Notification, Agency } from '../generated/prisma/index';


export const getAuthUserDetails = async () => {
  const user = await currentUser();
  if (!user) {
    // Return null to avoid rendering the component if the user is not authenticated
    return null;
  }

  const userData = await db.user.findUnique({
    where: {
      email: user.emailAddresses[0].emailAddress,
    },
    include: {
      Agency: {
        include: {
          SidebarOption: true,
          SubAccount: {
            include: {
              SidebarOption: true
            },
          },
        },
      },
      Permissions: true,
    },
  })

  return userData
};

const getUser = async (authUser: any, subaccountId?: string) => {
  if (!authUser) {
    return db.user.findFirst({
      where: {
        Agency: {
          SubAccount: { some: { id: subaccountId } },
        },
      },
    });
  }

  return db.user.findUnique({
    where: { email: authUser.emailAddresses[0].emailAddress },
  });
};

export const saveActivityLogsNotification = async ({
  agencyId,
  description,
  subaccountId,
}: {
  agencyId?: string;
  description: string;
  subaccountId?: string;
}) => {
  const authUser = await currentUser();
  let userData;
  // console.log('authUser', authUser);
  
  if (!authUser) {
    const response = await db.user.findFirst({
      where: { Agency: { SubAccount: { some: { id: subaccountId } } } },
    });

    if (response) {
      userData = response;
    }
  } else {
    userData = await db.user.findUnique({
      where: {
        email: authUser?.emailAddresses[0].emailAddress,
      },
    });
  }

  if (!userData) {
    console.log("Could not find a user");
    return;
  }

  let foundAgencyId = agencyId;
  if (!foundAgencyId) {
    if (!subaccountId) {
      throw new Error(
        "You need to provide at least an agency Id or subaccount Id"
      );
    }
    const response = await db.subAccount.findUnique({
      where: { id: subaccountId },
    });

    // At times notifications are assigned to a subaccount, so we need to get the agency id from the subaccount
    if (response) foundAgencyId = response.agencyId;
  }

  if (subaccountId) {
    await db.notification.create({
      data: {
        notification: `${userData.name} | ${description}`,
        User: {
          connect: {
            id: userData.id,
          },
        },
        Agency: {
          connect: {
            id: foundAgencyId,
          },
        },
        SubAccount: {
          connect: {
            id: subaccountId,
          },
        },
      },
    });
  } else {
    await db.notification.create({
      data: {
        notification: `${userData.name} | ${description}`,
        User: {
          connect: {
            id: userData.id,
          },
        },
        Agency: {
          connect: {
            id: foundAgencyId,
          },
        },
      },
    });
  }
};

export const createTeamUser = async (agencyId: string, user: User) => {
  if(user.role === 'AGENCY_OWNER'){
    return null 
  }
  const response = await db.user.create({ data: {...user}})
  return response
};


export const verifyAndAcceptInvitation = async () => {
  const user = await currentUser();
  if (!user) {
    return redirect('/sign-in')
  }

  const invitationExists = await db.invitation.findFirst({
    where: {
      email: user.emailAddresses[0].emailAddress,
      status: 'PENDING'
    },
  })

  if (invitationExists) {
    const userDetails = await createTeamUser(invitationExists.agencyId,{
      email: invitationExists.email,
      agencyId: invitationExists.agencyId,
      avatarUrl: user.imageUrl,
      id: user.id,
      name: '${user.firstName} ${user.lastName}',
      role: invitationExists.role,
      createdAt: new Date(),
      updatedAt: new Date(),
    })

    await saveActivityLogsNotification({
      agencyId: invitationExists?.agencyId,
      description: `Joined the team`,
      subaccountId: undefined,
    })


    if(userDetails){
      (await clerkClient()).users.updateUserMetadata(user.id, {
        privateMetadata: {
        role: userDetails.role || 'SUBACCOUNT_USER',
        },
      })
      
      await db.invitation.delete({
        where: { email: userDetails.email },
      })

      return userDetails.agencyId
    } else return null
  } else {
    const agency = await db.user.findUnique({
      where: { email: user.emailAddresses[0].emailAddress },
    })
    return agency?.agencyId || null
  }
};