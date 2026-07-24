import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { getAllUnits } from '../data';
import { playCorrectSound, playWrongSound, playFanfareSound } from '../utils/audio';
import { recordWordReview, addXp } from '../utils/srs';
import type { VocabWord } from '../types';

interface Props {
  dark: boolean;
}

export default function SpeedChallengePage({ dark }: Props) {
  const units = getAllUnits();
  const allWords: VocabWord[] = units.flatMap(u => u.words);

  const [gameState, setGameState] = useState<'start' | 'playing' | 'ended'>('start');
  const [timeLeft, setTimeLeft] = useState(60);
  const [score, setScore] = useState(0);
  const [combo, setCombo] = useState(0);
  const [maxCombo, setMaxCombo] = useState(0);
  const [currentWord, setCurrentWord] = useState<VocabWord | null>(null);
  const [options, setOptions] = useState<string[]>([]);
  const [selectedOpt, setSelectedOpt] = useState<string | null>(null);

  // High score storage
  const [highScore, setHighScore] = useState(() => {
    try {
      return Number(localStorage.getItem('ori_speed_high_score') || 0);
    } catch (e) {
      return 0;
    }
  });

  const nextQuestion = useCallback(() => {
    if (allWords.length < 4) return;
    const randomWord = allWords[Math.floor(Math.random() * allWords.length)];
    const distractors = allWords
      .filter(w => w.id !== randomWord.id)
      .sort(() => Math.random() - 0.5)
      .slice(0, 3)
      .map(w => w.meaningVi);

    const opts = [randomWord.meaningVi, ...distractors].sort(() => Math.random() - 0.5);

    setCurrentWord(randomWord);
    setOptions(opts);
    setSelectedOpt(null);
  }, [allWords]);

  const startGame = () => {
    setScore(0);
    setCombo(0);
    setMaxCombo(0);
    setTimeLeft(60);
    setGameState('playing');
    nextQuestion();
  };

  // Timer loop
  useEffect(() => {
    let interval: any = null;
    if (gameState === 'playing' && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(prev => prev - 1);
      }, 1000);
    } else if (timeLeft === 0 && gameState === 'playing') {
      clearInterval(interval);
      setGameState('ended');
      playFanfareSound();

      if (score > highScore) {
        setHighScore(score);
        try {
          localStorage.setItem('ori_speed_high_score', String(score));
        } catch (e) {}
      }
      addXp(score);
    }
    return () => clearInterval(interval);
  }, [gameState, timeLeft, score, highScore]);

  const handleSelectOption = (opt: string) => {
    if (!currentWord || selectedOpt !== null) return;
    setSelectedOpt(opt);

    const isCorrect = opt === currentWord.meaningVi;

    if (isCorrect) {
      playCorrectSound();
      const nextCombo = combo + 1;
      setCombo(nextCombo);
      setMaxCombo(prev => Math.max(prev, nextCombo));

      const pointsEarned = 10 * (nextCombo >= 5 ? 3 : nextCombo >= 3 ? 2 : 1);
      setScore(prev => prev + pointsEarned);

      recordWordReview(currentWord.id, true);
    } else {
      playWrongSound();
      setCombo(0);
      recordWordReview(currentWord.id, false);
    }

    setTimeout(() => {
      nextQuestion();
    }, 400);
  };

  return (
    <div className="pt-6 max-w-xl mx-auto space-y-6 animate-fade-in pb-16">
      {/* Header */}
      <div className="flex items-center justify-between">
        <Link to="/" className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
          dark ? 'bg-surface-900 border-white/10 text-primary-300' : 'bg-white border-primary-100 text-primary-600'
        }`}>
          ← Trang chủ
        </Link>
        <span className="text-xs font-black uppercase tracking-wider text-amber-500 flex items-center gap-1">
          ⚡ High Score: {highScore} pts
        </span>
      </div>

      {/* START SCREEN */}
      {gameState === 'start' && (
        <div className={`p-8 rounded-3xl border text-center space-y-6 animate-slide-up shadow-2xl ${
          dark ? 'bg-gradient-to-br from-surface-900 via-surface-850 to-surface-800 border-amber-500/20' : 'bg-gradient-to-br from-white via-amber-50/20 to-primary-50/30 border-amber-200 shadow-amber-500/10'
        }`}>
          <div className="text-6xl animate-bounce">⚡</div>
          <div className="space-y-2">
            <span className="px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider bg-amber-500/15 text-amber-500">
              Game Show Phản Xạ TOEIC
            </span>
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight">Thử Thách Thần Tốc 60s</h2>
            <p className={`text-sm max-w-md mx-auto leading-relaxed ${dark ? 'text-surface-200/60' : 'text-surface-800/60'}`}>
              Trả lời đúng nhiều từ vựng nhất trong 60 giây! Trả lời đúng liên tiếp để nổ **Combo x2, x3, x5** và nhân chuỗi điểm số thưởng!
            </p>
          </div>

          <button
            onClick={startGame}
            className="w-full py-4 rounded-2xl bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 text-white font-black text-lg shadow-xl shadow-amber-500/30 hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            🔥 Bắt Đầu Thử Thách 60s!
          </button>
        </div>
      )}

      {/* PLAYING SCREEN */}
      {gameState === 'playing' && currentWord && (
        <div className="space-y-5">
          {/* Top Bar: Timer, Score, Combo */}
          <div className="grid grid-cols-3 gap-3 text-center">
            <div className={`p-3 rounded-2xl border ${dark ? 'bg-surface-900 border-white/10' : 'bg-white border-primary-100'}`}>
              <p className="text-[11px] font-bold opacity-50">Thời Gian</p>
              <p className={`text-2xl font-black font-mono ${timeLeft <= 10 ? 'text-rose-500 animate-pulse' : 'text-primary-500'}`}>
                {timeLeft}s
              </p>
            </div>
            <div className={`p-3 rounded-2xl border ${dark ? 'bg-surface-900 border-white/10' : 'bg-white border-primary-100'}`}>
              <p className="text-[11px] font-bold opacity-50">Điểm Số</p>
              <p className="text-2xl font-black text-amber-500 font-mono">{score}</p>
            </div>
            <div className={`p-3 rounded-2xl border ${dark ? 'bg-surface-900 border-white/10' : 'bg-white border-primary-100'}`}>
              <p className="text-[11px] font-bold opacity-50">Chuỗi Combo</p>
              <p className="text-2xl font-black text-emerald-500 font-mono">
                {combo > 0 ? `🔥 x${combo}` : '0'}
              </p>
            </div>
          </div>

          {/* Question Card */}
          <div className={`p-8 rounded-3xl border text-center space-y-3 shadow-xl ${
            dark ? 'bg-surface-900 border-white/10' : 'bg-white border-primary-100'
          }`}>
            <span className="text-xs font-black uppercase text-primary-500">
              {currentWord.partOfSpeech} • {currentWord.pronunciation?.us}
            </span>
            <h3 className="text-4xl font-black tracking-tight text-gradient bg-gradient-to-r from-primary-500 to-accent-500">
              {currentWord.word}
            </h3>
          </div>

          {/* 4 Options Grid */}
          <div className="grid gap-3 sm:grid-cols-2">
            {options.map((opt, i) => {
              let btnClass = dark
                ? 'bg-surface-900 border-white/10 hover:bg-surface-800 text-surface-200'
                : 'bg-white border-primary-100/50 hover:bg-primary-50 text-surface-800 shadow-sm';

              if (selectedOpt !== null) {
                if (opt === currentWord.meaningVi) {
                  btnClass = 'bg-emerald-500 text-white border-emerald-500 scale-105';
                } else if (opt === selectedOpt) {
                  btnClass = 'bg-rose-500 text-white border-rose-500';
                }
              }

              return (
                <button
                  key={i}
                  disabled={selectedOpt !== null}
                  onClick={() => handleSelectOption(opt)}
                  className={`p-4 rounded-2xl border text-base font-bold text-left transition-all ${btnClass}`}
                >
                  {opt}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* ENDED SCREEN */}
      {gameState === 'ended' && (
        <div className={`p-8 rounded-3xl border text-center space-y-6 animate-slide-up shadow-2xl ${
          dark ? 'bg-surface-900 border-emerald-500/30' : 'bg-white border-emerald-200 shadow-emerald-500/10'
        }`}>
          <div className="text-6xl animate-bounce">🏆</div>
          <div className="space-y-1">
            <h3 className="text-3xl font-black tracking-tight">Hết Giờ! Hoàn Thành Thử Thách</h3>
            <p className={`text-sm ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
              Bạn đã phản xạ từ vựng xuất sắc trong 60 giây.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-3 max-w-sm mx-auto">
            <div className={`p-4 rounded-2xl border ${dark ? 'bg-surface-850 border-white/10' : 'bg-primary-50 border-primary-100'}`}>
              <p className="text-xs font-bold opacity-50">Tổng Điểm Thưởng</p>
              <p className="text-3xl font-black text-amber-500">{score} pts</p>
            </div>
            <div className={`p-4 rounded-2xl border ${dark ? 'bg-surface-850 border-white/10' : 'bg-primary-50 border-primary-100'}`}>
              <p className="text-xs font-bold opacity-50">Max Combo</p>
              <p className="text-3xl font-black text-emerald-500">🔥 {maxCombo}</p>
            </div>
          </div>

          <div className="flex gap-3 justify-center">
            <button
              onClick={startGame}
              className="px-6 py-3.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white text-sm font-black shadow-lg shadow-amber-500/25 hover:scale-105 transition-all"
            >
              🔄 Chơi Lại Lần Nữa
            </button>
            <Link
              to="/"
              className={`px-6 py-3.5 rounded-2xl text-sm font-bold border transition-all ${
                dark ? 'bg-surface-800 border-white/10 text-surface-200' : 'bg-white border-surface-200 text-surface-800'
              }`}
            >
              Về Trang Chủ
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
