import { useParams, Link } from 'react-router-dom';
import { useState, useMemo } from 'react';
import { getUnit } from '../data';
import VocabularyCard from '../components/VocabularyCard';

interface Props {
  dark: boolean;
}

export default function UnitDetailPage({ dark }: Props) {
  const { unitId } = useParams<{ unitId: string }>();
  const unit = getUnit(unitId || '');
  const [search, setSearch] = useState('');
  const [filterPos, setFilterPos] = useState<string>('all');

  const filtered = useMemo(() => {
    if (!unit) return [];
    return unit.words.filter(w => {
      const matchSearch = !search || 
        w.word.toLowerCase().includes(search.toLowerCase()) ||
        w.meaningVi.toLowerCase().includes(search.toLowerCase());
      const matchPos = filterPos === 'all' || w.partOfSpeech === filterPos;
      return matchSearch && matchPos;
    });
  }, [unit, search, filterPos]);

  if (!unit) {
    return (
      <div className="pt-20 text-center">
        <p className="text-xl font-bold">Không tìm thấy bài học</p>
        <Link to="/" className="text-primary-500 underline mt-2 inline-block">← Về trang chủ</Link>
      </div>
    );
  }

  const posOptions = [
    { value: 'all', label: 'Tất cả' },
    { value: 'n', label: 'Danh từ' },
    { value: 'v', label: 'Động từ' },
    { value: 'adj', label: 'Tính từ' },
    { value: 'adv', label: 'Trạng từ' },
  ];

  // Tab state
  const [activeTab, setActiveTab] = useState<'vocab' | 'story'>('vocab');

  // Text-to-speech trigger
  const playWordAudio = (wordText: string) => {
    const utterance = new SpeechSynthesisUtterance(wordText);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  };

  // Interactive story renderer
  const renderStoryContent = (content: string) => {
    const parts = content.split(/(\*\*[^*]+\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        const cleanWord = part.replace(/\*\*/g, '');
        // Find matching word for details lookup
        const cleanWordLower = cleanWord.toLowerCase();
        const vocabWord = unit.words.find(
          w => w.word.toLowerCase() === cleanWordLower || 
          cleanWordLower.startsWith(w.word.toLowerCase().substring(0, 4))
        );
        
        return (
          <span
            key={index}
            onClick={() => playWordAudio(vocabWord?.word || cleanWord)}
            className={`inline-block px-1.5 py-0.5 mx-0.5 rounded font-black cursor-pointer hover:scale-[1.05] active:scale-[0.95] transition-all ${
              dark
                ? 'bg-primary-500/20 text-primary-300 border border-primary-500/30 hover:bg-primary-500 hover:text-white'
                : 'bg-primary-100 text-primary-700 hover:bg-primary-500 hover:text-white'
            }`}
            title="Nhấp để nghe phát âm"
          >
            {cleanWord}
          </span>
        );
      }
      return <span key={index}>{part}</span>;
    });
  };

  return (
    <div className="pt-6 space-y-6">
      {/* Breadcrumb & title */}
      <div className="animate-fade-in">
        <Link to="/" className={`text-xs font-medium hover:underline ${dark ? 'text-primary-300/50' : 'text-primary-500/50'}`}>
          ← Trang chủ
        </Link>
        <div className="flex items-start justify-between gap-4 mt-3">
          <div>
            <p className={`text-xs font-bold uppercase tracking-wider mb-1 ${dark ? 'text-primary-300/40' : 'text-primary-500/40'}`}>
              DAY {String(unit.day).padStart(2, '0')} • {unit.topic}
            </p>
            <h2 className="text-3xl font-black tracking-tight">{unit.title}</h2>
            <p className={`text-sm mt-1 ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
              {unit.words.length} từ vựng
            </p>
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-2.5 flex-wrap animate-fade-in" style={{ animationDelay: '80ms' }}>
        <Link
          to={`/unit/${unit.id}/flashcards`}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary-500 to-primary-600 text-white text-sm font-semibold shadow-lg shadow-primary-500/25 hover:shadow-primary-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
          Flashcard
        </Link>
        <Link
          to={`/unit/${unit.id}/quiz`}
          className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all hover:scale-[1.02] active:scale-[0.98] ${
            dark
              ? 'bg-accent-500/15 text-accent-400 border border-accent-500/20 hover:bg-accent-500/25'
              : 'bg-accent-500/10 text-accent-600 border border-accent-500/20 hover:bg-accent-500/20'
          }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          Làm Quiz
        </Link>
      </div>

      {/* Tab Switcher */}
      <div className="flex border-b border-white/5 animate-fade-in" style={{ animationDelay: '100ms' }}>
        <button
          onClick={() => setActiveTab('vocab')}
          className={`px-6 py-3 text-sm font-bold border-b-2 transition-all ${
            activeTab === 'vocab'
              ? 'border-primary-500 text-primary-500'
              : dark
                ? 'border-transparent text-surface-200/50 hover:text-surface-200/80'
                : 'border-transparent text-surface-800/40 hover:text-surface-800/70'
          }`}
        >
          Danh Sách Từ Vựng
        </button>
        {unit.story && (
          <button
            onClick={() => setActiveTab('story')}
            className={`px-6 py-3 text-sm font-bold border-b-2 transition-all flex items-center gap-2 ${
              activeTab === 'story'
                ? 'border-primary-500 text-primary-500'
                : dark
                  ? 'border-transparent text-surface-200/50 hover:text-surface-200/80'
                  : 'border-transparent text-surface-800/40 hover:text-surface-800/70'
            }`}
          >
            📚 Truyện Chêm Song Ngữ
          </button>
        )}
      </div>

      {activeTab === 'vocab' ? (
        <>
          {/* Search & filter */}
          <div className="flex flex-col sm:flex-row gap-3 animate-fade-in" style={{ animationDelay: '150ms' }}>
            <div className="relative flex-1">
              <svg className={`absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 ${dark ? 'text-surface-200/30' : 'text-surface-800/30'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              <input
                type="text"
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Tìm từ vựng..."
                className={`w-full pl-10 pr-4 py-2.5 rounded-xl text-sm border transition-all focus:outline-none focus:ring-2 ${
                  dark
                    ? 'bg-surface-900/60 border-white/5 focus:ring-primary-500/30 placeholder:text-surface-200/25'
                    : 'bg-white/80 border-primary-100/30 focus:ring-primary-300/50 placeholder:text-surface-800/25'
                }`}
              />
            </div>
            <div className="flex gap-1.5">
              {posOptions.map(opt => (
                <button
                  key={opt.value}
                  onClick={() => setFilterPos(opt.value)}
                  className={`px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
                    filterPos === opt.value
                      ? 'bg-primary-500 text-white shadow-md shadow-primary-500/25'
                      : dark
                        ? 'bg-surface-800/60 text-surface-200/50 hover:text-surface-200/80'
                        : 'bg-white/60 text-surface-800/40 hover:text-surface-800/70 border border-primary-100/20'
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {/* Word count */}
          <p className={`text-xs font-medium ${dark ? 'text-surface-200/30' : 'text-surface-800/30'}`}>
            Hiển thị {filtered.length}/{unit.words.length} từ
          </p>

          {/* Vocabulary list */}
          <div className="grid gap-4 sm:grid-cols-2">
            {filtered.map((word, i) => (
              <VocabularyCard key={word.id} word={word} index={i} dark={dark} />
            ))}
          </div>

          {filtered.length === 0 && (
            <div className="text-center py-16">
              <p className="text-4xl mb-3">🔍</p>
              <p className="font-semibold">Không tìm thấy từ vựng</p>
              <p className={`text-sm mt-1 ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>Thử tìm kiếm với từ khóa khác</p>
            </div>
          )}
        </>
      ) : (
        unit.story && (
          <div className="space-y-6 animate-fade-in">
            {/* Story Container */}
            <div className={`p-8 rounded-3xl border leading-relaxed text-base transition-all ${
              dark
                ? 'bg-surface-900/40 border-white/5 text-surface-200'
                : 'bg-white/80 border-primary-100/20 text-surface-800 shadow-xl shadow-primary-500/5'
            }`}>
              <h3 className="text-xl font-black mb-4 tracking-tight flex items-center gap-2">
                📖 {unit.story.title}
              </h3>
              <div className="space-y-4 text-justify leading-loose tracking-wide">
                {renderStoryContent(unit.story.content)}
              </div>
            </div>

            {/* Story Words list */}
            <div className="space-y-3">
              <h4 className="text-sm font-bold uppercase tracking-wider text-primary-500">
                Từ vựng trong truyện ({unit.story.words.length})
              </h4>
              <div className="grid gap-2 sm:grid-cols-2 md:grid-cols-3">
                {unit.story.words.map((w, index) => (
                  <div
                    key={index}
                    onClick={() => playWordAudio(w.word)}
                    className={`p-4 rounded-2xl border flex items-center justify-between cursor-pointer hover:scale-[1.02] active:scale-[0.98] transition-all ${
                      dark
                        ? 'bg-surface-900/60 border-white/5 hover:bg-surface-900'
                        : 'bg-white border-primary-100/25 hover:shadow-lg hover:shadow-primary-500/5 shadow-sm'
                    }`}
                  >
                    <div>
                      <p className="font-bold text-primary-500 text-sm">{w.word}</p>
                      <p className={`text-xs mt-0.5 ${dark ? 'text-surface-300' : 'text-surface-600'}`}>{w.meaningVi}</p>
                    </div>
                    <svg className="w-4 h-4 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                    </svg>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )
      )}
    </div>

  );
}
