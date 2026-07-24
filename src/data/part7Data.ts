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
    "id": "p7-01",
    "title": "Bai 01: Bao Tri Thiet Bi Nha May (Factory Equipment Maintenance Notice)",
    "type": "Announcement",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Apex Manufacturing Plant\nDATE: October 01\nSUBJECT: Factory Equipment Maintenance Notice\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding factory equipment maintenance notice. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving assembly line machinery.\n2. Important compliance procedure concerning technician inspection.\n3. Timely execution regarding safety hazard prevention.\n\nIf you have any questions or require further clarification, please contact our support desk at support@apexmanufacturingplant.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Apex Manufacturing Plant\nNGAY: Ngay 01 thang 10\nCHU DE: Bao Tri Thiet Bi Nha May\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den bao tri thiet bi nha may. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den assembly line machinery.\n2. Quy trinh tuan thu quan trong lien quan den technician inspection.\n3. Viec thuc thi dung han lien quan den safety hazard prevention.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@apexmanufacturingplant.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "assembly",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh assembly line machinery"
      },
      {
        "word": "technician",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh technician inspection"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-01-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Factory Equipment Maintenance Notice",
            "textVi": "Cap nhat lien quan den Bao Tri Thiet Bi Nha May"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Factory Equipment Maintenance Notice",
        "citationVi": "CHU DE: Bao Tri Thiet Bi Nha May",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Bao Tri Thiet Bi Nha May. Chon A."
      },
      {
        "id": "p7-01-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-01-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-02",
    "title": "Bai 02: Khieu Nai Dich Vu Khach San (Hotel Service Complaint & Refund Request)",
    "type": "Customer Complaint",
    "difficulty": "Nâng Cao (750+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Hotel Grandview\nDATE: October 02\nSUBJECT: Hotel Service Complaint & Refund Request\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding hotel service complaint & refund request. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving service dissatisfaction.\n2. Important compliance procedure concerning complimentary breakfast voucher.\n3. Timely execution regarding plumbing malfunction.\n\nIf you have any questions or require further clarification, please contact our support desk at support@hotelgrandview.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Hotel Grandview\nNGAY: Ngay 02 thang 10\nCHU DE: Khieu Nai Dich Vu Khach San\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den khieu nai dich vu khach san. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den service dissatisfaction.\n2. Quy trinh tuan thu quan trong lien quan den complimentary breakfast voucher.\n3. Viec thuc thi dung han lien quan den plumbing malfunction.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@hotelgrandview.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "service",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh service dissatisfaction"
      },
      {
        "word": "complimentary",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh complimentary breakfast voucher"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-02-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Hotel Service Complaint & Refund Request",
            "textVi": "Cap nhat lien quan den Khieu Nai Dich Vu Khach San"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Hotel Service Complaint & Refund Request",
        "citationVi": "CHU DE: Khieu Nai Dich Vu Khach San",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Khieu Nai Dich Vu Khach San. Chon A."
      },
      {
        "id": "p7-02-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-02-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-03",
    "title": "Bai 03: Thong Bao Thay Doi Lich Bay Hang Khong (Flight Schedule Change Notification)",
    "type": "Email",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Skyways Airlines\nDATE: October 03\nSUBJECT: Flight Schedule Change Notification\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding flight schedule change notification. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving flight SK-402.\n2. Important compliance procedure concerning runway maintenance.\n3. Timely execution regarding departure time pushed back.\n\nIf you have any questions or require further clarification, please contact our support desk at support@skywaysairlines.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Skyways Airlines\nNGAY: Ngay 03 thang 10\nCHU DE: Thong Bao Thay Doi Lich Bay Hang Khong\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den thong bao thay doi lich bay hang khong. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den flight SK-402.\n2. Quy trinh tuan thu quan trong lien quan den runway maintenance.\n3. Viec thuc thi dung han lien quan den departure time pushed back.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@skywaysairlines.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "flight",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh flight SK-402"
      },
      {
        "word": "runway",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh runway maintenance"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-03-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Flight Schedule Change Notification",
            "textVi": "Cap nhat lien quan den Thong Bao Thay Doi Lich Bay Hang Khong"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Flight Schedule Change Notification",
        "citationVi": "CHU DE: Thong Bao Thay Doi Lich Bay Hang Khong",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Thong Bao Thay Doi Lich Bay Hang Khong. Chon A."
      },
      {
        "id": "p7-03-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-03-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-04",
    "title": "Bai 04: Hoi Thao Dao Tao Ky Nang Lanh Dao (Executive Leadership Workshop)",
    "type": "Announcement",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: APEX Institute\nDATE: October 04\nSUBJECT: Executive Leadership Workshop\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding executive leadership workshop. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving leadership training.\n2. Important compliance procedure concerning Early Bird 15% discount.\n3. Timely execution regarding City Center Hotel.\n\nIf you have any questions or require further clarification, please contact our support desk at support@apexinstitute.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: APEX Institute\nNGAY: Ngay 04 thang 10\nCHU DE: Hoi Thao Dao Tao Ky Nang Lanh Dao\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den hoi thao dao tao ky nang lanh dao. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den leadership training.\n2. Quy trinh tuan thu quan trong lien quan den Early Bird 15% discount.\n3. Viec thuc thi dung han lien quan den City Center Hotel.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@apexinstitute.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "leadership",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh leadership training"
      },
      {
        "word": "Early",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh Early Bird 15% discount"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-04-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Executive Leadership Workshop",
            "textVi": "Cap nhat lien quan den Hoi Thao Dao Tao Ky Nang Lanh Dao"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Executive Leadership Workshop",
        "citationVi": "CHU DE: Hoi Thao Dao Tao Ky Nang Lanh Dao",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Hoi Thao Dao Tao Ky Nang Lanh Dao. Chon A."
      },
      {
        "id": "p7-04-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-04-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-05",
    "title": "Bai 05: Thong Bao Di Doi Tru So Van Phong (Office Relocation Memorandum)",
    "type": "Announcement",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Pinnacle Tower\nDATE: October 05\nSUBJECT: Office Relocation Memorandum\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding office relocation memorandum. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving corporate headquarters.\n2. Important compliance procedure concerning electronic keycards.\n3. Timely execution regarding September 12-13 move.\n\nIf you have any questions or require further clarification, please contact our support desk at support@pinnacletower.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Pinnacle Tower\nNGAY: Ngay 05 thang 10\nCHU DE: Thong Bao Di Doi Tru So Van Phong\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den thong bao di doi tru so van phong. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den corporate headquarters.\n2. Quy trinh tuan thu quan trong lien quan den electronic keycards.\n3. Viec thuc thi dung han lien quan den September 12-13 move.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@pinnacletower.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "corporate",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh corporate headquarters"
      },
      {
        "word": "electronic",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh electronic keycards"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-05-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Office Relocation Memorandum",
            "textVi": "Cap nhat lien quan den Thong Bao Di Doi Tru So Van Phong"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Office Relocation Memorandum",
        "citationVi": "CHU DE: Thong Bao Di Doi Tru So Van Phong",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Thong Bao Di Doi Tru So Van Phong. Chon A."
      },
      {
        "id": "p7-05-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-05-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-06",
    "title": "Bai 06: Quang Cao Tai Nghe Chong On Cao Cap (Noise-Canceling Headphones Ad)",
    "type": "Advertisement",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: AudioPro SoundShield X7\nDATE: October 06\nSUBJECT: Noise-Canceling Headphones Ad\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding noise-canceling headphones ad. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving 40-hour battery life.\n2. Important compliance procedure concerning free hardshell case.\n3. Timely execution regarding 98% noise reduction.\n\nIf you have any questions or require further clarification, please contact our support desk at support@audioprosoundshieldx7.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: AudioPro SoundShield X7\nNGAY: Ngay 06 thang 10\nCHU DE: Quang Cao Tai Nghe Chong On Cao Cap\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den quang cao tai nghe chong on cao cap. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den 40-hour battery life.\n2. Quy trinh tuan thu quan trong lien quan den free hardshell case.\n3. Viec thuc thi dung han lien quan den 98% noise reduction.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@audioprosoundshieldx7.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "40-hour",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh 40-hour battery life"
      },
      {
        "word": "free",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh free hardshell case"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-06-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Noise-Canceling Headphones Ad",
            "textVi": "Cap nhat lien quan den Quang Cao Tai Nghe Chong On Cao Cap"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Noise-Canceling Headphones Ad",
        "citationVi": "CHU DE: Quang Cao Tai Nghe Chong On Cao Cap",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Quang Cao Tai Nghe Chong On Cao Cap. Chon A."
      },
      {
        "id": "p7-06-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-06-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-07",
    "title": "Bai 07: Nang Cap He Thong CNTT & Bao Tri May Chu (IT Server Maintenance Notice)",
    "type": "Email",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: TechCorp IT Department\nDATE: October 07\nSUBJECT: IT Server Maintenance Notice\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding it server maintenance notice. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving cloud migration.\n2. Important compliance procedure concerning weekend maintenance window.\n3. Timely execution regarding internal portal offline.\n\nIf you have any questions or require further clarification, please contact our support desk at support@techcorpitdepartment.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: TechCorp IT Department\nNGAY: Ngay 07 thang 10\nCHU DE: Nang Cap He Thong CNTT & Bao Tri May Chu\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den nang cap he thong cntt & bao tri may chu. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den cloud migration.\n2. Quy trinh tuan thu quan trong lien quan den weekend maintenance window.\n3. Viec thuc thi dung han lien quan den internal portal offline.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@techcorpitdepartment.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "cloud",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh cloud migration"
      },
      {
        "word": "weekend",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh weekend maintenance window"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-07-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning IT Server Maintenance Notice",
            "textVi": "Cap nhat lien quan den Nang Cap He Thong CNTT & Bao Tri May Chu"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: IT Server Maintenance Notice",
        "citationVi": "CHU DE: Nang Cap He Thong CNTT & Bao Tri May Chu",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Nang Cap He Thong CNTT & Bao Tri May Chu. Chon A."
      },
      {
        "id": "p7-07-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-07-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-08",
    "title": "Bai 08: De Xuat Hop Dong Cung Cap Suat An Doanh Nghiep (Corporate Catering Service Proposal)",
    "type": "Business Proposal",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Gourmet Express Catering\nDATE: October 08\nSUBJECT: Corporate Catering Service Proposal\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding corporate catering service proposal. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving organic lunch menus.\n2. Important compliance procedure concerning flexible dietary choices.\n3. Timely execution regarding annual contract discount.\n\nIf you have any questions or require further clarification, please contact our support desk at support@gourmetexpresscatering.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Gourmet Express Catering\nNGAY: Ngay 08 thang 10\nCHU DE: De Xuat Hop Dong Cung Cap Suat An Doanh Nghiep\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den de xuat hop dong cung cap suat an doanh nghiep. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den organic lunch menus.\n2. Quy trinh tuan thu quan trong lien quan den flexible dietary choices.\n3. Viec thuc thi dung han lien quan den annual contract discount.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@gourmetexpresscatering.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "organic",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh organic lunch menus"
      },
      {
        "word": "flexible",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh flexible dietary choices"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-08-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Corporate Catering Service Proposal",
            "textVi": "Cap nhat lien quan den De Xuat Hop Dong Cung Cap Suat An Doanh Nghiep"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Corporate Catering Service Proposal",
        "citationVi": "CHU DE: De Xuat Hop Dong Cung Cap Suat An Doanh Nghiep",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve De Xuat Hop Dong Cung Cap Suat An Doanh Nghiep. Chon A."
      },
      {
        "id": "p7-08-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-08-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-09",
    "title": "Bai 09: Danh Gia Hieu Suat Cong Viec Hang Nam (Annual Performance Evaluation Process)",
    "type": "Announcement",
    "difficulty": "Nâng Cao (750+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Global HR Department\nDATE: October 09\nSUBJECT: Annual Performance Evaluation Process\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding annual performance evaluation process. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving self-assessment form.\n2. Important compliance procedure concerning manager review meeting.\n3. Timely execution regarding merit bonus qualification.\n\nIf you have any questions or require further clarification, please contact our support desk at support@globalhrdepartment.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Global HR Department\nNGAY: Ngay 09 thang 10\nCHU DE: Danh Gia Hieu Suat Cong Viec Hang Nam\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den danh gia hieu suat cong viec hang nam. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den self-assessment form.\n2. Quy trinh tuan thu quan trong lien quan den manager review meeting.\n3. Viec thuc thi dung han lien quan den merit bonus qualification.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@globalhrdepartment.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "self-assessment",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh self-assessment form"
      },
      {
        "word": "manager",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh manager review meeting"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-09-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Annual Performance Evaluation Process",
            "textVi": "Cap nhat lien quan den Danh Gia Hieu Suat Cong Viec Hang Nam"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Annual Performance Evaluation Process",
        "citationVi": "CHU DE: Danh Gia Hieu Suat Cong Viec Hang Nam",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Danh Gia Hieu Suat Cong Viec Hang Nam. Chon A."
      },
      {
        "id": "p7-09-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-09-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-10",
    "title": "Bai 10: Dat Tiec & Su Kien Tai Nha Hang Khach San (Hotel Banquet & Event Reservation)",
    "type": "Email",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: The Royal Palm Hotel\nDATE: October 10\nSUBJECT: Hotel Banquet & Event Reservation\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding hotel banquet & event reservation. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving private dining room.\n2. Important compliance procedure concerning custom 4-course menu.\n3. Timely execution regarding audio-visual equipment rental.\n\nIf you have any questions or require further clarification, please contact our support desk at support@theroyalpalmhotel.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: The Royal Palm Hotel\nNGAY: Ngay 10 thang 10\nCHU DE: Dat Tiec & Su Kien Tai Nha Hang Khach San\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den dat tiec & su kien tai nha hang khach san. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den private dining room.\n2. Quy trinh tuan thu quan trong lien quan den custom 4-course menu.\n3. Viec thuc thi dung han lien quan den audio-visual equipment rental.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@theroyalpalmhotel.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "private",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh private dining room"
      },
      {
        "word": "custom",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh custom 4-course menu"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-10-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Hotel Banquet & Event Reservation",
            "textVi": "Cap nhat lien quan den Dat Tiec & Su Kien Tai Nha Hang Khach San"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Hotel Banquet & Event Reservation",
        "citationVi": "CHU DE: Dat Tiec & Su Kien Tai Nha Hang Khach San",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Dat Tiec & Su Kien Tai Nha Hang Khach San. Chon A."
      },
      {
        "id": "p7-10-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-10-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-11",
    "title": "Bai 11: Tri Hoan Van Chuyen Hang Hoa Quoc Te (International Cargo Delay Notice)",
    "type": "Email",
    "difficulty": "Nâng Cao (750+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Global Logistics Freight\nDATE: October 11\nSUBJECT: International Cargo Delay Notice\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding international cargo delay notice. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving port congestion delay.\n2. Important compliance procedure concerning customs inspection clearance.\n3. Timely execution regarding expedited sea shipment.\n\nIf you have any questions or require further clarification, please contact our support desk at support@globallogisticsfreight.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Global Logistics Freight\nNGAY: Ngay 11 thang 10\nCHU DE: Tri Hoan Van Chuyen Hang Hoa Quoc Te\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den tri hoan van chuyen hang hoa quoc te. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den port congestion delay.\n2. Quy trinh tuan thu quan trong lien quan den customs inspection clearance.\n3. Viec thuc thi dung han lien quan den expedited sea shipment.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@globallogisticsfreight.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "port",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh port congestion delay"
      },
      {
        "word": "customs",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh customs inspection clearance"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-11-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning International Cargo Delay Notice",
            "textVi": "Cap nhat lien quan den Tri Hoan Van Chuyen Hang Hoa Quoc Te"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: International Cargo Delay Notice",
        "citationVi": "CHU DE: Tri Hoan Van Chuyen Hang Hoa Quoc Te",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Tri Hoan Van Chuyen Hang Hoa Quoc Te. Chon A."
      },
      {
        "id": "p7-11-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-11-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-12",
    "title": "Bai 12: Hop Dong Cho Thue Van Phong Thuong Mai (Commercial Office Lease Proposal)",
    "type": "Business Proposal",
    "difficulty": "Nâng Cao (750+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Highland Property Group\nDATE: October 12\nSUBJECT: Commercial Office Lease Proposal\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding commercial office lease proposal. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving square foot rental rate.\n2. Important compliance procedure concerning lease renewal terms.\n3. Timely execution regarding utility fee inclusion.\n\nIf you have any questions or require further clarification, please contact our support desk at support@highlandpropertygroup.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Highland Property Group\nNGAY: Ngay 12 thang 10\nCHU DE: Hop Dong Cho Thue Van Phong Thuong Mai\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den hop dong cho thue van phong thuong mai. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den square foot rental rate.\n2. Quy trinh tuan thu quan trong lien quan den lease renewal terms.\n3. Viec thuc thi dung han lien quan den utility fee inclusion.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@highlandpropertygroup.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "square",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh square foot rental rate"
      },
      {
        "word": "lease",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh lease renewal terms"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-12-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Commercial Office Lease Proposal",
            "textVi": "Cap nhat lien quan den Hop Dong Cho Thue Van Phong Thuong Mai"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Commercial Office Lease Proposal",
        "citationVi": "CHU DE: Hop Dong Cho Thue Van Phong Thuong Mai",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Hop Dong Cho Thue Van Phong Thuong Mai. Chon A."
      },
      {
        "id": "p7-12-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-12-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-13",
    "title": "Bai 13: Xac Nhan Dien Gia Chinh Hoi Nghi (Keynote Speaker Confirmation)",
    "type": "Email",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Tech Summit 2026\nDATE: October 13\nSUBJECT: Keynote Speaker Confirmation\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding keynote speaker confirmation. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving presentation slides deadline.\n2. Important compliance procedure concerning travel reimbursement form.\n3. Timely execution regarding VIP reception dinner.\n\nIf you have any questions or require further clarification, please contact our support desk at support@techsummit2026.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Tech Summit 2026\nNGAY: Ngay 13 thang 10\nCHU DE: Xac Nhan Dien Gia Chinh Hoi Nghi\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den xac nhan dien gia chinh hoi nghi. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den presentation slides deadline.\n2. Quy trinh tuan thu quan trong lien quan den travel reimbursement form.\n3. Viec thuc thi dung han lien quan den VIP reception dinner.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@techsummit2026.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "presentation",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh presentation slides deadline"
      },
      {
        "word": "travel",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh travel reimbursement form"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-13-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Keynote Speaker Confirmation",
            "textVi": "Cap nhat lien quan den Xac Nhan Dien Gia Chinh Hoi Nghi"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Keynote Speaker Confirmation",
        "citationVi": "CHU DE: Xac Nhan Dien Gia Chinh Hoi Nghi",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Xac Nhan Dien Gia Chinh Hoi Nghi. Chon A."
      },
      {
        "id": "p7-13-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-13-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-14",
    "title": "Bai 14: Chuong Trinh Nghi Su Hop Hoi Dong Quan Tri (Board of Directors Meeting Agenda)",
    "type": "Announcement",
    "difficulty": "Nâng Cao (750+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: OmniCorp Executive Board\nDATE: October 14\nSUBJECT: Board of Directors Meeting Agenda\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding board of directors meeting agenda. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving quarterly financial report.\n2. Important compliance procedure concerning shareholder dividend vote.\n3. Timely execution regarding expansion strategy proposal.\n\nIf you have any questions or require further clarification, please contact our support desk at support@omnicorpexecutiveboard.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: OmniCorp Executive Board\nNGAY: Ngay 14 thang 10\nCHU DE: Chuong Trinh Nghi Su Hop Hoi Dong Quan Tri\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den chuong trinh nghi su hop hoi dong quan tri. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den quarterly financial report.\n2. Quy trinh tuan thu quan trong lien quan den shareholder dividend vote.\n3. Viec thuc thi dung han lien quan den expansion strategy proposal.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@omnicorpexecutiveboard.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "quarterly",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh quarterly financial report"
      },
      {
        "word": "shareholder",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh shareholder dividend vote"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-14-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Board of Directors Meeting Agenda",
            "textVi": "Cap nhat lien quan den Chuong Trinh Nghi Su Hop Hoi Dong Quan Tri"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Board of Directors Meeting Agenda",
        "citationVi": "CHU DE: Chuong Trinh Nghi Su Hop Hoi Dong Quan Tri",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Chuong Trinh Nghi Su Hop Hoi Dong Quan Tri. Chon A."
      },
      {
        "id": "p7-14-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-14-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-15",
    "title": "Bai 15: Quy Dinh Phan Bo Ngan Sach Cac Phong Ban (Department Budget Allocation Notice)",
    "type": "Announcement",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Finance & Accounting Division\nDATE: October 15\nSUBJECT: Department Budget Allocation Notice\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding department budget allocation notice. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving fiscal year expenditure limit.\n2. Important compliance procedure concerning purchase order approval.\n3. Timely execution regarding reimbursement claim cutoff.\n\nIf you have any questions or require further clarification, please contact our support desk at support@finance&accountingdivision.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Finance & Accounting Division\nNGAY: Ngay 15 thang 10\nCHU DE: Quy Dinh Phan Bo Ngan Sach Cac Phong Ban\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den quy dinh phan bo ngan sach cac phong ban. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den fiscal year expenditure limit.\n2. Quy trinh tuan thu quan trong lien quan den purchase order approval.\n3. Viec thuc thi dung han lien quan den reimbursement claim cutoff.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@finance&accountingdivision.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "fiscal",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh fiscal year expenditure limit"
      },
      {
        "word": "purchase",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh purchase order approval"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-15-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Department Budget Allocation Notice",
            "textVi": "Cap nhat lien quan den Quy Dinh Phan Bo Ngan Sach Cac Phong Ban"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Department Budget Allocation Notice",
        "citationVi": "CHU DE: Quy Dinh Phan Bo Ngan Sach Cac Phong Ban",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Quy Dinh Phan Bo Ngan Sach Cac Phong Ban. Chon A."
      },
      {
        "id": "p7-15-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-15-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-16",
    "title": "Bai 16: Bao Cao Khao Sat Hai Long Khach Hang (Customer Satisfaction Survey Report)",
    "type": "Advertisement",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Apex Consumer Research\nDATE: October 16\nSUBJECT: Customer Satisfaction Survey Report\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding customer satisfaction survey report. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving net promoter score.\n2. Important compliance procedure concerning feedback form submission.\n3. Timely execution regarding free gift drawing entry.\n\nIf you have any questions or require further clarification, please contact our support desk at support@apexconsumerresearch.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Apex Consumer Research\nNGAY: Ngay 16 thang 10\nCHU DE: Bao Cao Khao Sat Hai Long Khach Hang\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den bao cao khao sat hai long khach hang. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den net promoter score.\n2. Quy trinh tuan thu quan trong lien quan den feedback form submission.\n3. Viec thuc thi dung han lien quan den free gift drawing entry.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@apexconsumerresearch.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "net",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh net promoter score"
      },
      {
        "word": "feedback",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh feedback form submission"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-16-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Customer Satisfaction Survey Report",
            "textVi": "Cap nhat lien quan den Bao Cao Khao Sat Hai Long Khach Hang"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Customer Satisfaction Survey Report",
        "citationVi": "CHU DE: Bao Cao Khao Sat Hai Long Khach Hang",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Bao Cao Khao Sat Hai Long Khach Hang. Chon A."
      },
      {
        "id": "p7-16-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-16-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-17",
    "title": "Bai 17: Quy Dinh An Toan & Ve Sinh Benh Vien (Hospital Hygiene & Safety Protocol)",
    "type": "Announcement",
    "difficulty": "Nâng Cao (750+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: St. Jude Medical Center\nDATE: October 17\nSUBJECT: Hospital Hygiene & Safety Protocol\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding hospital hygiene & safety protocol. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving sterilization compliance.\n2. Important compliance procedure concerning sanitizer dispenser placement.\n3. Timely execution regarding protective gear requirement.\n\nIf you have any questions or require further clarification, please contact our support desk at support@st.judemedicalcenter.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: St. Jude Medical Center\nNGAY: Ngay 17 thang 10\nCHU DE: Quy Dinh An Toan & Ve Sinh Benh Vien\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den quy dinh an toan & ve sinh benh vien. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den sterilization compliance.\n2. Quy trinh tuan thu quan trong lien quan den sanitizer dispenser placement.\n3. Viec thuc thi dung han lien quan den protective gear requirement.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@st.judemedicalcenter.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "sterilization",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh sterilization compliance"
      },
      {
        "word": "sanitizer",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh sanitizer dispenser placement"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-17-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Hospital Hygiene & Safety Protocol",
            "textVi": "Cap nhat lien quan den Quy Dinh An Toan & Ve Sinh Benh Vien"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Hospital Hygiene & Safety Protocol",
        "citationVi": "CHU DE: Quy Dinh An Toan & Ve Sinh Benh Vien",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Quy Dinh An Toan & Ve Sinh Benh Vien. Chon A."
      },
      {
        "id": "p7-17-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-17-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-18",
    "title": "Bai 18: Cung Cap Nguyen Lieu Huu Co Tiem Banh (Organic Flour Supply Agreement)",
    "type": "Email",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Artisan Bakery Suppliers\nDATE: October 18\nSUBJECT: Organic Flour Supply Agreement\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding organic flour supply agreement. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving certified organic grains.\n2. Important compliance procedure concerning bulk discount pricing.\n3. Timely execution regarding weekly delivery schedule.\n\nIf you have any questions or require further clarification, please contact our support desk at support@artisanbakerysuppliers.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Artisan Bakery Suppliers\nNGAY: Ngay 18 thang 10\nCHU DE: Cung Cap Nguyen Lieu Huu Co Tiem Banh\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den cung cap nguyen lieu huu co tiem banh. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den certified organic grains.\n2. Quy trinh tuan thu quan trong lien quan den bulk discount pricing.\n3. Viec thuc thi dung han lien quan den weekly delivery schedule.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@artisanbakerysuppliers.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "certified",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh certified organic grains"
      },
      {
        "word": "bulk",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh bulk discount pricing"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-18-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Organic Flour Supply Agreement",
            "textVi": "Cap nhat lien quan den Cung Cap Nguyen Lieu Huu Co Tiem Banh"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Organic Flour Supply Agreement",
        "citationVi": "CHU DE: Cung Cap Nguyen Lieu Huu Co Tiem Banh",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Cung Cap Nguyen Lieu Huu Co Tiem Banh. Chon A."
      },
      {
        "id": "p7-18-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-18-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-19",
    "title": "Bai 19: Nang Cap Day Chuyen San Xuat O To (Automotive Assembly Line Upgrade)",
    "type": "Announcement",
    "difficulty": "Nâng Cao (750+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: Apex Motors Plant #3\nDATE: October 19\nSUBJECT: Automotive Assembly Line Upgrade\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding automotive assembly line upgrade. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving robotic arm installation.\n2. Important compliance procedure concerning production output capacity.\n3. Timely execution regarding technician training workshop.\n\nIf you have any questions or require further clarification, please contact our support desk at support@apexmotorsplant#3.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: Apex Motors Plant #3\nNGAY: Ngay 19 thang 10\nCHU DE: Nang Cap Day Chuyen San Xuat O To\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den nang cap day chuyen san xuat o to. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den robotic arm installation.\n2. Quy trinh tuan thu quan trong lien quan den production output capacity.\n3. Viec thuc thi dung han lien quan den technician training workshop.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@apexmotorsplant#3.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "robotic",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh robotic arm installation"
      },
      {
        "word": "production",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh production output capacity"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-19-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Automotive Assembly Line Upgrade",
            "textVi": "Cap nhat lien quan den Nang Cap Day Chuyen San Xuat O To"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Automotive Assembly Line Upgrade",
        "citationVi": "CHU DE: Nang Cap Day Chuyen San Xuat O To",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Nang Cap Day Chuyen San Xuat O To. Chon A."
      },
      {
        "id": "p7-19-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-19-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  },
  {
    "id": "p7-20",
    "title": "Bai 20: Quang Cao Khai Truong Sieu Thi Khuyen Mai (Retail Superstore Grand Opening)",
    "type": "Advertisement",
    "difficulty": "Trung Bình (550+)",
    "passageEn": "OFFICIAL DOCUMENT / CORRESPONDENCE\n\nORGANIZATION: MegaMart Supercenter\nDATE: October 20\nSUBJECT: Retail Superstore Grand Opening\n\nDear Valued Partners and Team Members,\n\nWe are pleased to share key updates regarding retail superstore grand opening. Our primary objective is to maintain operational excellence and deliver high-quality standards across all business units.\n\nPlease take note of the following important points:\n1. Key operational aspect involving first 100 shoppers gift.\n2. Important compliance procedure concerning doorbuster discount deals.\n3. Timely execution regarding loyalty reward card sign-up.\n\nIf you have any questions or require further clarification, please contact our support desk at support@megamartsupercenter.com or call our direct office extension.\n\nSincerely,\nExecutive Management Team",
    "passageVi": "TAI LIEU CHINH THUC / THU TU\n\nTO CHUC: MegaMart Supercenter\nNGAY: Ngay 20 thang 10\nCHU DE: Quang Cao Khai Truong Sieu Thi Khuyen Mai\n\nKinh gui cac Doi tac va Thanh vien Doi ngu,\n\nChung toi han hanh chia se nhung cap nhat quan trong lien quan den quang cao khai truong sieu thi khuyen mai. Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao tren toan bo cac don vi kinh doanh.\n\nVui long luu y cac diem quan trong sau:\n1. Khia canh van hanh chinh lien quan den first 100 shoppers gift.\n2. Quy trinh tuan thu quan trong lien quan den doorbuster discount deals.\n3. Viec thuc thi dung han lien quan den loyalty reward card sign-up.\n\nNeu ban co bat ky cau hoi nao hoac can lam ro them, vui long lien he voi quay ho tro cua chung toi tai support@megamartsupercenter.com hoac goi cho so may le truc tiep cua van phong chung toi.\n\nTran trong,\nDoi ngu Quan ly Dieu hanh",
    "keyWords": [
      {
        "word": "first",
        "partOfSpeech": "n",
        "pronunciation": "/ˈɒpəreɪʃn/",
        "meaningVi": "khia canh first 100 shoppers gift"
      },
      {
        "word": "doorbuster",
        "partOfSpeech": "v",
        "pronunciation": "/kəmˈplaɪəns/",
        "meaningVi": "quy trinh doorbuster discount deals"
      },
      {
        "word": "objective",
        "partOfSpeech": "n",
        "pronunciation": "/əbˈdʒektɪv/",
        "meaningVi": "muc tieu chinh"
      }
    ],
    "questions": [
      {
        "id": "p7-20-q1",
        "questionEn": "What is the main topic of this document?",
        "questionVi": "Chu de chinh cua tai lieu nay la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "Updates concerning Retail Superstore Grand Opening",
            "textVi": "Cap nhat lien quan den Quang Cao Khai Truong Sieu Thi Khuyen Mai"
          },
          {
            "key": "B",
            "textEn": "Cancellation of all company flights",
            "textVi": "Huy bo toan bo cac chuyen bay cong ty"
          },
          {
            "key": "C",
            "textEn": "Resignation of the chief accountant",
            "textVi": "Su tu chuc cua ke toan truong"
          },
          {
            "key": "D",
            "textEn": "An increase in employee parking fees",
            "textVi": "Tang phi do xe cua nhan vien"
          }
        ],
        "answerKey": "A",
        "citationEn": "SUBJECT: Retail Superstore Grand Opening",
        "citationVi": "CHU DE: Quang Cao Khai Truong Sieu Thi Khuyen Mai",
        "explanationVi": "Phan chu de (Subject) khang dinh ro day la thong bao cap nhat ve Quang Cao Khai Truong Sieu Thi Khuyen Mai. Chon A."
      },
      {
        "id": "p7-20-q2",
        "questionEn": "What is stated as the organization's primary objective?",
        "questionVi": "Muc tieu chinh cua to chuc duoc neu la gi?",
        "options": [
          {
            "key": "A",
            "textEn": "To maintain operational excellence and high-quality standards",
            "textVi": "Duy tri su xuat sac trong van hanh va tieu chuan chat luong cao"
          },
          {
            "key": "B",
            "textEn": "To cut operational costs by 50%",
            "textVi": "Cat giam 50% chi phi van hanh"
          },
          {
            "key": "C",
            "textEn": "To expand into international retail markets",
            "textVi": "Mo rong sang cac thi truong ban le quoc te"
          },
          {
            "key": "D",
            "textEn": "To relocate to a different city",
            "textVi": "Chuyen tru so sang thanh pho khac"
          }
        ],
        "answerKey": "A",
        "citationEn": "Our primary objective is to maintain operational excellence and deliver high-quality standards...",
        "citationVi": "Muc tieu chinh cua chung toi la duy tri su xuat sac trong van hanh va mang lai cac tieu chuan chat luong cao...",
        "explanationVi": "Doan 2 neu ro muc tieu chinh: 'maintain operational excellence and deliver high-quality standards'. Chon A."
      },
      {
        "id": "p7-20-q3",
        "questionEn": "How can staff contact the support desk?",
        "questionVi": "Lam the nao nhan vien co the lien he voi quay ho tro?",
        "options": [
          {
            "key": "A",
            "textEn": "By sending an email or calling the office extension",
            "textVi": "Bang cach gui email hoac goi so may le van phong"
          },
          {
            "key": "B",
            "textEn": "By visiting the building security room",
            "textVi": "Gap truc tiep phong bao ve toa nha"
          },
          {
            "key": "C",
            "textEn": "By mailing a printed letter",
            "textVi": "Gui thu in qua duong buu dien"
          },
          {
            "key": "D",
            "textEn": "By contacting an external lawyer",
            "textVi": "Lien he luat su ben ngoai"
          }
        ],
        "answerKey": "A",
        "citationEn": "contact our support desk at support@...com or call our direct office extension.",
        "citationVi": "lien he voi quay ho tro cua chung toi tai support@...com hoac goi cho so may le truc tiep...",
        "explanationVi": "Doan cuoi ghi ro cach lien he la gui email hoac goi so may le van phong. Chon A."
      }
    ]
  }
];
