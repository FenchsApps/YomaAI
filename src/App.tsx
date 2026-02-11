import { Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import MainPage from './pages/MainPage'
import CreateIdeaPage from './pages/CreateIdeaPage'
import SettingsPage from './pages/SettingsPage'

export default function App() {
  return (
    <div className="flex min-h-screen flex-col bg-white">
      <Header />
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/create" element={<CreateIdeaPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
      <Footer />
    </div>
  )
}
