import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { VocabWord } from '../types';

interface Props {
  word: VocabWord;
  index: number;
  unitId: string;
  dark: boolean;
  viewMode?: 'flashcard' | 'list';
  onOpenAiModal?: (word: VocabWord) => void;
}

function FrequencyStars({ count }: { count: number }) {
  return (
    <span className="flex gap-0.5" title={`Tần suất xuất hiện: ${count === 3 ? 'rất cao' : count === 2 ? 'cao' : 'trung bình'}`}>
      {[1, 2, 3].map(i => (
        <svg key={i} className={`w-3.5 h-3.5 ${i <= count ? 'text-warning' : 'text-surface-200 dark:text-surface-800'}`} fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
        </svg>
      ))}
    </span>
  );
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

export default function VocabularyCard({ word, index, unitId, dark, viewMode = 'flashcard', onOpenAiModal }: Props) {
  const [flipped, setFlipped] = useState(false);

  const posColors: Record<string, string> = {
    n: 'bg-blue-500/15 text-blue-600 dark:bg-blue-400/20 dark:text-blue-300 border border-blue-500/20',
    v: 'bg-emerald-500/15 text-emerald-600 dark:bg-emerald-400/20 dark:text-emerald-300 border border-emerald-500/20',
    adj: 'bg-amber-500/15 text-amber-600 dark:bg-amber-400/20 dark:text-amber-300 border border-amber-500/20',
    adv: 'bg-purple-500/15 text-purple-600 dark:bg-purple-400/20 dark:text-purple-300 border border-purple-500/20',
  };

  // If in static list mode, render standard full view
  if (viewMode === 'list') {
    return (
      <article
        className={`rounded-2xl border p-5 transition-all duration-300 hover:shadow-lg animate-fade-in ${
          dark
            ? 'bg-surface-900/60 border-white/5 hover:border-primary-500/30'
            : 'bg-white/80 border-primary-100/40 hover:border-primary-300/60 shadow-sm'
        }`}
        style={{ animationDelay: `${index * 30}ms` }}
      >
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className={`text-xs font-bold px-2 py-0.5 rounded-md ${dark ? 'bg-surface-800 text-surface-200/50' : 'bg-surface-100 text-surface-800/40'}`}>
                #{index + 1}
              </span>
              <h3 className="text-xl font-black tracking-tight">{word.word}</h3>
              <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${posColors[word.partOfSpeech] || 'bg-gray-100 text-gray-600'}`}>
                {word.partOfSpeech}
              </span>
              <FrequencyStars count={word.frequency} />
            </div>
            <p className={`text-xs font-medium mt-1 ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
              {word.pronunciation?.us && `[${word.pronunciation.us}]`}
            </p>
          </div>
          <div className="flex items-center gap-1.5 shrink-0">
            {onOpenAiModal && (
              <button
                onClick={() => onOpenAiModal(word)}
                className={`p-2 rounded-xl text-xs font-bold transition-all hover:scale-105 ${
                  dark ? 'bg-accent-500/20 text-accent-400' : 'bg-accent-500/10 text-accent-600'
                }`}
                title="Mở Ví Dụ Song Ngữ AI"
              >
                🤖 AI Ví Dụ
              </button>
            )}
            <button
              onClick={() => speak(word.word)}
              className={`p-2.5 rounded-xl flex items-center justify-center transition-all hover:scale-110 active:scale-95 ${
                dark ? 'bg-primary-500/20 text-primary-300' : 'bg-primary-100 text-primary-600'
              }`}
              title={`Phát âm ${word.word}`}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.536 8.464a5 5 0 010 7.072M17.95 6.05a8 8 0 010 11.9M6.5 8.788V15.212a1 1 0 001.052.986l5.318-.531A1 1 0 0013.5 14.7V9.3a1 1 0 00-.63-.966l-5.318-.531A1 1 0 006.5 8.788z"/>
              </svg>
            </button>
          </div>
        </div>

        <p className={`text-base font-extrabold mb-3 ${dark ? 'text-accent-400' : 'text-primary-600'}`}>
          {word.meaningVi}
        </p>

        {word.exampleEn && (
          <div className={`rounded-xl p-3.5 mb-3 text-xs sm:text-sm ${dark ? 'bg-surface-800/60 border border-white/5' : 'bg-primary-50/50 border border-primary-100/30'}`}>
            <p className="font-semibold leading-relaxed"
               dangerouslySetInnerHTML={{
                 __html: word.exampleEn.replace(
                   new RegExp(`\\b${word.word}\\w*\\b`, 'gi'),
                   '<strong class="text-primary-500">$&</strong>'
                 )
               }}
            />
            <p className={`mt-1 text-xs ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
              {word.exampleVi}
            </p>
          </div>
        )}
      </article>
    );
  }

  // Interactive 3D Flip Flashcard Card Mode
  return (
    <div className="perspective-1000 animate-fade-in" style={{ animationDelay: `${index * 30}ms` }}>
      <div
        onClick={() => setFlipped(!flipped)}
        className={`relative w-full aspect-[16/11] cursor-pointer preserve-3d transition-transform duration-500 ${
          flipped ? 'rotate-y-180' : ''
        }`}
      >
        {/* FRONT SIDE (Tiếng Anh) */}
        <div className={`absolute inset-0 backface-hidden rounded-2xl p-5 flex flex-col justify-between border shadow-lg transition-all hover:scale-[1.01] ${
          dark
            ? 'bg-gradient-to-br from-surface-900 via-surface-850 to-surface-800 border-white/10 shadow-black/40'
            : 'bg-gradient-to-br from-white via-primary-50/20 to-primary-100/30 border-primary-100 shadow-primary-500/5'
        }`}>
          {/* Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className={`text-xs font-bold px-2 py-0.5 rounded-md ${dark ? 'bg-surface-800 text-surface-200/50' : 'bg-surface-100 text-surface-800/40'}`}>
                #{index + 1}
              </span>
              <span className={`text-[11px] font-extrabold px-2 py-0.5 rounded-full ${posColors[word.partOfSpeech] || 'bg-gray-100 text-gray-600'}`}>
                {word.partOfSpeech}
              </span>
            </div>
            <FrequencyStars count={word.frequency} />
          </div>

          {/* Center Word & Pronounce */}
          <div className="text-center space-y-2 my-auto">
            <h3 className="text-2xl sm:text-3xl font-black tracking-tight text-primary-500">
              {word.word}
            </h3>
            <p className={`text-xs font-medium ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
              {word.pronunciation?.us && `[${word.pronunciation.us}]`}
            </p>
            <div className="flex justify-center gap-1.5">
              <button
                onClick={(e) => { e.stopPropagation(); speak(word.word); }}
                className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-[11px] font-bold transition-all hover:scale-105 ${
                  dark ? 'bg-primary-500/20 text-primary-300' : 'bg-primary-100 text-primary-600'
                }`}
              >
                🔊 Nghe âm
              </button>
              {onOpenAiModal && (
                <button
                  onClick={(e) => { e.stopPropagation(); onOpenAiModal(word); }}
                  className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-[11px] font-extrabold transition-all hover:scale-105 ${
                    dark ? 'bg-accent-500/20 text-accent-400' : 'bg-accent-500/10 text-accent-600'
                  }`}
                >
                  🤖 Ví dụ AI
                </button>
              )}
            </div>
          </div>

          {/* Footer instruction */}
          <div className="flex justify-between items-center text-[11px] font-medium pt-2 border-t border-dashed border-primary-500/10">
            <span className={dark ? 'text-surface-200/40' : 'text-surface-800/40'}>
              🔄 Click để xem nghĩa & ví dụ
            </span>
            <Link
              to={`/unit/${unitId}/flashcards`}
              onClick={(e) => e.stopPropagation()}
              className="text-primary-500 font-bold hover:underline"
            >
              Học Flashcard →
            </Link>
          </div>
        </div>

        {/* BACK SIDE (Tiếng Việt & Ví dụ) */}
        <div className={`absolute inset-0 backface-hidden rotate-y-180 rounded-2xl p-5 flex flex-col justify-between border shadow-lg transition-all ${
          dark
            ? 'bg-gradient-to-br from-surface-900 via-primary-950/30 to-surface-850 border-primary-500/30 shadow-black/40'
            : 'bg-gradient-to-br from-primary-50/60 via-white to-accent-50/30 border-primary-200 shadow-primary-500/10'
        }`}>
          {/* Header */}
          <div className="flex justify-between items-center">
            <span className="text-xs font-black text-primary-500">
              {word.word} ({word.partOfSpeech})
            </span>
            <div className="flex gap-1">
              {onOpenAiModal && (
                <button
                  onClick={(e) => { e.stopPropagation(); onOpenAiModal(word); }}
                  className={`p-1.5 rounded-lg text-xs font-bold ${dark ? 'bg-accent-500/20 text-accent-400' : 'bg-accent-500/10 text-accent-600'}`}
                >
                  🤖 Ví dụ AI
                </button>
              )}
              <button
                onClick={(e) => { e.stopPropagation(); speak(word.word); }}
                className={`p-1.5 rounded-lg text-xs font-bold ${dark ? 'bg-surface-800 text-primary-300' : 'bg-primary-100 text-primary-600'}`}
              >
                🔊 Nghe
              </button>
            </div>
          </div>

          {/* Meaning & Example */}
          <div className="space-y-2 my-auto">
            <h4 className={`text-xl sm:text-2xl font-black ${dark ? 'text-accent-400' : 'text-primary-600'}`}>
              {word.meaningVi}
            </h4>

            {word.exampleEn && (
              <div className={`rounded-xl p-2.5 text-xs text-left leading-relaxed border ${
                dark ? 'bg-surface-900/80 border-white/10' : 'bg-white border-primary-100'
              }`}>
                <p className="font-semibold"
                   dangerouslySetInnerHTML={{
                     __html: word.exampleEn.replace(
                       new RegExp(`\\b${word.word}\\w*\\b`, 'gi'),
                       '<strong class="text-primary-500">$&</strong>'
                     )
                   }}
                />
                <p className={`mt-0.5 text-[11px] ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                  {word.exampleVi}
                </p>
              </div>
            )}
          </div>

          {/* Footer instruction */}
          <div className="flex justify-between items-center text-[11px] font-medium pt-2 border-t border-dashed border-primary-500/10">
            <span className={dark ? 'text-surface-200/40' : 'text-surface-800/40'}>
              🔄 Click để quay lại từ tiếng Anh
            </span>
            <span className="font-bold text-accent-500">
              Đã lật 💡
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
