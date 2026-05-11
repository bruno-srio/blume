import { createUploadthing, type FileRouter } from "uploadthing/next";
import { auth } from "@clerk/nextjs/server";
import { LOGO_ROUTE_MAX_FILE_SIZE } from "@/lib/uploadthing-limits";

const f = createUploadthing();

const authenticateUser = () => {
  const user = auth();
  // If you throw, the user will not be able to upload
  if (!user) throw new Error("Unauthorized");
  // Whatever is returned here is accessible in onUploadComplete as `metadata`
  return user;
};

// FileRouter for your app, can contain multiple FileRoutes
export const ourFileRouter = {
  // Define as many FileRoutes as you like, each with a unique routeSlug
  subaccountLogo: f({
    image: { maxFileSize: LOGO_ROUTE_MAX_FILE_SIZE, maxFileCount: 1 },
  })
    .middleware(authenticateUser)
    .onUploadComplete(() => {}),
  avatar: f({
    image: { maxFileSize: LOGO_ROUTE_MAX_FILE_SIZE, maxFileCount: 1 },
  })
    .middleware(authenticateUser)
    .onUploadComplete(() => {}),
  agencyLogo: f({
    image: { maxFileSize: LOGO_ROUTE_MAX_FILE_SIZE, maxFileCount: 1 },
  })
    .middleware(authenticateUser)
    .onUploadComplete(() => {}),
  media: f({
    image: { maxFileSize: LOGO_ROUTE_MAX_FILE_SIZE, maxFileCount: 1 },
  })
    .middleware(authenticateUser)
    .onUploadComplete(() => {}),
} satisfies FileRouter;

export type OurFileRouter = typeof ourFileRouter;
