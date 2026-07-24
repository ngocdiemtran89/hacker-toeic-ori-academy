import { useState, useEffect } from 'react';
import { playFanfareSound } from '../utils/audio';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  dark: boolean;
}

export default function PomodoroTimerModal({ isOpen, onClose, dark }: Props) {
  const [secondsLeft, setSecondsLeft] = useState(25 * 60);
  const [isActive, setIsActive] = useState(false);
  const [mode, setMode] = useState<'work' | 'break'>('work');
  const [sessionCount, setSessionCount] = useState(0);

  useEffect(() => {
    let interval: any = null;
    if (isActive && secondsLeft > 0) {
      interval = setInterval(() => {
        setSecondsLeft(prev => prev - 1);
      }, 1000);
    } else if (secondsLeft === 0) {
      clearInterval(interval);
      setIsActive(false);
      playFanfareSound();
      if (mode === 'work') {
        setSessionCount(c => c + 1);
        setMode('break');
        setSecondsLeft(5 * 60); // 5 minute break
      } else {
        setMode('work');
        setSecondsLeft(25 * 60); // 25 minute work
      }
    }
    return () => clearInterval(interval);
  }, [isActive, secondsLeft, mode]);

  if (!isOpen) return null;

  const minutes = Math.floor(secondsLeft / 60);
  const secs = secondsLeft % 60;
  const timeFormatted = `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  const totalSeconds = mode === 'work' ? 25 * 60 : 5 * 60;
  const progressPercent = ((totalSeconds - secondsLeft) / totalSeconds) * 100;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className={`relative w-full max-w-md p-8 rounded-3xl border shadow-2xl text-center space-y-6 animate-slide-up ${
        dark ? 'bg-surface-900 border-white/10 text-surface-200' : 'bg-white border-primary-100 text-surface-800'
      }`}>
        {/* Close Button */}
        <button
          onClick={onClose}
          className={`absolute top-4 right-4 p-2 rounded-full transition-all ${
            dark ? 'hover:bg-surface-800 text-surface-200/50' : 'hover:bg-surface-100 text-surface-800/50'
          }`}
        >
          ✕
        </button>

        {/* Title */}
        <div className="space-y-1">
          <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
            mode === 'work' ? 'bg-primary-500/15 text-primary-500' : 'bg-emerald-500/15 text-emerald-500'
          }`}>
            {mode === 'work' ? '🍅 Phiên Học Tập Trung (25 Phút)' : '☕ Thời Gian Nghỉ Ngơi (5 Phút)'}
          </span>
          <h3 className="text-xl font-black pt-1">
            {mode === 'work' ? 'Phương Pháp Pomodoro TOEIC' : 'Thư giãn trí não!'}
          </h3>
        </div>

        {/* Circular Ring Timer Display */}
        <div className="relative w-48 h-48 mx-auto flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="44"
              className={`stroke-current ${dark ? 'text-surface-800' : 'text-primary-100'}`}
              strokeWidth="8"
              fill="transparent"
            />
            <circle
              cx="50"
              cy="50"
              r="44"
              className={`stroke-current transition-all duration-1000 ${
                mode === 'work' ? 'text-primary-500' : 'text-emerald-500'
              }`}
              strokeWidth="8"
              strokeDasharray="276.46"
              strokeDashoffset={276.46 - (276.46 * progressPercent) / 100}
              strokeLinecap="round"
              fill="transparent"
            />
          </svg>

          <div className="absolute flex flex-col items-center">
            <span className="text-4xl font-black tracking-tight font-mono">
              {timeFormatted}
            </span>
            <span className={`text-[11px] font-medium mt-1 ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
              {isActive ? 'Đang chạy ⏳' : 'Tạm dừng ⏸️'}
            </span>
          </div>
        </div>

        {/* Completed Sessions Stats */}
        <div className={`p-3 rounded-2xl text-xs font-semibold flex justify-center items-center gap-2 ${
          dark ? 'bg-surface-850 border border-white/5' : 'bg-primary-50 border border-primary-100'
        }`}>
          <span>🔥 Bạn đã hoàn thành:</span>
          <strong className="text-primary-500 text-sm font-black">{sessionCount} phiên Pomodoro</strong>
        </div>

        {/* Timer Actions */}
        <div className="flex justify-center gap-3">
          <button
            onClick={() => setIsActive(!isActive)}
            className={`px-6 py-3 rounded-2xl text-sm font-black text-white shadow-lg transition-all hover:scale-105 active:scale-95 ${
              isActive
                ? 'bg-amber-500 shadow-amber-500/30'
                : 'bg-gradient-to-r from-primary-500 to-accent-500 shadow-primary-500/30'
            }`}
          >
            {isActive ? '⏸️ Tạm Dừng' : '▶️ Bắt Đầu Học'}
          </button>
          
          <button
            onClick={() => {
              setIsActive(false);
              setSecondsLeft(mode === 'work' ? 25 * 60 : 5 * 60);
            }}
            className={`px-4 py-3 rounded-2xl text-sm font-bold border transition-all ${
              dark ? 'bg-surface-800 border-white/10 text-surface-200/60 hover:bg-surface-700' : 'bg-surface-100 border-surface-200 text-surface-800/60 hover:bg-surface-200'
            }`}
          >
            🔄 Đặt Lại
          </button>
        </div>

        <p className={`text-[11px] leading-relaxed ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
          💡 <strong>Quy tắc Pomodoro 20 năm TOEIC</strong>: Học ngắt quãng 25 phút giúp trí não tiếp thu từ vựng ở trạng thái đỉnh cao mà không bị quá tải.
        </p>
      </div>
    </div>
  );
}
