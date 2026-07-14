import { Link } from 'react-router-dom';
import { getAllUnits } from '../data';

interface Props {
  dark: boolean;
}

export default function DashboardPage({ dark }: Props) {
  const units = getAllUnits();

  return (
    <div className="pt-8 space-y-8">
      {/* Hero */}
      <section className="text-center py-10 space-y-4 animate-fade-in">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold bg-gradient-to-r from-primary-500/10 to-accent-500/10 text-primary-600 dark:text-primary-300 border border-primary-200/30 dark:border-primary-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-accent-500 animate-pulse" />
          ORI ACADEMY - TOEIC - Giao tiếp phản xạ - Phỏng vấn xin việc Hàng Không từ 2013 đến nay
        </div>
        <h2 className="text-4xl sm:text-5xl font-black tracking-tight">
          Học từ vựng TOEIC
          <br />
          <span className="gradient-text">mỗi ngày 30 phút</span>
        </h2>
        <p className={`max-w-lg mx-auto text-base ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
          40 từ vựng mỗi bài • Flashcard tương tác • Quiz kiểm tra • Phát âm chuẩn
        </p>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 sm:grid-cols-4 gap-3 animate-slide-up" style={{ animationDelay: '100ms' }}>
        {[
          { label: 'Units', value: units.length, icon: '📚' },
          { label: 'Từ vựng', value: units.reduce((s, u) => s + u.words.length, 0), icon: '📝' },
          { label: 'Chủ đề', value: units.length, icon: '🎯' },
          { label: 'Quiz', value: units.reduce((s, u) => s + u.quiz.length, 0), icon: '✅' },
        ].map(stat => (
          <div key={stat.label} className={`rounded-2xl p-4 text-center transition-all hover:scale-[1.02] ${
            dark ? 'bg-surface-900/60 border border-white/5' : 'bg-white/70 border border-primary-100/30 shadow-sm'
          }`}>
            <p className="text-2xl mb-1">{stat.icon}</p>
            <p className="text-2xl font-bold gradient-text">{stat.value}</p>
            <p className={`text-xs font-medium ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>{stat.label}</p>
          </div>
        ))}
      </section>

      {/* Review Quiz CTA */}
      <section className="animate-fade-in" style={{ animationDelay: '150ms' }}>
        <Link
          to="/review-quiz"
          className={`block rounded-3xl p-6 sm:p-8 border relative overflow-hidden transition-all hover:scale-[1.01] active:scale-[0.99] group ${
            dark
              ? 'bg-gradient-to-r from-primary-950/40 via-accent-950/20 to-surface-900/60 border-white/5 hover:border-primary-500/20'
              : 'bg-gradient-to-r from-primary-500/5 via-accent-500/5 to-white border-primary-100/30 hover:border-primary-300/40 shadow-xl shadow-primary-500/5'
          }`}
        >
          {/* Decorative background glow */}
          <div className="absolute -right-24 -top-24 w-48 h-48 rounded-full bg-primary-500/15 blur-3xl group-hover:scale-150 transition-all duration-700" />
          <div className="absolute -left-24 -bottom-24 w-48 h-48 rounded-full bg-accent-500/15 blur-3xl group-hover:scale-150 transition-all duration-700" />

          <div className="relative flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
            <div className="space-y-2">
              <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                dark ? 'bg-primary-500/20 text-primary-300' : 'bg-primary-100 text-primary-700'
              }`}>
                ⚡ Tính năng học thông minh
              </span>
              <h3 className="text-2xl font-black tracking-tight">Trắc Nghiệm Ôn Tập (Review Quiz)</h3>
              <p className={`text-sm max-w-xl leading-relaxed ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                Học qua 10 từ ngẫu nhiên trắc nghiệm từ toàn bộ 18 chủ đề. Hệ thống <strong>Lặp lại từ sai (Spaced Repetition)</strong> sẽ liên tục đưa lại các từ bạn chọn sai cho đến khi thuộc lòng mới thôi!
              </p>
            </div>
            <div className="shrink-0 w-full sm:w-auto">
              <span className="w-full sm:w-auto text-center inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-bold shadow-lg shadow-primary-500/20 group-hover:shadow-primary-500/40 transition-shadow">
                Bắt đầu ôn tập 🚀
              </span>
            </div>
          </div>
        </Link>
      </section>

      {/* Unit list */}
      <section className="space-y-4">
        <h3 className="text-lg font-bold">Danh sách bài học</h3>
        <div className="grid gap-4 sm:grid-cols-2">
          {units.map((unit, i) => (
            <Link
              key={unit.id}
              to={`/unit/${unit.id}`}
              className={`group rounded-2xl border p-6 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 animate-slide-up ${
                dark
                  ? 'bg-surface-900/60 border-white/5 hover:border-primary-500/30 hover:shadow-primary-500/10'
                  : 'bg-white/80 border-primary-100/40 hover:border-primary-300/60 hover:shadow-primary-200/20'
              }`}
              style={{ animationDelay: `${200 + i * 80}ms` }}
            >
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center shadow-lg shadow-primary-500/20 group-hover:shadow-primary-500/40 transition-shadow shrink-0">
                  <span className="text-white text-lg font-black">
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
                  <h4 className="text-lg font-bold truncate group-hover:text-primary-500 transition-colors">
                    {unit.title}
                  </h4>
                  <p className={`text-sm mt-1 ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
                    {unit.words.length} từ vựng • {unit.quiz.length} bài quiz
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
