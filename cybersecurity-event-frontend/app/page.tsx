'use client'

import { useEffect, useState } from 'react'
import SatyajitPage from './SatyajitPage'
import EleventhDayPage from './EleventhDayPage'

export default function RootPage() {
  const [isEleventhDay, setIsEleventhDay] = useState(false)
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
    // Check if the current environment's API URL points to the Eleventh Day backend
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || ''
    if (apiUrl.includes('eleventh-day')) {
      setIsEleventhDay(true)
    }
    setIsMounted(true)
  }, [])

  if (!isMounted) {
    return null // or a loading spinner
  }

  if (isEleventhDay) {
    return <EleventhDayPage />
  }

  return <SatyajitPage />
}
