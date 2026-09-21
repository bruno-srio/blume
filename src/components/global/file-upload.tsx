import React from 'react'
import Image from 'next/image'
import { FileIcon, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { UploadDropzone } from '@/lib/uploadthing'
import { AspectRatio } from '@/components/ui/aspect-ratio'

type Props = {
  apiEndpoint: 'agencyLogo' | 'avatar' | 'subaccountLogo'
  onChange: (url?: string) => void
  value?: string
}

const SIDEBAR_LOGO_HINT = 'Recommended size: 320×100 (16:5). Any size will be scaled to fit.'

const FileUpload = ({ apiEndpoint, onChange, value }: Props) => {
  const type = value?.split('.').pop()
  // Sidebar logos preview in the same 16:5 box the rail uses, so uploads don't look cropped later.
  const isSidebarLogo =
    apiEndpoint === 'agencyLogo' || apiEndpoint === 'subaccountLogo'

  if (value) {
    return (
      <div className='flex flex-col justify-center items-center gap-2 w-full'>
        {type !== 'pdf' ? (
          isSidebarLogo ? (
            <AspectRatio
              ratio={16 / 5}
              className='relative w-full max-w-sm overflow-hidden rounded-md bg-muted/30'
            >
              <Image
                src={value}
                alt='uploaded image'
                className='object-contain'
                fill
                sizes='320px'
              />
            </AspectRatio>
          ) : (
            <div className='relative w-40 h-40 overflow-hidden'>
              <Image
                src={value}
                alt='uploaded image'
                className='object-contain'
                fill
              />
            </div>
          )
        ) : (
          <div className='relative flex items-center p-2 mt-2 rounded-md bg-background/10'>
            <FileIcon />
            <a
              href=''
              target='_blank'
              rel='noopener noreferrer'
              className='ml-2 text-sm text-indigo-500 dark:text-indigo-400 hover:underline'
            >
              View PDF
            </a>
          </div>
        )}
        {isSidebarLogo && (
          <p className='text-xs text-muted-foreground text-center'>
            {SIDEBAR_LOGO_HINT}
          </p>
        )}
        <Button onClick={() => onChange('')} variant='ghost' type='button'>
          <X className='h-4 w-4' />
          Remove Logo
        </Button>
      </div>
    )
  }

  return (
    <div className='w-full bg-muted/30 space-y-2'>
      <UploadDropzone
        endpoint={apiEndpoint}
        onClientUploadComplete={(res) => {
          // Form only stores the URL — UploadThing already hosted the file.
          onChange(res?.[0].url)
        }}
        onUploadError={(error: Error) => {
          console.log(error)
        }}
      />
      {isSidebarLogo && (
        <p className='text-xs text-muted-foreground text-center px-2 pb-2'>
          {SIDEBAR_LOGO_HINT}
        </p>
      )}
    </div>
  )
}

export default FileUpload
