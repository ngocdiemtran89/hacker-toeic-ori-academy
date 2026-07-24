import { useParams, Link } from 'react-router-dom';
import { useState, useCallback, useEffect } from 'react';
import { getUnit } from '../data';
import type { VocabWord } from '../types';

interface Props {
  dark: boolean;
}

function speakText(text: string) {
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

  const [words, setWords] = useState<VocabWord[]>([]);
  const [current, setCurrent] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [known, setKnown] = useState<Set<string>>(new Set());
  const [autoPlay, setAutoPlay] = useState(true);
  const [startWithVietnamese, setStartWithVietnamese] = useState(false);
  const [isShuffled, setIsShuffled] = useState(false);

  // Initialize words
  useEffect(() => {
    if (unit?.words) {
      setWords([...unit.words]);
    }
  }, [unit]);

  const word = words[current];

  // Auto speak on word change
  useEffect(() => {
    if (autoPlay && word && !flipped) {
      speakText(word.word);
    }
  }, [current, autoPlay, word]);

  const flip = useCallback(() => setFlipped(f => !f), []);

  const handleNext = useCallback((isKnown?: boolean) => {
    if (word && isKnown !== undefined) {
      setKnown(prev => {
        const nextSet = new Set(prev);
        if (isKnown) {
          nextSet.add(word.id);
        } else {
          nextSet.delete(word.id);
        }
        return nextSet;
      });
    }
    setFlipped(false);
    setTimeout(() => {
      setCurrent(c => Math.min(c + 1, words.length - 1));
    }, 120);
  }, [word, words.length]);

  const handlePrev = useCallback(() => {
    setFlipped(false);
    setTimeout(() => {
      setCurrent(c => Math.max(c - 1, 0));
    }, 120);
  }, []);

  const shuffleWords = useCallback(() => {
    if (!unit?.words) return;
    setFlipped(false);
    setCurrent(0);
    if (!isShuffled) {
      const shuffled = [...unit.words].sort(() => Math.random() - 0.5);
      setWords(shuffled);
      setIsShuffled(true);
    } else {
      setWords([...unit.words]);
      setIsShuffled(false);
    }
  }, [unit, isShuffled]);

  const restart = useCallback(() => {
    setFlipped(false);
    setCurrent(0);
    setKnown(new Set());
  }, []);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === ' ' || e.key === 'Enter' || e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        e.preventDefault();
        flip();
      } else if (e.key === 'ArrowLeft') {
        handlePrev();
      } else if (e.key === 'ArrowRight') {
        handleNext();
      } else if (e.key === '1') {
        handleNext(false);
      } else if (e.key === '2') {
        handleNext(true);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [flip, handleNext, handlePrev]);

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

  // Determine front and back content based on startWithVietnamese preference
  const isFrontVietnamese = startWithVietnamese ? !flipped : flipped;

  return (
    <div className="pt-4 max-w-xl mx-auto space-y-5 pb-12 animate-fade-in">
      {/* Top Header */}
      <div className="flex items-center justify-between">
        <Link 
          to={`/unit/${unit.id}`} 
          className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
            dark ? 'bg-surface-900 border-white/10 text-primary-300 hover:bg-surface-800' : 'bg-white border-primary-100/50 text-primary-600 hover:bg-primary-50'
          }`}
        >
          ← {unit.title}
        </Link>
        <div className="flex items-center gap-2">
          {/* Auto sound toggle */}
          <button
            onClick={() => setAutoPlay(!autoPlay)}
            title={autoPlay ? 'Tự động phát âm: Bật' : 'Tự động phát âm: Tắt'}
            className={`p-2 rounded-xl border text-xs font-medium transition-all ${
              autoPlay 
                ? 'bg-primary-500/10 border-primary-500/30 text-primary-500' 
                : dark ? 'bg-surface-900 border-white/10 text-surface-200/40' : 'bg-white border-surface-200 text-surface-800/40'
            }`}
          >
            {autoPlay ? '🔊 Đọc tự động' : '🔇 Tắt âm'}
          </button>
          
          {/* Shuffle button */}
          <button
            onClick={shuffleWords}
            title="Trộn từ vựng"
            className={`p-2 rounded-xl border text-xs font-medium transition-all ${
              isShuffled 
                ? 'bg-accent-500/10 border-accent-500/30 text-accent-500' 
                : dark ? 'bg-surface-900 border-white/10 text-surface-200/40' : 'bg-white border-surface-200 text-surface-800/40'
            }`}
          >
            🔀 Trộn từ
          </button>

          {/* Flip Mode button */}
          <button
            onClick={() => setStartWithVietnamese(!startWithVietnamese)}
            title="Đổi mặt thẻ khởi đầu"
            className={`p-2 rounded-xl border text-xs font-medium transition-all ${
              startWithVietnamese 
                ? 'bg-purple-500/10 border-purple-500/30 text-purple-400' 
                : dark ? 'bg-surface-900 border-white/10 text-surface-200/40' : 'bg-white border-surface-200 text-surface-800/40'
            }`}
          >
            {startWithVietnamese ? '🇻🇳 Mặt trước: Tiếng Việt' : '🇬🇧 Mặt trước: Tiếng Anh'}
          </button>
        </div>
      </div>

      {/* Progress Bar & Counter */}
      <div className="space-y-1.5">
        <div className="flex justify-between items-center text-xs font-bold px-1">
          <span className={dark ? 'text-surface-200/60' : 'text-surface-800/60'}>
            Tiến độ thẻ: {current + 1} / {words.length} ({Math.round(progress)}%)
          </span>
          <div className="flex gap-4">
            <span className="text-success flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-success"></span>
              Đã thuộc: {known.size}
            </span>
            <span className={dark ? 'text-surface-200/40' : 'text-surface-800/40'}>
              Chưa thuộc: {words.length - known.size}
            </span>
          </div>
        </div>
        <div className={`h-2 rounded-full overflow-hidden ${dark ? 'bg-surface-800' : 'bg-primary-100/60'}`}>
          <div
            className="h-full rounded-full bg-gradient-to-r from-primary-500 via-accent-500 to-emerald-400 transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* 3D Flashcard Canvas */}
      <div className="perspective-1000">
        <div
          onClick={flip}
          className={`relative w-full aspect-[4/3] sm:aspect-[16/11] cursor-pointer preserve-3d transition-transform duration-500 ${flipped ? 'rotate-y-180' : ''}`}
        >
          {/* FRONT SIDE */}
          <div className={`absolute inset-0 backface-hidden rounded-3xl p-6 sm:p-8 flex flex-col justify-between border shadow-2xl transition-all ${
            dark
              ? 'bg-gradient-to-br from-surface-900 via-surface-850 to-surface-800 border-white/10 shadow-black/50'
              : 'bg-gradient-to-br from-white via-primary-50/30 to-primary-100/20 border-primary-100 shadow-primary-500/10'
          }`}>
            {/* Top Row: Part of speech & IPA */}
            <div className="flex justify-between items-center">
              <span className={`px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider ${
                word.partOfSpeech.includes('n') ? 'bg-blue-500/15 text-blue-500 border border-blue-500/20' :
                word.partOfSpeech.includes('v') ? 'bg-emerald-500/15 text-emerald-500 border border-emerald-500/20' :
                word.partOfSpeech.includes('adj') ? 'bg-amber-500/15 text-amber-500 border border-amber-500/20' :
                'bg-purple-500/15 text-purple-400 border border-purple-500/20'
              }`}>
                {word.partOfSpeech}
              </span>
              {word.pronunciation && (
                <span className={`text-xs font-medium tracking-wide ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                  {word.pronunciation.us || word.pronunciation.uk}
                </span>
              )}
            </div>

            {/* Center: Main Word & Pronounce Speaker */}
            {!isFrontVietnamese ? (
              <div className="text-center space-y-4 my-auto">
                <h3 className="text-4xl sm:text-5xl font-black tracking-tight text-gradient bg-gradient-to-r from-primary-500 to-accent-500">
                  {word.word}
                </h3>
                <div className="flex justify-center gap-2">
                  <button
                    onClick={(e) => { e.stopPropagation(); speakText(word.word); }}
                    className={`px-4 py-2 rounded-2xl flex items-center gap-2 text-xs font-bold transition-all hover:scale-105 active:scale-95 ${
                      dark ? 'bg-primary-500/20 text-primary-300 hover:bg-primary-500/30' : 'bg-primary-100 text-primary-600 hover:bg-primary-200'
                    }`}
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15.536 8.464a5 5 0 010 7.072M17.95 6.05a8 8 0 010 11.9M6.5 8.788V15.212a1 1 0 001.052.986l5.318-.531A1 1 0 0013.5 14.7V9.3a1 1 0 00-.63-.966l-5.318-.531A1 1 0 006.5 8.788z"/>
                    </svg>
                    Phát âm US
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center space-y-3 my-auto">
                <span className={`text-xs font-bold uppercase tracking-wider ${dark ? 'text-primary-300/40' : 'text-primary-500/40'}`}>
                  Nghĩa tiếng Việt
                </span>
                <h3 className={`text-2xl sm:text-3xl font-black ${dark ? 'text-accent-400' : 'text-primary-600'}`}>
                  {word.meaningVi}
                </h3>
              </div>
            )}

            {/* Bottom Tip */}
            <div className="text-center">
              <span className={`inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1 rounded-full border ${
                dark ? 'bg-surface-800/60 border-white/5 text-surface-200/40' : 'bg-white/80 border-surface-200/50 text-surface-800/50'
              }`}>
                🔄 Chạm để lật xem mặt sau
              </span>
            </div>
          </div>

          {/* BACK SIDE */}
          <div className={`absolute inset-0 backface-hidden rotate-y-180 rounded-3xl p-6 sm:p-8 flex flex-col justify-between border shadow-2xl transition-all ${
            dark
              ? 'bg-gradient-to-br from-surface-900 via-primary-950/40 to-surface-850 border-primary-500/30 shadow-black/50'
              : 'bg-gradient-to-br from-primary-50/50 via-white to-accent-50/30 border-primary-200 shadow-primary-500/10'
          }`}>
            {/* Header info */}
            <div className="flex justify-between items-center">
              <span className={`text-xs font-bold uppercase tracking-wider ${dark ? 'text-accent-400' : 'text-primary-600'}`}>
                {word.word} ({word.partOfSpeech})
              </span>
              <button
                onClick={(e) => { e.stopPropagation(); speakText(word.word); }}
                className={`p-1.5 rounded-xl text-xs font-bold transition-all ${
                  dark ? 'bg-surface-800 text-primary-300' : 'bg-primary-100 text-primary-600'
                }`}
              >
                🔊 Nghe lại
              </button>
            </div>

            {/* Vietnamese Meaning & Example */}
            <div className="space-y-3 my-auto">
              {!isFrontVietnamese ? (
                <div>
                  <h4 className={`text-2xl sm:text-3xl font-black mb-2 ${dark ? 'text-accent-400' : 'text-primary-600'}`}>
                    {word.meaningVi}
                  </h4>
                </div>
              ) : (
                <div>
                  <h4 className="text-3xl font-black text-primary-500 mb-1">
                    {word.word}
                  </h4>
                  <p className={`text-xs font-medium ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                    {word.pronunciation?.us || word.pronunciation?.uk}
                  </p>
                </div>
              )}

              {/* Example sentence box */}
              {word.exampleEn && (
                <div className={`rounded-2xl p-3.5 text-left text-xs sm:text-sm space-y-1 border ${
                  dark ? 'bg-surface-900/80 border-white/10' : 'bg-white border-primary-100 shadow-sm'
                }`}>
                  <p className="font-semibold leading-relaxed"
                     dangerouslySetInnerHTML={{
                       __html: word.exampleEn.replace(
                         new RegExp(`\\b${word.word}\\w*\\b`, 'gi'),
                         '<strong class="text-primary-500 font-black">$&</strong>'
                       )
                     }}
                  />
                  <p className={`text-xs italic ${dark ? 'text-surface-200/60' : 'text-surface-800/60'}`}>
                    {word.exampleVi}
                  </p>
                </div>
              )}

              {/* Extra Info Badges */}
              <div className="flex flex-wrap gap-1.5 justify-center text-[11px]">
                {word.synonyms && word.synonyms.length > 0 && (
                  <span className={`px-2 py-0.5 rounded-lg border ${
                    dark ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' : 'bg-emerald-50 border-emerald-200 text-emerald-700'
                  }`}>
                    Đồng nghĩa: {word.synonyms.join(', ')}
                  </span>
                )}
                {word.antonyms && word.antonyms.length > 0 && (
                  <span className={`px-2 py-0.5 rounded-lg border ${
                    dark ? 'bg-rose-500/10 border-rose-500/20 text-rose-400' : 'bg-rose-50 border-rose-200 text-rose-700'
                  }`}>
                    Trái nghĩa: {word.antonyms.join(', ')}
                  </span>
                )}
                {word.toeicNotes && word.toeicNotes.length > 0 && (
                  <span className={`px-2 py-0.5 rounded-lg border ${
                    dark ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' : 'bg-amber-50 border-amber-200 text-amber-700'
                  }`}>
                    TOEIC: {word.toeicNotes[0]}
                  </span>
                )}
              </div>
            </div>

            {/* Bottom Tip */}
            <div className="text-center">
              <span className={`inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1 rounded-full border ${
                dark ? 'bg-surface-800/60 border-white/5 text-surface-200/40' : 'bg-white/80 border-surface-200/50 text-surface-800/50'
              }`}>
                🔄 Chạm để quay lại mặt trước
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Control Buttons */}
      <div className="flex items-center justify-between gap-2 pt-2">
        {/* Previous */}
        <button
          onClick={handlePrev}
          disabled={current === 0}
          className={`px-4 py-3 rounded-2xl flex items-center gap-1.5 text-xs font-bold transition-all disabled:opacity-30 ${
            dark ? 'bg-surface-900 border border-white/10 text-surface-200 hover:bg-surface-800' : 'bg-white border border-surface-200 text-surface-800 hover:bg-surface-100'
          }`}
        >
          ← Trước (Left)
        </button>

        {/* Learning Status Actions */}
        <div className="flex gap-2">
          <button
            onClick={() => handleNext(false)}
            className={`px-4 py-3 rounded-2xl text-xs font-extrabold transition-all border shadow-sm ${
              dark
                ? 'bg-rose-500/15 border-rose-500/30 text-rose-400 hover:bg-rose-500/25'
                : 'bg-rose-50 border-rose-200 text-rose-600 hover:bg-rose-100'
            }`}
          >
            Chưa thuộc 😕 (1)
          </button>
          
          <button
            onClick={() => handleNext(true)}
            className="px-5 py-3 rounded-2xl text-xs font-black bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 hover:scale-105 active:scale-95 transition-all"
          >
            Đã thuộc 🎉 (2)
          </button>
        </div>

        {/* Next */}
        <button
          onClick={() => handleNext()}
          disabled={current === words.length - 1}
          className={`px-4 py-3 rounded-2xl flex items-center gap-1.5 text-xs font-bold transition-all disabled:opacity-30 ${
            dark ? 'bg-surface-900 border border-white/10 text-surface-200 hover:bg-surface-800' : 'bg-white border border-surface-200 text-surface-800 hover:bg-surface-100'
          }`}
        >
          Tiếp (Right) →
        </button>
      </div>

      {/* Keyboard Hint */}
      <div className="text-center text-[11px] opacity-40 font-medium tracking-wide">
        💡 Mẹo bàn phím: <strong>Spacebar</strong> (Lật thẻ) • <strong>Mũi tên Trái/Phải</strong> (Chuyển thẻ) • <strong>Phím 1</strong> (Chưa thuộc) • <strong>Phím 2</strong> (Đã thuộc)
      </div>

      {/* Done State Modal / Section */}
      {isDone && (
        <div className={`mt-6 text-center rounded-3xl p-8 animate-slide-up border shadow-2xl ${
          dark ? 'bg-gradient-to-br from-surface-900 to-surface-850 border-emerald-500/30' : 'bg-gradient-to-br from-white to-emerald-50/50 border-emerald-200'
        }`}>
          <div className="text-5xl mb-3 animate-bounce">🏆</div>
          <h3 className="text-2xl font-black tracking-tight mb-1">Hoàn thành bài học!</h3>
          <p className={`text-sm mb-6 ${dark ? 'text-surface-200/60' : 'text-surface-800/60'}`}>
            Bạn đã vượt qua toàn bộ {words.length} thẻ Flashcard và ghi nhớ <strong className="text-emerald-500">{known.size} từ vựng</strong>.
          </p>
          <div className="flex flex-wrap gap-3 justify-center">
            <button
              onClick={restart}
              className="px-6 py-3 rounded-2xl bg-gradient-to-r from-primary-500 to-primary-600 text-white text-xs font-bold shadow-lg shadow-primary-500/25 hover:scale-105 transition-all"
            >
              🔄 Học lại từ đầu
            </button>
            <Link
              to={`/unit/${unit.id}/quiz`}
              className="px-6 py-3 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-500 text-white text-xs font-bold shadow-lg shadow-emerald-500/25 hover:scale-105 transition-all"
            >
              📝 Kiểm tra Quiz ngay →
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
