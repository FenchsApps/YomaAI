import { useState, useEffect, useCallback, useMemo } from 'react'

interface TypewriterDialogProps {
  onComplete: () => void
}

const DIALOG_LINES = [
  "Hi! I'll save you from the agony, at least partially, hee-hee..",
  "I'll help you create an idea for your masterpiece! Are you ready?",
]

const CHAR_DELAY = 3 // ms per character

export default function TypewriterDialog({ onComplete }: TypewriterDialogProps) {
  const [currentLine, setCurrentLine] = useState(0)
  const [displayedText, setDisplayedText] = useState('')
  const [charIndex, setCharIndex] = useState(0)

  const lineComplete = useMemo(() => {
    if (currentLine >= DIALOG_LINES.length) return true
    return charIndex >= DIALOG_LINES[currentLine].length
  }, [charIndex, currentLine])

  const skipAll = useCallback(() => {
    onComplete()
  }, [onComplete])

  // Typewriter effect
  useEffect(() => {
    if (currentLine >= DIALOG_LINES.length) return

    const line = DIALOG_LINES[currentLine]

    if (charIndex < line.length) {
      const timer = setTimeout(() => {
        setDisplayedText((prev) => prev + line[charIndex])
        setCharIndex((prev) => prev + 1)
      }, CHAR_DELAY)
      return () => clearTimeout(timer)
    }
  }, [charIndex, currentLine])

  const handleNext = () => {
    if (currentLine < DIALOG_LINES.length - 1) {
      setCurrentLine((prev) => prev + 1)
      setDisplayedText('')
      setCharIndex(0)
    } else {
      onComplete()
    }
  }

  return (
    <div className="flex min-h-[calc(100vh-140px)] flex-col items-center justify-center px-6">
      <div className="relative z-10 w-full max-w-2xl">
        {/* Dialog box */}
        <div
          className="border-2 border-gray-800 bg-white/90 p-8"
          style={{ borderRadius: '4px 6px 3px 5px' }}
        >
          {/* Yoma name tag */}
          <div
            className="mb-4 inline-block border-b-2 border-dashed border-gray-400 pb-1 text-lg text-gray-900"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            Yoma:
          </div>

          {/* Typewriter text */}
          <p
            className={`min-h-[3rem] text-xl text-gray-800 ${!lineComplete ? 'typewriter-cursor' : ''}`}
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            {displayedText}
          </p>
        </div>

        {/* Buttons */}
        <div className="mt-6 flex items-center justify-between">
          <button
            onClick={skipAll}
            className="text-sm text-gray-400 underline decoration-dashed underline-offset-2 hover:text-gray-600"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            Skip dialog
          </button>

          {lineComplete && (
            <button
              onClick={handleNext}
              className="sketchy-btn"
            >
              {currentLine < DIALOG_LINES.length - 1 ? 'Next' : "Let's go!"}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
