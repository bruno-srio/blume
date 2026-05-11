/**
 * UploadThing v7 exposes helpers only from `@uploadthing/react` (no `/hooks` subpath).
 * `generateUpload*` replaces the old `generateComponents` factory; call each once with
 * `OurFileRouter` so presigned URLs and client callbacks stay typed against this file router.
 */
import {
  generateReactHelpers,
  generateUploadButton,
  generateUploadDropzone,
  generateUploader,
} from "@uploadthing/react";

import type { OurFileRouter } from "@/app/api/uploadthing/core";

export const UploadButton = generateUploadButton<OurFileRouter>();
export const UploadDropzone = generateUploadDropzone<OurFileRouter>();
export const Uploader = generateUploader<OurFileRouter>();

export const { useUploadThing, uploadFiles } =
  generateReactHelpers<OurFileRouter>();
