// Spaced Repetition System (Leitner 5-Box Algorithm) & User Gamification Storage

export interface SrsWordData {
  wordId: string;
  box: number; // 1 to 5
  lastReviewed: number;
  nextDue: number;
  correctCount: number;
  wrongCount: number;
}

export interface UserStats {
  xp: number;
  streak: number;
  lastActiveDate: string; // YYYY-MM-DD
  level: number;
  levelName: string;
}

const SRS_STORAGE_KEY = 'ori_toeic_srs_data';
const STATS_STORAGE_KEY = 'ori_toeic_user_stats';

const BOX_INTERVALS_MS = [
  0,
  1 * 24 * 60 * 60 * 1000,  // Box 1: 1 day
  2 * 24 * 60 * 60 * 1000,  // Box 2: 2 days
  4 * 24 * 60 * 60 * 1000,  // Box 3: 4 days
  7 * 24 * 60 * 60 * 1000,  // Box 4: 7 days
  14 * 24 * 60 * 60 * 1000, // Box 5: 14 days
];

const LEVEL_NAMES = [
  'Mầm Chồi TOEIC ☘️',
  'Tập Sự TOEIC 350+ 🐣',
  'Chiến Binh TOEIC 550+ ⚔️',
  'Cao Thủ TOEIC 750+ 🏆',
  'Huyền Thoại TOEIC 900+ 👑',
];

export function getSrsMap(): Record<string, SrsWordData> {
  try {
    const raw = localStorage.getItem(SRS_STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch (e) {
    return {};
  }
}

export function saveSrsMap(map: Record<string, SrsWordData>) {
  try {
    localStorage.setItem(SRS_STORAGE_KEY, JSON.stringify(map));
  } catch (e) {}
}

export function getWordSrs(wordId: string): SrsWordData {
  const map = getSrsMap();
  if (map[wordId]) return map[wordId];
  return {
    wordId,
    box: 1,
    lastReviewed: 0,
    nextDue: Date.now(),
    correctCount: 0,
    wrongCount: 0,
  };
}

export function recordWordReview(wordId: string, isCorrect: boolean): SrsWordData {
  const map = getSrsMap();
  const current = getWordSrs(wordId);
  const now = Date.now();

  let nextBox = current.box;
  if (isCorrect) {
    nextBox = Math.min(current.box + 1, 5);
  } else {
    nextBox = 1; // Reset back to box 1 on mistake
  }

  const updated: SrsWordData = {
    wordId,
    box: nextBox,
    lastReviewed: now,
    nextDue: now + BOX_INTERVALS_MS[nextBox],
    correctCount: current.correctCount + (isCorrect ? 1 : 0),
    wrongCount: current.wrongCount + (isCorrect ? 0 : 1),
  };

  map[wordId] = updated;
  saveSrsMap(map);

  // Award XP
  addXp(isCorrect ? 15 : 5);

  return updated;
}

export function getUserStats(): UserStats {
  const defaultStats: UserStats = {
    xp: 0,
    streak: 1,
    lastActiveDate: new Date().toISOString().split('T')[0],
    level: 1,
    levelName: LEVEL_NAMES[0],
  };

  try {
    const raw = localStorage.getItem(STATS_STORAGE_KEY);
    if (!raw) return defaultStats;
    const stats: UserStats = JSON.parse(raw);

    // Update streak logic
    const today = new Date().toISOString().split('T')[0];
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];

    if (stats.lastActiveDate === yesterday) {
      // Streak continues
    } else if (stats.lastActiveDate !== today) {
      // Reset streak if missed more than 1 day
      stats.streak = 1;
    }
    stats.lastActiveDate = today;
    stats.level = calculateLevel(stats.xp);
    stats.levelName = LEVEL_NAMES[Math.min(stats.level - 1, LEVEL_NAMES.length - 1)];

    return stats;
  } catch (e) {
    return defaultStats;
  }
}

export function addXp(amount: number): UserStats {
  const stats = getUserStats();
  const today = new Date().toISOString().split('T')[0];
  const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];

  if (stats.lastActiveDate === yesterday) {
    stats.streak += 1;
  } else if (stats.lastActiveDate !== today) {
    stats.streak = 1;
  }

  stats.lastActiveDate = today;
  stats.xp += amount;
  stats.level = calculateLevel(stats.xp);
  stats.levelName = LEVEL_NAMES[Math.min(stats.level - 1, LEVEL_NAMES.length - 1)];

  try {
    localStorage.setItem(STATS_STORAGE_KEY, JSON.stringify(stats));
  } catch (e) {}

  return stats;
}

function calculateLevel(xp: number): number {
  if (xp >= 1500) return 5;
  if (xp >= 700) return 4;
  if (xp >= 300) return 3;
  if (xp >= 100) return 2;
  return 1;
}
