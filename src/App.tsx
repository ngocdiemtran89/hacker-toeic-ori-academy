import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Header from './components/Header';
import DashboardPage from './pages/DashboardPage';
import UnitDetailPage from './pages/UnitDetailPage';
import FlashcardPage from './pages/FlashcardPage';
import QuizPage from './pages/QuizPage';
import ReviewQuizPage from './pages/ReviewQuizPage';

export default function App() {
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem('ori-dark-mode');
    return saved ? JSON.parse(saved) : false;
  });

  useEffect(() => {
    localStorage.setItem('ori-dark-mode', JSON.stringify(dark));
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  return (
    <BrowserRouter>
      <div className={`min-h-screen transition-colors duration-300 ${
        dark 
          ? 'bg-surface-950 text-surface-100' 
          : 'bg-gradient-to-br from-primary-50 via-white to-accent-400/10 text-surface-900'
      }`}>
        <Header dark={dark} onToggleDark={() => setDark(!dark)} />
        <main className="max-w-6xl mx-auto px-4 sm:px-6 pb-12">
          <Routes>
            <Route path="/" element={<DashboardPage dark={dark} />} />
            <Route path="/unit/:unitId" element={<UnitDetailPage dark={dark} />} />
            <Route path="/unit/:unitId/flashcards" element={<FlashcardPage dark={dark} />} />
            <Route path="/unit/:unitId/quiz" element={<QuizPage dark={dark} />} />
            <Route path="/review-quiz" element={<ReviewQuizPage dark={dark} />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
