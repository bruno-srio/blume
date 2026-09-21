import React from 'react'

const Page = ({params}: {params: {agencyId: string}}) => {
  // Placeholder until the agency dashboard widgets land.
  return (
    <div>{params.agencyId}</div>
  )
}

export default Page