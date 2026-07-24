import { useState, useEffect } from 'react';

interface Props {
  dark: boolean;
}

const MOTIVATIONAL_QUOTES = [
  "💡 Mỗi từ vựng bạn thuộc hôm nay là một bước gần hơn với tấm bằng TOEIC 750+ và ước mơ Hàng Không!",
  "🚀 Học TOEIC không khó, khó nhất là thắng cái nệm ấm! Bạn đã vào web nghĩa là đã thắng 90% đối thủ rồi đấy!",
  "⭐ Sai 1 câu không sao, sai 10 câu cũng không sao! Nhấp 1 cái lật Flashcard là nhớ sâu luôn 10 năm!",
  "🎯 Chỉ cần 25 phút Pomodoro mỗi ngày, mốc 800+ TOEIC cũng phải nghiêng mình bái phục bạn!",
  "✈️ Học hết 18 Unit hôm nay, mai môt đi phỏng vấn Hàng Không trả lời tự tin lướt sóng luôn!"
];

export default function MotivationWelcomeBanner({ dark }: Props) {
  const [quoteIndex, setQuoteIndex] = useState(0);
  const [copied, setCopied] = useState(false);

  // Cycle motivational quotes every 8 seconds
  useEffect(() => {
    const timer = setInterval(() => {
      setQuoteIndex(prev => (prev + 1) % MOTIVATIONAL_QUOTES.length);
    }, 8000);
    return () => clearInterval(timer);
  }, []);

  // Time of day greeting
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return "🌅 Chào buổi sáng Chiến Binh TOEIC ORI!";
    if (hour < 18) return "☀️ Chào buổi chiều bạn học siêu chăm chỉ!";
    return "🌙 Chào buổi tối! Nạp năng lượng TOEIC cùng ORI nhé!";
  };

  const handleCopyReferral = () => {
    try {
      const shareUrl = window.location.origin;
      const text = `Cùng tớ cày TOEIC 750+ với ứng dụng học từ vựng siêu cuốn của ORI ACADEMY nhé: ${shareUrl}`;
      navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 3000);
    } catch (e) {}
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* 1. Warm Greeting & Motivational Quote Box */}
      <div className={`p-6 rounded-3xl border shadow-xl relative overflow-hidden transition-all ${
        dark 
          ? 'bg-gradient-to-r from-primary-950/40 via-surface-900 to-accent-950/30 border-primary-500/20' 
          : 'bg-gradient-to-r from-primary-500/10 via-white to-accent-500/10 border-primary-200/50 shadow-primary-500/5'
      }`}>
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1.5 flex-1">
            <span className="text-xs font-black uppercase tracking-wider text-primary-500 flex items-center gap-1">
              {getGreeting()}
            </span>
            <p className="text-base sm:text-lg font-bold leading-snug animate-fade-in text-gradient bg-gradient-to-r from-primary-500 to-accent-500">
              {MOTIVATIONAL_QUOTES[quoteIndex]}
            </p>
          </div>

          <button
            onClick={() => setQuoteIndex((quoteIndex + 1) % MOTIVATIONAL_QUOTES.length)}
            className={`shrink-0 px-3.5 py-2 rounded-2xl text-xs font-bold transition-all border ${
              dark ? 'bg-surface-800 border-white/10 text-primary-300 hover:bg-surface-700' : 'bg-white border-primary-100 text-primary-600 hover:bg-primary-50 shadow-sm'
            }`}
            title="Đổi câu động lực khác"
          >
            🎲 Đổi câu hay khác
          </button>
        </div>
      </div>

      {/* 2. Gentle & Witty ORI Referral Banner */}
      <div className={`p-5 rounded-3xl border flex flex-col sm:flex-row items-center justify-between gap-4 transition-all ${
        dark
          ? 'bg-surface-900/80 border-amber-500/20 text-surface-200'
          : 'bg-amber-50/60 border-amber-200/70 text-surface-800 shadow-sm'
      }`}>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-amber-500/20 flex items-center justify-center text-xl shrink-0">
            🍧
          </div>
          <div className="space-y-0.5 text-xs sm:text-sm">
            <p className="font-extrabold text-amber-500">
              Rủ bạn thân cùng học tại ORI ACADEMY — Vui x10, đỗ TOEIC cùng nhau! 🤝
            </p>
            <p className={`text-xs ${dark ? 'text-surface-200/60' : 'text-surface-800/60'}`}>
              Học 1 mình dễ nản, có cạ cứng học chung rủ nhau lật Flashcard kéo mốc 800+ siêu nhanh. Nhớ thì thầm vào tai bạn thân: <em>"Vào ORI cày TOEIC với tớ đi!"</em> nhé! 😉
            </p>
          </div>
        </div>

        <button
          onClick={handleCopyReferral}
          className={`shrink-0 px-4 py-2.5 rounded-2xl text-xs font-black transition-all shadow-md flex items-center gap-1.5 ${
            copied
              ? 'bg-emerald-500 text-white shadow-emerald-500/20'
              : 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-amber-500/20 hover:scale-105 active:scale-95'
          }`}
        >
          {copied ? '✅ Đã Coppy Link Mời!' : '🔗 Copy Link Mời Bạn Thân'}
        </button>
      </div>
    </div>
  );
}
