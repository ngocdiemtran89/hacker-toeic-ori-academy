import { useParams, Link } from 'react-router-dom';
import { useState, useMemo, useEffect } from 'react';
import { getUnit } from '../data';
import type { QuizFillQuestion, VocabWord } from '../types';

interface Props {
  dark: boolean;
}

interface MCQuestion {
  word: VocabWord;
  options: string[];
  correctAnswer: string;
}

export default function QuizPage({ dark }: Props) {
  const { unitId } = useParams<{ unitId: string }>();
  const unit = getUnit(unitId || '');

  // Tab state
  const [activeTab, setActiveTab] = useState<'fill' | 'mc'>('fill');

  // Fill quiz logic states
  const fillQuiz = useMemo(() => {
    if (!unit) return null;
    return unit.quiz.find(q => q.type === 'fill-in-the-blank');
  }, [unit]);

  const fillQuestions = (fillQuiz?.questions || []) as QuizFillQuestion[];
  const [fillAnswers, setFillAnswers] = useState<Record<number, string>>({});
  const [fillSubmitted, setFillSubmitted] = useState(false);

  const fillScore = fillSubmitted
    ? fillQuestions.reduce((s, q, i) => s + (fillAnswers[i] === q.a ? 1 : 0), 0)
    : 0;

  const handleFillSubmit = () => setFillSubmitted(true);
  const handleFillRetry = () => {
    setFillAnswers({});
    setFillSubmitted(false);
  };

  // Group fill questions by their option sets
  const fillGroups: { options: string[]; items: { q: QuizFillQuestion; idx: number }[] }[] = [];
  fillQuestions.forEach((q, idx) => {
    const key = q.options.join('|');
    let group = fillGroups.find(g => g.items[0] && (g.items[0].q.options.join('|') === key));
    if (!group) {
      group = { options: q.options, items: [] };
      fillGroups.push(group);
    }
    group.items.push({ q, idx });
  });

  // Multiple Choice (MC) logic states
  const [mcQuestions, setMcQuestions] = useState<MCQuestion[]>([]);
  const [mcAnswers, setMcAnswers] = useState<Record<number, string>>({});
  const [mcSubmitted, setMcSubmitted] = useState(false);

  // Generate MC questions on mount / retry
  const generateMCQuestions = () => {
    if (!unit) return;
    
    // Pick 10 random words from this unit
    const shuffledWords = [...unit.words].sort(() => 0.5 - Math.random()).slice(0, 10);
    
    const newQuestions = shuffledWords.map(word => {
      const correctAnswer = word.meaningVi.split(',')[0].split(';')[0].trim();
      
      // Get other random meanings from this unit as distractors
      const distractors = unit.words
        .filter(w => w.id !== word.id)
        .map(w => w.meaningVi.split(',')[0].split(';')[0].trim())
        .filter((value, index, self) => self.indexOf(value) === index && value !== correctAnswer);
        
      // Shuffle and take 3 distractors
      const shuffledDistractors = distractors.sort(() => 0.5 - Math.random()).slice(0, 3);
      const options = [correctAnswer, ...shuffledDistractors].sort(() => 0.5 - Math.random());
      
      return {
        word,
        options,
        correctAnswer
      };
    });
    
    setMcQuestions(newQuestions);
    setMcAnswers({});
    setMcSubmitted(false);
  };

  useEffect(() => {
    generateMCQuestions();
  }, [unit]);

  const mcScore = mcSubmitted
    ? mcQuestions.reduce((s, q, i) => s + (mcAnswers[i] === q.correctAnswer ? 1 : 0), 0)
    : 0;

  const handleMcSubmit = () => setMcSubmitted(true);
  const handleMcRetry = () => {
    generateMCQuestions();
  };

  if (!unit || !fillQuiz) {
    return (
      <div className="pt-20 text-center">
        <p className="text-xl font-bold">Không tìm thấy quiz</p>
        <Link to="/" className="text-primary-500 underline mt-2 inline-block">← Về trang chủ</Link>
      </div>
    );
  }

  // Voice TTS
  const playAudio = (wordText: string) => {
    const utterance = new SpeechSynthesisUtterance(wordText);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="pt-6 max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div className="animate-fade-in">
        <Link to={`/unit/${unit.id}`} className={`text-xs font-medium hover:underline ${dark ? 'text-primary-300/50' : 'text-primary-500/50'}`}>
          ← {unit.title}
        </Link>
        <h2 className="text-2xl font-black tracking-tight mt-2">Daily Checkup</h2>
        <p className={`text-sm mt-1 ${dark ? 'text-surface-200/40' : 'text-surface-800/40'}`}>
          Luyện tập kiến thức từ vựng qua 2 dạng bài tập trắc nghiệm khác nhau.
        </p>
      </div>

      {/* Tab Switcher */}
      <div className="flex border-b border-white/5 animate-fade-in" style={{ animationDelay: '50ms' }}>
        <button
          onClick={() => setActiveTab('fill')}
          className={`px-6 py-3 text-sm font-bold border-b-2 transition-all ${
            activeTab === 'fill'
              ? 'border-primary-500 text-primary-500'
              : dark
                ? 'border-transparent text-surface-200/50 hover:text-surface-200/80'
                : 'border-transparent text-surface-800/40 hover:text-surface-800/70'
          }`}
        >
          📝 Điền Chỗ Trống
        </button>
        <button
          onClick={() => setActiveTab('mc')}
          className={`px-6 py-3 text-sm font-bold border-b-2 transition-all ${
            activeTab === 'mc'
              ? 'border-primary-500 text-primary-500'
              : dark
                ? 'border-transparent text-surface-200/50 hover:text-surface-200/80'
                : 'border-transparent text-surface-800/40 hover:text-surface-800/70'
          }`}
        >
          🎯 Trắc Nghiệm Nghĩa
        </button>
      </div>

      {activeTab === 'fill' ? (
        <div className="space-y-6">
          {/* Score banner */}
          {fillSubmitted && (
            <div className={`rounded-2xl p-6 text-center animate-slide-up ${
              fillScore === fillQuestions.length
                ? 'bg-gradient-to-r from-success/10 to-accent-500/10 border border-success/20'
                : fillScore >= fillQuestions.length * 0.7
                  ? 'bg-gradient-to-r from-warning/10 to-primary-500/10 border border-warning/20'
                  : 'bg-gradient-to-r from-danger/10 to-primary-500/10 border border-danger/20'
            }`}>
              <p className="text-4xl mb-2">{fillScore === fillQuestions.length ? '🏆' : fillScore >= fillQuestions.length * 0.7 ? '👏' : '💪'}</p>
              <p className="text-2xl font-black">{fillScore}/{fillQuestions.length}</p>
              <p className={`text-sm mt-1 ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                {fillScore === fillQuestions.length
                  ? 'Xuất sắc! Bạn đã điền đúng toàn bộ từ!'
                  : fillScore >= fillQuestions.length * 0.7
                    ? 'Tốt lắm! Cần chú ý thêm một vài chỗ.'
                    : 'Cần ôn tập kỹ hơn về ngữ cảnh nhé!'}
              </p>
              <button
                onClick={handleFillRetry}
                className="mt-4 px-5 py-2 rounded-xl bg-gradient-to-r from-primary-500 to-primary-600 text-white text-sm font-semibold shadow-lg shadow-primary-500/25 hover:scale-[1.02] active:scale-[0.98] transition-all"
              >
                Làm lại
              </button>
            </div>
          )}

          {/* Question groups */}
          <div className="space-y-8">
            {fillGroups.map((group, gi) => (
              <div key={gi} className="space-y-4 animate-fade-in" style={{ animationDelay: `${gi * 100}ms` }}>
                {/* Option bank */}
                <div className={`flex flex-wrap gap-2 p-3 rounded-xl ${dark ? 'bg-surface-900/60 border border-white/5' : 'bg-white/60 border border-primary-100/20'}`}>
                  {group.options.map(opt => (
                    <span key={opt} className={`px-3 py-1.5 rounded-lg text-sm font-semibold ${
                      dark ? 'bg-primary-500/10 text-primary-300' : 'bg-primary-50 text-primary-600'
                    }`}>
                      {opt}
                    </span>
                  ))}
                </div>

                {/* Questions */}
                {group.items.map(({ q, idx }) => {
                  const isCorrect = fillSubmitted && fillAnswers[idx] === q.a;
                  const isWrong = fillSubmitted && fillAnswers[idx] !== q.a;

                  return (
                    <div
                      key={idx}
                      className={`rounded-2xl border p-5 transition-all ${
                        isCorrect
                          ? 'border-success/30 bg-success/5'
                          : isWrong
                            ? 'border-danger/30 bg-danger/5'
                            : dark
                              ? 'bg-surface-900/60 border-white/5'
                              : 'bg-white/80 border-primary-100/30'
                      }`}
                    >
                      <p className="text-sm font-medium leading-relaxed mb-3">
                        <span className={`font-bold mr-2 ${dark ? 'text-primary-300/50' : 'text-primary-500/50'}`}>
                          {String(idx + 1).padStart(2, '0')}.
                        </span>
                        {q.q.split('___').map((part, pi, arr) => (
                          <span key={pi}>
                            {part}
                            {pi < arr.length - 1 && (
                              <select
                                value={fillAnswers[idx] || ''}
                                onChange={e => setFillAnswers(prev => ({ ...prev, [idx]: e.target.value }))}
                                disabled={fillSubmitted}
                                className={`mx-1 px-3 py-1 rounded-lg text-sm font-semibold border-b-2 appearance-none cursor-pointer transition-all ${
                                  fillSubmitted
                                    ? isCorrect
                                      ? 'border-success text-success bg-success/10'
                                      : 'border-danger text-danger bg-danger/10'
                                    : dark
                                      ? 'bg-surface-800 border-primary-500/30 text-surface-100'
                                      : 'bg-primary-50 border-primary-300/50 text-surface-900'
                                }`}
                              >
                                <option value="">—chọn—</option>
                                {group.options.map(o => (
                                  <option key={o} value={o}>{o}</option>
                                ))}
                              </select>
                            )}
                          </span>
                        ))}
                      </p>

                      {fillSubmitted && isWrong && (
                        <p className="text-xs text-danger font-semibold mt-2">
                          ✗ Đáp án đúng: <strong>{q.a}</strong>
                        </p>
                      )}
                      {fillSubmitted && isCorrect && (
                        <p className="text-xs text-success font-semibold mt-2">
                          ✓ Chính xác!
                        </p>
                      )}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>

          {/* Submit */}
          {!fillSubmitted && (
            <div className="flex justify-center pt-4">
              <button
                onClick={handleFillSubmit}
                disabled={Object.keys(fillAnswers).length < fillQuestions.length}
                className="px-8 py-3 rounded-2xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-bold shadow-xl shadow-primary-500/25 hover:shadow-primary-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Nộp bài ✨
              </button>
            </div>
          )}
        </div>
      ) : (
        /* Tab 2: Multiple Choice Meanings (Trắc Nghiệm Nghĩa) */
        <div className="space-y-6">
          {/* Score banner */}
          {mcSubmitted && (
            <div className={`rounded-2xl p-6 text-center animate-slide-up ${
              mcScore === 10
                ? 'bg-gradient-to-r from-success/10 to-accent-500/10 border border-success/20'
                : mcScore >= 7
                  ? 'bg-gradient-to-r from-warning/10 to-primary-500/10 border border-warning/20'
                  : 'bg-gradient-to-r from-danger/10 to-primary-500/10 border border-danger/20'
            }`}>
              <p className="text-4xl mb-2">{mcScore === 10 ? '👑' : mcScore >= 7 ? '👏' : '💪'}</p>
              <p className="text-2xl font-black">{mcScore}/10</p>
              <p className={`text-sm mt-1 ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
                {mcScore === 10
                  ? 'Xuất sắc! Bạn đã chọn đúng 100% nghĩa của từ!'
                  : mcScore >= 7
                    ? 'Khá tốt! Luyện tập thêm vài lần để nhớ sâu hơn nhé.'
                    : 'Cần ôn lại bài để nắm vững nghĩa từ vựng.'}
              </p>
              <button
                onClick={handleMcRetry}
                className="mt-4 px-5 py-2 rounded-xl bg-gradient-to-r from-primary-500 to-primary-600 text-white text-sm font-semibold shadow-lg shadow-primary-500/25 hover:scale-[1.02] active:scale-[0.98] transition-all"
              >
                Chơi vòng mới ⚡
              </button>
            </div>
          )}

          {/* MC Questions List */}
          <div className="space-y-6">
            {mcQuestions.map((q, idx) => {
              const isSelectedCorrect = mcSubmitted && mcAnswers[idx] === q.correctAnswer;
              const isSelectedWrong = mcSubmitted && mcAnswers[idx] !== q.correctAnswer;

              return (
                <div
                  key={idx}
                  className={`rounded-2xl border p-5 transition-all animate-fade-in ${
                    isSelectedCorrect
                      ? 'border-success/30 bg-success/5'
                      : isSelectedWrong
                        ? 'border-danger/30 bg-danger/5'
                        : dark
                          ? 'bg-surface-900/60 border-white/5'
                          : 'bg-white/80 border-primary-100/30'
                  }`}
                  style={{ animationDelay: `${idx * 50}ms` }}
                >
                  <div className="flex items-center justify-between gap-3 mb-4">
                    <h3 className="text-lg font-black tracking-tight flex items-center gap-2">
                      <span className="opacity-40">{idx + 1}.</span> {q.word.word}
                    </h3>
                    <button
                      onClick={() => playAudio(q.word.word)}
                      className={`p-1.5 rounded-xl border hover:scale-105 active:scale-95 transition-all ${
                        dark ? 'bg-surface-800 border-white/5' : 'bg-primary-50 border-primary-100/10 text-primary-500'
                      }`}
                      title="Nghe phát âm"
                    >
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                      </svg>
                    </button>
                  </div>

                  <div className="grid gap-2 sm:grid-cols-2">
                    {q.options.map(opt => {
                      const isChosen = mcAnswers[idx] === opt;
                      const isCorrectOpt = opt === q.correctAnswer;
                      
                      let optClass = dark
                        ? 'bg-surface-850 hover:bg-surface-800 text-surface-200 border-white/5'
                        : 'bg-white hover:bg-primary-50/20 text-surface-800 border-primary-100/25';
                        
                      if (mcSubmitted) {
                        if (isCorrectOpt) {
                          optClass = 'bg-success/15 border-success text-success font-bold';
                        } else if (isChosen) {
                          optClass = 'bg-danger/15 border-danger text-danger font-bold';
                        } else {
                          optClass = dark ? 'opacity-20 border-transparent' : 'opacity-30 border-transparent';
                        }
                      } else if (isChosen) {
                        optClass = 'bg-primary-500/10 border-primary-500 text-primary-500 font-bold';
                      }

                      return (
                        <button
                          key={opt}
                          disabled={mcSubmitted}
                          onClick={() => setMcAnswers(prev => ({ ...prev, [idx]: opt }))}
                          className={`py-3 px-4 rounded-xl border text-sm text-left transition-all ${optClass}`}
                        >
                          {opt}
                        </button>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Submit */}
          {!mcSubmitted && (
            <div className="flex justify-center pt-4">
              <button
                onClick={handleMcSubmit}
                disabled={Object.keys(mcAnswers).length < mcQuestions.length}
                className="px-8 py-3 rounded-2xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-bold shadow-xl shadow-primary-500/25 hover:shadow-primary-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Nộp bài ✨
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
