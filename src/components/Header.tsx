import { Link, useLocation } from 'react-router-dom'

export default function Header() {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <header className="relative z-10 border-b-2 border-dashed border-gray-800/30 bg-white/60 backdrop-blur-sm">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        {/* Logo */}
        <Link
          to="/"
          className="flex items-center gap-2 no-underline"
        >
          <span
            className="text-3xl text-gray-900"
            style={{ fontFamily: "'Walter Turncoat', cursive" }}
          >
            YomaAI
          </span>
        </Link>

        {/* Navigation */}
        <nav className="flex items-center gap-3">
          <Link to="/">
            <button className={`nav-btn ${isActive('/') ? 'active' : ''}`}>
              Main
            </button>
          </Link>

          <Link to="/create">
            <button className={`nav-btn ${isActive('/create') ? 'active' : ''}`}>
              Create new Idea
            </button>
          </Link>

          <Link to="/settings">
            <button className={`nav-btn ${isActive('/settings') ? 'active' : ''}`}>
              Settings
            </button>
          </Link>

          <a
            href="https://github.com/FenchsApps/YomaAI"
            target="_blank"
            rel="noopener noreferrer"
          >
            <button className="nav-btn">
              GithubRepo
            </button>
          </a>
        </nav>
      </div>

      {/* Decorative doodle line under header */}
      <svg
        className="absolute bottom-0 left-0 w-full"
        height="4"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M0,2 Q50,0 100,2 T200,2 T300,2 T400,2 T500,2 T600,2 T700,2 T800,2 T900,2 T1000,2 T1100,2 T1200,2 T1300,2 T1400,2 T1500,2 T1600,2 T1700,2 T1800,2 T1900,2 T2000,2"
          fill="none"
          stroke="#1a1a1a"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
      </svg>
    </header>
  )
}
