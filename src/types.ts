export interface Derivative {
  word: string;
  partOfSpeech: string;
  meaningVi: string;
}

export interface VocabWord {
  id: string;
  word: string;
  partOfSpeech: string;
  pronunciation: { uk: string; us: string };
  frequency: number;
  meaningVi: string;
  exampleEn: string;
  exampleVi: string;
  derivatives: Derivative[];
  synonyms: string[];
  antonyms: string[];
  toeicNotes: string[];
  needsReview: boolean;
}

export interface QuizMatchingQuestion {
  q: string;
  a: string;
}

export interface QuizFillQuestion {
  q: string;
  options: string[];
  a: string;
}

export interface QuizSection {
  id: string;
  type: 'matching' | 'fill-in-the-blank';
  instruction: string;
  questions: QuizMatchingQuestion[] | QuizFillQuestion[];
}

export interface StoryWord {
  word: string;
  meaningVi: string;
}

export interface BilingualStory {
  title: string;
  content: string;
  words: StoryWord[];
}

export interface Unit {
  id: string;
  day: number;
  title: string;
  topic: string;
  sourcePages: number[];
  words: VocabWord[];
  story?: BilingualStory;
  quiz: QuizSection[];
}

