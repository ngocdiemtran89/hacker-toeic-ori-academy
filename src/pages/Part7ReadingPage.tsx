import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { part7Passages, Part7PassageSet } from '../data/part7Data';
import { playCorrectSound, playWrongSound, playFanfareSound } from '../utils/audio';
import { addXp } from '../utils/srs';

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

export default function Part7ReadingPage({ dark }: Props) {
  const [selectedPassageId, setSelectedPassageId] = useState<string>(part7Passages[0].id);
  const [showBilingualPassage, setShowBilingualPassage] = useState(false);
  const [userAnswers, setUserAnswers] = useState<Record<string, 'A' | 'B' | 'C' | 'D'>>({});
  const [submitted, setSubmitted] = useState(false);
  const [highlightedCitation, setHighlightedCitation] = useState<string | null>(null);

  const passage: Part7PassageSet = part7Passages.find(p => p.id === selectedPassageId) || part7Passages[0];

  useEffect(() => {
    setUserAnswers({});
    setSubmitted(false);
    setHighlightedCitation(null);
  }, [selectedPassageId]);

  const handleSelectOption = (questionId: string, optionKey: 'A' | 'B' | 'C' | 'D') => {
    if (submitted) return;
    setUserAnswers(prev => ({
      ...prev,
      [questionId]: optionKey,
    }));
  };

  const handleSubmit = () => {
    if (submitted) return;
    setSubmitted(true);

    let correctCount = 0;
    passage.questions.forEach(q => {
      if (userAnswers[q.id] === q.answerKey) {
        correctCount++;
      }
    });

    if (correctCount === passage.questions.length) {
      playFanfareSound();
      addXp(100);
    } else if (correctCount > 0) {
      playCorrectSound();
      addXp(correctCount * 20);
    } else {
      playWrongSound();
    }
  };

  return (
    <div className="pt-6 max-w-5xl mx-auto space-y-6 animate-fade-in pb-16">
      {/* Top Navigation */}
      <div className="flex items-center justify-between">
        <Link to="/" className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
          dark ? 'bg-surface-900 border-white/10 text-primary-300' : 'bg-white border-primary-100 text-primary-600'
        }`}>
          ← Trang chủ
        </Link>

        <span className={`text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full ${
          dark ? 'bg-accent-500/20 text-accent-400' : 'bg-accent-500/10 text-accent-600'
        }`}>
          🎯 TOEIC Part 7 Reading Mastery
        </span>
      </div>

      {/* Title & Selector */}
      <div className="space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span className="text-xs font-black uppercase tracking-wider text-primary-500">
              Đọc Hiểu Đoạn Văn & Trích Dẫn Dẫn Chứng
            </span>
            <h2 className="text-2xl sm:text-3xl font-black tracking-tight">{passage.title}</h2>
          </div>

          {/* Passage Select Dropdown */}
          <select
            value={selectedPassageId}
            onChange={e => setSelectedPassageId(e.target.value)}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold border transition-all ${
              dark ? 'bg-surface-900 border-white/10 text-surface-200' : 'bg-white border-primary-100 text-surface-800'
            }`}
          >
            {part7Passages.map(p => (
              <option key={p.id} value={p.id}>
                [{p.type}] {p.title.substring(0, 35)}...
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Split Grid: Left = Passage & Vocab, Right = Questions & Citations */}
      <div className="grid gap-6 lg:grid-cols-12 items-start">
        {/* LEFT COLUMN: Passage (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className={`p-6 sm:p-8 rounded-3xl border shadow-xl relative transition-all ${
            dark ? 'bg-surface-900/90 border-white/10' : 'bg-white border-primary-100'
          }`}>
            {/* Header controls inside passage */}
            <div className="flex items-center justify-between pb-4 mb-4 border-b border-primary-500/10">
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                dark ? 'bg-primary-500/20 text-primary-300' : 'bg-primary-100 text-primary-700'
              }`}>
                {passage.type} • {passage.difficulty}
              </span>

              {/* Toggle Bilingual Passage */}
              <button
                onClick={() => setShowBilingualPassage(!showBilingualPassage)}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all border ${
                  showBilingualPassage
                    ? 'bg-accent-500 text-white border-accent-500 shadow-sm'
                    : dark ? 'bg-surface-800 border-white/10 text-surface-200/60' : 'bg-surface-100 border-surface-200 text-surface-800/60'
                }`}
              >
                {showBilingualPassage ? '🇻🇳 Đang hiện Dịch Song Ngữ' : '🇬🇧 Hiện Dịch Song Ngữ'}
              </button>
            </div>

            {/* Passage Text */}
            <div className="space-y-4 text-sm sm:text-base leading-relaxed tracking-wide font-sans">
              {!showBilingualPassage ? (
                <div className="whitespace-pre-line">
                  {passage.passageEn.split('\n').map((line, lIdx) => {
                    const isCitation = highlightedCitation && line.includes(highlightedCitation);
                    return (
                      <p
                        key={lIdx}
                        className={`transition-all duration-300 rounded px-1.5 py-0.5 ${
                          isCitation
                            ? 'bg-amber-400/30 text-amber-600 font-bold ring-2 ring-amber-400 rounded-lg animate-pulse'
                            : ''
                        }`}
                      >
                        {line}
                      </p>
                    );
                  })}
                </div>
              ) : (
                <div className="space-y-4">
                  {passage.passageEn.split('\n\n').map((paraEn, pIdx) => {
                    const paraVi = passage.passageVi.split('\n\n')[pIdx] || '';
                    return (
                      <div key={pIdx} className={`p-4 rounded-2xl border space-y-2 ${
                        dark ? 'bg-surface-850 border-white/5' : 'bg-primary-50/30 border-primary-100'
                      }`}>
                        <p className="font-semibold text-primary-500 whitespace-pre-line">
                          {paraEn}
                        </p>
                        <p className={`text-xs italic whitespace-pre-line ${dark ? 'text-surface-200/70' : 'text-surface-800/70'}`}>
                          🇻🇳 {paraVi}
                        </p>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          {/* Passage Key Vocabulary Drawer */}
          <div className={`p-6 rounded-3xl border space-y-3 ${
            dark ? 'bg-surface-900/60 border-white/5' : 'bg-white border-primary-100 shadow-sm'
          }`}>
            <h4 className="text-xs font-black uppercase text-accent-500 tracking-wider">
              📚 Từ Vựng Trọng Tâm Trong Bài Đọc ({passage.keyWords.length})
            </h4>
            <div className="grid gap-2 sm:grid-cols-2">
              {passage.keyWords.map((kw, idx) => (
                <div
                  key={idx}
                  onClick={() => speakText(kw.word)}
                  className={`p-3 rounded-2xl border flex items-center justify-between cursor-pointer hover:scale-[1.02] transition-all ${
                    dark ? 'bg-surface-850 border-white/5' : 'bg-primary-50/40 border-primary-100'
                  }`}
                >
                  <div>
                    <span className="font-bold text-xs text-primary-500">
                      {kw.word} ({kw.partOfSpeech})
                    </span>
                    <p className={`text-[11px] font-medium ${dark ? 'text-surface-200/60' : 'text-surface-800/60'}`}>
                      {kw.meaningVi}
                    </p>
                  </div>
                  <span className="text-xs">🔊</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: Questions & Citations (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="space-y-4">
            {passage.questions.map((q, qIdx) => {
              const selectedKey = userAnswers[q.id];
              const isCorrect = selectedKey === q.answerKey;

              return (
                <div
                  key={q.id}
                  className={`p-6 rounded-3xl border space-y-4 transition-all shadow-md ${
                    dark ? 'bg-surface-900/90 border-white/10' : 'bg-white border-primary-100'
                  }`}
                >
                  {/* Question Header */}
                  <div className="space-y-1">
                    <span className="text-xs font-black uppercase text-primary-500">
                      Câu Hỏi {qIdx + 1} / {passage.questions.length}
                    </span>
                    <h4 className="text-base font-bold leading-snug">{q.questionEn}</h4>
                    <p className={`text-xs italic ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                      🇻🇳 {q.questionVi}
                    </p>
                  </div>

                  {/* Options */}
                  <div className="space-y-2">
                    {q.options.map(opt => {
                      const isSelected = selectedKey === opt.key;
                      let optStyle = dark
                        ? 'bg-surface-850 border-white/5 hover:bg-surface-800'
                        : 'bg-white border-primary-100/60 hover:bg-primary-50 shadow-sm';

                      if (submitted) {
                        if (opt.key === q.answerKey) {
                          optStyle = 'bg-emerald-500/20 border-emerald-500 text-emerald-400 font-bold';
                        } else if (isSelected && !isCorrect) {
                          optStyle = 'bg-rose-500/20 border-rose-500 text-rose-400';
                        }
                      } else if (isSelected) {
                        optStyle = 'bg-primary-500 text-white border-primary-500 font-bold shadow-md';
                      }

                      return (
                        <button
                          key={opt.key}
                          disabled={submitted}
                          onClick={() => handleSelectOption(q.id, opt.key)}
                          className={`w-full p-3 rounded-2xl border text-left text-xs transition-all flex items-start gap-2.5 ${optStyle}`}
                        >
                          <span className="font-mono font-bold shrink-0">{opt.key}.</span>
                          <div className="flex-1 min-w-0">
                            <p className="font-semibold">{opt.textEn}</p>
                            <p className={`text-[11px] mt-0.5 ${isSelected ? 'opacity-90' : 'opacity-60'}`}>
                              🇻🇳 {opt.textVi}
                            </p>
                          </div>
                        </button>
                      );
                    })}
                  </div>

                  {/* Explanation & Evidence Citation (After Submission) */}
                  {submitted && (
                    <div className={`p-4 rounded-2xl border space-y-2.5 text-xs animate-slide-up ${
                      isCorrect 
                        ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
                        : 'bg-rose-500/10 border-rose-500/30 text-rose-400'
                    }`}>
                      <div className="flex justify-between items-center">
                        <span className="font-black uppercase tracking-wider text-[11px]">
                          {isCorrect ? '✅ Đáp Án Đúng' : '❌ Chưa Chính Xác'}
                        </span>
                        <button
                          onClick={() => setHighlightedCitation(q.citationEn)}
                          className="px-2.5 py-1 rounded-lg bg-amber-500/20 border border-amber-500/30 text-amber-400 font-bold text-[10px] hover:bg-amber-500/30 transition-all"
                        >
                          📌 Soi Dẫn Chứng Bài Đọc
                        </button>
                      </div>

                      {/* Evidence Citation */}
                      <div className="p-3 rounded-xl bg-black/20 border border-white/5 space-y-1">
                        <p className="font-bold text-[11px] text-amber-400">📌 Bằng chứng trong bài đọc (Citation):</p>
                        <p className="font-semibold italic text-surface-100">"{q.citationEn}"</p>
                        <p className="text-[11px] opacity-70">🇻🇳 "{q.citationVi}"</p>
                      </div>

                      {/* Step-by-step reasoning */}
                      <div className="space-y-1 pt-1">
                        <p className="font-bold text-primary-400">💡 Giải thích chi tiết:</p>
                        <p className="leading-relaxed opacity-90">{q.explanationVi}</p>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}

            {/* Submit / Reset Action */}
            <div className="pt-2">
              {!submitted ? (
                <button
                  onClick={handleSubmit}
                  disabled={Object.keys(userAnswers).length < passage.questions.length}
                  className="w-full py-4 rounded-2xl bg-gradient-to-r from-primary-500 via-accent-500 to-emerald-500 text-white font-black text-sm shadow-xl shadow-primary-500/25 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-40"
                >
                  🚀 Nộp Bài & Xem Trích Dẫn Dẫn Chứng!
                </button>
              ) : (
                <button
                  onClick={() => {
                    setUserAnswers({});
                    setSubmitted(false);
                    setHighlightedCitation(null);
                  }}
                  className="w-full py-3.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-black text-sm shadow-lg shadow-amber-500/20 hover:scale-[1.02] active:scale-[0.98] transition-all"
                >
                  🔄 Làm Lại Bài Đọc Này
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
