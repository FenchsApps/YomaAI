import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import TypewriterDialog from '../components/TypewriterDialog'
import { ideaSettings } from '../data/ideaOptions'

type Phase = 'dialog' | 'settings' | 'loading' | 'result'

function getInitialPhase(): Phase {
  const skipDialog = localStorage.getItem('yoma-skip-dialog')
  return skipDialog === 'true' ? 'settings' : 'dialog'
}

export default function CreateIdeaPage() {
  const [phase, setPhase] = useState<Phase>(getInitialPhase)
  const [selections, setSelections] = useState<Record<string, string>>({})
  const [additionalDetails, setAdditionalDetails] = useState('')
  const [result, setResult] = useState('')
  const [error, setError] = useState('')

  const handleDialogComplete = () => {
    setPhase('settings')
  }

  const handleSelectionChange = (id: string, value: string) => {
    setSelections((prev) => ({ ...prev, [id]: value }))
  }

  const buildUserPrompt = (): string => {
    const parts: string[] = []

    for (const setting of ideaSettings) {
      const value = selections[setting.id]
      if (value) {
        parts.push(`${setting.label}: ${value}`)
      }
    }

    const details = additionalDetails.trim()

    if (parts.length === 0 && !details) {
      return 'Generate a completely original creative idea. Surprise me with something unique!'
    }

    let prompt = 'Create an original creative idea based on these preferences:\n\n'

    if (parts.length > 0) {
      prompt += parts.join('\n') + '\n\n'
    }

    if (details) {
      prompt += `Additional Details from the creator:\n${details}\n\n`
    }

    prompt += 'Remember: Be original, avoid clichés. Create something truly unique and surprising!'

    return prompt
  }

  const handleGenerate = async () => {
    setPhase('loading')
    setError('')
    setResult('')

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: buildUserPrompt() }),
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.error || 'Something went wrong')
        setPhase('settings')
        return
      }

      setResult(data.result)
      setPhase('result')
    } catch {
      setError('Failed to connect to the server')
      setPhase('settings')
    }
  }

  const handleStartOver = () => {
    setSelections({})
    setAdditionalDetails('')
    setResult('')
    setError('')
    setPhase('settings')
  }

  const filledCount = Object.values(selections).filter(Boolean).length

  // ── DIALOG PHASE ──
  if (phase === 'dialog') {
    return (
      <main className="paper-bg relative">
        <TypewriterDialog onComplete={handleDialogComplete} />
      </main>
    )
  }

  // ── LOADING PHASE ──
  if (phase === 'loading') {
    return (
      <main className="paper-bg relative flex min-h-[calc(100vh-140px)] flex-col items-center justify-center px-6">
        <div className="relative z-10 flex flex-col items-center gap-6">
          <div className="doodle-star text-5xl">~</div>
          <p
            className="text-2xl text-gray-700"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            Yoma is crafting your idea...
          </p>
          <p
            className="text-gray-400"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            This may take a moment
          </p>
        </div>
      </main>
    )
  }

  // ── RESULT PHASE ──
  if (phase === 'result') {
    return (
      <main className="paper-bg relative min-h-[calc(100vh-140px)] px-6 py-12">
        <div className="relative z-10 mx-auto max-w-3xl">
          <h1
            className="mb-8 text-center text-3xl text-gray-900 md:text-4xl"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            Yoma's Idea
          </h1>

          <div
            className="border-2 border-gray-800 bg-white/90 p-8"
            style={{
              fontFamily: "'Chilanka', cursive",
              borderRadius: '3px 5px 2px 4px',
              fontSize: '1.05rem',
              lineHeight: '1.9',
            }}
          >
            <div className="prose-yoma text-gray-800">
              <ReactMarkdown>{result}</ReactMarkdown>
            </div>
          </div>

          <div className="mt-8 flex justify-center gap-4">
            <button onClick={handleStartOver} className="sketchy-btn">
              Create Another Idea
            </button>
            <button onClick={handleGenerate} className="sketchy-btn">
              Regenerate
            </button>
          </div>
        </div>
      </main>
    )
  }

  // ── SETTINGS PHASE ──
  return (
    <main className="paper-bg relative min-h-[calc(100vh-140px)] px-6 py-12">
      <div className="relative z-10 mx-auto max-w-4xl">
        {/* Title */}
        <h1
          className="mb-2 text-center text-3xl text-gray-900 md:text-4xl"
          style={{ fontFamily: "'Chilanka', cursive" }}
        >
          Craft Your Idea
        </h1>
        <p
          className="mb-10 text-center text-gray-500"
          style={{ fontFamily: "'Chilanka', cursive" }}
        >
          Configure your dream project — the more you fill in, the more tailored the idea!
          <br />
          <span className="text-xs text-gray-400">
            ({filledCount} of {ideaSettings.length} settings configured)
          </span>
        </p>

        {/* Error */}
        {error && (
          <div
            className="mb-6 border-2 border-red-300 bg-red-50/80 p-4 text-center text-red-700"
            style={{
              fontFamily: "'Chilanka', cursive",
              borderRadius: '4px 2px 5px 3px',
            }}
          >
            {error}
          </div>
        )}

        {/* Settings Grid */}
        <div className="mb-12 grid grid-cols-1 gap-5 md:grid-cols-2">
          {ideaSettings.map((setting) => (
            <div key={setting.id} className="flex flex-col gap-1">
              <label
                htmlFor={setting.id}
                className="text-sm text-gray-700"
                style={{ fontFamily: "'Chilanka', cursive" }}
              >
                {setting.label}
              </label>
              <select
                id={setting.id}
                value={selections[setting.id] || ''}
                onChange={(e) => handleSelectionChange(setting.id, e.target.value)}
                className="sketchy-select"
              >
                <option value="">— not selected —</option>
                {setting.options.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>

        {/* Additional Details */}
        <div className="mb-12">
          <label
            htmlFor="additional-details"
            className="mb-2 block text-lg text-gray-900"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            Additional Details
          </label>
          <p
            className="mb-3 text-sm text-gray-400"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            Anything extra you want Yoma to know — fanfiction source, specific characters, universe lore, plot twists, or any other wishes!
          </p>
          <textarea
            id="additional-details"
            value={additionalDetails}
            onChange={(e) => setAdditionalDetails(e.target.value)}
            placeholder="e.g. This is a fanfiction based on Naruto universe. I want the main character to be a rogue ninja from the Hidden Mist Village..."
            className="sketchy-textarea"
            rows={4}
          />
        </div>

        {/* Create Button */}
        <div className="flex justify-center">
          <button onClick={handleGenerate} className="rainbow-btn">
            Create!
          </button>
        </div>
      </div>
    </main>
  )
}
