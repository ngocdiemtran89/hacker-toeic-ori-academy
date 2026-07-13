import re
import difflib

# Helper function to remove accents for matching
def to_ascii(text):
    if not text:
        return ""
    import unicodedata
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    return text.lower()

# Clean word function
def clean_word(w):
    w = w.strip()
    w = re.sub(r'^[\'"`\s\-\*]+', '', w)
    w = re.sub(r'[\'"`\s\-\*]+$', '', w)
    w = re.sub(r'^(n|v|adj|adv|phr)\s+', '', w, flags=re.IGNORECASE)
    return w.strip()

# Split Vietnamese and English from block text
def split_vietnamese_english_v3(word_name, text):
    text_clean = re.sub(r'\s+', ' ', text)
    
    # Try matching POS followed by Vietnamese meaning and English example
    pos_match = re.match(r'^(n|v|adj|adv|phr|prep|conj|aelj|adi|ad\)|ad\}|ad|aci|rn|ri|à|ñ|V|N|ADJ|ADV|ph|ph\))\b\s*', text_clean, re.IGNORECASE)
    pos = "n"
    if pos_match:
        pos = pos_match.group(1).lower()
        text_clean = text_clean[pos_match.end():].strip()
    
    # Find the boundary where English text starts
    # English sentences usually start with a capital letter or standard English words
    words = text_clean.split(' ')
    eng_start_idx = len(words)
    
    for i in range(len(words)):
        w = words[i].strip('.,()"-')
        # If word is capitalized and not at the very beginning, or is a common English word
        if i > 0 and w and w[0].isupper() and not w.lower() in ['tôi', 'anh', 'chị', 'ông', 'bà', 'nó', 'chúng']:
            eng_start_idx = i
            break
        if w.lower() in ['the', 'a', 'an', 'this', 'that', 'please', 'employees', 'only', 'all', 'if', 'when', 'for', 'we', 'you', 'they', 'our', 'he', 'she']:
            eng_start_idx = i
            break
            
    meaning_vi = ' '.join(words[:eng_start_idx]).strip()
    eng_vi = ' '.join(words[eng_start_idx:]).strip()
    
    return pos, meaning_vi, eng_vi

# Parse examples (English and Vietnamese)
def parse_examples(text):
    if not text:
        return "", "", []
        
    # Split into English and Vietnamese sentences
    # English sentences end with . ? ! followed by a Vietnamese word
    sentences = re.split(r'(?<=[.?!])\s+(?=[A-ZÀ-ỹ])', text)
    
    example_en = ""
    example_vi = ""
    toeic_notes = []
    
    if len(sentences) >= 2:
        example_en = sentences[0].strip()
        example_vi = sentences[1].strip()
        # The rest are notes
        for s in sentences[2:]:
            s_clean = s.strip()
            if s_clean:
                toeic_notes.append(s_clean)
    elif len(sentences) == 1:
        example_en = sentences[0].strip()
        
    return example_en, example_vi, toeic_notes

# Read Day 2 page content
with open('content/hackers_toeic_unit_01_18_full.md', 'r') as f:
    content = f.read()

pages = re.split(r'<!-- PDF_PAGE: \d+ -->', content)
day2_pages = pages[42:52]  # Pages 43 to 52 (index 42 to 51)

blacklist = {'day', 'pdf_page', 'trang pdf', 'tỷ lệ xuất hiện rất cao', 'tỷ lệ xuất hiện cao', 'tỷ lệ xuất hiện trung bình', 
             'từ vựng thường gặp trong part', 'từ vựng thường gặp trong', 'tuyển dụng', 'phép tắc', 'quy định', 
             'công việc', 'văn phòng', 'trang', 'pdf', 'hackers', 'vocabulary', 'daily', 'checkup'}

words_data = []

pos_map = {
    "v": "v", "V": "v", "y": "v",
    "n": "n", "N": "n", "rn": "n", "ri": "n", "à": "n", "ñ": "n", "m": "n", "nì": "n",
    "adj": "adj", "ADJ": "adj", "aelj": "adj", "adi": "adj", "ad": "adj", "aci": "adj", "ad)": "adj", "ad}": "adj",
    "adv": "adv", "ADV": "adv", "adlv": "adv", "adly": "adv",
    "phr": "phr", "ph": "phr", "ph)": "phr",
    "prep": "prep", "conj": "conj"
}

# POS regex pattern including m and nì
pos_pattern = r'(?:^|\s)\b(n|v|adj|adv|phr|prep|conj|aelj|adi|ad\)|ad\}|ad|aci|rn|ri|à|ñ|V|N|ADJ|ADV|ph|ph\)|m|nì)\b(?=\s)'

for page_idx, p in enumerate(day2_pages):
    p_num = page_idx + 43
    print(f"\n--- PROCESSING PAGE {p_num} ---")
    
    # 1. Extract vocabulary words
    words_raw = re.findall(r'[\'\"#]?([a-zA-ZÀ-ÿ\s\-\’\:\.]+)\*+', p)
    page_words = []
    for w in words_raw:
        w_clean = clean_word(w)
        if len(w_clean.split()) > 3: continue
        if len(w_clean) > 2 and w_clean not in blacklist:
            # count stars
            stars_match = re.search(re.escape(w) + r'\s*(\*+)', p)
            freq = len(stars_match.group(1)) if stars_match else 2
            page_words.append({'word': w_clean, 'frequency': freq})
            
    print("Extracted words:", [pw['word'] for pw in page_words])
    
    # 2. Extract content blocks
    pos_matches = list(re.finditer(pos_pattern, p))
    page_blocks = []
    for idx, m in enumerate(pos_matches):
        start = m.start(1)
        end = pos_matches[idx+1].start(1) if idx + 1 < len(pos_matches) else len(p)
        page_blocks.append({
            'pos': m.group(1),
            'text': p[start:end].strip()
        })
        
    print("Blocks count:", len(page_blocks))
    
    # 3. Find positions of words in text
    word_positions = []
    for pw in page_words:
        w_pat = re.compile(re.escape(pw['word']) + r'\s*\*+', re.IGNORECASE)
        w_match = w_pat.search(p)
        if w_match:
            word_positions.append({'word': pw['word'], 'pos': w_match.start()})
            
    # 4. Map blocks
    for b in page_blocks:
        pos_raw, meaning_vi_raw, eng_vi_raw = split_vietnamese_english_v3('dummy', b['text'])
        example_en_raw, example_vi_raw, toeic_notes = parse_examples(eng_vi_raw)
        
        # Semantic mapping
        best_match_score = -1
        matched_word_obj = None
        en_clean = to_ascii(example_en_raw)
        
        for wp in word_positions:
            w_clean = to_ascii(wp['word'])
            score = difflib.SequenceMatcher(None, w_clean, en_clean).ratio()
            
            # Containment bonus
            w_base = w_clean[:4]
            if w_base in en_clean or w_clean in en_clean:
                score += 2.0
                
            if score > best_match_score:
                best_match_score = score
                matched_word_obj = wp
                
        if matched_word_obj:
            w_name = matched_word_obj['word']
            pos_mapped = pos_map.get(pos_raw.lower(), "n")
            print(f"Block: {pos_raw} -> mapped to {w_name} ({pos_mapped}) | Score: {best_match_score:.2f}")
            print(f"  meaning: {meaning_vi_raw}")
            print(f"  ex_en: {example_en_raw}")
        else:
            print(f"Block: {pos_raw} -> NO MATCH!")
