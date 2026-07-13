import { Link } from 'react-router-dom';

interface HeaderProps {
  dark: boolean;
  onToggleDark: () => void;
}

export default function Header({ dark, onToggleDark }: HeaderProps) {
  return (
    <header className={`sticky top-0 z-50 border-b transition-all duration-300 ${
      dark
        ? 'bg-surface-950/80 border-white/5'
        : 'bg-white/70 border-primary-100/50'
    } backdrop-blur-xl`}>
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center shadow-lg shadow-primary-500/25 group-hover:shadow-primary-500/40 transition-shadow">
            <span className="text-white font-bold text-sm">ORI</span>
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight leading-none">
              <span className="gradient-text">TOEIC Vocabulary</span>
            </h1>
            <p className={`text-[10px] font-medium tracking-wide ${dark ? 'text-surface-200/50' : 'text-primary-400/70'}`}>
              ORI ACADEMY • Since 2013
            </p>
          </div>
        </Link>

        <div className="flex items-center gap-2">
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
