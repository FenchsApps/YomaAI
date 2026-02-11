import { useState } from 'react'

function getInitialSkipDialog(): boolean {
  return localStorage.getItem('yoma-skip-dialog') === 'true'
}

export default function SettingsPage() {
  const [skipDialog, setSkipDialog] = useState(getInitialSkipDialog)

  const handleToggle = () => {
    const next = !skipDialog
    setSkipDialog(next)
    localStorage.setItem('yoma-skip-dialog', String(next))
  }

  return (
    <main className="paper-bg relative min-h-[calc(100vh-140px)] px-6 py-12">
      <div className="relative z-10 mx-auto max-w-2xl">
        <h1
          className="mb-8 text-center text-3xl text-gray-900 md:text-4xl"
          style={{ fontFamily: "'Chilanka', cursive" }}
        >
          Settings
        </h1>

        <div
          className="border-2 border-gray-800 bg-white/90 p-6"
          style={{ borderRadius: '3px 5px 2px 4px' }}
        >
          {/* Skip Dialog Toggle */}
          <div className="flex items-center justify-between">
            <div>
              <p
                className="text-lg text-gray-900"
                style={{ fontFamily: "'Chilanka', cursive" }}
              >
                Skip Yoma's intro dialog
              </p>
              <p
                className="text-sm text-gray-400"
                style={{ fontFamily: "'Chilanka', cursive" }}
              >
                Go straight to idea settings when creating
              </p>
            </div>

            <button
              onClick={handleToggle}
              className={`relative h-7 w-12 rounded-full border-2 border-gray-800 transition-colors ${
                skipDialog ? 'bg-gray-800' : 'bg-white'
              }`}
            >
              <span
                className={`absolute top-0.5 h-4 w-4 rounded-full border border-gray-800 transition-all ${
                  skipDialog
                    ? 'left-6 bg-white'
                    : 'left-1 bg-gray-800'
                }`}
              />
            </button>
          </div>
        </div>
      </div>
    </main>
  )
}
