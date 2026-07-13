import { useState, FormEvent } from 'react';

interface PasswordGateProps {
  dark: boolean;
  onSuccess: () => void;
}

export default function PasswordGate({ dark, onSuccess }: PasswordGateProps) {
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (password.trim().toLowerCase() === 'oritoeic') {
      setError(false);
      onSuccess();
    } else {
      setError(true);
      setPassword('');
    }
  };

  return (
    <div className={`min-h-screen flex items-center justify-center p-4 transition-colors duration-300 ${
      dark 
        ? 'bg-surface-950 text-surface-100' 
        : 'bg-gradient-to-br from-primary-50 via-white to-accent-400/10 text-surface-900'
    }`}>
      {/* Interactive Background Glows */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl" />
      </div>

      <div className="relative w-full max-w-md">
        {/* Glow behind card */}
        <div className="absolute -inset-0.5 bg-gradient-to-r from-primary-500 to-accent-500 rounded-2xl blur opacity-30 group-hover:opacity-100 transition duration-1000 group-hover:duration-200" />

        <div className={`relative px-8 py-10 rounded-2xl shadow-2xl border backdrop-blur-xl ${
          dark 
            ? 'bg-surface-900/80 border-white/5' 
            : 'bg-white/80 border-primary-100/50'
        }`}>
          {/* Header */}
          <div className="flex flex-col items-center text-center mb-8">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center shadow-lg shadow-primary-500/25 mb-4 relative">
              {/* Pulsing Lock Icon Ring */}
              <div className="absolute inset-0 rounded-2xl bg-primary-500/20 animate-ping pointer-events-none" />
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
            
            <h2 className="text-2xl font-black tracking-tight mb-2">
              <span className="gradient-text">ORI TOEIC ACADEMY</span>
            </h2>
            <p className={`text-xs font-medium tracking-wide ${dark ? 'text-surface-400' : 'text-primary-600/70'}`}>
              Học Từ Vựng TOEIC Hiệu Quả
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="password" className={`block text-xs font-semibold uppercase tracking-wider mb-2 ${
                dark ? 'text-surface-400' : 'text-primary-700'
              }`}>
                Mật khẩu truy cập
              </label>
              
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Nhập mật khẩu học tập..."
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    if (error) setError(false);
                  }}
                  autoFocus
                  className={`w-full h-12 px-4 pr-12 rounded-xl border text-sm transition-all duration-200 ${
                    error
                      ? 'border-red-500 bg-red-500/5 text-red-900 dark:text-red-200 focus:ring-red-500/20'
                      : dark
                        ? 'border-white/10 bg-surface-950 text-white focus:border-primary-500 focus:ring-primary-500/20'
                        : 'border-primary-200 bg-primary-50/30 text-surface-900 focus:border-primary-500 focus:ring-primary-500/20'
                  } focus:outline-none focus:ring-4`}
                />

                {/* Show/Hide Toggle */}
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className={`absolute right-3 top-1/2 -translate-y-1/2 p-1.5 rounded-lg transition-colors ${
                    dark ? 'text-surface-400 hover:text-white' : 'text-primary-400 hover:text-primary-600'
                  }`}
                >
                  {showPassword ? (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.542 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                  )}
                </button>
              </div>

              {/* Error feedback */}
              {error && (
                <p className="mt-2 text-xs font-medium text-red-500 flex items-center gap-1.5 animate-shake">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  Mật khẩu không chính xác. Vui lòng thử lại.
                </p>
              )}
            </div>

            <button
              type="submit"
              className="w-full h-12 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-semibold text-sm shadow-lg shadow-primary-500/25 hover:shadow-primary-500/45 hover:scale-[1.02] active:scale-[0.98] active:brightness-95 transition-all duration-200 flex items-center justify-center gap-2"
            >
              <span>Xác Nhận Truy Cập</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
