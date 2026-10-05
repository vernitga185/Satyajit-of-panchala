'use client'

import { useEffect, useState } from 'react'
import SatyajitPage from './SatyajitPage'

export default function RootPage() {
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
    setIsMounted(true)
  }, [])

  if (!isMounted) {
    return null
  }

  return <SatyajitPage />
}
