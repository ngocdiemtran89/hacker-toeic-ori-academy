export interface Part7Vocabulary {
  word: string;
  partOfSpeech: string;
  pronunciation: string;
  meaningVi: string;
}

export interface Part7Question {
  id: string;
  questionEn: string;
  questionVi: string;
  options: {
    key: 'A' | 'B' | 'C' | 'D';
    textEn: string;
    textVi: string;
  }[];
  answerKey: 'A' | 'B' | 'C' | 'D';
  citationEn: string;
  citationVi: string;
  explanationVi: string;
}

export interface Part7PassageSet {
  id: string;
  title: string;
  type: 'Email' | 'Announcement' | 'Advertisement' | 'Customer Complaint' | 'Business Proposal';
  difficulty: 'Trung Bình (550+)' | 'Nâng Cao (750+)';
  passageEn: string;
  passageVi: string;
  keyWords: Part7Vocabulary[];
  questions: Part7Question[];
}

export const part7Passages: Part7PassageSet[] = [
  {
    id: 'p7-01',
    title: 'Thông Báo Bảo Trì Thiết Bị Nhà Máy (Factory Equipment Maintenance Notice)',
    type: 'Announcement',
    difficulty: 'Trung Bình (550+)',
    passageEn: `MEMORANDUM

TO: All Manufacturing Plant Personnel
FROM: David Miller, Operations Manager
DATE: October 14
SUBJECT: Scheduled Equipment Maintenance and Safety Protocol

Please be advised that annual maintenance on the primary assembly line machinery in Building B is scheduled for Saturday, October 18, from 8:00 A.M. to 4:00 P.M.

During this period, all automated conveyor belts and heavy industrial devices will be temporarily shut down to allow technical engineers to inspect and replace worn components. Employees who are not part of the maintenance team are strictly prohibited from entering Building B during these hours to prevent potential safety hazards.

Production operations will resume as normal at 6:00 A.M. on Monday, October 20. If your work schedule is affected by this disruption, please contact your shift supervisor immediately to arrange alternative assignments.

Thank you for your cooperation in maintaining our safety standards.`,
    passageVi: `THÔNG BÁO NỘI BỘ

GỬI ĐẾN: Toàn thể nhân viên Nhà máy Sản xuất
TỪ: David Miller, Trưởng phòng Vận hành
NGÀY: 14 tháng 10
CHỦ ĐỀ: Bảo trì thiết bị theo kế hoạch và Quy tắc an toàn

Xin lưu ý rằng công tác bảo trì định kỳ hằng năm đối với hệ thống máy móc dây chuyền lắp ráp chính tại Tòa nhà B dự kiến diễn ra vào Thứ Bảy, ngày 18 tháng 10, từ 8:00 sáng đến 4:00 chiều.

Trong khoảng thời gian này, toàn bộ băng chuyền tự động và thiết bị công nghiệp nặng sẽ tạm thời ngừng hoạt động để các kỹ sư kỹ thuật kiểm tra và thay thế các linh kiện đã bị mòn. Những nhân viên không thuộc đội bảo trì bị nghiêm cấm vào Tòa nhà B trong những giờ này nhằm ngăn ngừa các nguy cơ mất an toàn tiềm ẩn.

Hoạt động sản xuất sẽ trở lại bình thường vào lúc 6:00 sáng Thứ Hai, ngày 20 tháng 10. Nếu lịch làm việc của bạn bị ảnh hưởng bởi sự gián đoạn này, vui lòng liên hệ với người giám sát ca làm việc của bạn ngay lập tức để sắp xếp công việc thay thế.

Cảm ơn sự hợp tác của các bạn trong việc duy trì các tiêu chuẩn an toàn của chúng ta.`,
    keyWords: [
      { word: 'maintenance', partOfSpeech: 'n', pronunciation: '/ˈmeɪntənəns/', meaningVi: 'sự bảo trì, bảo dưỡng' },
      { word: 'assembly line', partOfSpeech: 'n', pronunciation: '/əˈsembli laɪn/', meaningVi: 'dây chuyền lắp ráp' },
      { word: 'temporarily', partOfSpeech: 'adv', pronunciation: '/ˈtemprərəli/', meaningVi: 'tạm thời' },
      { word: 'inspect', partOfSpeech: 'v', pronunciation: '/ɪnˈspekt/', meaningVi: 'kiểm tra, thanh tra' },
      { word: 'prohibited', partOfSpeech: 'adj', pronunciation: '/prəˈhɪbɪtɪd/', meaningVi: 'bị cấm' },
      { word: 'hazard', partOfSpeech: 'n', pronunciation: '/ˈhæzəd/', meaningVi: 'mối nguy hiểm, rủi ro' },
      { word: 'resume', partOfSpeech: 'v', pronunciation: '/rɪˈzjuːm/', meaningVi: 'trở lại, tiếp tục' },
    ],
    questions: [
      {
        id: 'q1',
        questionEn: 'What is the main purpose of the memorandum?',
        questionVi: 'Mục đích chính của thông báo nội bộ này là gì?',
        options: [
          { key: 'A', textEn: 'To announce the hiring of new technical engineers', textVi: 'Để thông báo việc tuyển dụng kỹ sư kỹ thuật mới' },
          { key: 'B', textEn: 'To inform staff about upcoming machinery maintenance', textVi: 'Để thông báo cho nhân viên về việc bảo trì máy móc sắp tới' },
          { key: 'C', textEn: 'To change the operating hours of Building B permanently', textVi: 'Để thay đổi vĩnh viễn giờ hoạt động của Tòa nhà B' },
          { key: 'D', textEn: 'To promote David Miller to Operations Manager', textVi: 'Để thăng chức cho David Miller lên vị trí Trưởng phòng Vận hành' },
        ],
        answerKey: 'B',
        citationEn: 'Please be advised that annual maintenance on the primary assembly line machinery in Building B is scheduled for Saturday, October 18...',
        citationVi: 'Xin lưu ý rằng công tác bảo trì định kỳ hằng năm đối với hệ thống máy móc dây chuyền lắp ráp chính tại Tòa nhà B dự kiến diễn ra vào Thứ Bảy, ngày 18 tháng 10...',
        explanationVi: 'Đoạn mở đầu nêu rõ mục đích thông báo về đợt bảo trì máy móc định kỳ (annual maintenance) vào Thứ Bảy ngày 18/10. Do đó đáp án B là hoàn toàn chính xác.',
      },
      {
        id: 'q2',
        questionEn: 'Who is prohibited from entering Building B on October 18?',
        questionVi: 'Ai bị cấm vào Tòa nhà B vào ngày 18 tháng 10?',
        options: [
          { key: 'A', textEn: 'Technical engineers', textVi: 'Các kỹ sư kỹ thuật' },
          { key: 'B', textEn: 'Shift supervisors', textVi: 'Các người giám sát ca' },
          { key: 'C', textEn: 'Workers not involved in maintenance', textVi: 'Công nhân không tham gia vào việc bảo trì' },
          { key: 'D', textEn: 'Building safety inspectors', textVi: 'Các thanh tra an toàn tòa nhà' },
        ],
        answerKey: 'C',
        citationEn: 'Employees who are not part of the maintenance team are strictly prohibited from entering Building B during these hours...',
        citationVi: 'Những nhân viên không thuộc đội bảo trì bị nghiêm cấm vào Tòa nhà B trong những giờ này...',
        explanationVi: 'Đoạn 2 nêu rõ nhân viên không thuộc đội bảo trì (not part of the maintenance team) bị nghiêm cấm vào Tòa nhà B. Chọn C.',
      },
      {
        id: 'q3',
        questionEn: 'When will normal production operations resume?',
        questionVi: 'Khi nào hoạt động sản xuất bình thường sẽ trở lại?',
        options: [
          { key: 'A', textEn: 'On Friday, October 17 at 8:00 A.M.', textVi: 'Vào Thứ Sáu, 17/10 lúc 8:00 sáng' },
          { key: 'B', textEn: 'On Saturday, October 18 at 4:00 P.M.', textVi: 'Vào Thứ Bảy, 18/10 lúc 4:00 chiều' },
          { key: 'C', textEn: 'On Sunday, October 19 at midnight', textVi: 'Vào Chủ Nhật, 19/10 lúc giữa đêm' },
          { key: 'D', textEn: 'On Monday, October 20 at 6:00 A.M.', textVi: 'Vào Thứ Hai, 20/10 lúc 6:00 sáng' },
        ],
        answerKey: 'D',
        citationEn: 'Production operations will resume as normal at 6:00 A.M. on Monday, October 20.',
        citationVi: 'Hoạt động sản xuất sẽ trở lại bình thường vào lúc 6:00 sáng Thứ Hai, ngày 20 tháng 10.',
        explanationVi: 'Đoạn 3 khẳng định rõ ràng hoạt động sẽ trở lại bình thường vào lúc 6:00 A.M. ngày Thứ Hai, 20/10. Chọn D.',
      }
    ]
  },
  {
    id: 'p7-02',
    title: 'Email Khiếu Nại Dịch Vụ Khách Sạn & Bồi Thường (Hotel Service Complaint & Refund Request)',
    type: 'Customer Complaint',
    difficulty: 'Nâng Cao (750+)',
    passageEn: `EMAIL

FROM: Sarah Jenkins <s.jenkins@email.com>
TO: Customer Relations <service@grandviewhotel.com>
DATE: November 3
SUBJECT: Complaint Regarding Reservation #GV-8842

Dear Customer Relations Team,

I am writing to express my extreme disappointment with the service I received during my stay at the Grandview Hotel from October 30 to November 2. 

Upon my arrival, I was informed that the deluxe suite I had reserved two months in advance was unavailable due to a plumbing malfunction. As a result, I was downgraded to a standard room on the second floor. Although your receptionist promised that a complimentary breakfast voucher would be issued as compensation, I never received it despite asking twice at the front desk.

Furthermore, there was a prolonged power outage on Friday evening that lasted for over four hours, leaving the room without air conditioning or hot water. 

Given these circumstances, I request a partial refund of 30% of my total bill, as well as confirmation that the unfulfilled voucher promises will be addressed. I expect a prompt reply regarding this matter before I submit a formal review online.

Sincerely,
Sarah Jenkins`,
    passageVi: `THƯ ĐIỆN TỬ

TỪ: Sarah Jenkins <s.jenkins@email.com>
GỬI ĐẾN: Bộ phận Chăm sóc Khách hàng <service@grandviewhotel.com>
NGÀY: 3 tháng 11
CHỦ ĐỀ: Khiếu nại liên quan đến Mã đặt phòng #GV-8842

Kính gửi Đội ngũ Chăm sóc Khách hàng,

Tôi viết thư này để bày tỏ sự thất vọng sâu sắc đối với dịch vụ mà tôi nhận được trong thời gian lưu trú tại Khách sạn Grandview từ ngày 30 tháng 10 đến ngày 2 tháng 11.

Khi tôi đến nơi, tôi được thông báo rằng phòng hạng sang (deluxe suite) mà tôi đã đặt trước hai tháng không có sẵn do sự cố đường ống nước. Kết quả là tôi bị hạ hạng xuống phòng tiêu chuẩn ở tầng hai. Mặc dù nhân viên lễ tân của bạn đã hứa rằng một phiếu ăn sáng miễn phí sẽ được cấp để bồi thường, tôi chưa bao giờ nhận được nó mặc dù đã hỏi hai lần tại quầy lễ tân.

Hơn nữa, đã xảy ra một sự cố mất điện kéo dài vào tối Thứ Sáu kéo dài hơn bốn giờ, khiến phòng không có điều hòa hay nước nóng.

Trong những hoàn cảnh này, tôi yêu cầu hoàn lại một phần 30% tổng hóa đơn của tôi, cũng như xác nhận rằng những lời hứa về phiếu voucher chưa thực hiện sẽ được xử lý. Tôi mong đợi câu trả lời sớm về vấn đề này trước khi tôi gửi đánh giá chính thức trên mạng.

Trân trọng,
Sarah Jenkins`,
    keyWords: [
      { word: 'disappointment', partOfSpeech: 'n', pronunciation: '/ˌdɪsəˈpɔɪntmənt/', meaningVi: 'sự thất vọng' },
      { word: 'reserve', partOfSpeech: 'v', pronunciation: '/rɪˈzɜːv/', meaningVi: 'đặt trước, giữ chỗ' },
      { word: 'downgrade', partOfSpeech: 'v', pronunciation: '/ˌdaʊnˈɡreɪd/', meaningVi: 'hạ hạng, giảm cấp' },
      { word: 'complimentary', partOfSpeech: 'adj', pronunciation: '/ˌkɒmplɪˈmentri/', meaningVi: 'miễn phí, biếu tặng' },
      { word: 'compensation', partOfSpeech: 'n', pronunciation: '/ˌkɒmpenˈseɪʃn/', meaningVi: 'sự bồi thường' },
      { word: 'outage', partOfSpeech: 'n', pronunciation: '/ˈaʊtɪdʒ/', meaningVi: 'sự mất điện, sự gián đoạn' },
      { word: 'refund', partOfSpeech: 'n', pronunciation: '/ˈriːfʌnd/', meaningVi: 'sự hoàn tiền' },
    ],
    questions: [
      {
        id: 'q1',
        questionEn: 'Why was Ms. Jenkins given a standard room instead of a deluxe suite?',
        questionVi: 'Tại sao cô Jenkins lại bị đưa phòng tiêu chuẩn thay vì phòng hạng sang?',
        options: [
          { key: 'A', textEn: 'She booked her reservation too late', textVi: 'Cô ấy đặt phòng quá muộn' },
          { key: 'B', textEn: 'The original room had a plumbing problem', textVi: 'Phòng ban đầu bị sự cố đường ống nước' },
          { key: 'C', textEn: 'She requested a room on the second floor', textVi: 'Cô ấy yêu cầu một phòng ở tầng hai' },
          { key: 'D', textEn: 'The hotel was hosting a large conference', textVi: 'Khách sạn đang tổ chức một hội nghị lớn' },
        ],
        answerKey: 'B',
        citationEn: '...the deluxe suite I had reserved two months in advance was unavailable due to a plumbing malfunction.',
        citationVi: '...phòng hạng sang mà tôi đã đặt trước hai tháng không có sẵn do sự cố đường ống nước.',
        explanationVi: 'Trích dẫn đoạn 2 nêu rõ lý do phòng hạng sang không sẵn có là do "plumbing malfunction" (sự cố hỏng đường ống nước). Chọn B.',
      },
      {
        id: 'q2',
        questionEn: 'What did the receptionist fail to provide to Ms. Jenkins?',
        questionVi: 'Lễ tân đã không cung cấp được thứ gì cho cô Jenkins?',
        options: [
          { key: 'A', textEn: 'A free breakfast voucher', textVi: 'Một phiếu ăn sáng miễn phí' },
          { key: 'B', textEn: 'Her room key card', textVi: 'Thẻ khóa phòng của cô ấy' },
          { key: 'C', textEn: 'Directions to the second floor', textVi: 'Chỉ đường lên tầng hai' },
          { key: 'D', textEn: 'A receipt for her payment', textVi: 'Hóa đơn thanh toán của cô ấy' },
        ],
        answerKey: 'A',
        citationEn: '...receptionist promised that a complimentary breakfast voucher would be issued as compensation, I never received it...',
        citationVi: '...nhân viên lễ tân đã hứa rằng một phiếu ăn sáng miễn phí sẽ được cấp để bồi thường, tôi chưa bao giờ nhận được nó...',
        explanationVi: 'Đoạn 2 nêu rõ nhân viên lễ tân hứa đưa "complimentary breakfast voucher" nhưng cô chưa từng nhận được. Chọn A.',
      },
      {
        id: 'q3',
        questionEn: 'What action is Ms. Jenkins demanding from the hotel?',
        questionVi: 'Cô Jenkins đang yêu cầu hành động gì từ phía khách sạn?',
        options: [
          { key: 'A', textEn: 'A free stay for her next vacation', textVi: 'Một kỳ nghỉ miễn phí cho đợt tiếp theo' },
          { key: 'B', textEn: 'A 30% partial refund of her payment', textVi: 'Hoàn tiền một phần 30% khoản thanh toán' },
          { key: 'C', textEn: 'An apology letter from the general manager', textVi: 'Một thư xin lỗi từ tổng giám đốc' },
          { key: 'D', textEn: 'An immediate upgrade to a suite', textVi: 'Nâng cấp ngay lập tức lên phòng suite' },
        ],
        answerKey: 'B',
        citationEn: 'I request a partial refund of 30% of my total bill...',
        citationVi: 'Tôi yêu cầu hoàn lại một phần 30% tổng hóa đơn của tôi...',
        explanationVi: 'Đoạn 4 ghi rõ: "I request a partial refund of 30% of my total bill" (Yêu cầu hoàn lại 30% hóa đơn). Chọn B.',
      }
    ]
  }
];
