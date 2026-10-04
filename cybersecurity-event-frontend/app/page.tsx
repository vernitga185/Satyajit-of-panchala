'use client'

import { useState, useEffect, useRef } from 'react'
import {
  ChevronDown,
  Copy,
  MoreHorizontal,
  Send,
  Shield,
  Sparkles,
  ThumbsDown,
  ThumbsUp,
} from 'lucide-react'

const starterMessages = [
  {
    role: 'assistant',
    content:
      'The eleventh day begins. Drona has taken command, the field has split into formations, and every signal carries intent. Ask me to read the battle record, explain a maneuver, or decode what the opposing lines concealed.',
  },
]

export default function Page() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState(starterMessages)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Initialize session on mount
  useEffect(() => {
    const initSession = async () => {
      try {
        const res = await fetch(`/api/init`, {
          method: 'POST',
          headers: { 'X-Team-Id': 'TEAM_GUEST' }
        })
        if (res.ok) {
          const data = await res.json()
          setSessionId(data.session_id)
        }
      } catch (err) {
        console.error("Failed to init session", err)
      }
    }
    initSession()
  }, [])

  async function submit() {
    const value = input.trim()
    if (!value || isLoading || !sessionId) return
    
    setInput('')
    setMessages((current) => [
      ...current,
      { role: 'user', content: value },
    ])
    setIsLoading(true)

    try {
      const res = await fetch(`/api/chat`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Session-Id': sessionId 
        },
        body: JSON.stringify({ session_id: sessionId, message: value })
      })
      
      if (!res.ok) {
        setMessages((current) => [
          ...current,
          { role: 'assistant', content: `[Error: Server returned ${res.status}]` },
        ])
        setIsLoading(false)
        return
      }

      const data = await res.json()
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: data.response },
      ])
    } catch (err) {
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: `[Connection Error]` },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="flex h-screen bg-[#10100f] text-[#e8e0cf]">
      <section className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-16 items-center justify-between border-b border-[#d8b477]/15 px-4 sm:px-7"><div className="flex items-center gap-3"><div><div className="flex items-center gap-2 text-sm text-[#e6ddcd]"><span>Day XI · The Field of Kurukshetra</span><ChevronDown className="size-3.5 text-[#8c8477]" /></div><p className="mt-0.5 text-[9px] uppercase tracking-[0.2em] text-[#6e685f]">Drona commands · battlefield intelligence</p></div></div><div className="flex items-center gap-3"><span className="hidden text-[10px] uppercase tracking-[0.15em] text-[#777168] sm:block">Field log · XI / 18</span><button aria-label="More options" className="text-[#8d8679]"><MoreHorizontal className="size-5" /></button></div></header>
        <div className="flex flex-1 flex-col overflow-hidden">
          <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col overflow-auto px-4 py-8 sm:px-8 sm:py-12"><div className="mb-10 text-center"><div className="mx-auto mb-4 flex size-11 items-center justify-center rounded-full border border-[#c6944d]/35 bg-[#c6944d]/10 text-[#c6944d]"><Sparkles className="size-5" /></div><p className="mb-2 text-[10px] uppercase tracking-[0.28em] text-[#a87943]">Kurukshetra · Day XI</p><h1 className="font-serif text-2xl text-[#f0e7d6]">The field is listening.</h1><p className="mt-2 text-xs text-[#817a70]">Read the formations, signals, and hidden intelligence of the eleventh day.</p></div>
            <div className="flex flex-col gap-10">
              {messages.map((message, index) => (
                <div key={index} className={lex w-full }>
                  {message.role === 'assistant' ? (
                    <div className="flex max-w-[85%] gap-4">
                      <div className="mt-6 flex size-8 shrink-0 items-center justify-center rounded-full bg-[#1a1510] border border-[#c6944d]/40 shadow-sm text-[#c6944d]">
                        <Shield className="size-4" />
                      </div>
                      <div className="flex flex-col">
                        <span className="mb-1.5 ml-1 text-[10px] font-bold tracking-[0.2em] text-[#c6944d] uppercase">The Archive</span>
                        <div className="rounded-3xl rounded-tl-sm bg-white px-6 py-4 text-[15px] font-medium leading-relaxed text-black shadow-lg border-l-[4px] border-l-[#c6944d]">
                          {message.content}
                        </div>
                        <span className="mt-1.5 ml-1 text-[9px] text-[#6e685f]">Just now</span>
                      </div>
                    </div>
                  ) : (
                    <div className="flex max-w-[85%] gap-4 justify-end">
                      <div className="flex flex-col items-end">
                        <span className="mb-1.5 mr-1 text-[10px] font-bold tracking-[0.2em] text-[#a85b5b] uppercase">Seeker</span>
                        <div className="rounded-3xl rounded-tr-sm bg-white px-6 py-4 text-[15px] font-medium leading-relaxed text-black shadow-lg border-r-[4px] border-r-[#a85b5b]">
                          {message.content}
                        </div>
                        <span className="mt-1.5 mr-1 text-[9px] text-[#6e685f]">Just now</span>
                      </div>
                      <div className="mt-6 flex size-8 shrink-0 items-center justify-center rounded-full bg-[#2a1515] border border-[#a85b5b]/40 shadow-sm text-[#a85b5b]">
                        <div className="size-3.5 rounded-full bg-[#a85b5b]" />
                      </div>
                    </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </div>
          <div className="mx-auto w-full max-w-3xl px-4 pb-5 sm:px-8"><div className="mb-3 flex gap-2 overflow-x-auto pb-1"><Prompt text="Who commands today?" onClick={() => setInput('Who commands today?')} /><Prompt text="Map the formations" onClick={() => setInput('Map the formations')} /><Prompt text="Decode a battle signal" onClick={() => setInput('Decode a battle signal')} /></div><div className="rounded-2xl border border-[#d8b477]/25 bg-[#181815] p-2 shadow-[0_8px_30px_rgba(0,0,0,0.2)] focus-within:border-[#c6944d]/70"><div className="flex items-end gap-2"><textarea aria-label="Query the archive" value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter' && !event.shiftKey && !event.nativeEvent.isComposing && event.keyCode !== 229) { event.preventDefault(); submit() } }} placeholder="Search the archive..." rows={1} className="max-h-32 min-h-10 flex-1 resize-none bg-transparent px-3 py-2.5 text-sm text-[#eee6d6] outline-none placeholder:text-[#6e685f]" /><button aria-label="Submit query" onClick={submit} className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-[#c6944d] text-[#17130d] transition-colors hover:bg-[#e1b66f]"><Send className="size-4" /></button></div></div><p className="mt-2 text-center text-[10px] text-[#5f5a52]">Intelligence is parsed dynamically. Review the underlying source records.</p></div>
        </div>
      </section>
    </main>
  )
}

function Prompt({ text, onClick }: { text: string; onClick: () => void }) { return <button onClick={onClick} className="shrink-0 rounded-full border border-[#d8b477]/15 px-3 py-1.5 text-[10px] text-[#918a7e] transition-colors hover:border-[#c6944d]/50 hover:text-[#d8b477]">{text}</button> }





