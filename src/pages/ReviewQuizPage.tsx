import { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { getAllUnits } from '../data';
import type { VocabWord } from '../types';

interface Props {
  dark: boolean;
}

interface Question {
  word: VocabWord;
  options: string[];
  correctAnswer: string;
}

export default function ReviewQuizPage({ dark }: Props) {
  // Flatten all words from all units
  const allWords = useMemo(() => {
    return getAllUnits().flatMap(u => u.words);
  }, []);

  // Spaced repetition queues
  const [incorrectQueue, setIncorrectQueue] = useState<VocabWord[]>([]);
  const [currentQuestions, setCurrentQuestions] = useState<Question[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  
  // Interactive UI states
  const [selectedOpt, setSelectedOpt] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [score, setScore] = useState(0);
  const [roundCompleted, setRoundCompleted] = useState(false);
  const [wrongInRound, setWrongInRound] = useState<VocabWord[]>([]);
  const [roundNum, setRoundNum] = useState(1);

  // Generate a quiz round of 10 questions
  const generateRound = (queue: VocabWord[]) => {
    if (allWords.length === 0) return;

    // 1. Take words from incorrect queue first
    const selectedWords: VocabWord[] = [...queue.slice(0, 10)];

    // 2. Fill the rest of the 10 slots with random words from total pool
    const needed = 10 - selectedWords.length;
    if (needed > 0) {
      // Filter out words that are already in selectedWords
      const available = allWords.filter(w => !selectedWords.some(sw => sw.id === w.id));
      // Shuffle available words and take needed
      const shuffledAvailable = [...available].sort(() => 0.5 - Math.random());
      selectedWords.push(...shuffledAvailable.slice(0, needed));
    }

    // 3. Construct Question objects
    const newQuestions = selectedWords.map(word => {
      const correctAnswer = word.meaningVi.split(',')[0].split(';')[0].trim();
      
      // Get other random meanings for distractors
      const distractors = allWords
        .filter(w => w.id !== word.id)
        .map(w => w.meaningVi.split(',')[0].split(';')[0].trim())
        .filter((value, index, self) => self.indexOf(value) === index && value !== correctAnswer);

      // Take 3 random distractors
      const shuffledDistractors = distractors.sort(() => 0.5 - Math.random()).slice(0, 3);
      const options = [correctAnswer, ...shuffledDistractors].sort(() => 0.5 - Math.random());

      return {
        word,
        options,
        correctAnswer
      };
    });

    setCurrentQuestions(newQuestions);
    setCurrentIdx(0);
    setSelectedOpt(null);
    setIsCorrect(null);
    setScore(0);
    setRoundCompleted(false);
    setWrongInRound([]);
  };

  // Initialize first round
  useEffect(() => {
    generateRound([]);
  }, [allWords]);

  const activeQuestion = currentQuestions[currentIdx];

  // TTS Voice support
  const playAudio = (wordText: string) => {
    const utterance = new SpeechSynthesisUtterance(wordText);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  };

  const handleOptionClick = (option: string) => {
    if (selectedOpt !== null || !activeQuestion) return;

    setSelectedOpt(option);
    const correct = option === activeQuestion.correctAnswer;
    setIsCorrect(correct);

    if (correct) {
      setScore(s => s + 1);
      // If the word was in the incorrect queue, remove it (spaced repetition graduation)
      setIncorrectQueue(q => q.filter(w => w.id !== activeQuestion.word.id));
    } else {
      setWrongInRound(w => [...w, activeQuestion.word]);
      // If not already in incorrectQueue, add it so it is repeatedly injected in next rounds
      setIncorrectQueue(q => {
        if (q.some(w => w.id === activeQuestion.word.id)) return q;
        return [...q, activeQuestion.word];
      });
    }

    // Speak the word automatically
    playAudio(activeQuestion.word.word);
  };

  const handleNext = () => {
    if (currentIdx < 9) {
      setCurrentIdx(i => i + 1);
      setSelectedOpt(null);
      setIsCorrect(null);
    } else {
      setRoundCompleted(true);
    }
  };

  const handleStartNextRound = () => {
    setRoundNum(r => r + 1);
    generateRound(incorrectQueue);
  };

  if (currentQuestions.length === 0) {
    return (
      <div className="pt-20 text-center">
        <p className="text-xl font-bold">Đang tải câu hỏi...</p>
      </div>
    );
  }

  return (
    <div className="pt-6 max-w-xl mx-auto space-y-6">
      {/* Header */}
      <div className="animate-fade-in flex items-center justify-between">
        <div>
          <Link to="/" className={`text-xs font-medium hover:underline ${dark ? 'text-primary-300/50' : 'text-primary-500/50'}`}>
            ← Về trang chủ
          </Link>
          <h2 className="text-2xl font-black tracking-tight mt-1">Trắc Nghiệm Ôn Tập</h2>
        </div>
        <div className={`px-3 py-1.5 rounded-xl text-xs font-bold border ${
          dark ? 'bg-surface-900 border-white/5 text-surface-300' : 'bg-white border-primary-100/25 text-surface-700 shadow-sm'
        }`}>
          Vòng {roundNum} • Sai trong hàng đợi: {incorrectQueue.length}
        </div>
      </div>

      {!roundCompleted ? (
        <div className="space-y-6">
          {/* Progress bar */}
          <div className="w-full bg-black/10 dark:bg-white/5 h-2 rounded-full overflow-hidden">
            <div
              className="bg-gradient-to-r from-primary-500 to-accent-500 h-full transition-all duration-300"
              style={{ width: `${(currentIdx / 10) * 100}%` }}
            />
          </div>

          {/* Question Card */}
          {activeQuestion && (
            <div className={`p-8 rounded-3xl border text-center transition-all animate-scale-up ${
              dark
                ? 'bg-surface-900/40 border-white/5'
                : 'bg-white/80 border-primary-100/20 shadow-xl shadow-primary-500/5'
            }`}>
              <span className={`text-xs font-bold uppercase tracking-wider ${dark ? 'text-primary-400' : 'text-primary-600'}`}>
                Câu hỏi {currentIdx + 1}/10
              </span>
              <h3 className="text-4xl font-black tracking-tight mt-3 mb-2 select-all flex items-center justify-center gap-3">
                {activeQuestion.word.word}
                <button
                  onClick={() => playAudio(activeQuestion.word.word)}
                  className={`p-2 rounded-full border hover:scale-105 active:scale-95 transition-all ${
                    dark ? 'bg-surface-800 border-white/5 hover:bg-surface-700' : 'bg-primary-50 border-primary-100/20 hover:bg-primary-100 text-primary-600'
                  }`}
                  title="Nghe phát âm"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                  </svg>
                </button>
              </h3>
              <p className={`text-xs font-bold uppercase tracking-wider mb-6 opacity-50`}>
                {activeQuestion.word.partOfSpeech} • {activeQuestion.word.pronunciation.us || activeQuestion.word.pronunciation.uk}
              </p>

              {/* Multiple Choice Options */}
              <div className="grid gap-3">
                {activeQuestion.options.map((opt, oIdx) => {
                  const isSelected = selectedOpt === opt;
                  const isCorrectAnswer = opt === activeQuestion.correctAnswer;
                  
                  let btnStyle = dark 
                    ? 'bg-surface-800/60 border-white/5 hover:bg-surface-800 text-surface-200' 
                    : 'bg-white border-primary-100/25 hover:shadow-lg shadow-sm text-surface-800';
                  
                  if (selectedOpt !== null) {
                    if (isCorrectAnswer) {
                      btnStyle = 'bg-success/15 border-success text-success font-bold scale-[1.01]';
                    } else if (isSelected) {
                      btnStyle = 'bg-danger/15 border-danger text-danger font-bold animate-shake';
                    } else {
                      btnStyle = dark ? 'bg-surface-800/20 border-transparent text-surface-200/30' : 'bg-white/20 border-transparent text-surface-800/30';
                    }
                  }

                  return (
                    <button
                      key={oIdx}
                      onClick={() => handleOptionClick(opt)}
                      disabled={selectedOpt !== null}
                      className={`w-full py-4 px-6 rounded-2xl border text-sm font-semibold text-center transition-all ${btnStyle}`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>

              {/* Success / Error Message Banner */}
              {selectedOpt !== null && (
                <div className={`mt-6 p-4 rounded-2xl border flex items-center justify-center gap-2 animate-fade-in ${
                  isCorrect 
                    ? 'bg-success/10 border-success/20 text-success' 
                    : 'bg-danger/10 border-danger/20 text-danger'
                }`}>
                  <span className="text-lg">{isCorrect ? '✓' : '✗'}</span>
                  <span className="text-xs font-bold uppercase tracking-wider">
                    {isCorrect ? 'Tuyệt vời!' : `Sai rồi! Đáp án đúng: ${activeQuestion.correctAnswer}`}
                  </span>
                </div>
              )}
            </div>
          )}

          {/* Continue button */}
          {selectedOpt !== null && (
            <div className="flex justify-end animate-fade-in">
              <button
                onClick={handleNext}
                className="px-6 py-3 rounded-xl bg-gradient-to-r from-primary-500 to-primary-600 text-white text-sm font-semibold shadow-lg shadow-primary-500/25 hover:scale-[1.02] active:scale-[0.98] transition-all"
              >
                {currentIdx < 9 ? 'Tiếp tục →' : 'Xem kết quả 🏁'}
              </button>
            </div>
          )}
        </div>
      ) : (
        /* Round completed / Leitner summary card */
        <div className={`p-8 rounded-3xl border text-center transition-all animate-scale-up ${
          dark
            ? 'bg-surface-900/40 border-white/5'
            : 'bg-white/80 border-primary-100/20 shadow-xl shadow-primary-500/5'
        }`}>
          <p className="text-5xl mb-3">{score === 10 ? '👑' : score >= 7 ? '🌟' : '💪'}</p>
          <h3 className="text-2xl font-black tracking-tight">Kết quả Vòng {roundNum}</h3>
          
          <div className="my-6 grid grid-cols-2 gap-4">
            <div className={`p-4 rounded-2xl ${dark ? 'bg-success/5 border border-success/10' : 'bg-success/5 border border-success/15'}`}>
              <p className="text-2xl font-black text-success">{score}</p>
              <p className={`text-xs mt-0.5 font-bold uppercase tracking-wider ${dark ? 'text-surface-300' : 'text-surface-600'}`}>Trả lời đúng</p>
            </div>
            <div className={`p-4 rounded-2xl ${dark ? 'bg-danger/5 border border-danger/10' : 'bg-danger/5 border border-danger/15'}`}>
              <p className="text-2xl font-black text-danger">{10 - score}</p>
              <p className={`text-xs mt-0.5 font-bold uppercase tracking-wider ${dark ? 'text-surface-300' : 'text-surface-600'}`}>Trả lời sai</p>
            </div>
          </div>

          {incorrectQueue.length > 0 ? (
            <div className="space-y-4 text-left">
              <div className={`p-4 rounded-2xl border ${
                dark ? 'bg-surface-950/60 border-white/5' : 'bg-primary-50/50 border-primary-100/20'
              }`}>
                <h4 className="text-xs font-bold uppercase tracking-wider text-primary-500 mb-2">
                  Danh sách hàng đợi ôn tập ({incorrectQueue.length} từ)
                </h4>
                <p className={`text-xs leading-relaxed ${dark ? 'text-surface-300' : 'text-surface-600'}`}>
                  Các từ bạn trả lời sai sẽ tiếp tục được nhét liên tục vào các vòng quiz tiếp theo cho đến khi bạn trả lời đúng.
                </p>
              </div>

              {wrongInRound.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-danger/80">Từ vừa trả lời sai vòng này:</h4>
                  <div className="flex flex-wrap gap-2">
                    {wrongInRound.map(w => (
                      <span
                        key={w.id}
                        className={`px-3 py-1 rounded-xl text-xs font-bold border ${
                          dark ? 'bg-danger/10 border-danger/20 text-danger' : 'bg-danger/5 border-danger/15 text-danger'
                        }`}
                      >
                        {w.word}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <button
                onClick={handleStartNextRound}
                className="w-full mt-6 py-4 rounded-2xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-bold shadow-xl shadow-primary-500/25 hover:scale-[1.01] active:scale-[0.99] transition-all"
              >
                Bắt đầu vòng ôn tập tiếp theo ⚡
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="p-6 rounded-2xl bg-success/5 border border-success/10 text-success">
                <p className="font-bold">✨ Hoàn hảo! Hàng đợi ôn tập trống trơn! ✨</p>
                <p className="text-xs mt-1 leading-relaxed text-success/80">
                  Bạn đã xuất sắc trả lời đúng tất cả các từ trong danh sách ôn tập. Hãy tiếp tục chơi các vòng tiếp theo với các từ ngẫu nhiên mới!
                </p>
              </div>
              
              <button
                onClick={handleStartNextRound}
                className="w-full mt-6 py-4 rounded-2xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-bold shadow-xl shadow-primary-500/25 hover:scale-[1.01] active:scale-[0.99] transition-all"
              >
                Tiếp tục chơi vòng mới 🎉
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
