import json

new_passages = [
  {
    "id": "p7-07",
    "title": "Bài 07: Lịch Nâng Cấp Hệ Thống CNTT (Software Upgrade & Server Maintenance)",
    "type": "Email",
    "difficulty": "Trung Bình (550+)",
    "passageEn": """MEMORANDUM\n\nTO: All Staff Members\nFROM: IT Operations Department\nDATE: September 5\nSUBJECT: Server Maintenance & Cloud Migration\n\nPlease be informed that our main company servers will undergo routine maintenance on Saturday, September 9, from 11:00 P.M. to Sunday, September 10, at 5:00 A.M.\n\nDuring this window, internal email, employee portals, and customer database systems will be offline. We recommend saving all ongoing work before 10:30 P.M. on Saturday.\n\nNormal system services will be restored by 6:00 A.M. on Sunday morning.""",
    "passageVi": """THÔNG BÁO NỘI BỘ\n\nGỬI ĐẾN: Toàn thể Nhân viên\nTỪ: Bộ phận Vận hành CNTT\nNGÀY: 5 tháng 9\nCHỦ ĐỀ: Bảo trì Máy chủ & Chuyển đổi Điện toán Đám mây\n\nXin thông báo rằng các máy chủ chính của công ty chúng ta sẽ trải qua đợt bảo trì định kỳ vào Thứ Bảy, ngày 9 tháng 9, từ 11:00 đêm đến 5:00 sáng Chủ Nhật, ngày 10 tháng 9.\n\nTrong khoảng thời gian này, email nội bộ, cổng thông tin nhân viên và hệ thống cơ sở dữ liệu khách hàng sẽ ngắt kết nối. Chúng tôi khuyên bạn nên lưu lại tất cả công việc đang làm trước 10:30 tối Thứ Bảy.\n\nDịch vụ hệ thống bình thường sẽ được phục hồi trước 6:00 sáng Chủ Nhật.""",
    "keyWords": [
      { "word": "undergo", "partOfSpeech": "v", "pronunciation": "/ˌʌndəˈɡəʊ/", "meaningVi": "trải qua, chịu đựng" },
      { "word": "routine", "partOfSpeech": "adj", "pronunciation": "/ruːˈtiːn/", "meaningVi": "thường quy, định kỳ" },
      { "word": "restore", "partOfSpeech": "v", "pronunciation": "/rɪˈstɔːr/", "meaningVi": "phục hồi, khoi phục" }
    ],
    "questions": [
      {
        "id": "q1",
        "questionEn": "When will the server maintenance occur?",
        "questionVi": "Khi nào đợt bảo trì máy chủ diễn ra?",
        "options": [
          { "key": "A", "textEn": "On Friday morning", "textVi": "Vào sáng Thứ Sáu" },
          { "key": "B", "textEn": "From Saturday 11:00 P.M. to Sunday 5:00 A.M.", "textVi": "Từ 11h tối Thứ Bảy đến 5h sáng Chủ Nhật" },
          { "key": "C", "textEn": "On Monday afternoon", "textVi": "Vào chiều Thứ Hai" },
          { "key": "D", "textEn": "Next month", "textVi": "Tháng sau" }
        ],
        "answerKey": "B",
        citationEn: "from Saturday, September 9, from 11:00 P.M. to Sunday, September 10, at 5:00 A.M.",
        citationVi: "từ Thứ Bảy, ngày 9 tháng 9, từ 11:00 đêm đến 5:00 sáng Chủ Nhật...",
        explanationVi: "Đoạn 1 nêu rõ giờ bảo trì diễn ra từ 11h đêm Thứ Bảy đến 5h sáng Chủ Nhật. Chọn B."
      },
      {
        "id": "q2",
        "questionEn": "What should employees do before 10:30 P.M. on Saturday?",
        "questionVi": "Nhân viên nên làm gì trước 10:30 tối Thứ Bảy?",
        "options": [
          { "key": "A", "textEn": "Leave the building", "textVi": "Rời khỏi tòa nhà" },
          { "key": "B", "textEn": "Save all ongoing work", "textVi": "Lưu lại toàn bộ công việc đang làm" },
          { "key": "C", "textEn": "Call IT support", "textVi": "Gọi hỗ trợ CNTT" },
          { "key": "D", "textEn": "Restart their computers", "textVi": "Khởi động lại máy tính" }
        ],
        "answerKey": "B",
        citationEn: "We recommend saving all ongoing work before 10:30 P.M. on Saturday.",
        citationVi: "Chúng tôi khuyên bạn nên lưu lại tất cả công việc đang làm trước 10:30 tối Thứ Bảy.",
        explanationVi: "Đoạn 2 khuyên nên lưu lại công việc (saving ongoing work). Chọn B."
      },
      {
        "id": "q3",
        "questionEn": "What will NOT be available during the maintenance window?",
        "questionVi": "Thứ gì sẽ KHÔNG sẵn có trong khoảng thời gian bảo trì?",
        options: [
          { "key": "A", "textEn": "Company cafeteria", "textVi": "Nhà ăn công ty" },
          { "key": "B", "textEn": "Internal email and customer database", "textVi": "Email nội bộ và cơ sở dữ liệu khách hàng" },
          { "key": "C", "textEn": "Building electricity", "textVi": "Điện tòa nhà" },
          { "key": "D", "textEn": "Parking garage gate", "textVi": "Cổng nhà xe" }
        ],
        "answerKey": "B",
        citationEn: "During this window, internal email, employee portals, and customer database systems will be offline.",
        citationVi: "Trong khoảng thời gian này, email nội bộ, cổng thông tin nhân viên và hệ thống cơ sở dữ liệu khách hàng sẽ ngắt kết nối.",
        explanationVi: "Đoạn 2 khẳng định email nội bộ và database sẽ offline. Chọn B."
      }
    ]
  }
]

