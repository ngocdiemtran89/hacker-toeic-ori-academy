import { Link } from 'react-router-dom';
import { getAllUnits } from '../data';
import SpacedRepetitionWidget from '../components/SpacedRepetitionWidget';
import MotivationWelcomeBanner from '../components/MotivationWelcomeBanner';
import { getUserStats } from '../utils/srs';

interface Props {
  dark: boolean;
  onOpenPomodoro?: () => void;
}

export default function DashboardPage({ dark, onOpenPomodoro }: Props) {
  const units = getAllUnits();
  const stats = getUserStats();

  return (
    <div className="pt-6 space-y-8 pb-12">
      {/* Hero Banner */}
      <section className="text-center py-6 space-y-4 animate-fade-in">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold bg-gradient-to-r from-primary-500/10 to-accent-500/10 text-primary-600 dark:text-primary-300 border border-primary-200/30 dark:border-primary-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-accent-500 animate-pulse" />
          ORI ACADEMY - TOEIC - Giao tiếp phản xạ - Phỏng vấn xin việc Hàng Không từ 2013 đến nay
        </div>
        
        <h2 className="text-4xl sm:text-5xl font-black tracking-tight">
          Luyện Từ Vựng & Đọc Hiểu TOEIC
          <br />
          <span className="gradient-text">Part 7 Song Ngữ & Trích Dẫn Dẫn Chứng</span>
        </h2>
        
        <p className={`max-w-xl mx-auto text-sm sm:text-base ${dark ? 'text-surface-200/60' : 'text-surface-800/60'}`}>
          Ứng dụng <strong>Luyện Đọc Part 7 Song Ngữ</strong> + <strong>Lặp lại ngắt quãng (Leitner 5-Box SRS)</strong> + <strong>Pomodoro 25m</strong> giúp học viên chinh phục 700+ TOEIC dễ dàng.
        </p>

        {/* User Level Card */}
        <div className="inline-flex items-center gap-3 px-5 py-2.5 rounded-2xl bg-gradient-to-r from-amber-500/10 via-primary-500/10 to-emerald-500/10 border border-amber-500/20">
          <span className="text-xl">🏆</span>
          <div className="text-left">
            <p className="text-xs font-bold text-amber-500">{stats.levelName}</p>
            <p className={`text-[11px] ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
              Tích lũy <strong>{stats.xp} XP</strong> • Chuỗi học liên tục: <strong className="text-amber-500">🔥 {stats.streak} ngày</strong>
            </p>
          </div>
        </div>
      </section>

      {/* Motivational Welcome & Witty Referral Banner */}
      <section>
        <MotivationWelcomeBanner dark={dark} />
      </section>

      {/* FEATURED: Part 7 Reading Mastery Banner */}
      <section className="animate-fade-in" style={{ animationDelay: '60ms' }}>
        <Link
          to="/part7-reading"
          className={`block rounded-3xl p-6 sm:p-8 border relative overflow-hidden transition-all hover:scale-[1.01] active:scale-[0.99] group shadow-2xl ${
            dark
              ? 'bg-gradient-to-r from-emerald-950/40 via-primary-950/40 to-surface-900 border-emerald-500/30 hover:border-emerald-500/50'
              : 'bg-gradient-to-r from-emerald-500/10 via-teal-500/10 to-white border-emerald-200 shadow-emerald-500/10 hover:border-emerald-300'
          }`}
        >
          <div className="relative flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
            <div className="space-y-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider bg-emerald-500 text-white shadow-sm">
                🔥 Đột phá độc quyền cho học viên
              </span>
              <h3 className="text-2xl font-black tracking-tight">🎯 Luyện Đọc TOEIC Part 7 Song Ngữ & Soi Dẫn Chứng</h3>
              <p className={`text-xs sm:text-sm max-w-2xl leading-relaxed ${dark ? 'text-surface-200/70' : 'text-surface-800/70'}`}>
                Giải mã hoàn toàn Part 7 với <strong>Dịch Song Ngữ Dòng-Theo-Dòng</strong>, <strong>📌 Trích Dẫn Dẫn Chứng Bằng Chứng (Evidence Citations)</strong> trực tiếp trong bài đọc, và <strong>💡 Lời giải chi tiết câu hỏi (A, B, C, D)</strong>!
              </p>
            </div>
            <div className="shrink-0 w-full sm:w-auto">
              <span className="w-full sm:w-auto text-center inline-flex items-center justify-center gap-2 px-6 py-4 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-black text-sm shadow-xl shadow-emerald-500/25 group-hover:scale-105 transition-transform">
                Bắt Đầu Luyện Đọc Part 7 📖
              </span>
            </div>
          </div>
        </Link>
      </section>

      {/* Spaced Repetition (Leitner Box) Widget */}
      <section className="animate-fade-in" style={{ animationDelay: '80ms' }}>
        <SpacedRepetitionWidget dark={dark} onOpenPomodoro={onOpenPomodoro} />
      </section>

      {/* Quick Action Game Modes */}
      <section className="grid grid-cols-1 sm:grid-cols-2 gap-4 animate-fade-in" style={{ animationDelay: '120ms' }}>
        {/* Speed Challenge */}
        <Link
          to="/speed-challenge"
          className={`group p-6 rounded-3xl border relative overflow-hidden transition-all hover:scale-[1.02] active:scale-[0.98] ${
            dark
              ? 'bg-gradient-to-br from-amber-950/30 to-surface-900 border-amber-500/20 hover:border-amber-500/40'
              : 'bg-gradient-to-br from-amber-50/50 to-white border-amber-200 shadow-lg shadow-amber-500/5 hover:border-amber-300'
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <span className="text-2xl">⚡</span>
              <h3 className="text-xl font-black">Thử Thách Thần Tốc 60s</h3>
              <p className={`text-xs leading-relaxed max-w-xs ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                Trắc nghiệm 60 giây đo phản xạ từ vựng TOEIC cấp tốc. Nhân chuỗi điểm Combo x2, x3, x5!
              </p>
            </div>
            <span className="px-4 py-2 rounded-xl bg-amber-500 text-white font-extrabold text-xs shadow-md shadow-amber-500/25 group-hover:scale-105 transition-transform shrink-0">
              Chơi ngay ⚡
            </span>
          </div>
        </Link>

        {/* Review Quiz */}
        <Link
          to="/review-quiz"
          className={`group p-6 rounded-3xl border relative overflow-hidden transition-all hover:scale-[1.02] active:scale-[0.99] ${
            dark
              ? 'bg-gradient-to-br from-primary-950/30 to-surface-900 border-primary-500/20 hover:border-primary-500/40'
              : 'bg-gradient-to-br from-primary-50/50 to-white border-primary-200 shadow-lg shadow-primary-500/5 hover:border-primary-300'
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <span className="text-2xl">🚀</span>
              <h3 className="text-xl font-black">Trắc Nghiệm Ôn Tập (Review Quiz)</h3>
              <p className={`text-xs leading-relaxed max-w-xs ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                Trắc nghiệm 10 từ ngẫu nhiên từ 18 bài. Tự động bắt ôn lại từ sai đến khi thuộc lòng.
              </p>
            </div>
            <span className="px-4 py-2 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-extrabold text-xs shadow-md shadow-primary-500/25 group-hover:scale-105 transition-transform shrink-0">
              Ôn ngay 🚀
            </span>
          </div>
        </Link>
      </section>

      {/* Unit List */}
      <section className="space-y-4 pt-2">
        <div className="flex justify-between items-center">
          <h3 className="text-xl font-black tracking-tight">Danh sách 18 Bài Học TOEIC</h3>
          <span className={`text-xs font-semibold ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
            700+ từ vựng chuẩn thi
          </span>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          {units.map((unit, i) => (
            <Link
              key={unit.id}
              to={`/unit/${unit.id}`}
              className={`group rounded-2xl border p-5 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 animate-slide-up ${
                dark
                  ? 'bg-surface-900/60 border-white/5 hover:border-primary-500/30 shadow-black/20'
                  : 'bg-white/80 border-primary-100/40 hover:border-primary-300/60 shadow-sm'
              }`}
              style={{ animationDelay: `${150 + i * 50}ms` }}
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center shadow-md shadow-primary-500/20 group-hover:shadow-primary-500/40 transition-shadow shrink-0">
                  <span className="text-white text-base font-black">
                    {String(unit.day).padStart(2, '0')}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`text-[10px] font-bold uppercase tracking-wider ${dark ? 'text-primary-300/50' : 'text-primary-500/50'}`}>
                      DAY {String(unit.day).padStart(2, '0')}
                    </span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                      dark ? 'bg-accent-500/15 text-accent-400' : 'bg-accent-500/10 text-accent-600'
                    }`}>
                      {unit.topic}
                    </span>
                  </div>
                  <h4 className="text-base font-bold truncate group-hover:text-primary-500 transition-colors">
                    {unit.title}
                  </h4>
                  <p className={`text-xs mt-1 ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
                    {unit.words.length} từ vựng • Flashcards & Quiz
                  </p>
                </div>
                <svg className={`w-5 h-5 shrink-0 mt-1 transition-transform group-hover:translate-x-1 ${dark ? 'text-surface-200/20' : 'text-surface-800/20'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7"/>
                </svg>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
