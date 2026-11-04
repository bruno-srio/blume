import { Prisma, Notification, Role } from '@/generated/prisma';
import { 
  getUserPermissions,
  getAuthUserDetails,
} from '@/lib/queries';

export type NotificationWithUser =
  | ({
      User: {
        id: string;
        name: string;
        avatarUrl: string;
        email: string;
        createdAt: Date;
        updatedAt: Date;
        role: Role;
        agencyId: string | null;
      };
    } & Notification)[]
  | undefined;

// Return types of the server actions in queries.ts, so client components can type the data they get back.
// TypeScript reads these off the functions, so if a query starts fetching different fields, these types update on their own.
export type UserWithPermissionsAndSubAccounts = 
  Prisma.PromiseReturnType<typeof getUserPermissions>;

export type AuthUserWithAgencySidebarOptionsSubAccounts =
  Prisma.PromiseReturnType<typeof getAuthUserDetails>;
