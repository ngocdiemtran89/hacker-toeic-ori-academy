import { useMemo } from 'react';
import { Link } from 'react-router-dom';
import { getSrsMap } from '../utils/srs';
import { getAllUnits } from '../data';

interface Props {
  dark: boolean;
  onOpenPomodoro?: () => void;
}

export default function SpacedRepetitionWidget({ dark, onOpenPomodoro }: Props) {
  const units = getAllUnits();
  const allWords = useMemo(() => units.flatMap(u => u.words), [units]);
  const srsMap = useMemo(() => getSrsMap(), []);

  // Compute Box counts
  const boxCounts = useMemo(() => {
    const counts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    allWords.forEach(w => {
      const srs = srsMap[w.id];
      const box = srs ? srs.box : 1;
      counts[box as keyof typeof counts] += 1;
    });
    return counts;
  }, [allWords, srsMap]);

  // Compute due words
  const dueCount = useMemo(() => {
    const now = Date.now();
    return allWords.filter(w => {
      const srs = srsMap[w.id];
      if (!srs) return true; // new words due
      return srs.nextDue <= now;
    }).length;
  }, [allWords, srsMap]);

  return (
    <div className={`rounded-3xl border p-6 space-y-5 transition-all shadow-xl ${
      dark 
        ? 'bg-gradient-to-br from-surface-900 via-surface-850 to-surface-800 border-white/10 shadow-black/40' 
        : 'bg-gradient-to-br from-white via-primary-50/30 to-accent-50/20 border-primary-100 shadow-primary-500/5'
    }`}>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="space-y-1">
          <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${
            dark ? 'bg-accent-500/20 text-accent-400' : 'bg-accent-500/10 text-accent-600'
          }`}>
            🧠 Thuật Toán Spaced Repetition (Hộp Leitner 5 Cấp)
          </span>
          <h3 className="text-xl font-black tracking-tight">Phương Pháp Học Ngắt Quãng Spaced Repetition</h3>
        </div>

        {onOpenPomodoro && (
          <button
            onClick={onOpenPomodoro}
            className="px-4 py-2 rounded-2xl bg-gradient-to-r from-rose-500 to-amber-500 text-white font-extrabold text-xs shadow-md shadow-rose-500/20 hover:scale-105 transition-all self-start sm:self-auto"
          >
            🍅 Mở Chế Độ Pomodoro 25m
          </button>
        )}
      </div>

      {/* 5 Leitner Boxes Cards */}
      <div className="grid grid-cols-5 gap-2 text-center">
        {[
          { box: 1, label: 'Box 1', title: 'Từ Mới / Sai', interval: '1 Ngày', count: boxCounts[1], color: 'from-rose-500 to-red-500' },
          { box: 2, label: 'Box 2', title: 'Nhớ Sơ Sơ', interval: '2 Ngày', count: boxCounts[2], color: 'from-amber-500 to-orange-500' },
          { box: 3, label: 'Box 3', title: 'Khá Thuộc', interval: '4 Ngày', count: boxCounts[3], color: 'from-yellow-500 to-amber-500' },
          { box: 4, label: 'Box 4', title: 'Rất Thuộc', interval: '7 Ngày', count: boxCounts[4], color: 'from-teal-500 to-emerald-500' },
          { box: 5, label: 'Box 5', title: 'Trí Nhớ Dài Hạn', interval: '14 Ngày', count: boxCounts[5], color: 'from-emerald-500 to-green-500' },
        ].map(b => (
          <div key={b.box} className={`p-2.5 sm:p-3 rounded-2xl border flex flex-col justify-between transition-all ${
            dark ? 'bg-surface-900/80 border-white/5' : 'bg-white border-primary-100 shadow-sm'
          }`}>
            <div>
              <span className={`text-[10px] font-black uppercase text-transparent bg-clip-text bg-gradient-to-r ${b.color}`}>
                {b.label}
              </span>
              <p className="text-xs font-bold truncate mt-0.5" title={b.title}>{b.title}</p>
              <p className={`text-[9px] ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>{b.interval}</p>
            </div>
            <p className="text-lg sm:text-2xl font-black font-mono mt-2 text-primary-500">{b.count}</p>
          </div>
        ))}
      </div>

      {/* Due Banner & Actions */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-1 border-t border-dashed border-primary-500/10">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🔥</span>
          <div>
            <p className="text-xs font-bold">
              Hôm nay bạn có <strong className="text-rose-500 text-sm">{dueCount} từ</strong> đến hạn ôn tập ngắt quãng!
            </p>
            <p className={`text-[11px] ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
              Ôn đúng mốc thời gian giúp từ vựng ghi nhớ sâu gấp 10 lần phương pháp học thuộc lòng thông thường.
            </p>
          </div>
        </div>

        <div className="flex gap-2 shrink-0 w-full sm:w-auto">
          <Link
            to="/speed-challenge"
            className="flex-1 sm:flex-initial text-center px-4 py-2.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-extrabold text-xs shadow-md shadow-amber-500/20 hover:scale-105 transition-all"
          >
            ⚡ Game 60s
          </Link>
          <Link
            to="/review-quiz"
            className="flex-1 sm:flex-initial text-center px-5 py-2.5 rounded-2xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-extrabold text-xs shadow-md shadow-primary-500/20 hover:scale-105 transition-all"
          >
            🚀 Ôn Spaced Repetition
          </Link>
        </div>
      </div>
    </div>
  );
}
