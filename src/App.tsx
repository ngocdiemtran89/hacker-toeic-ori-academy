import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Header from './components/Header';
import PasswordGate from './components/PasswordGate';
import DashboardPage from './pages/DashboardPage';
import UnitDetailPage from './pages/UnitDetailPage';
import FlashcardPage from './pages/FlashcardPage';
import QuizPage from './pages/QuizPage';
import ReviewQuizPage from './pages/ReviewQuizPage';
import SpeedChallengePage from './pages/SpeedChallengePage';
import Part7ReadingPage from './pages/Part7ReadingPage';
import PomodoroTimerModal from './components/PomodoroTimerModal';

export default function App() {
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem('ori-dark-mode');
    return saved ? JSON.parse(saved) : false;
  });

  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem('ori-auth') === 'true';
  });

  const [isPomodoroOpen, setIsPomodoroOpen] = useState(false);

  useEffect(() => {
    localStorage.setItem('ori-dark-mode', JSON.stringify(dark));
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  const handleAuthSuccess = () => {
    localStorage.setItem('ori-auth', 'true');
    setIsAuthenticated(true);
  };

  const handleLock = () => {
    localStorage.removeItem('ori-auth');
    setIsAuthenticated(false);
  };

  if (!isAuthenticated) {
    return <PasswordGate dark={dark} onSuccess={handleAuthSuccess} />;
  }

  return (
    <BrowserRouter>
      <div className={`min-h-screen transition-colors duration-300 ${
        dark 
          ? 'bg-surface-950 text-surface-100' 
          : 'bg-gradient-to-br from-primary-50 via-white to-accent-400/10 text-surface-900'
      }`}>
        <Header 
          dark={dark} 
          onToggleDark={() => setDark(!dark)} 
          onLock={handleLock}
          isAuthenticated={isAuthenticated}
          onOpenPomodoro={() => setIsPomodoroOpen(true)}
        />
        <main className="max-w-6xl mx-auto px-4 sm:px-6 pb-12">
          <Routes>
            <Route path="/" element={<DashboardPage dark={dark} onOpenPomodoro={() => setIsPomodoroOpen(true)} />} />
            <Route path="/unit/:unitId" element={<UnitDetailPage dark={dark} />} />
            <Route path="/unit/:unitId/flashcards" element={<FlashcardPage dark={dark} />} />
            <Route path="/unit/:unitId/quiz" element={<QuizPage dark={dark} />} />
            <Route path="/review-quiz" element={<ReviewQuizPage dark={dark} />} />
            <Route path="/speed-challenge" element={<SpeedChallengePage dark={dark} />} />
            <Route path="/part7-reading" element={<Part7ReadingPage dark={dark} />} />
          </Routes>
        </main>

        {/* Global Pomodoro Timer Modal */}
        <PomodoroTimerModal
          isOpen={isPomodoroOpen}
          onClose={() => setIsPomodoroOpen(false)}
          dark={dark}
        />
      </div>
    </BrowserRouter>
  );
}
