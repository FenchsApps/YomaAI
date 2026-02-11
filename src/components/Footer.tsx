export default function Footer() {
  return (
    <footer className="relative z-10 border-t-2 border-dashed border-gray-800/30 bg-white/60 backdrop-blur-sm">
      <div className="mx-auto max-w-5xl px-6 py-6">
        <div className="flex flex-col items-center gap-3 text-center">
          {/* Decorative pencil doodle */}
          <span className="text-lg opacity-60">〜 ✎ 〜</span>

          <p
            className="text-sm text-gray-700"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            Made with ♥ by{' '}
            <a
              href="https://github.com/FenchsApps"
              target="_blank"
              rel="noopener noreferrer"
              className="font-bold text-gray-900 underline decoration-dashed underline-offset-2 hover:text-gray-600"
            >
              FenchsApps
            </a>
          </p>

          <div
            className="flex items-center gap-4 text-xs text-gray-500"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            <a
              href="https://github.com/FenchsApps/YomaAI"
              target="_blank"
              rel="noopener noreferrer"
              className="underline decoration-dashed underline-offset-2 hover:text-gray-700"
            >
              GitHub Repository
            </a>
            <span>•</span>
            <span>AGPL-3.0 License</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
