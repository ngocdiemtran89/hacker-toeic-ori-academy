import { useParams, Link } from 'react-router-dom';
import { useState, useCallback } from 'react';
import { getUnit } from '../data';

interface Props {
  dark: boolean;
}

function speak(text: string) {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'en-US';
    utter.rate = 0.85;
    window.speechSynthesis.speak(utter);
  }
}

export default function FlashcardPage({ dark }: Props) {
  const { unitId } = useParams<{ unitId: string }>();
  const unit = getUnit(unitId || '');
  const [current, setCurrent] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [known, setKnown] = useState<Set<string>>(new Set());

  const words = unit?.words || [];
  const word = words[current];

  const flip = useCallback(() => setFlipped(f => !f), []);

  const next = useCallback((isKnown: boolean) => {
    if (word && isKnown) {
      setKnown(prev => new Set(prev).add(word.id));
    }
    setFlipped(false);
    setTimeout(() => {
      setCurrent(c => Math.min(c + 1, words.length - 1));
    }, 150);
  }, [word, words.length]);

  const prev = useCallback(() => {
    setFlipped(false);
    setTimeout(() => {
      setCurrent(c => Math.max(c - 1, 0));
    }, 150);
  }, []);

  const restart = useCallback(() => {
    setFlipped(false);
    setCurrent(0);
    setKnown(new Set());
  }, []);

  if (!unit || !word) {
    return (
      <div className="pt-20 text-center">
        <p className="text-xl font-bold">Không tìm thấy bài học</p>
        <Link to="/" className="text-primary-500 underline mt-2 inline-block">← Về trang chủ</Link>
      </div>
    );
  }

  const progress = ((current + 1) / words.length) * 100;
  const isDone = current === words.length - 1 && flipped;

  return (
    <div className="pt-6 max-w-lg mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between animate-fade-in">
        <Link to={`/unit/${unit.id}`} className={`text-xs font-medium hover:underline ${dark ? 'text-primary-300/50' : 'text-primary-500/50'}`}>
          ← {unit.title}
        </Link>
        <span className={`text-xs font-bold ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
          {current + 1} / {words.length}
        </span>
      </div>

      {/* Progress bar */}
      <div className={`h-1.5 rounded-full overflow-hidden ${dark ? 'bg-surface-800' : 'bg-primary-100/60'}`}>
        <div
          className="h-full rounded-full bg-gradient-to-r from-primary-500 to-accent-500 transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Stats */}
      <div className="flex justify-center gap-6 text-xs font-semibold">
        <span className="flex items-center gap-1.5 text-success">
          <span className="w-2 h-2 rounded-full bg-success" />
          Đã thuộc: {known.size}
        </span>
        <span className={`flex items-center gap-1.5 ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
          <span className={`w-2 h-2 rounded-full ${dark ? 'bg-surface-800' : 'bg-surface-200'}`} />
          Còn lại: {words.length - known.size}
        </span>
      </div>

      {/* Flashcard */}
      <div className="perspective-1000">
        <div
          onClick={flip}
          className={`relative w-full aspect-[3/4] sm:aspect-[4/3] cursor-pointer preserve-3d transition-transform duration-500 ${flipped ? 'rotate-y-180' : ''}`}
        >
          {/* Front */}
          <div className={`absolute inset-0 backface-hidden rounded-3xl p-8 flex flex-col items-center justify-center text-center border shadow-2xl ${
            dark
              ? 'bg-gradient-to-br from-surface-900 to-surface-800 border-white/5 shadow-black/30'
              : 'bg-gradient-to-br from-white to-primary-50/50 border-primary-100/30 shadow-primary-200/20'
          }`}>
            <span className={`text-xs font-bold uppercase tracking-wider mb-4 ${dark ? 'text-primary-300/40' : 'text-primary-500/40'}`}>
              {word.partOfSpeech} • [{word.pronunciation.us}]
            </span>
            <h3 className="text-4xl sm:text-5xl font-black tracking-tight mb-4">{word.word}</h3>
            <button
              onClick={(e) => { e.stopPropagation(); speak(word.word); }}
              className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all hover:scale-110 active:scale-95 ${
                dark ? 'bg-primary-500/15 text-primary-300' : 'bg-primary-100 text-primary-500'
              }`}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.536 8.464a5 5 0 010 7.072M17.95 6.05a8 8 0 010 11.9M6.5 8.788V15.212a1 1 0 001.052.986l5.318-.531A1 1 0 0013.5 14.7V9.3a1 1 0 00-.63-.966l-5.318-.531A1 1 0 006.5 8.788z"/>
              </svg>
            </button>
            <p className={`absolute bottom-6 text-xs ${dark ? 'text-surface-200/20' : 'text-surface-800/20'}`}>
              Nhấn để lật thẻ
            </p>
          </div>

          {/* Back */}
          <div className={`absolute inset-0 backface-hidden rotate-y-180 rounded-3xl p-8 flex flex-col items-center justify-center text-center border shadow-2xl ${
            dark
              ? 'bg-gradient-to-br from-primary-900/40 to-surface-900 border-primary-500/20 shadow-black/30'
              : 'bg-gradient-to-br from-primary-50 to-white border-primary-200/40 shadow-primary-200/20'
          }`}>
            <span className={`text-xs font-bold uppercase tracking-wider mb-3 ${dark ? 'text-primary-300/40' : 'text-primary-500/40'}`}>
              Nghĩa tiếng Việt
            </span>
            <h3 className={`text-2xl sm:text-3xl font-black mb-4 ${dark ? 'text-accent-400' : 'text-primary-600'}`}>
              {word.meaningVi}
            </h3>
            <div className={`rounded-xl p-4 text-sm max-w-sm ${dark ? 'bg-surface-800/60' : 'bg-white/80 border border-primary-100/20'}`}>
              <p className="font-medium leading-relaxed"
                 dangerouslySetInnerHTML={{
                   __html: word.exampleEn.replace(
                     new RegExp(`\\b${word.word}\\w*\\b`, 'gi'),
                     '<strong class="text-primary-500">$&</strong>'
                   )
                 }}
              />
              <p className={`mt-2 text-xs ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
                {word.exampleVi}
              </p>
            </div>
            {word.synonyms.length > 0 && (
              <p className={`mt-3 text-xs ${dark ? 'text-surface-200/30' : 'text-surface-800/30'}`}>
                Đồng nghĩa: <strong>{word.synonyms.join(', ')}</strong>
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-center gap-3">
        <button
          onClick={prev}
          disabled={current === 0}
          className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all disabled:opacity-20 ${
            dark ? 'bg-surface-800 text-surface-200/60 hover:bg-surface-800/80' : 'bg-white border border-primary-100/30 text-surface-800/50 hover:bg-primary-50'
          }`}
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>

        <button
          onClick={() => next(false)}
          disabled={current === words.length - 1}
          className={`px-6 py-3 rounded-2xl text-sm font-semibold transition-all disabled:opacity-20 ${
            dark
              ? 'bg-danger/15 text-danger border border-danger/20 hover:bg-danger/25'
              : 'bg-red-50 text-red-500 border border-red-200/30 hover:bg-red-100/80'
          }`}
        >
          Chưa thuộc 😕
        </button>
        <button
          onClick={() => next(true)}
          disabled={current === words.length - 1}
          className="px-6 py-3 rounded-2xl text-sm font-semibold bg-gradient-to-r from-success to-accent-500 text-white shadow-lg shadow-success/25 hover:shadow-success/40 transition-all disabled:opacity-20"
        >
          Đã thuộc 🎉
        </button>

        <button
          onClick={() => next(false)}
          disabled={current === words.length - 1}
          className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all disabled:opacity-20 ${
            dark ? 'bg-surface-800 text-surface-200/60 hover:bg-surface-800/80' : 'bg-white border border-primary-100/30 text-surface-800/50 hover:bg-primary-50'
          }`}
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
      </div>

      {/* Done state */}
      {isDone && (
        <div className={`text-center rounded-2xl p-8 animate-slide-up ${
          dark ? 'bg-surface-900/60 border border-white/5' : 'bg-white/80 border border-primary-100/30'
        }`}>
          <p className="text-4xl mb-3">🎊</p>
          <h3 className="text-xl font-bold mb-1">Hoàn thành!</h3>
          <p className={`text-sm mb-4 ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
            Bạn đã thuộc {known.size}/{words.length} từ vựng
          </p>
          <div className="flex gap-3 justify-center">
            <button
              onClick={restart}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary-500 to-primary-600 text-white text-sm font-semibold shadow-lg shadow-primary-500/25 hover:scale-[1.02] active:scale-[0.98] transition-all"
            >
              Học lại
            </button>
            <Link
              to={`/unit/${unit.id}/quiz`}
              className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all hover:scale-[1.02] ${
                dark ? 'bg-accent-500/15 text-accent-400 border border-accent-500/20' : 'bg-accent-500/10 text-accent-600 border border-accent-500/20'
              }`}
            >
              Làm Quiz →
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
