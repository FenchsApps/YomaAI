import { Link } from 'react-router-dom'

export default function MainPage() {
  return (
    <main className="paper-bg relative flex min-h-[calc(100vh-140px)] flex-col items-center justify-center px-6">
      {/* Content */}
      <div className="relative z-10 flex flex-col items-center gap-8 text-center">
        {/* Main heading */}
        <h1
          className="max-w-2xl text-4xl leading-snug text-gray-900 md:text-5xl"
          style={{ fontFamily: "'Chilanka', cursive" }}
        >
          Can't come up with an idea for your work?
        </h1>

        {/* Subtitle */}
        <p
          className="text-xl text-gray-600 md:text-2xl"
          style={{ fontFamily: "'Chilanka', cursive" }}
        >
          YomaAI will help you with that!
        </p>

        {/* CTA Button */}
        <Link to="/create">
          <button
            className="sketchy-btn mt-4 text-lg"
            style={{ fontFamily: "'Chilanka', cursive" }}
          >
            Create Idea with Yoma
          </button>
        </Link>
      </div>
    </main>
  )
}
