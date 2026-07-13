import type { VocabWord } from '../types';

interface Props {
  word: VocabWord;
  index: number;
  dark: boolean;
}

function FrequencyStars({ count }: { count: number }) {
  return (
    <span className="flex gap-0.5" title={`Tần suất xuất hiện: ${count === 3 ? 'rất cao' : count === 2 ? 'cao' : 'trung bình'}`}>
      {[1, 2, 3].map(i => (
        <svg key={i} className={`w-3 h-3 ${i <= count ? 'text-warning' : 'text-surface-200 dark:text-surface-800'}`} fill="currentColor" viewBox="0 0 20 20">
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

export default function VocabularyCard({ word, index, dark }: Props) {
  const posColors: Record<string, string> = {
    n: 'bg-blue-500/10 text-blue-600 dark:bg-blue-400/15 dark:text-blue-300',
    v: 'bg-emerald-500/10 text-emerald-600 dark:bg-emerald-400/15 dark:text-emerald-300',
    adj: 'bg-purple-500/10 text-purple-600 dark:bg-purple-400/15 dark:text-purple-300',
    adv: 'bg-amber-500/10 text-amber-600 dark:bg-amber-400/15 dark:text-amber-300',
  };

  return (
    <article
      className={`group rounded-2xl border p-5 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5 animate-fade-in ${
        dark
          ? 'bg-surface-900/60 border-white/5 hover:border-primary-500/30 hover:shadow-primary-500/5'
          : 'bg-white/80 border-primary-100/40 hover:border-primary-300/60 hover:shadow-primary-200/30'
      }`}
      style={{ animationDelay: `${index * 40}ms` }}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2.5 flex-wrap">
            <span className={`text-xs font-bold px-1.5 py-0.5 rounded-md ${dark ? 'bg-surface-800 text-surface-200/50' : 'bg-surface-100 text-surface-800/40'}`}>
              {index + 1}
            </span>
            <h3 className="text-xl font-bold tracking-tight">{word.word}</h3>
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${posColors[word.partOfSpeech] || 'bg-gray-100 text-gray-600'}`}>
              {word.partOfSpeech}
            </span>
            <FrequencyStars count={word.frequency} />
          </div>
          <p className={`text-sm mt-1 ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
            {word.pronunciation.us && `[${word.pronunciation.us}]`}
          </p>
        </div>
        <button
          onClick={() => speak(word.word)}
          className={`shrink-0 w-8 h-8 rounded-xl flex items-center justify-center transition-all hover:scale-110 active:scale-95 ${
            dark ? 'bg-primary-500/15 text-primary-300 hover:bg-primary-500/25' : 'bg-primary-50 text-primary-500 hover:bg-primary-100'
          }`}
          aria-label={`Phát âm ${word.word}`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.536 8.464a5 5 0 010 7.072M17.95 6.05a8 8 0 010 11.9M6.5 8.788V15.212a1 1 0 001.052.986l5.318-.531A1 1 0 0013.5 14.7V9.3a1 1 0 00-.63-.966l-5.318-.531A1 1 0 006.5 8.788z"/>
          </svg>
        </button>
      </div>

      {/* Meaning */}
      <p className={`text-base font-semibold mb-3 ${dark ? 'text-accent-400' : 'text-primary-600'}`}>
        {word.meaningVi}
      </p>

      {/* Example */}
      <div className={`rounded-xl p-3.5 mb-3 text-sm ${dark ? 'bg-surface-800/60' : 'bg-primary-50/50'}`}>
        <p className="font-medium leading-relaxed"
           dangerouslySetInnerHTML={{
             __html: word.exampleEn.replace(
               new RegExp(`\\b${word.word}\\w*\\b`, 'gi'),
               '<strong class="text-primary-500 underline decoration-primary-300/40 underline-offset-2">$&</strong>'
             )
           }}
        />
        <p className={`mt-1.5 leading-relaxed ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
          {word.exampleVi}
        </p>
      </div>

      {/* Expandable details */}
      {(word.derivatives.length > 0 || word.synonyms.length > 0 || word.antonyms.length > 0 || word.toeicNotes.length > 0) && (
        <details className="group/details">
          <summary className={`text-xs font-semibold cursor-pointer select-none flex items-center gap-1.5 py-1 ${
            dark ? 'text-primary-300/70 hover:text-primary-300' : 'text-primary-500/70 hover:text-primary-500'
          } transition-colors`}>
            <svg className="w-3.5 h-3.5 transition-transform group-open/details:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7"/>
            </svg>
            Xem thêm chi tiết
          </summary>
          <div className="mt-2 space-y-2 animate-fade-in">
            {word.derivatives.length > 0 && (
              <div className="flex flex-wrap gap-1.5">
                {word.derivatives.map(d => (
                  <span key={d.word} className={`text-xs px-2 py-1 rounded-lg ${dark ? 'bg-surface-800 text-surface-200/70' : 'bg-surface-100 text-surface-800/70'}`}>
                    <strong>{d.word}</strong> ({d.partOfSpeech}) {d.meaningVi}
                  </span>
                ))}
              </div>
            )}
            {word.synonyms.length > 0 && (
              <p className={`text-xs ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                <span className="font-semibold text-accent-500">Đồng nghĩa:</span> {word.synonyms.join(', ')}
              </p>
            )}
            {word.antonyms.length > 0 && (
              <p className={`text-xs ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                <span className="font-semibold text-danger">Trái nghĩa:</span> {word.antonyms.join(', ')}
              </p>
            )}
            {word.toeicNotes.map((note, i) => (
              <div key={i} className={`text-xs rounded-lg p-2.5 border-l-2 ${
                dark ? 'bg-primary-500/5 border-primary-500/30 text-surface-200/60' : 'bg-primary-50/80 border-primary-400/40 text-surface-800/60'
              }`}>
                💡 {note}
              </div>
            ))}
          </div>
        </details>
      )}
    </article>
  );
}
