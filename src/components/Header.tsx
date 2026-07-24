import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getUserStats } from '../utils/srs';

interface HeaderProps {
  dark: boolean;
  onToggleDark: () => void;
  onLock?: () => void;
  isAuthenticated?: boolean;
  onOpenPomodoro?: () => void;
}

export default function Header({ dark, onToggleDark, onLock, isAuthenticated, onOpenPomodoro }: HeaderProps) {
  const [stats, setStats] = useState(() => getUserStats());

  useEffect(() => {
    const timer = setInterval(() => {
      setStats(getUserStats());
    }, 2000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className={`sticky top-0 z-50 border-b transition-all duration-300 ${
      dark
        ? 'bg-surface-950/80 border-white/5'
        : 'bg-white/70 border-primary-100/50'
    } backdrop-blur-xl`}>
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center shadow-lg shadow-primary-500/25 group-hover:shadow-primary-500/40 transition-shadow shrink-0">
            <span className="text-white font-bold text-sm">ORI</span>
          </div>
          <div className="min-w-0">
            <h1 className="text-base font-bold tracking-tight leading-none">
              <span className="gradient-text">TOEIC Vocabulary</span>
            </h1>
            <p className={`text-[10px] font-medium tracking-wide truncate ${dark ? 'text-surface-200/50' : 'text-primary-400/70'}`}>
              <span className="md:hidden">ORI ACADEMY - TOEIC (Từ 2013)</span>
              <span className="hidden md:inline">ORI ACADEMY - TOEIC - Giao tiếp phản xạ - Phỏng vấn xin việc Hàng Không từ 2013 đến nay</span>
            </p>
          </div>
        </Link>

        {/* Right Controls */}
        <div className="flex items-center gap-2">
          {/* Gamification Streak & XP Badge */}
          <div className={`hidden sm:flex items-center gap-2 px-3 py-1 rounded-xl text-xs font-bold border ${
            dark ? 'bg-surface-900 border-white/10' : 'bg-white border-primary-100 shadow-sm'
          }`}>
            <span className="text-amber-500 flex items-center gap-1" title="Số ngày học liên tục">
              🔥 {stats.streak} ngày
            </span>
            <span className="opacity-20">|</span>
            <span className="text-emerald-500" title={stats.levelName}>
              ⚡ {stats.xp} XP ({stats.levelName.split(' ')[0]})
            </span>
          </div>

          {/* Pomodoro Button */}
          {onOpenPomodoro && (
            <button
              onClick={onOpenPomodoro}
              className="px-3 py-1.5 rounded-xl bg-gradient-to-r from-rose-500 to-amber-500 text-white text-xs font-bold shadow-md shadow-rose-500/20 hover:scale-105 active:scale-95 transition-all flex items-center gap-1"
              title="Mở Chế độ Học Pomodoro 25 phút"
            >
              🍅 <span className="hidden sm:inline">Pomodoro</span>
            </button>
          )}

          {/* Lock Button */}
          {isAuthenticated && onLock && (
            <button
              onClick={onLock}
              className={`w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-200 hover:scale-105 active:scale-95 ${
                dark
                  ? 'bg-surface-800 text-surface-200 hover:bg-surface-800/80 hover:text-red-400'
                  : 'bg-primary-50 text-primary-600 hover:bg-primary-100 hover:text-red-500'
              }`}
              title="Khóa website"
              aria-label="Lock website"
            >
              <svg className="w-4.5 h-4.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </button>
          )}

          {/* Dark mode toggle */}
          <button
            onClick={onToggleDark}
            className={`w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-200 hover:scale-105 active:scale-95 ${
              dark
                ? 'bg-surface-800 text-yellow-400 hover:bg-surface-800/80'
                : 'bg-primary-50 text-primary-600 hover:bg-primary-100'
            }`}
            aria-label="Toggle dark mode"
          >
            {dark ? (
              <svg className="w-4.5 h-4.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd"/>
              </svg>
            ) : (
              <svg className="w-4.5 h-4.5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
              </svg>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