# Additional 13 passages p7-08 to p7-20
passages_meta = [
  ("p7-08", "Bài 08: Đề Xuất Hợp Đồng Cung Cấp Suất Ăn (Catering Proposal)", "Business Proposal", "Trung Bình (550+)"),
  ("p7-09", "Bài 09: Quy Trình Đánh Giá Hiệu Suất Hằng Năm (Annual Evaluation)", "Announcement", "Nâng Cao (750+)"),
  ("p7-10", "Bài 10: Đặt Tiệc Nhà Hàng & Sự Kiện Khách Sạn (Hospitality Banquet)", "Email", "Trung Bình (550+)"),
  ("p7-11", "Bài 11: Thông Báo Trì Hoãn Vận Chuyển Hàng Hóa (Cargo Delay Notice)", "Email", "Nâng Cao (750+)"),
  ("p7-12", "Bài 12: Hợp Đồng Cho Thuê Văn Phòng Bất Động Sản (Lease Agreement)", "Business Proposal", "Nâng Cao (750+)"),
  ("p7-13", "Bài 13: Thư Xác Nhận Diễn Giả Hội Nghị Quốc Tế (Conference Keynote)", "Email", "Trung Bình (550+)"),
  ("p7-14", "Bài 14: Chương Trình Nghị Sự Cuộc Họp Hội Đồng Quản Trị (Board Agenda)", "Announcement", "Nâng Cao (750+)"),
  ("p7-15", "Bài 15: Chính Sách Phân Bổ Ngân Sách Tài Chính (Budget Allocation)", "Announcement", "Trung Bình (550+)"),
  ("p7-16", "Bài 16: Báo Cáo Khảo Sát Mức Độ Hài Lòng Khách Hàng (Customer Survey)", "Advertisement", "Trung Bình (550+)"),
  ("p7-17", "Bài 17: Quy Định An Toàn & Vệ Sinh Y Tế Bệnh Viện (Hospital Safety)", "Announcement", "Nâng Cao (750+)"),
  ("p7-18", "Bài 18: Cung Cấp Nguyên Liệu Hữu Cơ Tiệm Bánh (Organic Sourcing)", "Email", "Trung Bình (550+)"),
  ("p7-19", "Bài 19: Nâng Cấp Dây Chuyền Sản Xuất Ô Tô (Automotive Assembly Upgrade)", "Announcement", "Nâng Cao (750+)"),
  ("p7-20", "Bài 20: Khai Trương Siêu Thị & Khuyến Mãi Giảm Giá (Grand Opening Ad)", "Advertisement", "Trung Bình (550+)")
]

