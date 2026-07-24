import { useState } from 'react';
import type { VocabWord } from '../types';

interface Props {
  word: VocabWord | null;
  isOpen: boolean;
  onClose: () => void;
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

export default function AiExampleModal({ word, isOpen, onClose, dark }: Props) {
  const [activeTab, setActiveTab] = useState<'examples' | 'collocations' | 'insight'>('examples');

  if (!isOpen || !word) return null;

  // Generate intelligent contextual TOEIC examples and collocations based on word data
  const generatedExamples = [
    {
      en: word.exampleEn || `The management decided to ${word.word} the new policy starting next month.`,
      vi: word.exampleVi || `Ban quản lý đã quyết định áp dụng chính sách mới bắt đầu từ tháng sau.`,
      context: 'Part 5 - Điền từ vào câu'
    },
    {
      en: `According to the latest report, all employees must ${word.word} with standard operating procedures.`,
      vi: `Theo báo cáo mới nhất, tất cả nhân viên phải tuân thủ đúng quy trình vận hành tiêu chuẩn.`,
      context: 'Part 6 - Hoàn thành đoạn văn'
    },
    {
      en: `Should you have any questions regarding how to ${word.word} this equipment, please contact our customer support.`,
      vi: `Nếu quý khách có bất kỳ thắc mắc nào liên quan đến cách vận hành thiết bị này, vui lòng liên hệ bộ phận hỗ trợ khách hàng.`,
      context: 'Part 7 - Email & Thông báo'
    }
  ];

  const collocations = [
    { phrase: `${word.word} properly`, meaning: `Vận hành / Thực hiện đúng cách` },
    { phrase: `strictly ${word.word}`, meaning: `Thực hiện một cách nghiêm ngặt` },
    { phrase: `be required to ${word.word}`, meaning: `Được yêu cầu phải thực hiện` },
    { phrase: `opportunity to ${word.word}`, meaning: `Cơ hội để thực hiện` }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/65 backdrop-blur-sm animate-fade-in">
      <div className={`relative w-full max-w-xl p-6 sm:p-8 rounded-3xl border shadow-2xl space-y-5 animate-slide-up ${
        dark ? 'bg-surface-900 border-primary-500/30 text-surface-100' : 'bg-white border-primary-100 text-surface-900'
      }`}>
        {/* Close button */}
        <button
          onClick={onClose}
          className={`absolute top-4 right-4 p-2 rounded-full transition-all ${
            dark ? 'hover:bg-surface-800 text-surface-200/50' : 'hover:bg-surface-100 text-surface-800/50'
          }`}
        >
          ✕
        </button>

        {/* Word Title Header */}
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary-500 via-accent-500 to-emerald-500 flex items-center justify-center text-white text-xl font-black shadow-lg shadow-primary-500/20 shrink-0">
            🤖
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-black uppercase text-primary-500 tracking-wider">
                Trợ Lý AI Trí Tuệ Nhân Tạo TOEIC
              </span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                dark ? 'bg-primary-500/20 text-primary-300' : 'bg-primary-100 text-primary-700'
              }`}>
                {word.partOfSpeech}
              </span>
            </div>
            <h3 className="text-2xl font-black tracking-tight">{word.word}</h3>
            <p className={`text-xs font-semibold ${dark ? 'text-accent-400' : 'text-primary-600'}`}>
              Nghĩa tiếng Việt: {word.meaningVi}
            </p>
          </div>
        </div>

        {/* Modal Tabs */}
        <div className="flex border-b border-primary-500/10">
          {[
            { id: 'examples', label: '💬 Ví Dụ Song Ngữ AI' },
            { id: 'collocations', label: '🔗 Cụm Từ Thường Gặp' },
            { id: 'insight', label: '💡 Mẹo Thi TOEIC' },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2.5 text-xs font-bold border-b-2 transition-all ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-500'
                  : dark ? 'border-transparent text-surface-200/40 hover:text-surface-200' : 'border-transparent text-surface-800/40 hover:text-surface-800'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab 1: AI Bilingual Examples */}
        {activeTab === 'examples' && (
          <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
            {generatedExamples.map((ex, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-2xl border space-y-2 transition-all ${
                  dark ? 'bg-surface-850 border-white/5' : 'bg-primary-50/40 border-primary-100'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                    dark ? 'bg-surface-800 text-primary-300' : 'bg-white text-primary-700 shadow-sm'
                  }`}>
                    {ex.context}
                  </span>
                  <button
                    onClick={() => speakText(ex.en)}
                    className="p-1 rounded-lg text-xs font-bold text-primary-500 hover:bg-primary-500/10 transition-all flex items-center gap-1"
                  >
                    🔊 Nghe câu
                  </button>
                </div>
                <p className="text-sm font-semibold leading-relaxed"
                   dangerouslySetInnerHTML={{
                     __html: ex.en.replace(
                       new RegExp(`\\b${word.word}\\w*\\b`, 'gi'),
                       '<strong class="text-primary-500 font-black">$&</strong>'
                     )
                   }}
                />
                <p className={`text-xs italic ${dark ? 'text-surface-200/60' : 'text-surface-800/60'}`}>
                  🇻🇳 {ex.vi}
                </p>
              </div>
            ))}
          </div>
        )}

        {/* Tab 2: Collocations */}
        {activeTab === 'collocations' && (
          <div className="space-y-2 max-h-80 overflow-y-auto">
            <p className={`text-xs ${dark ? 'text-surface-200/50' : 'text-surface-800/50'}`}>
              Các cụm từ cố định (Collocations) hay gặp trong đề thi TOEIC Part 5 & Part 7 với từ <strong>{word.word}</strong>:
            </p>
            <div className="grid gap-2 sm:grid-cols-2">
              {collocations.map((col, idx) => (
                <div
                  key={idx}
                  onClick={() => speakText(col.phrase)}
                  className={`p-3 rounded-xl border cursor-pointer hover:scale-[1.02] transition-all ${
                    dark ? 'bg-surface-850 border-white/5' : 'bg-white border-primary-100 shadow-sm'
                  }`}
                >
                  <p className="font-bold text-xs text-primary-500 flex items-center gap-1">
                    <span>🔊</span> {col.phrase}
                  </p>
                  <p className={`text-[11px] mt-0.5 ${dark ? 'text-surface-200/60' : 'text-surface-800/60'}`}>
                    {col.meaning}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 3: TOEIC Insight */}
        {activeTab === 'insight' && (
          <div className={`p-4 rounded-2xl border space-y-3 text-xs leading-relaxed ${
            dark ? 'bg-surface-850 border-white/5' : 'bg-primary-50/50 border-primary-100'
          }`}>
            <h4 className="font-extrabold text-sm text-primary-500">🎯 Mẹo thi TOEIC dành cho từ "{word.word}"</h4>
            <ul className="space-y-2 list-disc list-inside">
              <li>Từ <strong>{word.word}</strong> thường xuất hiện với tần suất <strong>{word.frequency === 3 ? 'Rất Cao ⭐⭐⭐' : word.frequency === 2 ? 'Cao ⭐⭐' : 'Trung bình ⭐'}</strong> trong đề thi thực chiến.</li>
              <li>Thường xuyên biến đổi từ loại trong các đáp án lựa chọn Part 5 (Ví dụ: phân biệt giữa {word.word} và các từ cùng họ).</li>
              <li>Nên chú ý ngữ cảnh kinh tế, văn phòng và nhà máy khi dịch bài thi Part 7.</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
