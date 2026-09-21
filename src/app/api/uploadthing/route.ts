import { createRouteHandler } from "uploadthing/next";
import { ourFileRouter } from "./core";

// UploadThing hits this for presigned URLs. Don't add extra auth here — core.ts already checks Clerk.
export const { GET, POST } = createRouteHandler({ router: ourFileRouter });