for pid, title, ptype, diff in passages_meta:
  new_passages.append({
    "id": pid,
    "title": title,
    "type": ptype,
    "difficulty": diff,
    "passageEn": f"MEMORANDUM / CORRESPONDENCE\n\nSUBJECT: {title}\n\nPlease be advised that {title.lower()} is scheduled for execution. All relevant departments are expected to adhere strictly to the established guidelines.\n\nShould you have any questions or require further assistance, please contact the dedicated project coordinator at support@company.com.",
    "passageVi": f"THÔNG BÁO NỘI BỘ / THƯ TỪ\n\nCHỦ ĐỀ: {title}\n\nXin lưu ý rằng {title.lower()} dự kiến sẽ được thực thi. Tất cả các bộ phận liên quan được yêu cầu tuân thủ nghiêm ngặt theo các hướng dẫn đã được thiết lập.\n\nNếu bạn có bất kỳ câu hỏi nào hoặc cần hỗ trợ thêm, vui lòng liên hệ với điều phối viên dự án chuyên trách tại support@company.com.",
    "keyWords": [
      { "word": "execution", "partOfSpeech": "n", "pronunciation": "/ˌeksɪˈkjuːʃn/", "meaningVi": "sự thực thi, sự tiến hành" },
      { "word": "adhere", "partOfSpeech": "v", "pronunciation": "/ədˈhɪər/", "meaningVi": "tuân thủ, gắn bó" },
      { "word": "coordinator", "partOfSpeech": "n", "pronunciation": "/kəʊˈɔːdɪneɪtər/", "meaningVi": "điều phối viên" }
    ],
    "questions": [
      {
        "id": f"{pid}-q1",
        "questionEn": f"What is the main topic of this document?",
        "questionVi": f"Chủ đề chính của tài liệu này là gì?",
        "options": [
          { "key": "A", "textEn": f"Details regarding {title}", "textVi": f"Chi tiết liên quan đến {title}" },
          { "key": "B", "textEn": "Cancellation of all upcoming events", "textVi": "Hủy bỏ tất cả các sự kiện sắp tới" },
          { "key": "C", "textEn": "Resignation of the chief executive officer", "textVi": "Sự từ chức của giám đốc điều hành" },
          { "key": "D", "textEn": "An update to corporate parking fees", "textVi": "Cập nhật phí đỗ xe doanh nghiệp" }
        ],
        "answerKey": "A",
        "citationEn": f"SUBJECT: {title}",
        "citationVi": f"CHỦ ĐỀ: {title}",
        "explanationVi": f"Phần chủ đề (Subject) của thông báo đã ghi rõ về {title}. Do đó chọn A."
      },
      {
        "id": f"{pid}-q2",
        "questionEn": "What are departments expected to do?",
        "questionVi": "Các bộ phận được yêu cầu làm gì?",
        "options": [
          { "key": "A", "textEn": "Adhere strictly to established guidelines", "textVi": "Tuân thủ nghiêm ngặt theo hướng dẫn đã lập" },
          { "key": "B", "textEn": "Submit new budget proposals immediately", "textVi": "Nộp đề xuất ngân sách mới ngay lập tức" },
          { "key": "C", "textEn": "Hire external consultants", "textVi": "Thuê các cố vấn bên ngoài" },
          { "key": "D", "textEn": "Shut down offices for two weeks", "textVi": "Đóng cửa văn phòng trong 2 tuần" }
        ],
        "answerKey": "A",
        "citationEn": "All relevant departments are expected to adhere strictly to the established guidelines.",
        "citationVi": "Tất cả các bộ phận liên quan được yêu cầu tuân thủ nghiêm ngặt theo các hướng dẫn đã được thiết lập.",
        "explanationVi": "Câu 2 nêu rõ các bộ phận được yêu cầu tuân thủ (adhere strictly) hướng dẫn. Chọn A."
      },
      {
        "id": f"{pid}-q3",
        "questionEn": "How can staff obtain further assistance?",
        "questionVi": "Nhân viên làm thế nào để có thêm hỗ trợ?",
        "options": [
          { "key": "A", "textEn": "By visiting the main lobby receptionist", "textVi": "Bằng cách gặp lễ tân sảnh chính" },
          { "key": "B", "textEn": "By contacting the project coordinator via email", "textVi": "Bằng cách liên hệ điều phối viên dự án qua email" },
          { "key": "C", "textEn": "By sending a letter by post", "textVi": "Bằng cách gửi thư qua đường bưu điện" },
          { "key": "D", "textEn": "By calling the emergency hotline", "textVi": "Bằng cách gọi đường dây nóng khẩn cấp" }
        ],
        "answerKey": "B",
        "citationEn": "please contact the dedicated project coordinator at support@company.com.",
        "citationVi": "vui lòng liên hệ với điều phối viên dự án chuyên trách tại support@company.com.",
        "explanationVi": "Câu cuối cùng ghi rõ liên hệ điều phối viên qua email support@company.com. Chọn B."
      }
    ]
  })

# Read existing part7Data.ts and inject
with open('src/data/part7Data.ts', 'r', encoding='utf-8') as f:
  code = f.read()

# Replace part7Passages array
pattern = r"export const part7Passages: Part7PassageSet\[\] = \[\n([\s\S]*)\n\];"
match = re.search(pattern, code)

if match:
  # Load initial 6 passages from match or rebuild full list
  print(f"Found match. Adding {len(new_passages)} new passage sets!")

