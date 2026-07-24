import re
import json
import os
import random
import difflib

path = '/Users/katetran/.gemini/antigravity-ide/scratch/ori-toeic-vocab/content/hackers_toeic_unit_01_18_full.md'
output_dir = '/Users/katetran/.gemini/antigravity-ide/scratch/ori-toeic-vocab/src/content/units'

os.makedirs(output_dir, exist_ok=True)

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# DAY titles and topics
DAY_INFO = {
    1: {"title": "Thoát cảnh thất nghiệp", "topic": "Tuyển dụng"},
    2: {"title": "Quy định về trang phục", "topic": "Phép tắc - Quy định"},
    3: {"title": "Cao thủ chốn văn phòng", "topic": "Công việc văn phòng (1)"},
    4: {"title": "Bí quyết kinh doanh", "topic": "Công việc văn phòng (2)"},
    5: {"title": "Vũ khí bí mật", "topic": "Công việc văn phòng (3)"},
    6: {"title": "Ngày nghỉ", "topic": "Thời gian rảnh - Cộng đồng"},
    7: {"title": "Chiến lược marketing", "topic": "Marketing (1)"},
    8: {"title": "Chiến lược marketing", "topic": "Marketing (2)"},
    9: {"title": "Hồi sinh nền kinh tế", "topic": "Kinh tế"},
    10: {"title": "Cao thủ mua sắm", "topic": "Mua sắm"},
    11: {"title": "Ra mắt sản phẩm mới", "topic": "Phát triển sản phẩm"},
    12: {"title": "Tự động hóa ở nhà máy", "topic": "Sản xuất"},
    13: {"title": "Khách hàng là thượng đế", "topic": "Dịch vụ khách hàng"},
    14: {"title": "Mục đích chuyến công tác", "topic": "Du lịch - Sân bay"},
    15: {"title": "Đàm phán hợp đồng", "topic": "Hợp đồng"},
    16: {"title": "Hiệp định thương mại", "topic": "Giao dịch"},
    17: {"title": "Giao hàng nhanh", "topic": "Thương mại - Vận chuyển"},
    18: {"title": "Món ăn đặc biệt", "topic": "Nơi lưu trú - Nhà hàng"}
}

STORIES_DB = {
    1: {
        "title": "Giấc Mơ Tiếp Viên Hàng Không Của ORI",
        "words": ["inform", "résumé", "opening", "applicant", "requirement", "meet", "qualified", "candidate", "confidence", "professional"],
        "template": "Từ nhỏ, cô bé ORI đã nuôi dưỡng ước mơ trở thành một tiếp viên hàng không. Ngay khi nghe tin hãng hàng không quốc gia {w0} (thông báo) tuyển dụng, ORI đã hào hứng chuẩn bị. Cô dành cả tối để viết một bản {w1} (sơ yếu lý lịch) thật ấn tượng. Hãng đang có một {w2} (vị trí trống) lớn cho đoàn bay quốc tế. Là một {w3} (ứng viên) trẻ tuổi, ORI biết mình cần chuẩn bị kỹ càng để đáp ứng mọi {w4} (yêu cầu) khắt khe của hội đồng. Cô tự nhủ bản thân phải {w5} (đáp ứng) được các tiêu chuẩn về ngoại ngữ và kỹ năng mềm để chứng minh mình là người {w6} (đủ năng lực). ORI tin rằng cô là một {w7} (ứng viên) sáng giá. Với sự tự tin ({w8}) và tác phong làm việc {w9} (chuyên nghiệp), ORI bước vào phòng phỏng vấn với nụ cười rạng rỡ."
    },
    2: {
        "title": "ORI Học Nội Quy Đoàn Bay",
        "words": ["submit", "policy", "comply", "regulation", "exception", "adhere", "severely", "permission", "access", "procedure"],
        "template": "Sau khi trúng tuyển, ORI tham gia khóa đào tạo tân binh. Ngày đầu tiên, cô được yêu cầu {w0} (nộp) các giấy tờ tùy thân. Giáo viên chủ nhiệm phổ biến về {w1} (chính sách) an toàn của hãng hàng không. ORI tự nhủ mình phải {w2} (tuân thủ) nghiêm ngặt mọi {w3} (quy định) của ngành bay. Ở đây, tuyệt đối không có {w4} (ngoại lệ) nào cho việc đi muộn hay sai tác phong. Các học viên phải {w5} (bám sát/tuân thủ) các tiêu chuẩn an toàn bay. Bất kỳ vi phạm nào cũng sẽ bị phạt {w6} (nặng nề). Chỉ khi được sự {w7} (cho phép) của giáo viên, ORI mới có quyền {w8} (tiếp cận) khu vực mô phỏng buồng lái. Cô chăm chỉ thực hành từng {w9} (thủ tục) khẩn cấp để đảm bảo an toàn tuyệt đối cho hành khách sau này."
    },
    3: {
        "title": "Ngày Đầu Đi Làm Của ORI",
        "words": ["department", "colleague", "assist", "delegate", "coordinate", "supervisor", "remind", "instruction", "submit", "assignment"],
        "template": "Hôm nay là ngày đầu tiên ORI nhận việc tại {w0} (phòng ban) dịch vụ mặt đất. Các {w1} (đồng nghiệp) đón tiếp cô rất nồng hậu. ORI được phân công {w2} (hỗ trợ) anh nhóm trưởng trong việc hướng dẫn hành khách. Nhóm trưởng tin tưởng {w3} (giao phó) cho ORI nhiệm vụ quản lý thẻ lên tàu bay. Cô phải {w4} (phối hợp) nhịp nhàng với tổ bay để đảm bảo chuyến bay đúng giờ. Người {w5} (giám sát) trực tiếp của ORI liên tục {w6} (nhắc nhở) cô phải chú ý đến các chi tiết nhỏ. Theo đúng {w7} (hướng dẫn) làm việc, ORI đã hoàn thành xuất sắc và {w8} (nộp) bản báo cáo cuối ngày. Cô cảm thấy rất vui vì đã hoàn thành {w9} (nhiệm vụ) đầu tiên một cách trọn vẹn."
    },
    4: {
        "title": "ORI Chuẩn Bị Cho Cuộc Họp Lớn",
        "words": ["schedule", "meeting", "agenda", "conduct", "discuss", "review", "report", "decision", "executive", "deadline"],
        "template": "Để chuẩn bị cho mùa bay cao điểm, phòng của ORI có một {w0} (lịch trình) làm việc dày đặc. Sáng nay, cô phụ trách chuẩn bị cho một {w1} (cuộc họp) quan trọng. ORI cẩn thận soạn thảo {w2} (chương trình nghị sự) và gửi cho mọi người. Buổi họp được {w3} (tiến hành) lúc 9 giờ sáng dưới sự chủ trì của giám đốc. Cả nhóm cùng {w4} (thảo luận) về cách nâng cao chất lượng dịch vụ. Giám đốc yêu cầu {w5} (xem xét/đánh giá) lại bản {w6} (báo cáo) doanh thu tháng trước. Mọi {w7} (quyết định) đưa ra đều phải được thông qua bởi ban {w8} (điều hành). ORI ghi chép cẩn thận các mốc {w9} (hạn chót) công việc để cả nhóm cùng theo sát."
    },
    5: {
        "title": "ORI Sắp Xếp Hồ Sơ Lưu Trữ",
        "words": ["file", "document", "cabinet", "folder", "organize", "retrieve", "archive", "sensitive", "confidential", "update"],
        "template": "Chiều nay, ORI được phân công dọn dẹp phòng lưu trữ. Cô phải sắp xếp lại toàn bộ {w0} (hồ sơ) và {w1} (tài liệu) của các chuyến bay cũ. ORI xếp gọn gàng các tài liệu vào tủ {w2} (tủ đựng tài liệu) lớn. Cô dán nhãn từng chiếc {w3} (thư mục bìa giấy) để dễ dàng tìm kiếm. Việc {w4} (tổ chức/sắp xếp) này giúp mọi người dễ dàng {w5} (tìm lại/lấy lại) thông tin khi cần thiết. Nhiều hồ sơ trong phòng {w6} (lưu trữ) này chứa thông tin {w7} (nhạy cảm) và mang tính chất {w8} (mật/bảo mật). ORI làm việc hết sức cẩn thận, đồng thời {w9} (cập nhật) hệ thống dữ liệu điện tử của phòng ban."
    },
    6: {
        "title": "Cuối Tuần Vui Vẻ Của ORI",
        "words": ["relax", "activity", "community", "participate", "organize", "gather", "entertainment", "hobby", "outdoor", "enjoy"],
        "template": "Sau một tuần làm việc chăm chỉ, ORI muốn dành thời gian để {w0} (thư giãn). Cô đăng ký tham gia một {w1} (hoạt động) tình nguyện của {w2} (cộng đồng) hàng không. Rất nhiều đồng nghiệp cùng {w3} (tham gia) chuyến đi này. Ban tổ chức đã {w4} (tổ chức) một buổi dã ngoại tuyệt vời. Mọi người {w5} (tụ họp/tập trung) tại một công viên xanh mát. Họ cùng chơi trò chơi, chia sẻ về {w6} (sở thích) cá nhân và thưởng thức các tiết mục {w7} (giải trí) cây nhà lá vườn. ORI rất yêu thích các hoạt động {w8} (ngoài trời) này. Cô thật sự {w9} (tận hưởng) không khí trong lành và những tiếng cười sảng khoái bên bạn bè."
    },
    7: {
        "title": "Chiến Dịch Marketing Cho Đường Bay Mới",
        "words": ["market", "campaign", "advertisement", "target", "customer", "strategy", "promotion", "attract", "brand", "budget"],
        "template": "ORI được điều động hỗ trợ phòng truyền thông quảng bá đường bay mới đến Paris. Cả nhóm đang nghiên cứu {w0} (thị trường) khách du lịch trẻ tuổi. Họ lên kế hoạch cho một {w1} (chiến dịch) truyền thông quy mô lớn. ORI tham gia thiết kế các ấn phẩm {w2} (quảng cáo) trực tuyến. Chiến dịch này {w3} (nhắm tới) đối tượng là {w4} (khách hàng) yêu thích khám phá ẩm thực. Nhờ {w5} (chiến lược) tiếp cận sáng tạo và các chương trình {w6} (khuyến mãi) hấp dẫn, đường bay mới nhanh chóng {w7} (thu hút) sự chú ý lớn. Sự thành công này giúp nâng tầm giá trị {w8} (thương hiệu) của hãng, dù {w9} (ngân sách) chi ra ban đầu là cực kỳ tiết kiệm."
    },
    8: {
        "title": "Phân Tích Phản Hồi Khách Hàng",
        "words": ["survey", "feedback", "response", "analyze", "consumer", "preference", "satisfaction", "report", "result", "improve"],
        "template": "Để đánh giá hiệu quả chiến dịch marketing, ORI cùng nhóm nghiên cứu tiến hành làm một bản {w0} (khảo sát) trực tuyến. Họ nhận được rất nhiều {w1} (phản hồi) tích cực từ hành khách. Tỷ lệ {w2} (phản hồi/trả lời) khảo sát vượt mong đợi. ORI chịu trách nhiệm tổng hợp và {w3} (phân tích) số liệu. Qua đó, cô hiểu rõ hơn về {w4} (người tiêu dùng) và {w5} (sự ưu tiên/sở thích) của họ khi chọn hãng bay. Chỉ số {w6} (sự hài lòng) của khách hàng tăng vọt. ORI đã viết một bản {w7} (báo cáo) tóm tắt gửi giám đốc. {w8} (Kết quả) này là động lực để hãng tiếp tục {w9} (cải thiện) chất lượng phục vụ trên mọi chuyến bay."
    },
    9: {
        "title": "ORI Đọc Tin Tức Kinh Tế Hàng Không",
        "words": ["economy", "growth", "inflation", "industry", "recover", "revenue", "profit", "demand", "passenger", "cost"],
        "template": "Buổi sáng tại quán cà phê, ORI chăm chú đọc báo về tình hình {w0} (kinh tế) toàn cầu. Báo cáo chỉ ra sự {w1} (tăng trưởng) mạnh mẽ của ngành dịch vụ. Mặc dù áp lực {w2} (lạm phát) vẫn còn, nhưng {w3} (ngành công nghiệp) hàng không đang dần {w4} (phục hồi) nhanh chóng. Doanh thu ({w5}) của hãng bay đạt mức kỷ lục, mang lại {w6} (lợi nhuận) lớn cho các nhà đầu tư. Sự phục hồi này là nhờ {w7} (nhu cầu) đi lại bằng đường hàng không của {w8} (hành khách) tăng cao sau đại dịch. Hãng bay của ORI cũng đã tối ưu hóa {w9} (chi phí) vận hành để giữ mức giá vé ổn định cho mọi người."
    },
    10: {
        "title": "ORI Mua Sắm Chuẩn Bị Cho Chuyến Bay",
        "words": ["store", "purchase", "price", "discount", "receipt", "refund", "customer", "quality", "warranty", "choice"],
        "template": "Chuẩn bị cho chuyến bay huấn luyện dài ngày, ORI đi mua sắm tại một {w0} (cửa hàng) vali cao cấp. Cô quyết định {w1} (mua) một chiếc vali kéo chuyên dụng. Vali có {w2} (giá cả) khá đắt nhưng nhờ chương trình {w3} (giảm giá) cho nhân viên, cô tiết kiệm được một khoản lớn. ORI nhận hóa đơn ({w4}) từ thu ngân và cất giữ cẩn thận phòng khi cần đổi trả hoặc {w5} (hoàn tiền). Người bán hàng chăm sóc {w6} (khách hàng) vô cùng chu đáo. Chiếc vali có {w7} (chất lượng) tuyệt vời cùng thời hạn {w8} (bảo hành) lên tới 5 năm. Đây chắc chắn là {w9} (sự lựa chọn) đúng đắn nhất của ORI cho những chuyến đi dài."
    },
    11: {
        "title": "Ý Tưởng Phát Triển Sản Phẩm Mới",
        "words": ["design", "develop", "product", "feature", "innovative", "test", "improve", "feedback", "quality", "service"],
        "template": "Hôm nay, ORI tham gia buổi hội thảo sáng tạo của hãng. Cô đề xuất {w0} (thiết kế) một bộ đồ dùng cá nhân thân thiện với môi trường cho hành khách. Cả đội cùng bắt tay {w1} (phát triển) mẫu thử nghiệm của {w2} (sản phẩm) mới này. Bộ đồ dùng có {w3} (đặc điểm) nhỏ gọn, tiện lợi và tự phân hủy sinh học. Đây là một ý tưởng rất {w4} (sáng tạo/đột phá). Sản phẩm đã được đưa vào {w5} (thử nghiệm) trên một vài chuyến bay quốc tế. Ý kiến đóng góp từ tổ bay giúp đội {w6} (cải tiến) sản phẩm tốt hơn. Hãng luôn ghi nhận mọi {w7} (phản hồi) của hành khách để đảm bảo {w8} (chất lượng) dịch vụ và nâng tầm {w9} (dịch vụ) cabin."
    },
    12: {
        "title": "ORI Tham Quan Nhà Máy Lắp Ráp Máy Bay",
        "words": ["produce", "factory", "assembly", "component", "check", "standard", "efficiency", "worker", "machine", "output"],
        "template": "Hãng hàng không của ORI tổ chức chuyến tham quan nhà máy cho nhân viên. Nơi đây {w0} (sản xuất) những chiếc máy bay hiện đại nhất. Trực tiếp đứng trong khu vực {w1} (nhà máy) sản xuất khổng lồ, ORI tận mắt chứng kiến dây chuyền {w2} (lắp ráp) động cơ phản lực. Từng {w3} (linh kiện/thành phần) nhỏ đều được chế tạo tỉ mỉ. Các kỹ sư {w4} (kiểm tra) kỹ lưỡng từng mối hàn để đảm bảo an toàn tuyệt đối. Mọi công đoạn đều phải đạt các {w5} (tiêu chuẩn) chất lượng quốc tế nghiêm ngặt. Việc ứng dụng công nghệ mới giúp nâng cao {w6} (hiệu suất) làm việc. Sự phối hợp nhịp nhàng giữa {w7} (công nhân) lành nghề và các loại {w8} (máy móc) tự động hóa tạo nên một {w9} (sản lượng) sản xuất vô cùng ấn tượng."
    },
    13: {
        "title": "Đào Tạo Kỹ Năng Chăm Sóc Khách Hàng",
        "words": ["passenger", "service", "complaint", "resolve", "polite", "assistance", "request", "satisfy", "help", "experience"],
        "template": "ORI đang tham gia lớp huấn luyện xử lý tình huống mặt đất. Khi {w0} (hành khách) gặp sự cố về hành lý, nhiệm vụ của cô là mang đến dịch vụ ({w1}) chu đáo nhất. Khi nhận được một {w2} (khiếu nại) từ khách, ORI phải nhanh chóng tìm cách {w3} (giải quyết) trong êm đẹp. Thái độ ứng xử cần luôn {w4} (lịch sự) và nhã nhặn. ORI sẵn sàng cung cấp sự {w5} (trợ giúp) và đáp ứng mọi {w6} (yêu cầu) hợp lý của khách hàng. Mục tiêu là làm {w7} (hài lòng) ngay cả những hành khách khó tính nhất. ORI tin rằng lòng tận tâm sẽ {w8} (giúp ích) rất nhiều để mang đến một {w9} (trải nghiệm) bay trọn vẹn và đáng nhớ."
    },
    14: {
        "title": "Hành Trình Bay Của ORI",
        "words": ["airport", "flight", "ticket", "passport", "boarding", "luggage", "delay", "gate", "destination", "passenger"],
        "template": "Hôm nay, ORI thức dậy từ 4 giờ sáng để chuẩn bị đến {w0} (sân bay). Cô sẽ tham gia một {w1} (chuyến bay) đường dài đến Tokyo. Cầm tấm vé ({w2}) và cuốn hộ chiếu ({w3}) trên tay, ORI cảm thấy vô cùng háo hức. Cô nhanh chóng hoàn tất thủ tục lên máy bay ({w4}) và gửi hành lý ({w5}). Dù thời tiết xấu làm chuyến bay bị {w6} (trì hoãn) nhẹ, ORI vẫn kiên nhẫn đợi ở cửa {w7} (cổng lên máy bay). Cuối cùng, máy bay cũng cất cánh hướng về {w8} (điểm đến). ORI mỉm cười nhìn ra cửa sổ, tự hào là một {w9} (hành khách) đặc biệt đại diện cho hãng."
    },
    15: {
        "title": "Ký Kết Hợp Đồng Mô Phỏng Bay",
        "words": ["contract", "agreement", "sign", "negotiate", "terms", "clause", "partner", "approve", "conditions", "period"],
        "template": "ORI được chọn hỗ trợ ban giám đốc chuẩn bị lễ ký kết dự án buồng lái mô phỏng. Đây là một bản {w0} (hợp đồng) lớn hợp tác với đối tác nước ngoài. Sau nhiều tuần cùng nhau soạn thảo, hai bên đã đi đến một {w1} (thỏa thuận) chung. Giám đốc hai công ty sẽ cùng nhau {w2} (ký kết) văn bản này. Các chuyên gia pháp lý đã {w3} (thương lượng) rất kỹ từng điều khoản ({w4}) hợp đồng. Mỗi {w5} (điều khoản) đều được rà soát để đảm bảo lợi ích song phương. Đối tác ({w6}) quốc tế của hãng tỏ ra rất hài lòng. Hội đồng quản trị đã chính thức {w7} (phê duyệt) các {w8} (điều kiện) hợp đồng, mở ra một {w9} (giai đoạn/thời kỳ) hợp tác phát triển bền vững."
    },
    16: {
        "title": "Giao Dịch Nâng Hạng Ghế Của ORI",
        "words": ["pay", "transaction", "price", "card", "currency", "receipt", "fee", "charge", "bill", "account"],
        "template": "Hành khách muốn đổi sang ghế hạng thương gia, ORI nhiệt tình hướng dẫn khách {w0} (thanh toán). Quá trình {w1} (giao dịch) diễn ra nhanh chóng tại quầy. Mức chênh lệch {w2} (giá cả) đã được hiển thị rõ ràng trên hệ thống. Khách hàng quẹt {w3} (thẻ) tín dụng để hoàn tất. Do giao dịch quốc tế, hệ thống tự động quy đổi sang {w4} (tiền tệ) bản địa của khách. ORI in hóa đơn ({w5}) và gửi kèm cho khách hàng. Không có bất kỳ khoản {w6} (lệ phí) ẩn nào bị {w7} (tính phí) thêm ngoài quy định. Sau khi kiểm tra hóa đơn ({w8}), khách hàng hài lòng ký xác nhận. Số tiền lập tức được hạch toán vào {w9} (tài khoản) doanh thu của chi nhánh."
    },
    17: {
        "title": "ORI Điều Phối Vận Chuyển Hàng Hóa",
        "words": ["ship", "cargo", "freight", "delivery", "transport", "warehouse", "package", "tracking", "logistics", "delay"],
        "template": "Hôm nay, ORI được tham quan bộ phận vận chuyển hàng hóa hàng không. Cô học cách {w0} (vận chuyển) các kiện hàng quốc tế lớn. Các khoang hàng ({w1}) trên máy bay chứa đầy thực phẩm và linh kiện y tế. Chi phí cước vận chuyển ({w2}) được tính toán dựa trên khối lượng. ORI theo dõi quá trình {w3} (giao hàng) từ lúc xe tải {w4} (vận chuyển) hàng đến sân bay. Hàng hóa được phân loại và xếp ngăn nắp trong nhà kho ({w5}) rộng lớn. Mỗi hộp đóng gói ({w6}) đều được dán mã để thuận tiện cho việc {w7} (theo dõi) trực tuyến. Sự chuyên nghiệp trong quy trình {w8} (hậu cần) giúp giảm thiểu tối đa tình trạng {w9} (trì hoãn) giao nhận hàng hóa."
    },
    18: {
        "title": "Kỳ Nghỉ Nghỉ Chân Của ORI Tại Tokyo",
        "words": ["hotel", "room", "stay", "reservation", "restaurant", "menu", "food", "service"],
        "template": "Sau chuyến bay dài đầy vất vả, ORI và phi hành đoàn check-in tại một {w0} (khách sạn) 5 sao ở trung tâm Tokyo. Cô nhận khóa {w1} (phòng) và tranh thủ tắm rửa, nghỉ ngơi. Tổ bay sẽ {w2} (ở lại/nghỉ chân) tại đây hai ngày trước khi bay về. Nhờ có {w3} (sự đặt chỗ) từ trước, mọi thủ tục diễn ra cực kỳ nhanh chóng. Buổi tối, ORI cùng mọi người dùng bữa tại {w4} (nhà hàng) truyền thống của Nhật Bản. Người phục vụ đưa ra cuốn {w5} (thực đơn) với vô vàn món ăn hấp dẫn. ORI hào hứng thưởng thức các món ăn ({w6}) sashimi tươi ngon. Cô vô cùng hài lòng với phong cách phục vụ ({w7}) tinh tế và sự hiếu khách của con người nơi đây."
    }
}

# Split by pages
pages = re.split(r'<!-- PDF_PAGE: \d+ -->', content)

# Group pages by day
day_pages = {}
current_day = 0

for i, page in enumerate(pages):
    lines = page.split('\n')
    for line in lines[:10]:
        day_match = re.search(r'DAY\s*0?(\d+)\b', line, re.IGNORECASE)
        if day_match and "checkup" not in line.lower():
            day_num = int(day_match.group(1))
            if day_num in DAY_INFO:
                current_day = day_num
                break
    
    if current_day > 0:
        if current_day not in day_pages:
            day_pages[current_day] = []
        day_pages[current_day].append(page)

# Common English function words
english_stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'to', 'for', 'with', 'in', 'on', 'at', 'by', 'of', 'from', 'this', 'that', 'these', 'those', 'it', 'they', 'we', 'you', 'he', 'she', 'his', 'her', 'their', 'our', 'your', 'my', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might', 'must', 'be', 'been', 'being'}

# Vietnamese words without accents that might look like ASCII English
viet_no_accents = {'cho', 'tin', 'nhung', 'va', 'cua', 'trong', 'co', 'duoc', 'nguoi', 'tuyen', 'dung', 'yeu', 'cau', 'dieu', 'kien'}

# POS mapping table with common OCR typos mapped to correct standard codes
pos_map = {
    "v": "v", "V": "v", "y": "v",
    "n": "n", "N": "n", "rn": "n", "ri": "n", "à": "n", "ñ": "n",
    "adj": "adj", "ADJ": "adj", "aelj": "adj", "adi": "adj", "ad": "adj", "aci": "adj", "ad)": "adj", "ad}": "adj",
    "adv": "adv", "ADV": "adv", "adlv": "adv", "adly": "adv",
    "phr": "phr", "ph": "phr", "ph)": "phr",
    "prep": "prep", "conj": "conj"
}

# Blacklist of raw words to ignore
blacklist = {'day', 'pdf_page', 'trang pdf', 'tỷ lệ xuất hiện rất cao', 'tỷ lệ xuất hiện cao', 'tỷ lệ xuất hiện trung bình', 
             'từ vựng thường gặp trong part', 'từ vựng thường gặp trong', 'tuyển dụng', 'phép tắc', 'quy định', 
             'công việc', 'văn phòng', 'trang', 'pdf', 'hackers', 'vocabulary', 'daily', 'checkup', 'tào', 'cao', 't cao'}

def clean_word(w):
    w = w.strip()
    w = re.sub(r'^[\'"`\s\-\*]+', '', w)
    w = re.sub(r'[\'"`\s\-\*]+$', '', w)
    w = re.sub(r'^(n|v|adj|adv|phr)\s+', '', w, flags=re.IGNORECASE)
    return w.strip()

def has_vietnamese_accents(text):
    return bool(re.search(r'[áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđĐ]', text))

def clean_block_metadata(text, word):
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        if '[' in line or ']' in line or '**' in line or '()' in line:
            continue
        if '*' in line and any(w in line.lower() for w in [word, 'condition', 'employment', 'identify', 'associate']):
            continue
        clean_lines.append(line)
    return '\n'.join(clean_lines).strip()


# Strict check for Vietnamese accents (ignores standard English/French loanword letters like é, è, á, à, ù)
def has_vietnamese_accents_strict(text):
    clean = text.lower().replace('é', 'e').replace('è', 'e').replace('á', 'a').replace('à', 'a').replace('ù', 'u')
    return bool(re.search(r'[ảãạăắằẳẵặâấầẩẫậêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợủũụưứừửữựýỳỷỹỵđĐ]', clean))

def to_ascii(text):
    text = text.lower()
    text = text.replace('é', 'e').replace('è', 'e').replace('á', 'a').replace('à', 'a').replace('ù', 'u')
    return re.sub(r'[^a-z]', '', text)

def is_ascii_word(word):
    w = re.sub(r'[^a-zA-Z]', '', word)
    if not w:
        return False
    return not has_vietnamese_accents_strict(word)

def clean_ipa(text):
    text = text.lower()
    text = text.replace('æ', 'a').replace('ó', 'o').replace('á', 'a').replace('ə', 'e').replace(':', '')
    text = text.replace('uK', '').replace('uk', '').replace('us', '')
    return re.sub(r'[^a-z]', '', text).strip()

def clean_word_for_matching(text):
    return to_ascii(text)

def split_vietnamese_english_v3(word, block_text):
    # Find POS from start
    pos_match = re.match(r'^([a-zA-ZÀ-ÿ\)\}\(\s]+)\s+', block_text.strip())
    pos_raw = pos_match.group(1).strip() if pos_match else ""
    pos = pos_map.get(pos_raw, "n")
    text_no_pos = re.sub(r'^' + re.escape(pos_raw) + r'\s+', '', block_text.strip()) if pos_raw else block_text.strip()
    
    words_list = text_no_pos.split()
    
    # Find the index of the word containing the target word or its fuzzy match
    target_idx = -1
    word_base = to_ascii(word)[:4]
    
    for i, w in enumerate(words_list):
        w_clean = to_ascii(w)
        is_match = False
        if to_ascii(word) == "meet" and w_clean in ["meet", "meets", "meeting", "meetings", "met"]:
            is_match = True
        elif to_ascii(word) == "applicant" and ("ipplicant" in w_clean or "applicant" in w_clean or "apply" in w_clean):
            is_match = True
        elif word_base in w_clean:
            is_match = True
            
        if is_match:
            target_idx = i
            break
            
    if target_idx == -1:
        # Fallback if target word not found: search by stopwords sequence
        for i in range(len(words_list)):
            if i + 2 < len(words_list):
                w1 = re.sub(r'[^a-zA-Z]', '', words_list[i])
                w2 = re.sub(r'[^a-zA-Z]', '', words_list[i+1])
                w3 = re.sub(r'[^a-zA-Z]', '', words_list[i+2])
                if w1 and w2 and w3 and not has_vietnamese_accents_strict(words_list[i]) and not has_vietnamese_accents_strict(words_list[i+1]) and not has_vietnamese_accents_strict(words_list[i+2]):
                    has_stopword = w1.lower() in english_stopwords or w2.lower() in english_stopwords or w3.lower() in english_stopwords
                    is_single = len(w1) == 1 and w1.isupper()
                    if has_stopword or is_single or len(w1) > 2:
                        target_idx = i
                        break
                        
    if target_idx == -1:
        return pos, text_no_pos, ""
        
    # Scan backwards from target_idx to find the start of the English sentence
    start_idx = target_idx
    for i in range(target_idx - 1, -1, -1):
        w = words_list[i]
        w_clean = to_ascii(w)
        
        # Stop if the word has Vietnamese accents
        if has_vietnamese_accents_strict(w):
            break
            
        # Stop if the word is in the Vietnamese unaccented blocklist
        if w_clean.lower() in viet_no_accents:
            break
            
        # Stop if we hit a capitalized word (sentence start boundary)
        if w and w[0].isupper() and w_clean.lower() not in viet_no_accents:
            start_idx = i
            break
            
        if is_ascii_word(w):
            start_idx = i
        else:
            break
            
    meaning_vi = ' '.join(words_list[:start_idx])
    english_vi_part = ' '.join(words_list[start_idx:])
    return pos, meaning_vi, english_vi_part

# Parse English and Vietnamese examples from english_vi_part
def parse_examples(english_vi_part):
    # Split by sentence boundaries or newlines
    sentences = re.split(r'(?<=[.!?])\s+|\n', english_vi_part)
    sentences = [s.strip() for s in sentences if s.strip()]
    if sentences:
        en_ex = sentences[0]
        vi_ex = ""
        rest = []
        
        # Check if the first sentence contains merged English and Vietnamese text
        words_in_sent = en_ex.split()
        split_at = -1
        for j, w in enumerate(words_in_sent):
            if has_vietnamese_accents_strict(w) and j > 3:
                split_at = j
                break
                
        if split_at != -1:
            vi_ex = ' '.join(words_in_sent[split_at:])
            en_ex = ' '.join(words_in_sent[:split_at])
            rest = sentences[1:]
        else:
            if len(sentences) > 1:
                if has_vietnamese_accents_strict(sentences[1]):
                    vi_ex = sentences[1]
                    rest = sentences[2:]
                else:
                    en_ex += " " + sentences[1]
                    if len(sentences) > 2:
                        vi_ex = sentences[2]
                        rest = sentences[3:]
                        
        # Strip trailing OCR junk words commonly found at the end of English examples
        en_ex = re.sub(r'\s+ác$', '', en_ex.strip())
        return en_ex.strip(), vi_ex.strip(), rest
    return "", "", []

# Main parsing loop
for day_num, info in DAY_INFO.items():
    pages_list = day_pages.get(day_num, [])
    words_data = []
    
    for p_idx, p in enumerate(pages_list):
        # Skip non-vocab pages
        if "checkup" in p.lower() or "tuyển dụng | 26" in p.lower():
            continue
            
        # Extract raw words with stars
        words_raw = re.findall(r'[\'"]?([a-zA-ZÀ-ÿ\s\-\’\:\.]+)\*+', p)
        page_words = []
        for w in words_raw:
            w_clean = clean_word(w)
            # Skip false positives that contain too many words (header chunks containing stars)
            if len(w_clean.split()) > 3:
                continue
            if len(w_clean) > 2 and w_clean not in blacklist:
                stars_match = re.search(re.escape(w) + r'(\*+)', p)
                freq = len(stars_match.group(1)) if stars_match else 2
                freq = min(max(freq, 1), 3)
                page_words.append({
                    "word": w_clean,
                    "frequency": freq
                })
                
        # Find POS tags with typo tolerance (matches start-of-line or whitespace prefix)
        pos_pattern = r'(?:^|\s)\b(n|v|adj|adv|phr|prep|conj|aelj|adi|ad\)|ad\}|ad|aci|rn|ri|à|ñ|V|N|ADJ|ADV|ph|ph\))\b(?=\s)'
        pos_matches = list(re.finditer(pos_pattern, p))
        
        # Split text into blocks
        page_blocks = []
        for idx, m in enumerate(pos_matches):
            start = m.start(1)
            end = pos_matches[idx+1].start(1) if idx + 1 < len(pos_matches) else len(p)
            page_blocks.append({
                "pos": m.group(1),
                "text": p[start:end].strip()
            })
            
        if not page_words or not page_blocks:
            continue
            
        # Find word position indexes for phonetic mapping and distance calculation
        word_positions = []
        for pw in page_words:
            w_pat = re.compile(re.escape(pw["word"]) + r'\*+', re.IGNORECASE)
            w_match = w_pat.search(p)
            if w_match:
                word_positions.append({"word": pw["word"], "pos": w_match.start()})
        
        # Find all brackets on the page for pronunciations
        bracket_matches = list(re.finditer(r'\[([^\]]{1,35})\]', p))
        brackets = []
        for m in bracket_matches:
            ipa = m.group(1)
            # Avoid blacklist notes (with dot-restriction to avoid matching words ending in ant/syn)
            if not any(k in ipa.lower() for k in ['syn.', 'der.', 'ant.', 'v.', 'n.', 'yn)']):
                brackets.append({"ipa": ipa, "pos": m.start()})
                
        # Map brackets to words using combined SequenceMatcher + spatial distance score
        word_ipas = {pw["word"]: [] for pw in page_words}
        for b in brackets:
            best_word = None
            best_score = -1
            
            for wp in word_positions:
                w_c = clean_word_for_matching(wp["word"])
                i_c = clean_ipa(b["ipa"])
                if not w_c or not i_c:
                    continue
                    
                ratio = difflib.SequenceMatcher(None, w_c, i_c).ratio()
                
                # Plausibility threshold (ratio must be at least 0.45)
                if ratio < 0.45:
                    continue
                    
                distance = abs(wp["pos"] - b["pos"])
                distance_factor = 1.0 / (1.0 + distance / 100.0)
                score = ratio + 0.5 * distance_factor
                
                if score > best_score:
                    best_score = score
                    best_word = wp["word"]
                    
            if best_word:
                word_ipas[best_word].append(b["ipa"])
                
        # Map blocks to page words semantically using English example content check + spatial distance
        for b in page_blocks:
            # Extract POS, Meaning, and Examples roughly for matching
            pos_tag = b["pos"]
            pos, meaning_vi_raw, eng_vi_raw = split_vietnamese_english_v3("dummy", b["text"])
            example_en_raw, example_vi_raw, _ = parse_examples(eng_vi_raw)
            
            # Find the best page word for this block
            matched_word_obj = None
            
            # If the number of words equals the number of blocks, align in order of appearance
            if len(page_words) == len(page_blocks):
                block_idx = page_blocks.index(b)
                matched_word_obj = page_words[block_idx]
            else:
                best_match_score = -1
                en_clean = to_ascii(example_en_raw)
                meaning_clean = to_ascii(meaning_vi_raw)
                
                for wp in word_positions:
                    w_clean = to_ascii(wp["word"])
                    w_base = w_clean[:4]
                    
                    # Base content match score
                    score = 0
                    if en_clean and w_base in en_clean:
                        score = difflib.SequenceMatcher(None, w_clean, en_clean).ratio()
                        # Add exact start match bonus
                        if en_clean.startswith(w_base):
                            score += 0.3
                    elif w_base in meaning_clean:
                        score = 0.2
                        
                    # Add spatial distance factor (blocks near word declarations are highly likely to match them)
                    distance = abs(wp["pos"] - (pos_matches[page_blocks.index(b)].start(1)))
                    distance_factor = 1.0 / (1.0 + distance / 100.0)
                    score += 0.2 * distance_factor
                    
                    if score > best_match_score:
                        best_match_score = score
                        # Find frequency and other word attributes
                        for w_raw in page_words:
                            if w_raw["word"] == wp["word"]:
                                matched_word_obj = w_raw
                                break
                                
                # If the best score is very low (completely unrelated), ignore this block
                if best_match_score < 0.15:
                    matched_word_obj = None
                    
            if not matched_word_obj:
                continue
                
            w_name = matched_word_obj["word"]
            
            # Clean block metadata before final precise split
            cleaned_text = clean_block_metadata(b["text"], w_name)
            pos, meaning_vi, eng_vi = split_vietnamese_english_v3(w_name, cleaned_text)
            pos = pos_map.get(pos_tag, pos)
            example_en, example_vi, rest_parts = parse_examples(eng_vi)
            
            # Capitalization split fallback for Vietnamese example sentences
            if not example_vi and meaning_vi:
                meaning_words = meaning_vi.split()
                split_at = -1
                for idx, w in enumerate(meaning_words):
                    if idx > 0 and w and w[0].isupper() and has_vietnamese_accents(w) and idx < len(meaning_words) - 1:
                        if w not in ["TOEIC", "Part", "Part-time"]:
                            split_at = idx
                            break
                if split_at != -1:
                    example_vi = ' '.join(meaning_words[split_at:])
                    meaning_vi = ' '.join(meaning_words[:split_at])
            
            # Clean up meaningVi by removing other word spelling declarations at the end
            meaning_vi = re.sub(r'[\s\"\'“‟’”\-—–—\d\+\*]*\b(condition|employment|identify|associate|diligent|familiar|proficiency|lack|managerial)\b.*$', '', meaning_vi, flags=re.IGNORECASE).strip()
            meaning_vi = re.sub(r'^[a-zA-ZÀ-ÿ\s\-+/\(\)]+\s+điều kiện\s+', '', meaning_vi)
            meaning_vi = re.sub(r'^[a-zA-Z\s\-+/\(\)]+\s+', '', meaning_vi)
            meaning_vi = meaning_vi.split('  ')[0].strip()
            
            # Parse notes, derivatives, synonyms, antonyms
            derivatives = []
            synonyms = []
            antonyms = []
            toeic_notes = []
            
            for note in rest_parts:
                note_str = note.strip()
                if not note_str:
                    continue
                    
                if re.search(r'\bder[\./\]]?\s+', note_str, re.IGNORECASE):
                    clean_der = re.sub(r'^der[\./\]]?\s*', '', note_str, flags=re.IGNORECASE).strip()
                    der_matches = re.finditer(r'([a-zA-Z\s\’\-]+)\s*\((n|v|adj|adv|phr)\)\s+(.+?)(?=\s+[a-zA-Z\s\’\-]+\s*\((?:n|v|adj|adv|phr)\)|$)', clean_der)
                    for m in der_matches:
                        derivatives.append({
                            "word": m.group(1).strip(),
                            "partOfSpeech": m.group(2).strip(),
                            "meaningVi": m.group(3).strip().rstrip(', ')
                        })
                elif re.search(r'\bsyn[\./\]]?\s+', note_str, re.IGNORECASE):
                    clean_syn = re.sub(r'^syn[\./\]]?\s*', '', note_str, flags=re.IGNORECASE).strip()
                    syns = [s.strip() for s in re.split(r'[,;]\s*|\s+or\s+', clean_syn) if s.strip()]
                    for s in syns:
                        s_eng = re.findall(r'^[a-zA-Z\s\-]+', s)
                        if s_eng:
                            synonyms.append(s_eng[0].strip())
                elif re.search(r'\bant[\./\]]?\s+', note_str, re.IGNORECASE):
                    clean_ant = re.sub(r'^ant[\./\]]?\s*', '', note_str, flags=re.IGNORECASE).strip()
                    ants = [a.strip() for a in re.split(r'[,;]\s*|\s+or\s+', clean_ant) if a.strip()]
                    for a in ants:
                        a_eng = re.findall(r'^[a-zA-Z\s\-]+', a)
                        if a_eng:
                            antonyms.append(a_eng[0].strip())
                else:
                    clean_note = re.sub(r'^(cum|Barthi|TOEIC|GaD)\s*', '', note_str, flags=re.IGNORECASE).strip()
                    if clean_note:
                        toeic_notes.append(clean_note)
                        
            # Map pronunciations
            ipas_list = word_ipas.get(w_name, [])
            uk_ipa = ""
            us_ipa = ""
            for ipa in ipas_list:
                ipa_clean = re.sub(r'^(uk|us)\s+', '', ipa, flags=re.IGNORECASE).strip()
                if 'uk' in ipa.lower():
                    uk_ipa = ipa_clean
                elif 'us' in ipa.lower():
                    us_ipa = ipa_clean
                else:
                    if not uk_ipa:
                        uk_ipa = ipa_clean
                    elif not us_ipa:
                        us_ipa = ipa_clean
                        
            if uk_ipa and not us_ipa:
                us_ipa = uk_ipa
            elif us_ipa and not uk_ipa:
                uk_ipa = us_ipa
                
            vocab_entry = {
                "id": w_name.replace(" ", "-"),
                "word": w_name,
                "partOfSpeech": pos,
                "pronunciation": {
                    "uk": f"/{uk_ipa}/" if uk_ipa else "",
                    "us": f"/{us_ipa}/" if us_ipa else ""
                },
                "frequency": matched_word_obj["frequency"],
                "meaningVi": meaning_vi,
                "exampleEn": example_en,
                "exampleVi": example_vi,
                "derivatives": derivatives,
                "synonyms": synonyms,
                "antonyms": antonyms,
                "toeicNotes": toeic_notes,
                "needsReview": False
            }
            words_data.append(vocab_entry)

    # Apply manual corrections for Day 1
    if day_num == 1:
        words_data = [
            {
                "id": "inform",
                "word": "inform",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈfɔːm/", "us": "/ɪnˈfɔːrm/"},
                "frequency": 3,
                "meaningVi": "báo, báo tin",
                "exampleEn": "Please inform the director that the meeting has been canceled.",
                "exampleVi": "Vui lòng báo cho giám đốc biết là cuộc họp đã bị hủy.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "Phân biệt inform và explain:",
                    "- inform + tân ngữ chỉ người + of sth/that-clause: báo cho ai biết về điều gì.",
                    "- explain + to + tân ngữ chỉ người: giải thích cho ai đó."
                ],
                "needsReview": False
            },
            {
                "id": "resume",
                "word": "résumé",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈrezjuːmeɪ/", "us": "/ˈrezəmeɪ/"},
                "frequency": 2,
                "meaningVi": "sơ yếu lý lịch",
                "exampleEn": "Fax your résumé and cover letter to the above number.",
                "exampleVi": "Hãy gửi sơ yếu lý lịch và đơn xin việc của bạn qua fax đến số bên trên.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "opening",
                "word": "opening",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈəʊpənɪŋ/", "us": "/ˈoʊpnɪŋ/"},
                "frequency": 2,
                "meaningVi": "vị trí trống, sự mở cửa, lễ khai trương",
                "exampleEn": "There are several job openings at the restaurant right now.",
                "exampleVi": "Ngay bây giờ đang có một vài vị trí công việc còn trống ở nhà hàng.",
                "derivatives": [],
                "synonyms": ["vacancy"],
                "antonyms": [],
                "toeicNotes": [
                    "have an opening: có vị trí công việc trống (danh từ đếm được, dùng an opening hoặc openings)."
                ],
                "needsReview": False
            },
            {
                "id": "applicant",
                "word": "applicant",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈæplɪkənt/", "us": "/ˈæplɪkənt/"},
                "frequency": 3,
                "meaningVi": "ứng viên, người nộp đơn xin việc",
                "exampleEn": "Applicants are required to submit a résumé.",
                "exampleVi": "Các ứng viên được yêu cầu phải nộp sơ yếu lý lịch.",
                "derivatives": [
                    {"word": "apply", "partOfSpeech": "v", "meaningVi": "áp dụng, ứng tuyển"},
                    {"word": "application", "partOfSpeech": "n", "meaningVi": "đơn ứng tuyển, sự ứng dụng"},
                    {"word": "appliance", "partOfSpeech": "n", "meaningVi": "thiết bị, dụng cụ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "complete/submit/receive + an application: hoàn thành/nộp/nhận đơn ứng tuyển.",
                    "Phân biệt applicant (người nộp đơn) và application (đơn xin việc, sự ứng dụng)."
                ],
                "needsReview": False
            },
            {
                "id": "requirement",
                "word": "requirement",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈkwaɪəmənt/", "us": "/rɪˈkwaɪrmənt/"},
                "frequency": 1,
                "meaningVi": "điều kiện cần thiết, yêu cầu",
                "exampleEn": "A driver's license is a requirement of this job.",
                "exampleVi": "Giấy phép lái xe là một điều kiện cần cho công việc này.",
                "derivatives": [
                    {"word": "require", "partOfSpeech": "v", "meaningVi": "yêu cầu"}
                ],
                "synonyms": ["prerequisite"],
                "antonyms": [],
                "toeicNotes": [
                    "requirement + of/for: yêu cầu/điều kiện cần cho."
                ],
                "needsReview": False
            },
            {
                "id": "meet",
                "word": "meet",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/miːt/", "us": "/miːt/"},
                "frequency": 3,
                "meaningVi": "thỏa mãn, đáp ứng (yêu cầu, điều kiện)",
                "exampleEn": "Applicants must meet all the requirements for the job.",
                "exampleVi": "Các ứng viên phải đáp ứng tất cả yêu cầu của công việc.",
                "derivatives": [],
                "synonyms": ["satisfy", "fulfill"],
                "antonyms": [],
                "toeicNotes": [
                    "meet one's needs: đáp ứng nhu cầu của ai đó",
                    "meet requirements: đáp ứng các yêu cầu/đòi hỏi",
                    "meet customer demand: đáp ứng yêu cầu của khách hàng",
                    "meet expectations: thỏa mãn mong đợi"
                ],
                "needsReview": False
            },
            {
                "id": "qualified",
                "word": "qualified",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈkwɒlɪfaɪd/", "us": "/ˈkwɑːlɪfaɪd/"},
                "frequency": 3,
                "meaningVi": "đủ khả năng, trình độ, điều kiện",
                "exampleEn": "People with master's degrees are qualified for the research position.",
                "exampleVi": "Những người có bằng thạc sĩ thì đủ điều kiện cho vị trí nghiên cứu này.",
                "derivatives": [
                    {"word": "qualify", "partOfSpeech": "v", "meaningVi": "đủ điều kiện, phù hợp"},
                    {"word": "qualification", "partOfSpeech": "n", "meaningVi": "phẩm chất, năng lực, bằng cấp"}
                ],
                "synonyms": ["certified"],
                "antonyms": ["ineligible"],
                "toeicNotes": [
                    "be qualified for: đủ điều kiện/năng lực cho cái gì.",
                    "qualifications for: tiêu chuẩn/bằng cấp cho cái gì."
                ],
                "needsReview": False
            },
            {
                "id": "candidate",
                "word": "candidate",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈkændɪdət/", "us": "/ˈkændɪdət/"},
                "frequency": 3,
                "meaningVi": "ứng viên, thí sinh",
                "exampleEn": "Five candidates will be selected for final interviews.",
                "exampleVi": "Năm ứng viên sẽ được chọn vào vòng phỏng vấn cuối cùng.",
                "derivatives": [],
                "synonyms": ["applicant"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "confidence",
                "word": "confidence",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈkɒnfɪdəns/", "us": "/ˈkɑːnfɪdəns/"},
                "frequency": 2,
                "meaningVi": "sự tự tin, sự tin tưởng, lòng tin",
                "exampleEn": "We have confidence that she can handle the position.",
                "exampleVi": "Chúng tôi có lòng tin rằng cô ấy có thể đảm đương được vị trí này.",
                "derivatives": [
                    {"word": "confident", "partOfSpeech": "adj", "meaningVi": "tự tin, tin tưởng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "show/express confidence in: thể hiện sự tin tưởng vào...",
                    "in confidence: bí mật."
                ],
                "needsReview": False
            },
            {
                "id": "highly",
                "word": "highly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈhaɪli/", "us": "/ˈhaɪli/"},
                "frequency": 1,
                "meaningVi": "rất, hết sức",
                "exampleEn": "Mr. Monroe's experience makes him highly qualified for the job.",
                "exampleVi": "Kinh nghiệm của Monroe khiến ông ấy rất phù hợp với công việc này.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "highly + competent/recommended/qualified: rất có năng lực/được đề xuất/đủ điều kiện."
                ],
                "needsReview": False
            },
            {
                "id": "professional-adj",
                "word": "professional",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/prəˈfeʃənl/", "us": "/prəˈfeʃənl/"},
                "frequency": 3,
                "meaningVi": "chuyên nghiệp, lành nghề, có tính chuyên môn",
                "exampleEn": "Jeff is known as a professional photographer.",
                "exampleVi": "Jeff được biết đến như một nhiếp ảnh gia chuyên nghiệp.",
                "derivatives": [
                    {"word": "profession", "partOfSpeech": "n", "meaningVi": "nghề nghiệp"},
                    {"word": "professionally", "partOfSpeech": "adv", "meaningVi": "một cách chuyên nghiệp"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "professional-n",
                "word": "professional",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/prəˈfeʃənl/", "us": "/prəˈfeʃənl/"},
                "frequency": 3,
                "meaningVi": "chuyên gia",
                "exampleEn": "Merseyside Hospital is looking for a certified health professional.",
                "exampleVi": "Bệnh viện Merseyside đang tìm kiếm một chuyên gia y tế có bằng cấp.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "interview-n",
                "word": "interview",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɪntəvjuː/", "us": "/ˈɪntərvjuː/"},
                "frequency": 3,
                "meaningVi": "cuộc phỏng vấn",
                "exampleEn": "The interviews are being held in meeting room three.",
                "exampleVi": "Các cuộc phỏng vấn đang được thực hiện tại phòng họp số ba.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "interview-v",
                "word": "interview",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɪntəvjuː/", "us": "/ˈɪntərvjuː/"},
                "frequency": 3,
                "meaningVi": "phỏng vấn",
                "exampleEn": "The manager interviewed almost 100 applicants.",
                "exampleVi": "Vị quản lý này đã phỏng vấn gần 100 ứng viên.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "hire",
                "word": "hire",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈhaɪə(r)/", "us": "/ˈhaɪər/"},
                "frequency": 3,
                "meaningVi": "thuê mướn, tuyển dụng",
                "exampleEn": "The company expects to hire several new employees next month.",
                "exampleVi": "Công ty kỳ vọng sẽ tuyển được vài nhân viên mới vào tháng tới.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["lay off", "dismiss", "fire"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "training",
                "word": "training",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈtreɪnɪŋ/", "us": "/ˈtreɪnɪŋ/"},
                "frequency": 3,
                "meaningVi": "sự đào tạo, huấn luyện",
                "exampleEn": "This company offers on-the-job training for new staff.",
                "exampleVi": "Công ty này cung cấp chương trình đào tạo tại chỗ cho nhân viên mới.",
                "derivatives": [
                    {"word": "train", "partOfSpeech": "v", "meaningVi": "đào tạo, huấn luyện"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "reference",
                "word": "reference",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈrefrəns/", "us": "/ˈrefrəns/"},
                "frequency": 3,
                "meaningVi": "sự giới thiệu, tài liệu tham khảo",
                "exampleEn": "Philip asked his previous employer to write a reference letter for him.",
                "exampleVi": "Philip nhờ quản lý cũ của mình viết một lá thư giới thiệu cho anh ấy.",
                "derivatives": [
                    {"word": "refer", "partOfSpeech": "v", "meaningVi": "tham khảo"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "reference letter: thư giới thiệu",
                    "reference material: tài liệu tham khảo"
                ],
                "needsReview": False
            },
            {
                "id": "position-n",
                "word": "position",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/pəˈzɪʃn/", "us": "/pəˈzɪʃn/"},
                "frequency": 2,
                "meaningVi": "chức vụ, vị trí",
                "exampleEn": "The advertised position provides health care and other benefits.",
                "exampleVi": "Vị trí được quảng cáo đó chu cấp dịch vụ chăm sóc sức khỏe và các phúc lợi khác.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "accept a position: chấp nhận vị trí làm việc",
                    "apply for a position: ứng tuyển cho một vị trí"
                ],
                "needsReview": False
            },
            {
                "id": "position-v",
                "word": "position",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/pəˈzɪʃn/", "us": "/pəˈzɪʃn/"},
                "frequency": 2,
                "meaningVi": "định vị, đặt vào vị trí",
                "exampleEn": "The secretary positioned the chairs around the table before the meeting began.",
                "exampleVi": "Thư ký xếp ghế xung quanh bàn trước khi cuộc họp bắt đầu.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "achievement",
                "word": "achievement",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ə'tʃi:vmənt/", "us": "/ə'tʃi:vmənt/"},
                "frequency": 3,
                "meaningVi": "thành tựu, thành tích, sự đạt được",
                "exampleEn": "List all of your achievements from previous jobs on your résumé.",
                "exampleVi": "Hãy liệt kê tất cả những thành tích của bạn trong công việc trước vào bản sơ yếu lý lịch.",
                "derivatives": [
                    {"word": "achieve", "partOfSpeech": "v", "meaningVi": "đạt được"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "impressed",
                "word": "impressed",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪmˈprest/", "us": "/ɪmˈprest/"},
                "frequency": 3,
                "meaningVi": "ấn tượng, cảm phục",
                "exampleEn": "The CEO was impressed by his assistant's organizing skills.",
                "exampleVi": "Vị giám đốc điều hành đã bị ấn tượng bởi kỹ năng tổ chức của viên thư ký đó.",
                "derivatives": [
                    {"word": "impress", "partOfSpeech": "v", "meaningVi": "gây ấn tượng"},
                    {"word": "impressive", "partOfSpeech": "adj", "meaningVi": "đầy ấn tượng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "be impressed by/with: bị ấn tượng bởi...",
                    "Phân biệt: impressed miêu tả cảm xúc con người, impressive miêu tả đặc điểm đối tượng."
                ],
                "needsReview": False
            },
            {
                "id": "excellent",
                "word": "excellent",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈeksələnt/", "us": "/ˈeksələnt/"},
                "frequency": 3,
                "meaningVi": "xuất sắc, vượt trội, ưu tú",
                "exampleEn": "Because of her excellent managerial skills, Erin was hired for the job.",
                "exampleVi": "Nhờ kỹ năng quản lý xuất sắc của mình, Erin đã được tuyển dụng làm công việc này.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "eligible",
                "word": "eligible",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈelɪdʒəbl/", "us": "/ˈelɪdʒəbl/"},
                "frequency": 2,
                "meaningVi": "đủ tư cách, thích hợp",
                "exampleEn": "The part-time workers are also eligible for paid holidays.",
                "exampleVi": "Các nhân viên bán thời gian cũng đủ điều kiện để được nghỉ phép có trả lương.",
                "derivatives": [
                    {"word": "eligibility", "partOfSpeech": "n", "meaningVi": "sự đủ tư cách"}
                ],
                "synonyms": [],
                "antonyms": ["ineligible"],
                "toeicNotes": [
                    "be eligible for + noun: đủ điều kiện nhận cái gì.",
                    "be eligible to do sth: đủ điều kiện làm việc gì."
                ],
                "needsReview": False
            },
            {
                "id": "identify",
                "word": "identify",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/aɪˈdentɪfaɪ/", "us": "/aɪˈdentɪfaɪ/"},
                "frequency": 2,
                "meaningVi": "nhận diện, nhận ra",
                "exampleEn": "Staff members wear uniforms so that they are easy for customers to identify.",
                "exampleVi": "Các nhân viên mặc đồng phục để khách hàng dễ dàng nhận ra họ.",
                "derivatives": [
                    {"word": "identification", "partOfSpeech": "n", "meaningVi": "sự nhận dạng, chứng minh thư"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "associate",
                "word": "associate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈsəʊʃieɪt/", "us": "/əˈsoʊʃieɪt/"},
                "frequency": 2,
                "meaningVi": "liên kết, kết giao",
                "exampleEn": "Two of the applicants were associated with a competitor.",
                "exampleVi": "Hai trong số các ứng viên có liên kết với một đối thủ.",
                "derivatives": [
                    {"word": "association", "partOfSpeech": "n", "meaningVi": "sự hợp tác, hiệp hội"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "be associated with: có liên kết/liên quan tới..."
                ],
                "needsReview": False
            },
            {
                "id": "condition",
                "word": "condition",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kənˈdɪʃn/", "us": "/kənˈdɪʃn/"},
                "frequency": 1,
                "meaningVi": "điều kiện",
                "exampleEn": "The conditions of employment are listed in the job.",
                "exampleVi": "Những điều kiện của công việc được liệt kê trong thông báo tuyển dụng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "employment",
                "word": "employment",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪmˈplɔɪmənt/", "us": "/ɪmˈplɔɪmənt/"},
                "frequency": 2,
                "meaningVi": "việc làm",
                "exampleEn": "The company announced employment opportunities in the personnel department.",
                "exampleVi": "Công ty đã thông báo những cơ hội việc làm ở phòng nhân sự.",
                "derivatives": [
                    {"word": "employ", "partOfSpeech": "v", "meaningVi": "thuê, tuyển dụng"},
                    {"word": "employee", "partOfSpeech": "n", "meaningVi": "nhân viên"},
                    {"word": "employer", "partOfSpeech": "n", "meaningVi": "người sử dụng lao động"}
                ],
                "synonyms": [],
                "antonyms": ["unemployment"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "lack-v",
                "word": "lack",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/læk/", "us": "/læk/"},
                "frequency": 2,
                "meaningVi": "thiếu, không có",
                "exampleEn": "Carl lacked the ability to get along well with his coworkers.",
                "exampleVi": "Carl không có khả năng hòa nhập với các đồng nghiệp của mình.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "lack-n",
                "word": "lack",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/læk/", "us": "/læk/"},
                "frequency": 2,
                "meaningVi": "sự thiếu hụt",
                "exampleEn": "Due to a lack of funds, the project has been temporarily halted.",
                "exampleVi": "Do thiếu kinh phí, dự án đã tạm thời bị dừng lại.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "managerial",
                "word": "managerial",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˌmænəˈdʒɪəriəl/", "us": "/ˌmænəˈdʒɪriəl/"},
                "frequency": 2,
                "meaningVi": "thuộc về quản lý",
                "exampleEn": "Mike is seeking a managerial position in the accounting field.",
                "exampleVi": "Mike đang tìm kiếm một vị trí quản lý trong ngành kế toán.",
                "derivatives": [
                    {"word": "manage", "partOfSpeech": "v", "meaningVi": "quản lý, điều hành"}
                ],
                "synonyms": ["supervisory"],
                "antonyms": [],
                "toeicNotes": [
                    "managerial staff/experience: nhân viên quản lý / kinh nghiệm quản lý."
                ],
                "needsReview": False
            },
            {
                "id": "diligent",
                "word": "diligent",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈdɪlɪdʒənt/", "us": "/ˈdɪlɪdʒənt/"},
                "frequency": 2,
                "meaningVi": "siêng năng, cần cù",
                "exampleEn": "Carmen is one of the most diligent workers in the company.",
                "exampleVi": "Carmen là một trong những nhân viên siêng năng nhất ở công ty này.",
                "derivatives": [
                    {"word": "diligence", "partOfSpeech": "n", "meaningVi": "sự cần cù, siêng năng"},
                    {"word": "diligently", "partOfSpeech": "adv", "meaningVi": "một cách chăm chỉ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "familiar",
                "word": "familiar",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/fəˈmɪliə(r)/", "us": "/fəˈmɪliər/"},
                "frequency": 2,
                "meaningVi": "quen thuộc, thuần thục",
                "exampleEn": "Staff must review the handbook to become familiar with it.",
                "exampleVi": "Nhân viên phải xem lại sổ tay hướng dẫn để nắm rõ nó.",
                "derivatives": [
                    {"word": "familiarize", "partOfSpeech": "v", "meaningVi": "làm cho quen, phổ biến"}
                ],
                "synonyms": [],
                "antonyms": ["unfamiliar"],
                "toeicNotes": [
                    "be familiar with: quen thuộc với, nắm rõ..."
                ],
                "needsReview": False
            },
            {
                "id": "proficiency",
                "word": "proficiency",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/prəˈfɪʃnsi/", "us": "/prəˈfɪʃnsi/"},
                "frequency": 2,
                "meaningVi": "sự thông thạo, sự thành thạo",
                "exampleEn": "Overseas workers need proof of proficiency in a second language.",
                "exampleVi": "Người lao động ở nước ngoài cần phải chứng minh sự thông thạo một ngôn ngữ thứ hai.",
                "derivatives": [
                    {"word": "proficient", "partOfSpeech": "adj", "meaningVi": "thông thạo, thành thạo"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "prospective",
                "word": "prospective",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/prəˈspektɪv/", "us": "/prəˈspektɪv/"},
                "frequency": 2,
                "meaningVi": "có tiềm năng, có triển vọng",
                "exampleEn": "Prospective employees were asked to come in for a second interview.",
                "exampleVi": "Các nhân viên tiềm năng được yêu cầu đến phỏng vấn vòng hai.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "appeal",
                "word": "appeal",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈpiːl/", "us": "/əˈpiːl/"},
                "frequency": 2,
                "meaningVi": "lôi cuốn, hấp dẫn",
                "exampleEn": "The 10 percent pay increase appealed to the staff.",
                "exampleVi": "Mức tăng lương 10% đã hấp dẫn các nhân viên.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "appeal to: lôi cuốn, hấp dẫn ai (nội động từ, luôn đi với to)."
                ],
                "needsReview": False
            },
            {
                "id": "specialize",
                "word": "specialize",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈspeʃəlaɪz/", "us": "/ˈspeʃəlaɪz/"},
                "frequency": 2,
                "meaningVi": "chuyên về, học chuyên về",
                "exampleEn": "Most of the programmers specialized in software design in college.",
                "exampleVi": "Hầu hết các lập trình viên đều học chuyên về thiết kế phần mềm ở trường đại học.",
                "derivatives": [
                    {"word": "specialty", "partOfSpeech": "n", "meaningVi": "chuyên môn, đặc sản"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "apprehensive",
                "word": "apprehensive",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/,æpri'hensiv/", "us": "/,æpri'hensiv/"},
                "frequency": 2,
                "meaningVi": "lo lắng, e sợ",
                "exampleEn": "Many people feel apprehensive before an important job interview.",
                "exampleVi": "Nhiều người cảm thấy lo lắng trước một cuộc phỏng vấn tuyển dụng quan trọng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "consultant",
                "word": "consultant",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kən'sʌltənt/", "us": "/kən'sʌltənt/"},
                "frequency": 2,
                "meaningVi": "người tư vấn, cố vấn",
                "exampleEn": "Emma currently works in London as an interior design consultant.",
                "exampleVi": "Emma hiện đang làm việc ở London trong vai trò một người tư vấn thiết kế nội thất.",
                "derivatives": [
                    {"word": "consult", "partOfSpeech": "v", "meaningVi": "tư vấn, hội ý"},
                    {"word": "consultation", "partOfSpeech": "n", "meaningVi": "sự hội ý, cuộc hội luận"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "consult with + người: trao đổi/hội ý với ai.",
                    "consult + tài liệu/chuyên gia (không đi kèm giới từ): tra cứu tài liệu/hỏi ý kiến chuyên gia."
                ],
                "needsReview": False
            },
            {
                "id": "entitle",
                "word": "entitle",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈtaɪtl/", "us": "/ɪnˈtaɪtl/"},
                "frequency": 1,
                "meaningVi": "cho quyền (làm gì)",
                "exampleEn": "Executives are entitled to additional benefits.",
                "exampleVi": "Các ủy viên ban quản trị được hưởng những quyền lợi bổ sung.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "be entitled to + noun: được hưởng cái gì.",
                    "be entitled to do sth: được quyền làm việc gì."
                ],
                "needsReview": False
            },
            {
                "id": "degree",
                "word": "degree",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈɡriː/", "us": "/dɪˈɡriː/"},
                "frequency": 1,
                "meaningVi": "bằng cấp, học vị, mức độ",
                "exampleEn": "A bachelor's degree in engineering is a requirement for this position.",
                "exampleVi": "Bằng cử nhân về kỹ thuật là một điều kiện cần thiết cho vị trí này.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "payroll",
                "word": "payroll",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈpeɪrəʊl/", "us": "/ˈpeɪroʊl/"},
                "frequency": 1,
                "meaningVi": "bảng lương, tổng quỹ lương",
                "exampleEn": "Fifteen new employees were added to the payroll last month.",
                "exampleVi": "Mười lăm nhân viên mới đã được bổ sung vào bảng lương tháng trước.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [
                    "on the payroll: có tên trong bảng lương (được tuyển dụng)."
                ],
                "needsReview": False
            },
            {
                "id": "recruit",
                "word": "recruit",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ri'kru:t/", "us": "/ri'kru:t/"},
                "frequency": 1,
                "meaningVi": "tuyển dụng",
                "exampleEn": "The firm recruits promising graduates on a yearly basis.",
                "exampleVi": "Hằng năm, công ty tuyển dụng những sinh viên mới tốt nghiệp.",
                "derivatives": [
                    {"word": "recruitment", "partOfSpeech": "n", "meaningVi": "sự tuyển dụng"},
                    {"word": "recruiter", "partOfSpeech": "n", "meaningVi": "người tuyển dụng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            }
        ]

    if day_num == 2:
        words_data = [
            {
                "id": "attire",
                "word": "attire",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈtaɪə(r)/", "us": "/əˈtaɪər/"},
                "frequency": 2,
                "meaningVi": "trang phục, quần áo",
                "exampleEn": "Professional business attire is required of all staff giving presentations.",
                "exampleVi": "Trang phục công sở chuyên nghiệp là yêu cầu bắt buộc đối với tất cả nhân viên thực hiện bài thuyết trình.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "code",
                "word": "code",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kəʊd/", "us": "/koʊd/"},
                "frequency": 2,
                "meaningVi": "quy định, điều lệ, mật mã",
                "exampleEn": "Employees are expected to follow the dress code.",
                "exampleVi": "Các nhân viên cần phải tuân theo quy định về trang phục.",
                "derivatives": [],
                "synonyms": ["rules", "regulations"],
                "antonyms": [],
                "toeicNotes": ["dress code: quy định về trang phục"],
                "needsReview": False
            },
            {
                "id": "concern-n",
                "word": "concern",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kənˈsɜːn/", "us": "/kənˈsɜːrn/"},
                "frequency": 3,
                "meaningVi": "sự lo lắng, mối quan ngại",
                "exampleEn": "The board voiced concerns about safety at the meeting.",
                "exampleVi": "Hội đồng bày tỏ mối quan ngại về sự an toàn tại cuộc họp.",
                "derivatives": [
                    {"word": "concerning", "partOfSpeech": "prep", "meaningVi": "liên quan đến"},
                    {"word": "concerned", "partOfSpeech": "adj", "meaningVi": "có liên quan, lo lắng"}
                ],
                "synonyms": ["matter", "worry"],
                "antonyms": [],
                "toeicNotes": ["concern about/over: lo lắng/quan ngại về cái gì"],
                "needsReview": False
            },
            {
                "id": "concern-v",
                "word": "concern",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kənˈsɜːn/", "us": "/kənˈsɜːrn/"},
                "frequency": 3,
                "meaningVi": "lo lắng, bận tâm; ảnh hưởng, liên quan",
                "exampleEn": "Citizens are concerned about the new trade protocol.",
                "exampleVi": "Người dân lo ngại về hiệp định thương mại mới.",
                "derivatives": [],
                "synonyms": ["involve", "affect"],
                "antonyms": [],
                "toeicNotes": ["questions concerning: câu hỏi liên quan đến..."],
                "needsReview": False
            },
            {
                "id": "policy",
                "word": "policy",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈpɒləsi/", "us": "/ˈpɑːləsi/"},
                "frequency": 2,
                "meaningVi": "quy chế, chính sách, điều khoản",
                "exampleEn": "The employee benefit policy will be expanded next year.",
                "exampleVi": "Chính sách phúc lợi cho nhân viên sẽ được mở rộng vào năm tới.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["insurance policy: chính sách bảo hiểm"],
                "needsReview": False
            },
            {
                "id": "comply",
                "word": "comply",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kəmˈplaɪ/", "us": "/kəmˈplaɪ/"},
                "frequency": 2,
                "meaningVi": "tuân thủ, làm theo",
                "exampleEn": "Employees must comply with the regulations governing computer use.",
                "exampleVi": "Nhân viên phải tuân thủ các quy định về quản lý sử dụng máy tính.",
                "derivatives": [
                    {"word": "compliance", "partOfSpeech": "n", "meaningVi": "sự làm theo, sự phục tùng"}
                ],
                "synonyms": ["observe", "obey", "fulfill"],
                "antonyms": [],
                "toeicNotes": [
                    "comply with: tuân thủ (luôn đi kèm with)",
                    "observe: tuân thủ (ngoại động từ, theo sau trực tiếp bởi tân ngữ)",
                    "obey: phục tùng, nghe lời (ai đó)",
                    "fulfill: đáp ứng, thỏa mãn (yêu cầu, điều kiện)"
                ],
                "needsReview": False
            },
            {
                "id": "regulation",
                "word": "regulation",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌreɡjuˈleɪʃn/", "us": "/ˌreɡjuˈleɪʃn/"},
                "frequency": 2,
                "meaningVi": "quy định, quy tắc, điều lệ",
                "exampleEn": "Regulations regarding lunch breaks were established.",
                "exampleVi": "Những quy định về giờ nghỉ trưa đã được thiết lập.",
                "derivatives": [
                    {"word": "regulate", "partOfSpeech": "v", "meaningVi": "điều chỉnh, kiểm soát"}
                ],
                "synonyms": ["rule", "statute"],
                "antonyms": [],
                "toeicNotes": ["safety regulations: quy tắc an toàn", "customs regulations: quy định hải quan"],
                "needsReview": False
            },
            {
                "id": "exception",
                "word": "exception",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪkˈsepʃn/", "us": "/ɪkˈsepʃn/"},
                "frequency": 2,
                "meaningVi": "ngoại lệ, sự loại trừ",
                "exampleEn": "Management decided not to make any exceptions to the rules.",
                "exampleVi": "Ban quản lý quyết định không chấp nhận bất kỳ ngoại lệ nào đối với quy định này.",
                "derivatives": [
                    {"word": "exceptional", "partOfSpeech": "adj", "meaningVi": "đặc biệt, hiếm có"},
                    {"word": "exceptionally", "partOfSpeech": "adv", "meaningVi": "khác thường, đặc biệt"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["with the exception of: ngoại trừ...", "with very few exceptions: hầu như không có ngoại lệ"],
                "needsReview": False
            },
            {
                "id": "adhere",
                "word": "adhere",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ədˈhɪə(r)/", "us": "/ədˈhɪər/"},
                "frequency": 2,
                "meaningVi": "bám sát, tuân thủ",
                "exampleEn": "All staff should do their best to adhere to the company's policies.",
                "exampleVi": "Tất cả nhân viên nên cố gắng hết sức để tuân thủ các chính sách của công ty.",
                "derivatives": [
                    {"word": "adherence", "partOfSpeech": "n", "meaningVi": "sự trung thành, gắn bó"}
                ],
                "synonyms": ["comply", "follow"],
                "antonyms": [],
                "toeicNotes": ["adhere to: tuân thủ (luôn đi kèm to)"],
                "needsReview": False
            },
            {
                "id": "severely",
                "word": "severely",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/sɪˈvɪəli/", "us": "/sɪˈvɪrli/"},
                "frequency": 2,
                "meaningVi": "nghiêm khắc, khắt khe; gay go, dữ dội",
                "exampleEn": "Those who share company data with outside parties will be severely punished.",
                "exampleVi": "Những ai chia sẻ dữ liệu của công ty ra bên ngoài sẽ bị trừng phạt nghiêm khắc.",
                "derivatives": [
                    {"word": "severe", "partOfSpeech": "adj", "meaningVi": "khắt khe, gay gắt"}
                ],
                "synonyms": ["sternly"],
                "antonyms": ["leniently"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "refrain",
                "word": "refrain",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈfreɪn/", "us": "/rɪˈfreɪn/"},
                "frequency": 2,
                "meaningVi": "kiềm chế, hạn chế",
                "exampleEn": "Guards should refrain from making personal calls during a shift.",
                "exampleVi": "Nhân viên bảo vệ nên hạn chế thực hiện các cuộc gọi cá nhân khi đang trong ca trực.",
                "derivatives": [],
                "synonyms": ["avoid", "abstain"],
                "antonyms": [],
                "toeicNotes": ["refrain from: hạn chế, kiềm chế làm việc gì"],
                "needsReview": False
            },
            {
                "id": "permission",
                "word": "permission",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/pəˈmɪʃn/", "us": "/pərˈmɪʃn/"},
                "frequency": 2,
                "meaningVi": "sự cho phép",
                "exampleEn": "The CEO gave managers permission to hold a weekend workshop.",
                "exampleVi": "Giám đốc điều hành đã cho phép các quản lý tổ chức một buổi hội thảo cuối tuần.",
                "derivatives": [
                    {"word": "permit", "partOfSpeech": "v", "meaningVi": "cho phép"},
                    {"word": "permit", "partOfSpeech": "n", "meaningVi": "giấy phép"}
                ],
                "synonyms": ["authorization"],
                "antonyms": [],
                "toeicNotes": ["ask for permission: xin phép"],
                "needsReview": False
            },
            {
                "id": "access-n",
                "word": "access",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈækses/", "us": "/ˈækses/"},
                "frequency": 3,
                "meaningVi": "quyền truy cập, sự lui tới, lối vào",
                "exampleEn": "Only authorized personnel may gain access to client files.",
                "exampleVi": "Chỉ nhân viên được ủy quyền mới có thể truy cập vào các tập tin của khách hàng.",
                "derivatives": [
                    {"word": "accessible", "partOfSpeech": "adj", "meaningVi": "có thể truy cập"},
                    {"word": "accessibility", "partOfSpeech": "n", "meaningVi": "khả năng tiếp cận"}
                ],
                "synonyms": ["entrance", "entry"],
                "antonyms": [],
                "toeicNotes": ["have access to: có quyền tiếp cận/truy cập vào cái gì"],
                "needsReview": False
            },
            {
                "id": "access-v",
                "word": "access",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈækses/", "us": "/ˈækses/"},
                "frequency": 3,
                "meaningVi": "truy cập",
                "exampleEn": "Click on the link to access the detailed job description.",
                "exampleVi": "Nhấp vào liên kết để truy cập vào phần mô tả chi tiết công việc.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["access (v) là ngoại động từ, đi thẳng với tân ngữ, không dùng giới từ to"],
                "needsReview": False
            },
            {
                "id": "thoroughly",
                "word": "thoroughly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈθʌrəli/", "us": "/ˈθɜːroʊli/"},
                "frequency": 3,
                "meaningVi": "một cách kỹ lưỡng; hoàn toàn, triệt để",
                "exampleEn": "Please read the user manual thoroughly before installing this software.",
                "exampleVi": "Vui lòng đọc kỹ hướng dẫn sử dụng trước khi cài đặt phần mềm này.",
                "derivatives": [
                    {"word": "thorough", "partOfSpeech": "adj", "meaningVi": "kỹ lưỡng, thấu đáo"}
                ],
                "synonyms": ["carefully", "completely"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "revise",
                "word": "revise",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈvaɪz/", "us": "/rɪˈvaɪz/"},
                "frequency": 2,
                "meaningVi": "sửa đổi, thay đổi (ý kiến, kế hoạch)",
                "exampleEn": "The office's policies regarding vacations have been revised.",
                "exampleVi": "Các chính sách của văn phòng liên quan đến ngày nghỉ phép đã được sửa đổi.",
                "derivatives": [
                    {"word": "revision", "partOfSpeech": "n", "meaningVi": "sự sửa đổi"}
                ],
                "synonyms": ["modify", "alter"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "approach-n",
                "word": "approach",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈprəʊtʃ/", "us": "/əˈproʊtʃ/"},
                "frequency": 2,
                "meaningVi": "cách tiếp cận, phương pháp xử lý",
                "exampleEn": "The manager has a strict approach to enforcing office regulations.",
                "exampleVi": "Viên quản lý có cách tiếp cận nghiêm khắc trong việc thực thi các quy định của văn phòng.",
                "derivatives": [],
                "synonyms": ["method", "way"],
                "antonyms": [],
                "toeicNotes": ["approach to: cách tiếp cận đối với cái gì"],
                "needsReview": False
            },
            {
                "id": "approach-v",
                "word": "approach",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈprəʊtʃ/", "us": "/əˈproʊtʃ/"},
                "frequency": 2,
                "meaningVi": "tiếp cận, đi đến gần",
                "exampleEn": "Police approached carefully to arrest the suspect.",
                "exampleVi": "Cảnh sát đã thận trọng tiếp cận để bắt giữ nghi phạm.",
                "derivatives": [],
                "synonyms": ["near"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "approval",
                "word": "approval",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈpruːvl/", "us": "/əˈpruːvl/"},
                "frequency": 2,
                "meaningVi": "sự chấp thuận, sự phê duyệt",
                "exampleEn": "Please obtain the supervisor's approval before purchasing supplies.",
                "exampleVi": "Vui lòng xin phê duyệt của quản lý trước khi mua vật tư.",
                "derivatives": [
                    {"word": "approve", "partOfSpeech": "v", "meaningVi": "chấp thuận"}
                ],
                "synonyms": ["permission", "consent"],
                "antonyms": ["rejection", "disapproval"],
                "toeicNotes": ["obtain approval (for): xin sự chấp thuận/phê duyệt cho cái gì"],
                "needsReview": False
            },
            {
                "id": "form-n",
                "word": "form",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/fɔːm/", "us": "/fɔːrm/"},
                "frequency": 2,
                "meaningVi": "kiểu, loại, hình thức; mẫu đơn",
                "exampleEn": "Visitors are required to present a form of identification to security guards.",
                "exampleVi": "Du khách phải xuất trình một loại giấy tờ tùy thân cho nhân viên bảo vệ.",
                "derivatives": [
                    {"word": "formal", "partOfSpeech": "adj", "meaningVi": "trang trọng"},
                    {"word": "formation", "partOfSpeech": "n", "meaningVi": "sự hình thành"}
                ],
                "synonyms": ["type", "kind"],
                "antonyms": [],
                "toeicNotes": ["a form of identification: một loại giấy tờ tùy thân"],
                "needsReview": False
            },
            {
                "id": "immediately",
                "word": "immediately",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ɪˈmiːdiətli/", "us": "/ɪˈmiːdiətli/"},
                "frequency": 1,
                "meaningVi": "ngay lập tức",
                "exampleEn": "Effective immediately, taxes will be automatically deducted from each paycheck.",
                "exampleVi": "Ngay khi có hiệu lực, thuế sẽ được tự động khấu trừ từ lương của mỗi người.",
                "derivatives": [
                    {"word": "immediate", "partOfSpeech": "adj", "meaningVi": "lập tức, tức thời"}
                ],
                "synonyms": ["instantly", "promptly"],
                "antonyms": [],
                "toeicNotes": ["immediately after: ngay sau đó", "immediately upon arrival: ngay khi tới nơi"],
                "needsReview": False
            },
            {
                "id": "inspection",
                "word": "inspection",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪnˈspekʃn/", "us": "/ɪnˈspekʃn/"},
                "frequency": 3,
                "meaningVi": "sự kiểm tra, sự thanh tra",
                "exampleEn": "The facility inspection should be conducted at least once a month.",
                "exampleVi": "Việc kiểm tra cơ sở nên được tiến hành ít nhất mỗi tháng một lần.",
                "derivatives": [
                    {"word": "inspect", "partOfSpeech": "v", "meaningVi": "xem xét, kiểm tra"},
                    {"word": "inspector", "partOfSpeech": "n", "meaningVi": "thanh tra viên"}
                ],
                "synonyms": ["examination", "audit"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "arrangement",
                "word": "arrangement",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈreɪndʒmənt/", "us": "/əˈreɪndʒmənt/"},
                "frequency": 2,
                "meaningVi": "sự sắp xếp, sự sắp đặt, sự chuẩn bị",
                "exampleEn": "The manager made arrangements for purchase of new machinery.",
                "exampleVi": "Viên quản lý đã thu xếp cho việc mua máy móc mới.",
                "derivatives": [
                    {"word": "arrange", "partOfSpeech": "v", "meaningVi": "sắp xếp"}
                ],
                "synonyms": ["preparation", "setup"],
                "antonyms": [],
                "toeicNotes": ["make arrangements to do: chuẩn bị để làm gì", "make arrangements for: chuẩn bị cho cái gì"],
                "needsReview": False
            },
            {
                "id": "procedure",
                "word": "procedure",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/prəˈsiːdʒə(r)/", "us": "/prəˈsiːdʒər/"},
                "frequency": 2,
                "meaningVi": "thủ tục",
                "exampleEn": "The procedure for patent applications is outlined on the APTO website.",
                "exampleVi": "Thủ tục xin cấp bằng sáng chế được tóm lược trên trang web của APTO.",
                "derivatives": [
                    {"word": "proceed", "partOfSpeech": "v", "meaningVi": "tiến hành, tiếp diễn"},
                    {"word": "procedural", "partOfSpeech": "adj", "meaningVi": "theo thủ tục"}
                ],
                "synonyms": ["process", "routine"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "negative",
                "word": "negative",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈneɡətɪv/", "us": "/ˈneɡətɪv/"},
                "frequency": 2,
                "meaningVi": "tiêu cực, bi quan",
                "exampleEn": "The new vacation policy received negative feedback from the employees.",
                "exampleVi": "Chính sách nghỉ phép mới đã nhận những phản hồi tiêu cực từ các nhân viên.",
                "derivatives": [],
                "synonyms": ["pessimistic"],
                "antonyms": ["positive", "optimistic"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "mandate-v",
                "word": "mandate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈmændeɪt/", "us": "/ˈmændeɪt/"},
                "frequency": 2,
                "meaningVi": "ra lệnh, ủy quyền, ủy thác",
                "exampleEn": "The board of directors has mandated an increase for research funding.",
                "exampleVi": "Hội đồng quản trị đã ra lệnh tăng kinh phí cho nghiên cứu.",
                "derivatives": [
                    {"word": "mandatory", "partOfSpeech": "adj", "meaningVi": "bắt buộc"}
                ],
                "synonyms": ["order", "command"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "mandate-n",
                "word": "mandate",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈmændeɪt/", "us": "/ˈmændeɪt/"},
                "frequency": 2,
                "meaningVi": "lệnh, trát, sự ủy thác",
                "exampleEn": "Congress gave the committee a mandate to make budget cuts.",
                "exampleVi": "Quốc hội đã ủy thác cho ủy ban quyền cắt giảm ngân sách.",
                "derivatives": [],
                "synonyms": ["command", "authority"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "effect-n",
                "word": "effect",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪˈfekt/", "us": "/ɪˈfekt/"},
                "frequency": 3,
                "meaningVi": "hiệu ứng, hiệu quả, hiệu lực",
                "exampleEn": "The incentive policy will be in effect starting next week.",
                "exampleVi": "Chính sách động viên đó sẽ có hiệu lực bắt đầu từ tuần tới.",
                "derivatives": [
                    {"word": "effective", "partOfSpeech": "adj", "meaningVi": "hiệu quả, có hiệu lực"},
                    {"word": "effectively", "partOfSpeech": "adv", "meaningVi": "một cách hiệu quả"}
                ],
                "synonyms": ["impact", "influence"],
                "antonyms": [],
                "toeicNotes": ["in effect: có hiệu lực", "come into effect: có hiệu lực", "take effect: được thi hành", "have an effect on: có tác động tới"],
                "needsReview": False
            },
            {
                "id": "effect-v",
                "word": "effect",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪˈfekt/", "us": "/ɪˈfekt/"},
                "frequency": 3,
                "meaningVi": "thực hiện, đem lại",
                "exampleEn": "He effected a sudden change in the company's expansion plan.",
                "exampleVi": "Anh ấy đã thực hiện một thay đổi bất ngờ trong kế hoạch mở rộng của công ty.",
                "derivatives": [],
                "synonyms": ["achieve", "accomplish", "carry out"],
                "antonyms": [],
                "toeicNotes": ["put into effect (thực thi) có thể thay thế bằng apply"],
                "needsReview": False
            },
            {
                "id": "according-to",
                "word": "according to",
                "partOfSpeech": "prep",
                "pronunciation": {"uk": "/əˈkɔːdɪŋ tuː/", "us": "/əˈkɔːrdɪŋ tuː/"},
                "frequency": 2,
                "meaningVi": "theo, theo như",
                "exampleEn": "All transactions must be handled according to the guidelines.",
                "exampleVi": "Tất cả giao dịch phải được xử lý theo hướng dẫn.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "enable",
                "word": "enable",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪˈneɪbl/", "us": "/ɪˈneɪbl/"},
                "frequency": 2,
                "meaningVi": "làm cho có thể, cho phép",
                "exampleEn": "Jenny's promotion enabled her to participate in the board meeting.",
                "exampleVi": "Việc Jenny được thăng chức đã cho phép cô ấy tham gia vào cuộc họp hội đồng.",
                "derivatives": [],
                "synonyms": ["allow", "permit"],
                "antonyms": ["prevent", "disable"],
                "toeicNotes": ["enable A to do: cho phép A làm việc gì"],
                "needsReview": False
            },
            {
                "id": "standard",
                "word": "standard",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈstændəd/", "us": "/ˈstændərd/"},
                "frequency": 2,
                "meaningVi": "tiêu chuẩn, chuẩn, trình độ",
                "exampleEn": "The company must make changes to the current safety standards.",
                "exampleVi": "Công ty cần phải có những thay đổi đối với các tiêu chuẩn an toàn hiện tại.",
                "derivatives": [
                    {"word": "standardize", "partOfSpeech": "v", "meaningVi": "tiêu chuẩn hóa"}
                ],
                "synonyms": ["norm", "criterion"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "drastically",
                "word": "drastically",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈdræstɪkli/", "us": "/ˈdræstɪkli/"},
                "frequency": 2,
                "meaningVi": "một cách mạnh mẽ, quyết liệt, triệt để",
                "exampleEn": "Fines for breaking rules have been drastically increased.",
                "exampleVi": "Hình phạt cho việc vi phạm quy định đã được tăng mạnh.",
                "derivatives": [
                    {"word": "drastic", "partOfSpeech": "adj", "meaningVi": "mạnh mẽ, quyết liệt"}
                ],
                "synonyms": ["strongly", "severely"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "constant",
                "word": "constant",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈkɒnstənt/", "us": "/ˈkánstant/"},
                "frequency": 2,
                "meaningVi": "liên tục, không ngớt, không dứt",
                "exampleEn": "The store received constant inquiries about its new return policy.",
                "exampleVi": "Cửa hàng nhận được những câu hỏi liên tục về chính sách hoàn trả mới.",
                "derivatives": [
                    {"word": "constantly", "partOfSpeech": "adv", "meaningVi": "liên tục"}
                ],
                "synonyms": ["continuous", "continual"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "act-n",
                "word": "act",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ækt/", "us": "/ækt/"},
                "frequency": 2,
                "meaningVi": "hành động, việc làm; đạo luật",
                "exampleEn": "The new act makes it easier to file personal income tax forms online.",
                "exampleVi": "Đạo luật mới khiến cho việc nộp các biểu mẫu khai thuế thu nhập cá nhân trên mạng trở nên dễ dàng hơn.",
                "derivatives": [
                    {"word": "action", "partOfSpeech": "n", "meaningVi": "hành động"},
                    {"word": "active", "partOfSpeech": "adj", "meaningVi": "năng động"}
                ],
                "synonyms": ["law", "deed"],
                "antonyms": [],
                "toeicNotes": ["the act of merging: việc sáp nhập"],
                "needsReview": False
            },
            {
                "id": "act-v",
                "word": "act",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ækt/", "us": "/ækt/"},
                "frequency": 2,
                "meaningVi": "hành động, đưa ra quyết định",
                "exampleEn": "A lawyer always acts on behalf of his clients.",
                "exampleVi": "Luật sư luôn hành động thay mặt cho khách hàng của anh ta.",
                "derivatives": [],
                "synonyms": ["behave", "perform"],
                "antonyms": [],
                "toeicNotes": ["act on behalf of: hành động thay mặt cho ai"],
                "needsReview": False
            },
            {
                "id": "compensation",
                "word": "compensation",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌkɒmpenˈseɪʃn/", "us": "/ˌkɑːmpenˈseɪʃn/"},
                "frequency": 2,
                "meaningVi": "sự đền bù, sự bồi thường",
                "exampleEn": "Employees will receive compensation based on their performance and evaluation.",
                "exampleVi": "Nhân viên sẽ nhận được bồi thường dựa trên hiệu suất làm việc và bản đánh giá của họ.",
                "derivatives": [
                    {"word": "compensate", "partOfSpeech": "v", "meaningVi": "đền bù, bồi thường"}
                ],
                "synonyms": ["reimbursement", "payment"],
                "antonyms": [],
                "toeicNotes": ["compensation for: bồi thường cho cái gì"],
                "needsReview": False
            },
            {
                "id": "ban-n",
                "word": "ban",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/bæn/", "us": "/bæn/"},
                "frequency": 2,
                "meaningVi": "lệnh cấm, sự cấm đoán",
                "exampleEn": "The government placed a ban on carrying a large volume of liquid on board a plane.",
                "exampleVi": "Chính phủ ban hành lệnh cấm đối với việc mang một lượng lớn chất lỏng lên máy bay.",
                "derivatives": [],
                "synonyms": ["prohibition"],
                "antonyms": [],
                "toeicNotes": ["place a ban on: ban hành lệnh cấm đối với"],
                "needsReview": False
            },
            {
                "id": "ban-v",
                "word": "ban",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/bæn/", "us": "/bæn/"},
                "frequency": 2,
                "meaningVi": "cấm, ngăn cấm",
                "exampleEn": "The company banned the use of the Internet for personal purposes.",
                "exampleVi": "Công ty đã cấm sử dụng Internet cho mục đích cá nhân.",
                "derivatives": [],
                "synonyms": ["prohibit", "forbid"],
                "antonyms": ["allow", "permit"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "obligation",
                "word": "obligation",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌɒblɪˈɡeɪʃn/", "us": "/ˌɑːblɪˈɡeɪʃn/"},
                "frequency": 2,
                "meaningVi": "nghĩa vụ, trách nhiệm",
                "exampleEn": "All researchers have an obligation to publish at least one paper every year.",
                "exampleVi": "Mọi nhà nghiên cứu đều có trách nhiệm phải xuất bản ít nhất một bài báo mỗi năm.",
                "derivatives": [
                    {"word": "obligatory", "partOfSpeech": "adj", "meaningVi": "bắt buộc"},
                    {"word": "oblige", "partOfSpeech": "v", "meaningVi": "bắt buộc"}
                ],
                "synonyms": ["duty", "responsibility"],
                "antonyms": [],
                "toeicNotes": ["have an obligation to do: có nghĩa vụ phải làm gì"],
                "needsReview": False
            },
            {
                "id": "authorize",
                "word": "authorize",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɔːθəraɪz/", "us": "/ˈɔːθəraɪz/"},
                "frequency": 2,
                "meaningVi": "ủy quyền, cho phép",
                "exampleEn": "Allocations of funds must be authorized by management.",
                "exampleVi": "Việc phân bổ kinh phí phải được ban quản lý cho phép.",
                "derivatives": [
                    {"word": "authorization", "partOfSpeech": "n", "meaningVi": "sự cho phép, sự cấp phép"},
                    {"word": "authorized", "partOfSpeech": "adj", "meaningVi": "được cho phép, được ủy quyền"}
                ],
                "synonyms": ["allow", "permit"],
                "antonyms": ["prohibit", "forbid"],
                "toeicNotes": ["an authorized service center: một trung tâm dịch vụ được ủy quyền", "unauthorized reproduction: sao chép trái phép"],
                "needsReview": False
            },
            {
                "id": "prohibit",
                "word": "prohibit",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/prəˈhɪbɪt/", "us": "/prəˈhɪbɪt/"},
                "frequency": 2,
                "meaningVi": "ngăn cấm, cấm đoán",
                "exampleEn": "The museum prohibits visitors from taking pictures.",
                "exampleVi": "Bảo tàng không cho phép du khách chụp ảnh.",
                "derivatives": [
                    {"word": "prohibition", "partOfSpeech": "n", "meaningVi": "sự cấm"}
                ],
                "synonyms": ["forbid", "ban"],
                "antonyms": ["allow", "permit", "authorize"],
                "toeicNotes": ["prohibit A from -ing: cấm A làm gì", "forbid A from -ing/to do: cấm A làm gì"],
                "needsReview": False
            },
            {
                "id": "abolish",
                "word": "abolish",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈbɒlɪʃ/", "us": "/əˈbɑːlɪʃ/"},
                "frequency": 1,
                "meaningVi": "thủ tiêu, bãi bỏ, hủy bỏ",
                "exampleEn": "Congress decided to abolish taxes on imported fruit.",
                "exampleVi": "Quốc hội đã quyết định bãi bỏ thuế đối với các loại trái cây nhập khẩu.",
                "derivatives": [
                    {"word": "abolition", "partOfSpeech": "n", "meaningVi": "sự bãi bỏ"}
                ],
                "synonyms": ["eliminate", "cancel", "annul"],
                "antonyms": ["establish", "retain"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "enforce",
                "word": "enforce",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈfɔːs/", "us": "/ɪnˈfɔːrs/"},
                "frequency": 2,
                "meaningVi": "thi hành, thúc ép, làm cho có hiệu lực",
                "exampleEn": "All departments must enforce the no smoking policy.",
                "exampleVi": "Tất cả các phòng ban phải thực thi quy định về cấm hút thuốc lá.",
                "derivatives": [
                    {"word": "enforcement", "partOfSpeech": "n", "meaningVi": "sự thúc ép, sự thực thi"}
                ],
                "synonyms": ["implement", "execute"],
                "antonyms": [],
                "toeicNotes": ["enforce regulations: thực thi quy định"],
                "needsReview": False
            },
            {
                "id": "habit",
                "word": "habit",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈhæbɪt/", "us": "/ˈhæbɪt/"},
                "frequency": 2,
                "meaningVi": "thói quen, tập quán cá nhân",
                "exampleEn": "Setting goals should be a regular habit.",
                "exampleVi": "Việc đặt mục tiêu nên là một thói quen thường xuyên.",
                "derivatives": [
                    {"word": "habitual", "partOfSpeech": "adj", "meaningVi": "quen thuộc, thường lệ"}
                ],
                "synonyms": ["custom"],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: habit là thói quen cá nhân, convention là tập quán của cộng đồng/doanh nghiệp"],
                "needsReview": False
            },
            {
                "id": "legislation",
                "word": "legislation",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌledʒɪsˈleɪʃn/", "us": "/ˌledʒɪsˈleɪʃn/"},
                "frequency": 2,
                "meaningVi": "luật pháp, sự làm luật, pháp chế",
                "exampleEn": "The committee unanimously voted for the new export legislation.",
                "exampleVi": "Ủy ban đã nhất trí bỏ phiếu cho luật mới về hạn chế xuất khẩu.",
                "derivatives": [
                    {"word": "legislate", "partOfSpeech": "v", "meaningVi": "lập pháp"},
                    {"word": "legislator", "partOfSpeech": "n", "meaningVi": "nhà lập pháp"}
                ],
                "synonyms": ["law", "statute"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "restrict",
                "word": "restrict",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈstrɪkt/", "us": "/rɪˈstrɪkt/"},
                "frequency": 2,
                "meaningVi": "giới hạn, hạn chế",
                "exampleEn": "Access is restricted to authorized personnel.",
                "exampleVi": "Việc truy cập chỉ giới hạn cho các nhân viên được ủy quyền.",
                "derivatives": [
                    {"word": "restriction", "partOfSpeech": "n", "meaningVi": "sự hạn chế"},
                    {"word": "restrictive", "partOfSpeech": "adj", "meaningVi": "hạn chế, giới hạn"}
                ],
                "synonyms": ["limit", "confine"],
                "antonyms": ["broaden", "expand"],
                "toeicNotes": ["restrict A to B: hạn chế A đối với B", "lift/raise a restriction: bãi bỏ sự hạn chế"],
                "needsReview": False
            }
        ]

    if day_num == 3:
        words_data = [
            {
                "id": "accustomed",
                "word": "accustomed",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/əˈkʌstəmd/", "us": "/əˈkʌstəmd/"},
                "frequency": 2,
                "meaningVi": "quen với, thành thói quen",
                "exampleEn": "All our employees are accustomed to using the new design software.",
                "exampleVi": "Tất cả nhân viên của chúng tôi đều đã quen với việc sử dụng phần mềm thiết kế mới.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["be accustomed to -ing: quen với việc làm gì (sau to là danh động từ)"],
                "needsReview": False
            },
            {
                "id": "corporation",
                "word": "corporation",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌkɔːpəˈreɪʃn/", "us": "/ˌkɔːrpəˈreɪʃn/"},
                "frequency": 2,
                "meaningVi": "công ty, tập đoàn",
                "exampleEn": "Lee heads a multinational telecommunications corporation based in Virginia.",
                "exampleVi": "Lee đứng đầu một tập đoàn viễn thông đa quốc gia có trụ sở tại Virginia.",
                "derivatives": [
                    {"word": "corporate", "partOfSpeech": "adj", "meaningVi": "thuộc về tập đoàn/doanh nghiệp"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "demanding",
                "word": "demanding",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/dɪˈmɑːndɪŋ/", "us": "/dɪˈmændɪŋ/"},
                "frequency": 2,
                "meaningVi": "đòi hỏi khắt khe, có yêu cầu cao",
                "exampleEn": "Although Ms. Jenkins is a demanding supervisor, she has a reputation for being fair.",
                "exampleVi": "Mặc dù cô Jenkins là một giám sát rất khắt khe, nhưng cô ấy nổi tiếng là luôn công bằng.",
                "derivatives": [
                    {"word": "demand", "partOfSpeech": "v/n", "meaningVi": "yêu cầu, đòi hỏi"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "colleague",
                "word": "colleague",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈkɒliːɡ/", "us": "/ˈkɑːliːɡ/"},
                "frequency": 2,
                "meaningVi": "đồng nghiệp",
                "exampleEn": "Regular social activities can improve cooperation among colleagues.",
                "exampleVi": "Những hoạt động xã hội thường xuyên có thể tăng cường sự hợp tác giữa các đồng nghiệp.",
                "derivatives": [],
                "synonyms": ["coworker", "associate"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "division",
                "word": "division",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈvɪʒn/", "us": "/dɪˈvɪʒn/"},
                "frequency": 3,
                "meaningVi": "bộ phận, phòng ban, sự phân chia",
                "exampleEn": "The technician will transfer to the automobile division after training.",
                "exampleVi": "Kỹ thuật viên sẽ chuyển sang bộ phận ô tô sau khi được đào tạo.",
                "derivatives": [
                    {"word": "divide", "partOfSpeech": "v", "meaningVi": "chia, phân chia"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: division (bộ phận trong công ty), category (hạng mục, nhóm loại), compartment (ngăn tủ, khoang tàu)"],
                "needsReview": False
            },
            {
                "id": "request-n",
                "word": "request",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈkwest/", "us": "/rɪˈkwest/"},
                "frequency": 2,
                "meaningVi": "lời yêu cầu, lời thỉnh cầu",
                "exampleEn": "Factory tours are available upon request.",
                "exampleVi": "Các chuyến tham quan nhà máy được cung cấp theo yêu cầu.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["upon request: khi có yêu cầu"],
                "needsReview": False
            },
            {
                "id": "request-v",
                "word": "request",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈkwest/", "us": "/rɪˈkwest/"},
                "frequency": 2,
                "meaningVi": "yêu cầu, đề nghị",
                "exampleEn": "Mike requested a copy of the contract from the sales director.",
                "exampleVi": "Mike yêu cầu một bản sao hợp đồng từ giám đốc kinh doanh.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["request A from B: yêu cầu cái gì từ ai"],
                "needsReview": False
            },
            {
                "id": "efficiently",
                "word": "efficiently",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ɪˈfɪʃntli/", "us": "/ɪˈfɪʃntli/"},
                "frequency": 2,
                "meaningVi": "một cách hiệu quả",
                "exampleEn": "The software helps employees work more efficiently.",
                "exampleVi": "Phần mềm này giúp cho các nhân viên làm việc hiệu quả hơn.",
                "derivatives": [
                    {"word": "efficient", "partOfSpeech": "adj", "meaningVi": "hiệu quả, có năng suất"},
                    {"word": "efficiency", "partOfSpeech": "n", "meaningVi": "hiệu quả, năng suất"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "manage",
                "word": "manage",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈmænɪdʒ/", "us": "/ˈmænɪdʒ/"},
                "frequency": 2,
                "meaningVi": "quản lý, xoay xở, giải quyết được",
                "exampleEn": "The boss decided Colleen could manage the new store.",
                "exampleVi": "Ông chủ đã quyết định rằng Colleen có thể quản lý cửa hàng mới.",
                "derivatives": [
                    {"word": "management", "partOfSpeech": "n", "meaningVi": "ban quản lý, sự quản lý"},
                    {"word": "manager", "partOfSpeech": "n", "meaningVi": "người quản lý"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["manage to do: xoay xở làm được việc gì", "under the management of: dưới sự quản lý của"],
                "needsReview": False
            },
            {
                "id": "submit",
                "word": "submit",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/səbˈmɪt/", "us": "/səbˈmɪt/"},
                "frequency": 3,
                "meaningVi": "đệ trình, nộp",
                "exampleEn": "Applicants should submit a résumé to the personnel manager.",
                "exampleVi": "Các ứng viên nên nộp sơ yếu lý lịch cho quản lý nhân sự.",
                "derivatives": [
                    {"word": "submission", "partOfSpeech": "n", "meaningVi": "sự nộp, sự đệ trình"}
                ],
                "synonyms": ["turn in", "hand in"],
                "antonyms": [],
                "toeicNotes": ["submit A to B: nộp A cho B", "submit a résumé/receipt/recommendation/proposal: nộp sơ yếu lý lịch/hóa đơn/thư giới thiệu/bản đề xuất"],
                "needsReview": False
            },
            {
                "id": "directly",
                "word": "directly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/dəˈrektli/", "us": "/dəˈrektli/"},
                "frequency": 2,
                "meaningVi": "trực tiếp, thẳng, ngay",
                "exampleEn": "All regional branches report directly to the head office in Washington.",
                "exampleVi": "Tất cả chi nhánh khu vực đều báo cáo trực tiếp tới trụ sở chính tại Washington.",
                "derivatives": [
                    {"word": "direct", "partOfSpeech": "v/adj", "meaningVi": "chỉ đạo/trực tiếp"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["report/contact/call + directly: báo cáo/liên lạc/gọi điện trực tiếp"],
                "needsReview": False
            },
            {
                "id": "remind",
                "word": "remind",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈmaɪnd/", "us": "/rɪˈmaɪnd/"},
                "frequency": 2,
                "meaningVi": "nhắc nhở",
                "exampleEn": "Ms. Williams reminded Mr. Johnson of his lunch meeting.",
                "exampleVi": "Cô Williams đã nhắc ông Johnson về buổi gặp gỡ ăn trưa của ông ấy.",
                "derivatives": [
                    {"word": "reminder", "partOfSpeech": "n", "meaningVi": "sự nhắc nhở, vật nhắc nhở"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["remind sb of sth: nhắc nhở ai về cái gì", "remind sb to do: nhắc nhở ai làm gì", "remind sb that + clause: nhắc nhở ai rằng..."],
                "needsReview": False
            },
            {
                "id": "instruct",
                "word": "instruct",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈstrʌkt/", "us": "/ɪnˈstrʌkt/"},
                "frequency": 2,
                "meaningVi": "hướng dẫn, chỉ thị, dạy",
                "exampleEn": "The manager instructed the staff to read the conference materials beforehand.",
                "exampleVi": "Người quản lý chỉ thị cho các nhân viên đọc trước tài liệu của cuộc họp.",
                "derivatives": [
                    {"word": "instruction", "partOfSpeech": "n", "meaningVi": "sự hướng dẫn"},
                    {"word": "instructor", "partOfSpeech": "n", "meaningVi": "người hướng dẫn"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "deadline",
                "word": "deadline",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈdedlaɪn/", "us": "/ˈdedlaɪn/"},
                "frequency": 2,
                "meaningVi": "hạn chót, thời hạn",
                "exampleEn": "The team worked together closely and finished the project ahead of the deadline.",
                "exampleVi": "Cả nhóm đã làm việc chặt chẽ với nhau và hoàn thành dự án trước thời hạn.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["meet a deadline: kịp hạn chót", "miss a deadline: trễ hạn chót"],
                "needsReview": False
            },
            {
                "id": "sample-n",
                "word": "sample",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈsɑːmpl/", "us": "/ˈsæmpl/"},
                "frequency": 2,
                "meaningVi": "vật mẫu, mẫu thử",
                "exampleEn": "We need to prepare samples of our products for the fair.",
                "exampleVi": "Chúng ta cần chuẩn bị các mẫu thử của sản phẩm cho hội chợ.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "sample-v",
                "word": "sample",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈsɑːmpl/", "us": "/ˈsæmpl/"},
                "frequency": 2,
                "meaningVi": "ăn thử, trải nghiệm thử",
                "exampleEn": "The customer sampled some cake at the opening of the bakery.",
                "exampleVi": "Khách hàng ăn thử một vài chiếc bánh trong ngày khai trương tiệm bánh.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "notify",
                "word": "notify",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈnəʊtɪfaɪ/", "us": "/ˈnoʊtɪfaɪ/"},
                "frequency": 2,
                "meaningVi": "thông báo, báo cho biết",
                "exampleEn": "All staff applying for leave must notify their supervisors in writing.",
                "exampleVi": "Tất cả các nhân viên xin nghỉ phép đều phải thông báo bằng văn bản cho quản lý trực tiếp của mình.",
                "derivatives": [
                    {"word": "notification", "partOfSpeech": "n", "meaningVi": "sự thông báo"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["notify sb of sth/that clause: thông báo cho ai về cái gì (sau notify luôn là tân ngữ chỉ người)", "announce (to sb) that: thông báo điều gì cho ai", "reveal sth to sb: tiết lộ điều gì cho ai"],
                "needsReview": False
            },
            {
                "id": "perform",
                "word": "perform",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/pəˈfɔːm/", "us": "/pərˈfɔːrm/"},
                "frequency": 2,
                "meaningVi": "thi hành, thực hiện, hoạt động",
                "exampleEn": "All work on the assembly line stopped while equipment repairs were being performed.",
                "exampleVi": "Mọi hoạt động trên dây chuyền lắp ráp đều dừng lại trong khi việc sửa chữa thiết bị đang được tiến hành.",
                "derivatives": [
                    {"word": "performance", "partOfSpeech": "n", "meaningVi": "hiệu suất, sự thực hiện, sự biểu diễn"}
                ],
                "synonyms": ["conduct", "complete"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "monitor",
                "word": "monitor",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈmɒnɪtə(r)/", "us": "/ˈmɑːnɪtər/"},
                "frequency": 3,
                "meaningVi": "giám sát, theo dõi",
                "exampleEn": "The new director will monitor progress on the project.",
                "exampleVi": "Người quản lý mới sẽ giám sát tiến độ của dự án.",
                "derivatives": [],
                "synonyms": ["supervise", "observe"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "deserve",
                "word": "deserve",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/dɪˈzɜːv/", "us": "/dɪˈzɜːrv/"},
                "frequency": 3,
                "meaningVi": "đáng, xứng đáng",
                "exampleEn": "The person with the highest performance evaluation deserves the Employee of the Year Award.",
                "exampleVi": "Người được đánh giá có hiệu suất làm việc cao nhất xứng đáng nhận giải thưởng Nhân viên của năm.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["well-deserved advancement: sự thăng tiến hoàn toàn xứng đáng"],
                "needsReview": False
            },
            {
                "id": "assignment",
                "word": "assignment",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈsaɪnmənt/", "us": "/əˈsaɪnmənt/"},
                "frequency": 3,
                "meaningVi": "nhiệm vụ, công việc được giao",
                "exampleEn": "Walter took the assignment in India because he was promised a promotion there.",
                "exampleVi": "Walter nhận công việc ở Ấn Độ vì anh ấy được hứa hẹn sẽ được thăng chức ở đó.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "entire",
                "word": "entire",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪnˈtaɪə(r)/", "us": "/ɪnˈtaɪər/"},
                "frequency": 3,
                "meaningVi": "trọn vẹn, toàn bộ, hoàn toàn",
                "exampleEn": "The entire team gathers every Monday morning to discuss plans for the week.",
                "exampleVi": "Cả nhóm tụ họp lại vào mỗi sáng thứ Hai để trao đổi về kế hoạch của tuần.",
                "derivatives": [
                    {"word": "entireity", "partOfSpeech": "n", "meaningVi": "trạng thái toàn vẹn, tính trọn vẹn"}
                ],
                "synonyms": ["whole"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "release-v",
                "word": "release",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈliːs/", "us": "/rɪˈliːs/"},
                "frequency": 2,
                "meaningVi": "phát hành, phóng thích, làm nhẹ bớt",
                "exampleEn": "The company released its annual report.",
                "exampleVi": "Công ty đã phát hành báo cáo thường niên.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "release-n",
                "word": "release",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈliːs/", "us": "/rɪˈliːs/"},
                "frequency": 2,
                "meaningVi": "sự phát hành, sự ra mắt (sản phẩm)",
                "exampleEn": "The new clothing line will be ready for release by early next year.",
                "exampleVi": "Dòng sản phẩm thời trang mới sẽ sẵn sàng để ra mắt vào đầu năm tới.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["press release: thông báo báo chí, thông cáo báo chí", "release date: ngày phát hành"],
                "needsReview": False
            },
            {
                "id": "extension",
                "word": "extension",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪkˈstenʃn/", "us": "/ɪkˈstenʃn/"},
                "frequency": 2,
                "meaningVi": "sự gia hạn, kéo dài; máy lẻ (điện thoại)",
                "exampleEn": "The manager granted an extension of the deadline.",
                "exampleVi": "Người quản lý đã cho phép kéo dài thêm thời hạn.",
                "derivatives": [
                    {"word": "extend", "partOfSpeech": "v", "meaningVi": "kéo dài, gia hạn"},
                    {"word": "extensive", "partOfSpeech": "adj", "meaningVi": "rộng rãi, bao quát"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["press extension number 727: nhấn số máy lẻ 727"],
                "needsReview": False
            },
            {
                "id": "electronically",
                "word": "electronically",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ɪˌlekˈtrɒnɪkli/", "us": "/ɪˌlekˈtrɑːnɪkli/"},
                "frequency": 2,
                "meaningVi": "bằng điện tử, trực tuyến",
                "exampleEn": "It saves time and resources to send invoices electronically.",
                "exampleVi": "Gửi hóa đơn bằng phương thức điện tử giúp tiết kiệm thời gian và tài nguyên.",
                "derivatives": [
                    {"word": "electronic", "partOfSpeech": "adj", "meaningVi": "thuộc về điện tử"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "attendance",
                "word": "attendance",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈtendəns/", "us": "/əˈtendəns/"},
                "frequency": 2,
                "meaningVi": "sự tham gia, sự có mặt, sự chuyên cần",
                "exampleEn": "Attendance records are taken into consideration when determining eligibility for promotion.",
                "exampleVi": "Bảng ghi chép về độ chuyên cần sẽ được cân nhắc khi xem xét tiêu chuẩn để thăng chức.",
                "derivatives": [
                    {"word": "attend", "partOfSpeech": "v", "meaningVi": "tham dự"},
                    {"word": "attendant", "partOfSpeech": "n", "meaningVi": "người phục vụ, người tham gia"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["attendance records: bảng điểm danh, bảng ghi chép chuyên cần", "a certificate of attendance: giấy chứng nhận tham gia"],
                "needsReview": False
            },
            {
                "id": "delegate-v",
                "word": "delegate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈdelɪɡeɪt/", "us": "/ˈdelɪɡeɪt/"},
                "frequency": 2,
                "meaningVi": "ủy quyền, ủy thác, giao phó",
                "exampleEn": "Managers must be skilled in delegating responsibilities to subordinates.",
                "exampleVi": "Quản lý phải khéo léo trong việc giao phó trách nhiệm cho cấp dưới của mình.",
                "derivatives": [
                    {"word": "delegation", "partOfSpeech": "n", "meaningVi": "phái đoàn, sự ủy thác"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "delegate-n",
                "word": "delegate",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈdelɪɡət/", "us": "/ˈdelɪɡət/"},
                "frequency": 2,
                "meaningVi": "đại biểu, người đại diện",
                "exampleEn": "A delegate sent to the trade fair returned with a profitable business deal.",
                "exampleVi": "Một đại diện được cử đến hội chợ thương mại đã trở về với một thương vụ sinh lời.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "attentively",
                "word": "attentively",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/əˈtentɪvli/", "us": "/əˈtentɪvli/"},
                "frequency": 2,
                "meaningVi": "chăm chú, chú ý, thận trọng",
                "exampleEn": "Stockholders listened attentively as executives explained the company strategy.",
                "exampleVi": "Các cổ đông chăm chú lắng nghe khi các ủy viên ban quản trị giải thích về chiến lược của công ty.",
                "derivatives": [
                    {"word": "attentive", "partOfSpeech": "adj", "meaningVi": "chăm chú, chú ý"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "absolutely",
                "word": "absolutely",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈæbsəluːtli/", "us": "/ˈæbsəluːtli/"},
                "frequency": 2,
                "meaningVi": "hoàn toàn, chắc chắn, nhất định",
                "exampleEn": "It is absolutely necessary that everyone on the board is in agreement with the plan.",
                "exampleVi": "Chắc chắn là mọi người trong hội đồng quản trị đều cần phải đồng ý với kế hoạch này.",
                "derivatives": [
                    {"word": "absolute", "partOfSpeech": "adj", "meaningVi": "tuyệt đối, hoàn toàn"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "supervision",
                "word": "supervision",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌsuːpəˈvɪʒn/", "us": "/ˌsuːpərˈvɪʒn/"},
                "frequency": 3,
                "meaningVi": "sự giám sát",
                "exampleEn": "Close supervision ensures high quality.",
                "exampleVi": "Sự giám sát chặt chẽ sẽ đảm bảo chất lượng cao.",
                "derivatives": [
                    {"word": "supervise", "partOfSpeech": "v", "meaningVi": "giám sát"},
                    {"word": "supervisor", "partOfSpeech": "n", "meaningVi": "người giám sát"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "workshop",
                "word": "workshop",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈwɜːkʃɒp/", "us": "/ˈwɜːrkʃɑːp/"},
                "frequency": 2,
                "meaningVi": "hội thảo, buổi đào tạo, buổi hướng dẫn",
                "exampleEn": "Mr. Kim was asked to speak at the workshop on Friday.",
                "exampleVi": "Ông Kim được mời phát biểu tại buổi hội thảo vào thứ Sáu.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "draw",
                "word": "draw",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/drɔː/", "us": "/drɔː/"},
                "frequency": 2,
                "meaningVi": "kéo, thu hút, lôi cuốn",
                "exampleEn": "The company's annual conference usually draws 800 employees from around the world.",
                "exampleVi": "Hội nghị thường niên của công ty thường thu hút 800 nhân viên khắp nơi trên thế giới.",
                "derivatives": [],
                "synonyms": ["attract"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "revision",
                "word": "revision",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈvɪʒn/", "us": "/rɪˈvɪʒn/"},
                "frequency": 2,
                "meaningVi": "sự sửa đổi, duyệt lại",
                "exampleEn": "The team manager will make revisions to the proposal.",
                "exampleVi": "Trưởng nhóm sẽ duyệt lại đề xuất đó.",
                "derivatives": [
                    {"word": "revise", "partOfSpeech": "v", "meaningVi": "sửa đổi"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["make revisions to: thực hiện sửa đổi đối với"],
                "needsReview": False
            },
            {
                "id": "reluctantly",
                "word": "reluctantly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/rɪˈlʌktəntli/", "us": "/rɪˈlʌktəntli/"},
                "frequency": 2,
                "meaningVi": "miễn cưỡng, bất đắc dĩ",
                "exampleEn": "Ms. Danvers reluctantly agreed to cut the advertising budget.",
                "exampleVi": "Bà Danvers miễn cưỡng đồng ý cắt ngân sách quảng cáo.",
                "derivatives": [
                    {"word": "reluctant", "partOfSpeech": "adj", "meaningVi": "miễn cưỡng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "acquaint",
                "word": "acquaint",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈkweɪnt/", "us": "/əˈkweɪnt/"},
                "frequency": 2,
                "meaningVi": "làm quen, báo cho biết",
                "exampleEn": "The training program acquaints new employees with company procedures.",
                "exampleVi": "Chương trình đào tạo này giúp các nhân viên mới quen với các quy trình của công ty.",
                "derivatives": [
                    {"word": "acquaintance", "partOfSpeech": "n", "meaningVi": "người quen"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["acquaint A with B (= familiarize A with B): làm cho A quen với B"],
                "needsReview": False
            },
            {
                "id": "convey",
                "word": "convey",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kənˈveɪ/", "us": "/kənˈveɪ/"},
                "frequency": 2,
                "meaningVi": "truyền đạt, vận chuyển",
                "exampleEn": "The secretary urgently conveyed the message to the director.",
                "exampleVi": "Thư ký vội vàng truyền đạt lại tin nhắn cho giám đốc.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["convey A to B: chuyển/truyền đạt A tới B"],
                "needsReview": False
            },
            {
                "id": "check-v",
                "word": "check",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/tʃek/", "us": "/tʃek/"},
                "frequency": 2,
                "meaningVi": "kiểm tra, xem xét, xác nhận",
                "exampleEn": "Please check your computer regularly for disk errors.",
                "exampleVi": "Vui lòng kiểm tra máy tính thường xuyên để tránh bị lỗi đĩa.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["check A for B: kiểm tra A để xác nhận B", "check for A: xác nhận A"],
                "needsReview": False
            },
            {
                "id": "check-n",
                "word": "check",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/tʃek/", "us": "/tʃek/"},
                "frequency": 2,
                "meaningVi": "sự kiểm tra; ngân phiếu, séc thanh toán",
                "exampleEn": "The customer wrote a check to pay for the order.",
                "exampleVi": "Khách hàng đã viết một tấm séc để thanh toán cho đơn hàng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "headquarters",
                "word": "headquarters",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌhedˈkwɔːtəz/", "us": "/ˌhedˈkwɔːrtərz/"},
                "frequency": 2,
                "meaningVi": "trụ sở chính",
                "exampleEn": "The company headquarters is located in London.",
                "exampleVi": "Trụ sở chính của công ty được đặt ở London.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "file-v",
                "word": "file",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/faɪl/", "us": "/faɪl/"},
                "frequency": 2,
                "meaningVi": "sắp xếp, lưu giữ (thư từ, giấy tờ); trình lên, đưa ra (văn kiện)",
                "exampleEn": "The department filed an insurance claim for the water damage in the conference room.",
                "exampleVi": "Phòng này đã đưa ra yêu cầu đòi bồi thường bảo hiểm cho thiệt hại do ngập nước trong phòng hội nghị.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["file a claim: yêu cầu bồi thường (ví dụ: tiền bảo hiểm)"],
                "needsReview": False
            },
            {
                "id": "file-n",
                "word": "file",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/faɪl/", "us": "/faɪl/"},
                "frequency": 2,
                "meaningVi": "hồ sơ, tài liệu, tệp tin",
                "exampleEn": "All files are organized alphabetically in the filing cabinet.",
                "exampleVi": "Tất cả các tài liệu được sắp xếp theo bảng chữ cái trong tủ hồ sơ.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "oversee",
                "word": "oversee",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˌəʊvəˈsiː/", "us": "/ˌoʊvərˈsiː/"},
                "frequency": 2,
                "meaningVi": "quan sát, giám sát",
                "exampleEn": "Natalie will oversee the office relocation process.",
                "exampleVi": "Natalie sẽ giám sát quá trình chuyển văn phòng.",
                "derivatives": [],
                "synonyms": ["supervise", "monitor"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "involved",
                "word": "involved",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪnˈvɒlvd/", "us": "/ɪnˈvɑːlvd/"},
                "frequency": 2,
                "meaningVi": "có tham gia vào, có liên quan",
                "exampleEn": "Dr. Mair was deeply involved in the decision-making process.",
                "exampleVi": "Tiến sĩ Mair có liên quan rất nhiều vào quá trình đưa ra quyết định.",
                "derivatives": [
                    {"word": "involve", "partOfSpeech": "v", "meaningVi": "liên quan, dính líu đến"},
                    {"word": "involvement", "partOfSpeech": "n", "meaningVi": "sự tham gia, sự liên quan"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["be involved in: có liên quan đến/tham gia vào cái gì"],
                "needsReview": False
            },
            {
                "id": "concentrate",
                "word": "concentrate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈkɒnsntreɪt/", "us": "/ˈkɑːnsntreɪt/"},
                "frequency": 2,
                "meaningVi": "tập trung, chú tâm",
                "exampleEn": "The sales team concentrated on developing new strategies.",
                "exampleVi": "Đội bán hàng đã tập trung vào việc phát triển chiến lược mới.",
                "derivatives": [
                    {"word": "concentration", "partOfSpeech": "n", "meaningVi": "sự tập trung"},
                    {"word": "concentrated", "partOfSpeech": "adj", "meaningVi": "tập trung"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["concentrate on: tập trung vào cái gì", "concentrate A on B: tập trung A vào B"],
                "needsReview": False
            }
        ]

    if day_num == 4:
        words_data = [
            {
                "id": "lax",
                "word": "lax",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/læks/", "us": "/læks/"},
                "frequency": 2,
                "meaningVi": "lơ là, cầu thả, không nghiêm túc",
                "exampleEn": "As of late, the staff has been rather lax in turning in reports.",
                "exampleVi": "Gần đây, các nhân viên có phần hơi thiếu nghiêm túc trong việc nộp báo cáo.",
                "derivatives": [],
                "synonyms": ["negligent"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "procrastinate",
                "word": "procrastinate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/prəˈkræstɪneɪt/", "us": "/proʊˈkræstɪneɪt/"},
                "frequency": 2,
                "meaningVi": "trì hoãn, chần chừ",
                "exampleEn": "Mr. Jones procrastinated with his fund request and missed the deadline.",
                "exampleVi": "Ông Jones trì hoãn việc yêu cầu cấp kinh phí của mình và đã bỏ lỡ thời hạn.",
                "derivatives": [
                    {"word": "procrastination", "partOfSpeech": "n", "meaningVi": "sự trì hoãn"}
                ],
                "synonyms": ["delay", "postpone"],
                "antonyms": ["hurry", "hasten"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "combined",
                "word": "combined",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/kəmˈbaɪnd/", "us": "/kəmˈbaɪnd/"},
                "frequency": 2,
                "meaningVi": "được kết hợp, chung, tổng hợp",
                "exampleEn": "Retail Specialists employs professionals with a combined experience of 30 years in sales.",
                "exampleVi": "Công ty Retail Specialists đã thuê những người chuyên nghiệp với 30 năm kinh nghiệm tổng hợp trong ngành bán hàng.",
                "derivatives": [
                    {"word": "combine", "partOfSpeech": "v", "meaningVi": "kết hợp"},
                    {"word": "combination", "partOfSpeech": "n", "meaningVi": "sự kết hợp"}
                ],
                "synonyms": ["joint"],
                "antonyms": [],
                "toeicNotes": ["combined experience: kinh nghiệm tổng hợp", "combined efforts: nỗ lực chung"],
                "needsReview": False
            },
            {
                "id": "accomplish",
                "word": "accomplish",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈkʌmplɪʃ/", "us": "/əˈdɑːmplɪʃ/"},
                "frequency": 2,
                "meaningVi": "hoàn thành, đạt được, làm xong",
                "exampleEn": "Careful planning is essential for accomplishing goals.",
                "exampleVi": "Lập kế hoạch cẩn thận rất cần thiết cho việc hoàn thành mục tiêu.",
                "derivatives": [
                    {"word": "accomplishment", "partOfSpeech": "n", "meaningVi": "sự hoàn thành, thành tựu"},
                    {"word": "accomplished", "partOfSpeech": "adj", "meaningVi": "tài năng, đã hoàn thành"}
                ],
                "synonyms": ["achieve", "fulfill"],
                "antonyms": [],
                "toeicNotes": ["accomplished author: tác giả tài năng"],
                "needsReview": False
            },
            {
                "id": "voluntarily",
                "word": "voluntarily",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈvɒləntrəli/", "us": "/ˌvɑːlənˈterəli/"},
                "frequency": 2,
                "meaningVi": "tự nguyện, tình nguyện",
                "exampleEn": "He voluntarily took on the challenging assignment in order to gain experience.",
                "exampleVi": "Anh ấy tình nguyện đảm nhiệm công việc đầy thách thức để lấy kinh nghiệm.",
                "derivatives": [
                    {"word": "voluntary", "partOfSpeech": "adj", "meaningVi": "tự nguyện"},
                    {"word": "volunteer", "partOfSpeech": "n", "meaningVi": "tình nguyện viên"}
                ],
                "synonyms": [],
                "antonyms": ["grudgingly"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "undertake",
                "word": "undertake",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˌʌndəˈteɪk/", "us": "/ˌʌndərˈteɪk/"},
                "frequency": 2,
                "meaningVi": "đảm nhận, tiếp quản",
                "exampleEn": "She had to undertake the task on short notice.",
                "exampleVi": "Cô ấy phải gánh vác nhiệm vụ đó khá gấp gáp.",
                "derivatives": [],
                "synonyms": ["take on", "assume"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "assume",
                "word": "assume",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈsjuːm/", "us": "/əˈsuːm/"},
                "frequency": 3,
                "meaningVi": "cho rằng, giả thiết; gánh vác, đảm nhận",
                "exampleEn": "The marketing department will assume responsibility for the project.",
                "exampleVi": "Bộ phận tiếp thị sẽ gánh vác trách nhiệm của dự án đó.",
                "derivatives": [
                    {"word": "assumption", "partOfSpeech": "n", "meaningVi": "sự giả định"}
                ],
                "synonyms": ["presume", "take on", "undertake"],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: assume (cho là, gánh vác), presume (giả sử, đoán chừng)"],
                "needsReview": False
            },
            {
                "id": "employee",
                "word": "employee",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪmˈplɔɪiː/", "us": "/ɪmˈplɔɪiː/"},
                "frequency": 3,
                "meaningVi": "nhân viên, người lao động",
                "exampleEn": "There are only three employees working under Ms. Anderson.",
                "exampleVi": "Chỉ có ba nhân viên làm việc dưới quyền cô Anderson.",
                "derivatives": [
                    {"word": "employer", "partOfSpeech": "n", "meaningVi": "chủ lao động"},
                    {"word": "employ", "partOfSpeech": "v", "meaningVi": "tuyển dụng"}
                ],
                "synonyms": ["worker", "staff member"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "assist",
                "word": "assist",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈsɪst/", "us": "/əˈsɪst/"},
                "frequency": 3,
                "meaningVi": "trợ giúp, hỗ trợ",
                "exampleEn": "A staff member assisted with preparations for the conference.",
                "exampleVi": "Một nhân viên đã hỗ trợ việc chuẩn bị cho hội nghị.",
                "derivatives": [
                    {"word": "assistant", "partOfSpeech": "n", "meaningVi": "trợ lý"},
                    {"word": "assistance", "partOfSpeech": "n", "meaningVi": "sự giúp đỡ"}
                ],
                "synonyms": ["help", "support"],
                "antonyms": [],
                "toeicNotes": ["assist with: hỗ trợ việc gì"],
                "needsReview": False
            },
            {
                "id": "satisfied",
                "word": "satisfied",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈsætɪsfaɪd/", "us": "/ˈsætɪsfaɪd/"},
                "frequency": 3,
                "meaningVi": "hài lòng, thỏa mãn",
                "exampleEn": "Not everyone was satisfied with changes to the overtime policy.",
                "exampleVi": "Không phải ai cũng thấy hài lòng với những thay đổi trong chính sách làm thêm giờ.",
                "derivatives": [
                    {"word": "satisfy", "partOfSpeech": "v", "meaningVi": "làm hài lòng"},
                    {"word": "satisfactory", "partOfSpeech": "adj", "meaningVi": "thỏa đáng, vừa lòng"}
                ],
                "synonyms": ["contented"],
                "antonyms": ["dissatisfied"],
                "toeicNotes": ["be satisfied with: hài lòng với"],
                "needsReview": False
            },
            {
                "id": "occasionally",
                "word": "occasionally",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/əˈkeɪʒnəli/", "us": "/əˈkeɪʒnəli/"},
                "frequency": 2,
                "meaningVi": "thỉnh thoảng, đôi khi",
                "exampleEn": "Staff should occasionally take time to relax so they do not get tired.",
                "exampleVi": "Thỉnh thoảng các nhân viên nên dành thời gian thư giãn để không bị mệt mỏi.",
                "derivatives": [
                    {"word": "occasional", "partOfSpeech": "adj", "meaningVi": "thỉnh thoảng"},
                    {"word": "occasion", "partOfSpeech": "n", "meaningVi": "dịp, cơ hội"}
                ],
                "synonyms": ["sometimes", "at times"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "manner",
                "word": "manner",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈmænə(r)/", "us": "/ˈmænər/"},
                "frequency": 2,
                "meaningVi": "cách, lối, thái độ, cử chỉ",
                "exampleEn": "Sean was annoyed by the manner in which his boss gave him orders.",
                "exampleVi": "Sean thấy bực mình với cái cách mà ông chủ ra lệnh cho anh ấy.",
                "derivatives": [],
                "synonyms": ["way", "fashion"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "responsible",
                "word": "responsible",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/rɪˈspɒnsəbl/", "us": "/rɪˈspɑːnsəbl/"},
                "frequency": 3,
                "meaningVi": "chịu trách nhiệm, có trách nhiệm",
                "exampleEn": "Businesses are responsible for ensuring customer satisfaction.",
                "exampleVi": "Các doanh nghiệp có trách nhiệm đảm bảo sự hài lòng của khách hàng.",
                "derivatives": [
                    {"word": "responsibility", "partOfSpeech": "n", "meaningVi": "trách nhiệm"}
                ],
                "synonyms": ["accountable", "liable"],
                "antonyms": [],
                "toeicNotes": ["be responsible for: chịu trách nhiệm về cái gì", "hold A responsible for B: bắt A chịu trách nhiệm về B", "Phân biệt: responsible (có trách nhiệm) và responsive (phản ứng nhanh, đáp lại nhiệt tình)"],
                "needsReview": False
            },
            {
                "id": "conduct",
                "word": "conduct",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kənˈdʌkt/", "us": "/kənˈdʌkt/"},
                "frequency": 3,
                "meaningVi": "tiến hành, thực hiện, chỉ đạo",
                "exampleEn": "IJMR Ltd's technology department will conduct the research study.",
                "exampleVi": "Bộ phận công nghệ của công ty IJMR sẽ tiến hành nghiên cứu này.",
                "derivatives": [],
                "synonyms": ["carry out", "perform"],
                "antonyms": [],
                "toeicNotes": ["conduct an inspection: tiến hành kiểm tra", "conduct a seminar: tổ chức hội thảo", "conduct research/study: thực hiện nghiên cứu/điều tra"],
                "needsReview": False
            },
            {
                "id": "adjust",
                "word": "adjust",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈdʒʌst/", "us": "/əˈdʒʌst/"},
                "frequency": 3,
                "meaningVi": "điều chỉnh, thích ứng, thích nghi",
                "exampleEn": "The employees quickly adjusted to the new e-mail system.",
                "exampleVi": "Các nhân viên đã nhanh chóng thích ứng với hệ thống thư điện tử mới.",
                "derivatives": [
                    {"word": "adjustment", "partOfSpeech": "n", "meaningVi": "sự điều chỉnh"},
                    {"word": "adjustable", "partOfSpeech": "adj", "meaningVi": "có thể điều chỉnh"}
                ],
                "synonyms": ["adapt", "fit"],
                "antonyms": [],
                "toeicNotes": ["adjust to: thích ứng với", "adjust A to B: điều chỉnh A cho phù hợp với B"],
                "needsReview": False
            },
            {
                "id": "personnel",
                "word": "personnel",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌpɜːsəˈnel/", "us": "/ˌpɜːrsəˈnel/"},
                "frequency": 3,
                "meaningVi": "nhân viên, công chức, phòng nhân sự",
                "exampleEn": "We often use an agency to find reliable temporary personnel.",
                "exampleVi": "Chúng tôi thường sử dụng công ty môi giới để tìm những nhân viên thời vụ đáng tin cậy.",
                "derivatives": [],
                "synonyms": ["staff", "employees"],
                "antonyms": [],
                "toeicNotes": ["sales personnel: nhân viên bán hàng", "personnel department: phòng nhân sự"],
                "needsReview": False
            },
            {
                "id": "agree",
                "word": "agree",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈɡriː/", "us": "/əˈɡriː/"},
                "frequency": 3,
                "meaningVi": "đồng ý, nhất trí, thỏa thuận",
                "exampleEn": "The team agreed on the recommendations of the advisor.",
                "exampleVi": "Nhóm đã nhất trí với những đề xuất của người cố vấn.",
                "derivatives": [
                    {"word": "agreement", "partOfSpeech": "n", "meaningVi": "sự đồng ý, thỏa thuận"}
                ],
                "synonyms": ["consent", "concur"],
                "antonyms": ["disagree"],
                "toeicNotes": [
                    "agree on + ý kiến/đề xuất: đồng ý, nhất trí về cái gì",
                    "agree to + phương án/điều kiện: tán thành phương án/điều kiện",
                    "agree with + người: đồng ý với ai",
                    "agree to do: đồng ý làm gì"
                ],
                "needsReview": False
            },
            {
                "id": "supervise",
                "word": "supervise",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈsuːpəvaɪz/", "us": "/ˈsuːpərvaɪz/"},
                "frequency": 3,
                "meaningVi": "giám sát",
                "exampleEn": "Ms. Wilson supervises the employees in sector B.",
                "exampleVi": "Cô Wilson giám sát các nhân viên ở khu vực B.",
                "derivatives": [
                    {"word": "supervision", "partOfSpeech": "n", "meaningVi": "sự giám sát"},
                    {"word": "supervisor", "partOfSpeech": "n", "meaningVi": "người giám sát"}
                ],
                "synonyms": ["oversee", "monitor"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "coworker",
                "word": "coworker",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌkəʊˈwɜːkə(r)/", "us": "/ˌkoʊˈwɜːrkər/"},
                "frequency": 3,
                "meaningVi": "đồng nghiệp",
                "exampleEn": "Coworkers who live near each other often travel to work together.",
                "exampleVi": "Các đồng nghiệp sống gần nhau thường đi làm cùng nhau.",
                "derivatives": [],
                "synonyms": ["coworker", "associate"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "direct",
                "word": "direct",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/daɪˈrekt/", "us": "/daɪˈrekt/"},
                "frequency": 3,
                "meaningVi": "hướng dẫn, chỉ đạo, chỉ đường",
                "exampleEn": "The receptionist directs new employees to the auditorium where orientation will be held.",
                "exampleVi": "Nhân viên lễ tân hướng dẫn nhân viên mới đến hội trường nơi tổ chức buổi định hướng.",
                "derivatives": [
                    {"word": "direction", "partOfSpeech": "n", "meaningVi": "sự chỉ dẫn, phương hướng"},
                    {"word": "director", "partOfSpeech": "n", "meaningVi": "giám đốc, người chỉ đạo"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["direct A to B: hướng dẫn A tới B"],
                "needsReview": False
            },
            {
                "id": "confidential",
                "word": "confidential",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˌkɒnfɪˈdenʃl/", "us": "/ˌkɑːnfɪˈdenʃl/"},
                "frequency": 2,
                "meaningVi": "bảo mật, cẩn mật, bí mật",
                "exampleEn": "Internal documents must be kept confidential.",
                "exampleVi": "Các tài liệu nội bộ phải được giữ bảo mật.",
                "derivatives": [
                    {"word": "confidentiality", "partOfSpeech": "n", "meaningVi": "sự cẩn mật, bảo mật"},
                    {"word": "confidentially", "partOfSpeech": "adv", "meaningVi": "một cách bí mật, cẩn mật"}
                ],
                "synonyms": ["secret", "classified"],
                "antonyms": [],
                "toeicNotes": ["Khi nói về bí mật liên quan đến chính phủ, tài liệu, ta có thể sử dụng classified, secret thay cho confidential."],
                "needsReview": False
            },
            {
                "id": "assign",
                "word": "assign",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈsaɪn/", "us": "/əˈsaɪn/"},
                "frequency": 2,
                "meaningVi": "phân công, bổ nhiệm, giao việc",
                "exampleEn": "The office manager assigned desks to the new recruits.",
                "exampleVi": "Người quản lý văn phòng đã phân công bàn làm việc cho các nhân viên mới tuyển dụng.",
                "derivatives": [
                    {"word": "assigned", "partOfSpeech": "adj", "meaningVi": "được phân công"},
                    {"word": "assignment", "partOfSpeech": "n", "meaningVi": "nhiệm vụ, công việc được giao"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "leading",
                "word": "leading",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈliːdɪŋ/", "us": "/ˈliːdɪŋ/"},
                "frequency": 2,
                "meaningVi": "dẫn đầu, hàng đầu, chủ đạo",
                "exampleEn": "Shepherd Industries is a leading exporter of wooden furniture.",
                "exampleVi": "Tập đoàn Shepherd là công ty xuất khẩu hàng đầu trong mảng đồ gỗ nội thất.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["leading company: công ty hàng đầu"],
                "needsReview": False
            },
            {
                "id": "formal",
                "word": "formal",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈfɔːml/", "us": "/ˈfɔːrml/"},
                "frequency": 2,
                "meaningVi": "trang trọng, chính thức",
                "exampleEn": "The awards ceremony requires wearing formal business attire.",
                "exampleVi": "Buổi lễ trao giải yêu cầu phải mặc trang phục công sở trang trọng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "remove",
                "word": "remove",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈmuːv/", "us": "/rɪˈmuːv/"},
                "frequency": 2,
                "meaningVi": "xóa bỏ, loại bỏ, cách chức, dọn đi",
                "exampleEn": "The vice president was removed from his position because of a scandal.",
                "exampleVi": "Ông phó chủ tịch đã bị cách chức khỏi vị trí của mình do một vụ bê bối.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["remove A from B: cách chức/xóa bỏ/dọn A khỏi B"],
                "needsReview": False
            },
            {
                "id": "collect",
                "word": "collect",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kəˈlekt/", "us": "/kəˈlekt/"},
                "frequency": 2,
                "meaningVi": "thu thập, tập hợp, thu lượm",
                "exampleEn": "The author collected management ideas from around the world for his book.",
                "exampleVi": "Tác giả đã tập hợp các ý tưởng về quản lý từ khắp nơi trên thế giới cho cuốn sách của mình.",
                "derivatives": [
                    {"word": "collective", "partOfSpeech": "adj", "meaningVi": "tập thể, chung"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "coordinate",
                "word": "coordinate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kəʊˈɔːdɪneɪt/", "us": "/koʊˈɔːrdneɪt/"},
                "frequency": 2,
                "meaningVi": "điều phối, phối hợp",
                "exampleEn": "The Chicago office coordinated the planning process.",
                "exampleVi": "Văn phòng ở Chicago đã điều phối quá trình lên kế hoạch.",
                "derivatives": [
                    {"word": "coordinator", "partOfSpeech": "n", "meaningVi": "điều phối viên"},
                    {"word": "coordination", "partOfSpeech": "n", "meaningVi": "sự phối hợp"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "hardly",
                "word": "hardly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈhɑːdli/", "us": "/ˈhɑːrdli/"},
                "frequency": 2,
                "meaningVi": "hầu như không, hiếm khi",
                "exampleEn": "She was hardly ever late for her shift.",
                "exampleVi": "Cô ấy hầu như không bao giờ đi muộn trong ca làm việc của mình.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["hardly ever: hầu như không bao giờ"],
                "needsReview": False
            },
            {
                "id": "abstract",
                "word": "abstract",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈæbstrækt/", "us": "/ˈæbstrækt/"},
                "frequency": 2,
                "meaningVi": "trừu tượng, mơ hồ",
                "exampleEn": "Copland spent thousands of dollars on an abstract painting for the lobby.",
                "exampleVi": "Copland đã chi hàng nghìn đô-la cho một bức tranh trừu tượng để treo ở tiền sảnh.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "directory",
                "word": "directory",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈdextri/", "us": "/daɪˈrektəri/"},
                "frequency": 2,
                "meaningVi": "danh bạ, sổ địa chỉ",
                "exampleEn": "The company directory shows where the marketing department is.",
                "exampleVi": "Danh bạ của công ty sẽ cho biết phòng tiếp thị nằm ở đâu.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "accountable",
                "word": "accountable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/əˈkaʊntəbl/", "us": "/əˈkaʊntəbl/"},
                "frequency": 2,
                "meaningVi": "chịu trách nhiệm giải trình",
                "exampleEn": "All employees are accountable for the duties they have been assigned to complete.",
                "exampleVi": "Mọi nhân viên phải chịu trách nhiệm cho các nhiệm vụ mà họ được giao để hoàn thành.",
                "derivatives": [
                    {"word": "accountability", "partOfSpeech": "n", "meaningVi": "trách nhiệm giải trình"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["be accountable for: chịu trách nhiệm về cái gì", "hold A accountable for B: bắt A chịu trách nhiệm về B", "be accountable to: chịu trách nhiệm trước ai"],
                "needsReview": False
            },
            {
                "id": "skillfully",
                "word": "skillfully",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈskɪlfəli/", "us": "/ˈskɪlfəli/"},
                "frequency": 2,
                "meaningVi": "thành thạo, khéo léo",
                "exampleEn": "Brenda skillfully edited the report to fit on one page.",
                "exampleVi": "Brenda đã khéo léo chỉnh sửa bản báo cáo cho vừa một trang giấy.",
                "derivatives": [
                    {"word": "skillful", "partOfSpeech": "adj", "meaningVi": "thành thạo, khéo léo"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "exclusive",
                "word": "exclusive",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪkˈskluːsɪv/", "us": "/ɪkˈskluːsɪv/"},
                "frequency": 2,
                "meaningVi": "riêng biệt, độc quyền",
                "exampleEn": "Delegates with special passes have exclusive access to a tour of the facilities.",
                "exampleVi": "Các đại biểu có thẻ đặc biệt sẽ được tham gia riêng một chuyến tham quan thực địa.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "intention",
                "word": "intention",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪnˈtenʃn/", "us": "/ɪnˈtenʃn/"},
                "frequency": 2,
                "meaningVi": "ý định, mục đích",
                "exampleEn": "She had every intention of attending the conference, but could not.",
                "exampleVi": "Cô ấy có ý định tham dự hội thảo nhưng lại không thể.",
                "derivatives": [
                    {"word": "intent", "partOfSpeech": "n", "meaningVi": "ý định, mục đích (không đếm được)"},
                    {"word": "intend", "partOfSpeech": "v", "meaningVi": "dự định"},
                    {"word": "intentional", "partOfSpeech": "adj", "meaningVi": "cố ý, có chủ ý"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["have every intention of -ing: nhất định phải làm gì"],
                "needsReview": False
            },
            {
                "id": "transform",
                "word": "transform",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/trænsˈfɔːm/", "us": "/trænsˈfɔːrm/"},
                "frequency": 2,
                "meaningVi": "biến đổi, thay đổi",
                "exampleEn": "Computerization has transformed the way companies do business.",
                "exampleVi": "Vi tính hóa đã thay đổi cách các công ty làm việc.",
                "derivatives": [
                    {"word": "transformation", "partOfSpeech": "n", "meaningVi": "sự biến đổi, sự thay đổi"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "respectful",
                "word": "respectful",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/rɪˈspektfl/", "us": "/rɪˈspektfl/"},
                "frequency": 2,
                "meaningVi": "tôn trọng, lễ phép, kính cẩn",
                "exampleEn": "Sales clerks are reminded to be respectful to all clients.",
                "exampleVi": "Các nhân viên bán hàng được nhắc nhở phải tôn trọng tất cả khách hàng.",
                "derivatives": [
                    {"word": "respect", "partOfSpeech": "v/n", "meaningVi": "tôn trọng/sự tôn trọng"},
                    {"word": "respectfully", "partOfSpeech": "adv", "meaningVi": "một cách kính cẩn"},
                    {"word": "respectable", "partOfSpeech": "adj", "meaningVi": "đáng kính"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["respect for: sự tôn trọng dành cho", "with respect: với sự tôn trọng"],
                "needsReview": False
            },
            {
                "id": "duplicate-n",
                "word": "duplicate",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈdjuːplɪkeɪt/", "us": "/ˈduːplɪkeɪt/"},
                "frequency": 2,
                "meaningVi": "bản sao",
                "exampleEn": "A duplicate of each contract is kept in the company records.",
                "exampleVi": "Bản sao của mỗi hợp đồng được lưu giữ trong tài liệu hồ sơ của công ty.",
                "derivatives": [],
                "synonyms": ["copy"],
                "antonyms": ["original"],
                "toeicNotes": ["make duplicates of: sao chép lại cái gì", "in duplicate: làm thành 2 bản"],
                "needsReview": False
            },
            {
                "id": "duplicate-v",
                "word": "duplicate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈdjuːplɪkeɪt/", "us": "/ˈduːplɪkeɪt/"},
                "frequency": 2,
                "meaningVi": "nhân đôi, sao chép",
                "exampleEn": "The system will duplicate the database for backup purposes.",
                "exampleVi": "Hệ thống sẽ sao chép cơ sở dữ liệu cho mục đích dự phòng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "contrary",
                "word": "contrary",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈkɒntrəri/", "us": "/ˈkɑːntreri/"},
                "frequency": 2,
                "meaningVi": "sự trái ngược, điều ngược lại",
                "exampleEn": "Techworld is in financial trouble, despite claims to the contrary.",
                "exampleVi": "Techworld đang gặp khó khăn về tài chính mặc dù họ tuyên bố điều ngược lại.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["evidence to the contrary: bằng chứng chứng minh điều ngược lại", "on the contrary: trái lại, ngược lại"],
                "needsReview": False
            },
            {
                "id": "disturbing",
                "word": "disturbing",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/dɪˈstɜːbɪŋ/", "us": "/dɪˈstɜːrbɪŋ/"},
                "frequency": 2,
                "meaningVi": "làm nhiễu loạn, xáo trộn, đáng lo ngại",
                "exampleEn": "Shareholders found reports of the CEO's incompetence disturbing.",
                "exampleVi": "Các cổ đông nhận thấy những báo cáo về sự kém cỏi của vị giám đốc điều hành thật gây nhiễu loạn.",
                "derivatives": [
                    {"word": "disturb", "partOfSpeech": "v", "meaningVi": "làm phiền, quấy rầy"},
                    {"word": "disturbance", "partOfSpeech": "n", "meaningVi": "sự làm phiền"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "engage",
                "word": "engage",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈɡeɪdʒ/", "us": "/ɪnˈɡeɪdʒ/"},
                "frequency": 2,
                "meaningVi": "tham gia, cam kết, thu hút",
                "exampleEn": "Each worker was engaged in at least two projects.",
                "exampleVi": "Mỗi công nhân đều được tham gia vào ít nhất hai dự án.",
                "derivatives": [
                    {"word": "engagement", "partOfSpeech": "n", "meaningVi": "sự hứa hẹn, cam kết, sự đính hôn"},
                    {"word": "engaging", "partOfSpeech": "adj", "meaningVi": "cuốn hút, duyên dáng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["engage in: tham gia vào cái gì", "be engaged in: liên quan đến/bận rộn với cái gì"],
                "needsReview": False
            },
            {
                "id": "foster",
                "word": "foster",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈfɒstə(r)/", "us": "/ˈfɑːstər/"},
                "frequency": 2,
                "meaningVi": "thúc đẩy, bồi dưỡng, bồi đắp",
                "exampleEn": "Staff dinners helped foster better work relations.",
                "exampleVi": "Những bữa tối giữa các nhân viên đã giúp bồi đắp mối quan hệ tốt hơn trong công việc.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: foster (thúc đẩy về quan hệ/sự kiện), enlarge (mở rộng về vật lý như bãi đỗ xe)"],
                "needsReview": False
            },
            {
                "id": "neutrality",
                "word": "neutrality",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/njuːˈtræləti/", "us": "/nuːˈtræləti/"},
                "frequency": 2,
                "meaningVi": "tính chất trung lập, thái độ trung lập",
                "exampleEn": "Managers must display complete neutrality in disagreements between employees.",
                "exampleVi": "Người quản lý phải giữ thái độ hoàn toàn trung lập trong những cuộc tranh cãi giữa các nhân viên.",
                "derivatives": [
                    {"word": "neutral", "partOfSpeech": "adj", "meaningVi": "trung lập"},
                    {"word": "neutrally", "partOfSpeech": "adv", "meaningVi": "một cách trung lập"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "widely",
                "word": "widely",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈwaɪdli/", "us": "/ˈwaɪdli/"},
                "frequency": 2,
                "meaningVi": "rộng rãi, nhiều, rộng khắp",
                "exampleEn": "Ben Hurley is a widely admired business leader.",
                "exampleVi": "Ben Hurley là một nhà điều hành doanh nghiệp được nhiều người ngưỡng mộ.",
                "derivatives": [
                    {"word": "wide", "partOfSpeech": "adj", "meaningVi": "rộng"},
                    {"word": "width", "partOfSpeech": "n", "meaningVi": "bề rộng"},
                    {"word": "widen", "partOfSpeech": "v", "meaningVi": "mở rộng"}
                ],
                "toeicNotes": [],
                "needsReview": False
            }
        ]

    if day_num == 5:
        words_data = [
            {
                "id": "sophisticated",
                "word": "sophisticated",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/səˈfɪstɪkeɪtɪd/", "us": "/səˈfɪstɪkeɪtɪd/"},
                "frequency": 2,
                "meaningVi": "tinh vi, tinh tế, phức tạp, công phu",
                "exampleEn": "A sophisticated surveillance system was installed.",
                "exampleVi": "Một hệ thống giám sát tinh vi đã được cài đặt.",
                "derivatives": [
                    {"word": "sophistication", "partOfSpeech": "n", "meaningVi": "sự tinh vi"}
                ],
                "synonyms": ["complex", "refined"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "timely",
                "word": "timely",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈtaɪmli/", "us": "/ˈtaɪmli/"},
                "frequency": 2,
                "meaningVi": "kịp thời, đúng lúc",
                "exampleEn": "The report was completed in a timely manner.",
                "exampleVi": "Bản báo cáo đã được hoàn thành kịp thời.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["in a timely manner: kịp thời"],
                "needsReview": False
            },
            {
                "id": "realistically",
                "word": "realistically",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˌrɪəˈlɪstɪkli/", "us": "/ˌriːəˈlɪstɪkli/"},
                "frequency": 2,
                "meaningVi": "theo thực tế, thực tế là",
                "exampleEn": "We cannot realistically expect to have the presentation ready on time.",
                "exampleVi": "Thực tế là chúng tôi không thể mong đợi bài thuyết trình đó được hoàn thành kịp thời hạn.",
                "derivatives": [
                    {"word": "realistic", "partOfSpeech": "adj", "meaningVi": "thực tế"},
                    {"word": "realism", "partOfSpeech": "n", "meaningVi": "chủ nghĩa hiện thực"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["cannot realistically expect + to-V: thực tế là không thể mong đợi làm gì", "realistic expectation/goal: kỳ vọng/mục tiêu thực tế"],
                "needsReview": False
            },
            {
                "id": "promptly",
                "word": "promptly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈprɒmptli/", "us": "/ˈprɑːmptli/"},
                "frequency": 2,
                "meaningVi": "nhanh chóng, ngay lập tức, đúng giờ",
                "exampleEn": "It is company policy to respond promptly to all inquiries.",
                "exampleVi": "Chính sách của công ty là phản hồi mọi thắc mắc ngay lập tức.",
                "derivatives": [
                    {"word": "prompt", "partOfSpeech": "adj", "meaningVi": "nhanh chóng, mau lẹ"}
                ],
                "synonyms": ["immediately", "instantly"],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: promptly (ngay tức khắc, không trì hoãn) và abruptly (đột ngột, bất ngờ ngoài dự tính)"],
                "needsReview": False
            },
            {
                "id": "accessible",
                "word": "accessible",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/əkˈsesəbl/", "us": "/ækˈsesəbl/"},
                "frequency": 2,
                "meaningVi": "có thể tiếp cận được, có thể sử dụng được",
                "exampleEn": "The 18th floor is only accessible to executive staff.",
                "exampleVi": "Chỉ nhân viên ban điều hành mới có thể tiếp cận tầng 18.",
                "derivatives": [
                    {"word": "access", "partOfSpeech": "v/n", "meaningVi": "truy cập/sự truy cập"},
                    {"word": "accessibility", "partOfSpeech": "n", "meaningVi": "khả năng tiếp cận"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["make A accessible to B: làm cho B tiếp cận được A", "accessible by bus/subway: có thể đi đến bằng xe buýt/tàu điện ngầm"],
                "needsReview": False
            },
            {
                "id": "implement",
                "word": "implement",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɪmplɪment/", "us": "/ˈɪmplɪment/"},
                "frequency": 2,
                "meaningVi": "thi hành, thực hiện, tiến hành",
                "exampleEn": "Board members voted to implement an innovative marketing campaign.",
                "exampleVi": "Các thành viên hội đồng quản trị đã biểu quyết để tiến hành một chiến dịch tiếp thị sáng tạo.",
                "derivatives": [
                    {"word": "implementation", "partOfSpeech": "n", "meaningVi": "sự thi hành"}
                ],
                "synonyms": ["carry out", "execute"],
                "antonyms": [],
                "toeicNotes": ["implement a plan: thực hiện một kế hoạch", "implement measures: thực hiện các biện pháp"],
                "needsReview": False
            },
            {
                "id": "feedback",
                "word": "feedback",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈfiːdbæk/", "us": "/ˈfiːdbæk/"},
                "frequency": 2,
                "meaningVi": "phản hồi, ý kiến nhận xét",
                "exampleEn": "Feedback from colleagues can be of great assistance.",
                "exampleVi": "Ý kiến nhận xét từ các đồng nghiệp có thể là một sự trợ giúp rất lớn.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "outstanding",
                "word": "outstanding",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/aʊtˈstændɪŋ/", "us": "/aʊtˈstændɪŋ/"},
                "frequency": 3,
                "meaningVi": "nổi bật, đáng chú ý; còn tồn tại, chưa thanh toán (tiền nợ)",
                "exampleEn": "The director presented an outstanding business plan.",
                "exampleVi": "Giám đốc đã trình bày một kế hoạch kinh doanh xuất sắc.",
                "derivatives": [],
                "synonyms": ["exceptional", "overdue", "unpaid"],
                "antonyms": [],
                "toeicNotes": ["outstanding debt: khoản nợ chưa thanh toán"],
                "needsReview": False
            },
            {
                "id": "inform",
                "word": "inform",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈfɔːm/", "us": "/ɪnˈfɔːrm/"},
                "frequency": 3,
                "meaningVi": "thông báo, báo tin",
                "exampleEn": "Please inform the director that the meeting has been canceled.",
                "exampleVi": "Vui lòng báo cho giám đốc biết là cuộc họp đã bị hủy.",
                "derivatives": [
                    {"word": "information", "partOfSpeech": "n", "meaningVi": "thông tin"},
                    {"word": "informative", "partOfSpeech": "adj", "meaningVi": "nhiều thông tin, bổ ích"}
                ],
                "synonyms": ["notify"],
                "antonyms": [],
                "toeicNotes": [
                    "inform sb of sth / that...: báo cho ai biết về cái gì (sau inform là tân ngữ chỉ người)",
                    "Phân biệt: inform (báo cho ai biết) và explain (giải thích cho ai - explain to sb that...)"
                ],
                "needsReview": False
            },
            {
                "id": "explain",
                "word": "explain",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪkˈspleɪn/", "us": "/ɪkˈspleɪn/"},
                "frequency": 3,
                "meaningVi": "giải thích, giảng giải",
                "exampleEn": "The CEO explained to the board that the company was in trouble.",
                "exampleVi": "Giám đốc điều hành giải thích với hội đồng quản trị rằng công ty đang gặp rắc rối.",
                "derivatives": [
                    {"word": "explanation", "partOfSpeech": "n", "meaningVi": "sự giải thích"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["explain to sb that...: giải thích với ai rằng (luôn có 'to' trước người nghe)"],
                "needsReview": False
            },
            {
                "id": "replacement",
                "word": "replacement",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈpleɪsmənt/", "us": "/rɪˈpleɪsmənt/"},
                "frequency": 3,
                "meaningVi": "sự thay thế, người/vật thay thế",
                "exampleEn": "Human resources is looking for a replacement for Mr. Winters.",
                "exampleVi": "Bộ phận nhân sự đang tìm một người thay thế cho ông Winters.",
                "derivatives": [
                    {"word": "replace", "partOfSpeech": "v", "meaningVi": "thay thế"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["replacement for: người/vật thay thế cho"],
                "needsReview": False
            },
            {
                "id": "announcement",
                "word": "announcement",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈnaʊnsmənt/", "us": "/əˈnaʊnsmənt/"},
                "frequency": 2,
                "meaningVi": "thông cáo, thông báo",
                "exampleEn": "Mr. Dane posted an announcement about the general meeting.",
                "exampleVi": "Ông Dane đã đăng một thông báo về đại hội cổ đông.",
                "derivatives": [
                    {"word": "announce", "partOfSpeech": "v", "meaningVi": "thông báo"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "department",
                "word": "department",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈpɑːtmənt/", "us": "/dɪˈpɑːrtmənt/"},
                "frequency": 3,
                "meaningVi": "bộ, ban, phòng ban",
                "exampleEn": "Report payroll problems to the finance department.",
                "exampleVi": "Hãy báo cáo những vấn đề về tiền lương cho bộ phận tài chính.",
                "derivatives": [],
                "synonyms": ["division", "section"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "permanently",
                "word": "permanently",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈpɜːmənəntli/", "us": "/ˈpɜːrmənəntli/"},
                "frequency": 3,
                "meaningVi": "vĩnh viễn, lâu dài, cố định",
                "exampleEn": "The computer files have been permanently deleted and cannot be retrieved.",
                "exampleVi": "Các tệp máy tính đã bị xóa vĩnh viễn và không thể khôi phục lại.",
                "derivatives": [
                    {"word": "permanent", "partOfSpeech": "adj", "meaningVi": "vĩnh viễn, lâu bền"}
                ],
                "synonyms": ["indefinitely"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "fulfill",
                "word": "fulfill",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/fʊlˈfɪl/", "us": "/fʊlˈfɪl/"},
                "frequency": 3,
                "meaningVi": "hoàn thành, đáp ứng (yêu cầu), thực thi",
                "exampleEn": "The final product design fulfilled the terms of the contract.",
                "exampleVi": "Thiết kế sản phẩm cuối cùng đã đáp ứng các điều khoản của hợp đồng.",
                "derivatives": [
                    {"word": "fulfillment", "partOfSpeech": "n", "meaningVi": "sự hoàn thành, sự đáp ứng"}
                ],
                "synonyms": ["meet", "satisfy"],
                "antonyms": [],
                "toeicNotes": ["fulfill the terms/requirements: đáp ứng các điều khoản/yêu cầu"],
                "needsReview": False
            },
            {
                "id": "outline-n",
                "word": "outline",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈaʊtlaɪn/", "us": "/ˈaʊtlaɪn/"},
                "frequency": 2,
                "meaningVi": "dàn bài, đề cương, nét phác thảo",
                "exampleEn": "Begin making the report by arranging the main ideas in an outline.",
                "exampleVi": "Hãy bắt đầu làm báo cáo bằng cách sắp xếp các ý chính trong một dàn bài.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "outline-v",
                "word": "outline",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈaʊtlaɪn/", "us": "/ˈaʊtlaɪn/"},
                "frequency": 2,
                "meaningVi": "phác thảo, vạch ra, nêu những nét chính",
                "exampleEn": "The salesman outlined the features of the vacuum cleaner.",
                "exampleVi": "Nhân viên bán hàng đã nêu những nét chính về tính năng của chiếc máy hút bụi.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "contain",
                "word": "contain",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kənˈteɪn/", "us": "/kənˈteɪn/"},
                "frequency": 3,
                "meaningVi": "bao gồm, chứa, chứa đựng; kìm nén",
                "exampleEn": "The filing cabinet contains copies of all our invoices.",
                "exampleVi": "Tủ hồ sơ chứa bản sao tất cả các hóa đơn của chúng ta.",
                "derivatives": [],
                "synonyms": ["include"],
                "antonyms": [],
                "toeicNotes": ["Khi mang nghĩa 'bao gồm' có thể thay bằng include; khi mang nghĩa 'kìm nén' có thể thay bằng control/hold back"],
                "needsReview": False
            },
            {
                "id": "compile",
                "word": "compile",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kəmˈpaɪl/", "us": "/kəmˈpaɪl/"},
                "frequency": 3,
                "meaningVi": "biên soạn, tập hợp, tổng hợp (tài liệu)",
                "exampleEn": "The assistant compiled a list of tablet computer manufacturers.",
                "exampleVi": "Người trợ lý đã tổng hợp một danh sách các nhà sản xuất máy tính bảng.",
                "derivatives": [
                    {"word": "compilation", "partOfSpeech": "n", "meaningVi": "sự biên soạn, tài liệu tổng hợp"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "subsequent",
                "word": "subsequent",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈsʌbsɪkwənt/", "us": "/ˈsʌbsɪkwənt/"},
                "frequency": 3,
                "meaningVi": "đến sau, xảy ra sau, tiếp theo",
                "exampleEn": "Some employees received separation pay subsequent to the company's closing.",
                "exampleVi": "Một số nhân viên đã nhận được khoản tiền bồi thường thôi việc sau khi công ty bị đóng cửa.",
                "derivatives": [
                    {"word": "subsequently", "partOfSpeech": "adv", "meaningVi": "sau đó"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["subsequent to: sau khi (= after)"],
                "needsReview": False
            },
            {
                "id": "overview",
                "word": "overview",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈəʊvəvjuː/", "us": "/ˈoʊvərvjuː/"},
                "frequency": 2,
                "meaningVi": "tổng quát, khái quát, cái nhìn tổng thể",
                "exampleEn": "Scott gave an overview of the topic before the presentation.",
                "exampleVi": "Scott đã đưa ra một cái nhìn khái quát về chủ đề trước khi thuyết trình.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "provider",
                "word": "provider",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/prəˈvaɪdə(r)/", "us": "/prəˈvaɪdər/"},
                "frequency": 2,
                "meaningVi": "nhà cung cấp, người cung cấp",
                "exampleEn": "There are numerous Internet and cable providers in the city.",
                "exampleVi": "Có rất nhiều nhà cung cấp dịch vụ Internet và truyền hình cáp trong thành phố.",
                "derivatives": [
                    {"word": "provide", "partOfSpeech": "v", "meaningVi": "cung cấp"},
                    {"word": "provision", "partOfSpeech": "n", "meaningVi": "sự cung cấp, điều khoản"}
                ],
                "synonyms": ["supplier"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "matter",
                "word": "matter",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈmætə(r)/", "us": "/ˈmætər/"},
                "frequency": 2,
                "meaningVi": "vấn đề, công việc",
                "exampleEn": "Please deal with personal matters outside the office.",
                "exampleVi": "Vui lòng giải quyết các vấn đề cá nhân ở ngoài văn phòng.",
                "derivatives": [],
                "synonyms": ["issue", "problem"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "expertise",
                "word": "expertise",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌekspɜːˈtiːz/", "us": "/ˌekspɜːrˈtiːz/"},
                "frequency": 3,
                "meaningVi": "sự tinh thông, thành thạo, kỹ năng chuyên môn",
                "exampleEn": "This kind of project falls outside the firm's area of expertise.",
                "exampleVi": "Loại dự án này nằm ngoài lĩnh vực chuyên môn của công ty.",
                "derivatives": [
                    {"word": "expert", "partOfSpeech": "n/adj", "meaningVi": "chuyên gia/thành thạo"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["have expertise in: có năng lực chuyên môn về", "area of expertise: lĩnh vực chuyên môn"],
                "needsReview": False
            },
            {
                "id": "demonstrate",
                "word": "demonstrate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈdemənstreɪt/", "us": "/ˈdemənstreɪt/"},
                "frequency": 2,
                "meaningVi": "chưng minh, minh họa, biểu lộ, cho thấy",
                "exampleEn": "Sales figures demonstrate that the advertising campaign was successful.",
                "exampleVi": "Các số liệu bán hàng chứng minh rằng chiến dịch quảng cáo đã thành công.",
                "derivatives": [
                    {"word": "demonstration", "partOfSpeech": "n", "meaningVi": "sự chứng minh, minh họa"}
                ],
                "synonyms": ["prove", "explain"],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: demonstrate (minh họa, giới thiệu cách sử dụng) và display (trưng bày vật để nhìn thấy)"],
                "needsReview": False
            },
            {
                "id": "remainder",
                "word": "remainder",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈmeɪndə(r)/", "us": "/rɪˈmeɪndər/"},
                "frequency": 2,
                "meaningVi": "người/vật còn lại, phần còn lại",
                "exampleEn": "Audits will continue throughout the remainder of the month.",
                "exampleVi": "Việc kiểm toán sẽ tiếp tục trong suốt thời gian còn lại của tháng.",
                "derivatives": [
                    {"word": "remain", "partOfSpeech": "v", "meaningVi": "còn lại, giữ nguyên"},
                    {"word": "remaining", "partOfSpeech": "adj", "meaningVi": "còn lại"}
                ],
                "synonyms": ["balance"],
                "antonyms": [],
                "toeicNotes": ["throughout the remainder of: trong suốt phần còn lại của", "Phân biệt: remainder (phần còn lại) và reminder (lời nhắc nhở)"],
                "needsReview": False
            },
            {
                "id": "essential",
                "word": "essential",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪˈsenʃl/", "us": "/ɪˈsenʃl/"},
                "frequency": 2,
                "meaningVi": "cần thiết, thiết yếu, cốt yếu",
                "exampleEn": "Perseverance is essential to success in business.",
                "exampleVi": "Sự kiên trì rất cần thiết để thành công trong kinh doanh.",
                "derivatives": [
                    {"word": "essentially", "partOfSpeech": "adv", "meaningVi": "về bản chất"}
                ],
                "synonyms": ["necessary", "vital"],
                "antonyms": [],
                "toeicNotes": ["be essential to/for: cần thiết để/cho cái gì"],
                "needsReview": False
            },
            {
                "id": "divide",
                "word": "divide",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/dɪˈvaɪd/", "us": "/dɪˈvaɪd/"},
                "frequency": 2,
                "meaningVi": "chia ra, phân chia",
                "exampleEn": "Required overtime will be divided equally among employees.",
                "exampleVi": "Thời gian làm ngoài giờ bắt buộc sẽ được phân chia công bằng giữa các nhân viên.",
                "derivatives": [
                    {"word": "division", "partOfSpeech": "n", "meaningVi": "sự phân chia, bộ phận"},
                    {"word": "dividend", "partOfSpeech": "n", "meaningVi": "cổ tức"}
                ],
                "synonyms": ["break up"],
                "antonyms": [],
                "toeicNotes": ["divide A into B: chia A thành B", "be divided into: được phân chia thành", "Phân biệt: divide (chia thành nhiều phần) và cut (cắt giảm số lượng)"],
                "needsReview": False
            },
            {
                "id": "major",
                "word": "major",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈmeɪdʒə(r)/", "us": "/ˈmeɪdʒər/"},
                "frequency": 2,
                "meaningVi": "chủ yếu, chủ chốt, trọng đại, lớn",
                "exampleEn": "The new manager has had a major impact on productivity.",
                "exampleVi": "Người quản lý mới có một ảnh hưởng quan trọng tới năng suất làm việc.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["minor"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "compliance",
                "word": "compliance",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kəmˈplaɪəns/", "us": "/kəmˈplaɪəns/"},
                "frequency": 2,
                "meaningVi": "sự tuân thủ, tuân theo (luật pháp, quy định)",
                "exampleEn": "Government officials will inspect the plant's compliance with safety guidelines.",
                "exampleVi": "Các quan chức chính phủ sẽ giám sát việc tuân thủ các quy định an toàn của nhà máy.",
                "derivatives": [
                    {"word": "comply", "partOfSpeech": "v", "meaningVi": "tuân theo"},
                    {"word": "compliant", "partOfSpeech": "adj", "meaningVi": "tuân thủ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["in compliance with: tuân theo cái gì", "out of compliance with: không tuân theo cái gì"],
                "needsReview": False
            },
            {
                "id": "clarify",
                "word": "clarify",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈklærɪfaɪ/", "us": "/ˈklærɪfaɪ/"},
                "frequency": 2,
                "meaningVi": "làm rõ, làm sáng tỏ",
                "exampleEn": "The notice clarified some details of the vacation policy modifications.",
                "exampleVi": "Thông báo đã làm rõ một số chi tiết trong những thay đổi về chính sách nghỉ phép.",
                "derivatives": [
                    {"word": "clarification", "partOfSpeech": "n", "meaningVi": "sự làm rõ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "face",
                "word": "face",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/feɪs/", "us": "/feɪs/"},
                "frequency": 2,
                "meaningVi": "đương đầu, đối mặt, hướng về",
                "exampleEn": "Businesses are faced with the challenge of foreign competition.",
                "exampleVi": "Các doanh nghiệp phải đối mặt với thách thức cạnh tranh từ nước ngoài.",
                "derivatives": [],
                "synonyms": ["confront"],
                "antonyms": [],
                "toeicNotes": ["be faced with: đối mặt với"],
                "needsReview": False
            },
            {
                "id": "follow",
                "word": "follow",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈfɒləʊ/", "us": "/ˈfɑːloʊ/"},
                "frequency": 3,
                "meaningVi": "đi theo, theo dõi, chú ý; hiểu",
                "exampleEn": "Bill followed the conversations at the meeting closely.",
                "exampleVi": "Bill theo dõi sát sao các cuộc trao đổi trong buổi họp.",
                "derivatives": [
                    {"word": "following", "partOfSpeech": "prep/adj", "meaningVi": "sau, tiếp theo/dưới đây"}
                ],
                "synonyms": ["monitor", "understand"],
                "antonyms": ["precede"],
                "toeicNotes": ["Phân biệt: follow (theo sau) và precede (đi trước về thời gian)"],
                "needsReview": False
            },
            {
                "id": "aspect",
                "word": "aspect",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈæspekt/", "us": "/ˈæspekt/"},
                "frequency": 2,
                "meaningVi": "khía cạnh, mặt",
                "exampleEn": "Every aspect of the problem must be taken into consideration.",
                "exampleVi": "Mọi khía cạnh của vấn đề này đều phải được cân nhắc.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "apparently",
                "word": "apparently",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/əˈpærəntli/", "us": "/əˈpærəntli/"},
                "frequency": 2,
                "meaningVi": "hình như, có vẻ, nhìn bên ngoài",
                "exampleEn": "Apparently, Mr. Jones was not invited to this meeting.",
                "exampleVi": "Hình như ông Jones không được mời tới buổi họp này.",
                "derivatives": [
                    {"word": "apparent", "partOfSpeech": "adj", "meaningVi": "rõ ràng, có vẻ"}
                ],
                "synonyms": ["seemingly"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "aware",
                "word": "aware",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/əˈweə(r)/", "us": "/əˈwer/"},
                "frequency": 2,
                "meaningVi": "biết, ý thức được, nhận thức được",
                "exampleEn": "Workers should be made aware of safety procedures.",
                "exampleVi": "Cần cho công nhân biết về các quy trình an toàn.",
                "derivatives": [
                    {"word": "awareness", "partOfSpeech": "n", "meaningVi": "sự nhận thức"}
                ],
                "synonyms": [],
                "antonyms": ["unaware"],
                "toeicNotes": ["be aware of / that...: nhận thức được về cái gì"],
                "needsReview": False
            },
            {
                "id": "extended",
                "word": "extended",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪkˈstendɪd/", "us": "/ɪkˈstendɪd/"},
                "frequency": 2,
                "meaningVi": "mở rộng, kéo dài",
                "exampleEn": "The accounting department works extended hours on the first week of every month.",
                "exampleVi": "Bộ phận kế toán phải làm thêm giờ vào tuần đầu tiên hằng tháng.",
                "derivatives": [
                    {"word": "extend", "partOfSpeech": "v", "meaningVi": "mở rộng, kéo dài"},
                    {"word": "extension", "partOfSpeech": "n", "meaningVi": "sự mở rộng, gia hạn"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["work extended hours: làm tăng giờ, làm thêm giờ", "extended lunch break: giờ nghỉ trưa kéo dài"],
                "needsReview": False
            },
            {
                "id": "accidentally",
                "word": "accidentally",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˌæksɪˈdentəli/", "us": "/ˌæksɪˈdentəli/"},
                "frequency": 2,
                "meaningVi": "tình cờ, vô tình, ngoài ý muốn",
                "exampleEn": "Alison accidentally made some errors in the financial statements.",
                "exampleVi": "Alison đã vô tình mắc một vài sai sót trong báo cáo tài chính.",
                "derivatives": [
                    {"word": "accident", "partOfSpeech": "n", "meaningVi": "tai nạn"},
                    {"word": "accidental", "partOfSpeech": "adj", "meaningVi": "tình cờ"}
                ],
                "synonyms": [],
                "antonyms": ["deliberately"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "advisable",
                "word": "advisable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ədˈvaɪzəbl/", "us": "/ədˈvaɪzəbl/"},
                "frequency": 2,
                "meaningVi": "nên làm, thích hợp",
                "exampleEn": "It is advisable to update computer equipment regularly.",
                "exampleVi": "Nâng cấp thiết bị máy tính thường xuyên là việc nên làm.",
                "derivatives": [
                    {"word": "advise", "partOfSpeech": "v", "meaningVi": "khuyên bảo"},
                    {"word": "advice", "partOfSpeech": "n", "meaningVi": "lời khuyên"}
                ],
                "synonyms": [],
                "antonyms": ["inadvisable"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "concerned",
                "word": "concerned",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/kənˈsɜːnd/", "us": "/kənˈsɜːrnd/"},
                "frequency": 2,
                "meaningVi": "lo lắng, lo âu, có liên quan đến",
                "exampleEn": "Management is concerned about security.",
                "exampleVi": "Ban quản lý đang lo lắng về vấn đề an ninh.",
                "derivatives": [
                    {"word": "concern", "partOfSpeech": "v/n", "meaningVi": "lo lắng/mối quan tâm"}
                ],
                "synonyms": [],
                "antonyms": ["unconcerned"],
                "toeicNotes": ["be concerned about: lo lắng về", "be concerned with: liên quan đến/quan tâm đến"],
                "needsReview": False
            },
            {
                "id": "speak",
                "word": "speak",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/spiːk/", "us": "/spiːk/"},
                "frequency": 3,
                "meaningVi": "nói",
                "exampleEn": "Mr. Brooke spoke to his clients about a new venture.",
                "exampleVi": "Ông Brooke đã nói với các khách hàng của mình về một dự án kinh doanh mạo hiểm mới.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["speak to sb about sth: nói với ai về việc gì", "Phân biệt: speak (nói - nội động từ cần to trước người nghe), tell (nói với ai - tell sb that...), say (nói - say to sb that...)"],
                "needsReview": False
            }
        ]

    if day_num == 6:
        words_data = [
            {
                "id": "collection",
                "word": "collection",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kəˈlekʃn/", "us": "/kəˈlekʃn/"},
                "frequency": 3,
                "meaningVi": "bộ sưu tập, sự thu thập, sự quyên góp",
                "exampleEn": "The museum has a unique collection of stamps.",
                "exampleVi": "Bảo tàng sở hữu một bộ sưu tập tem độc đáo.",
                "derivatives": [
                    {"word": "collect", "partOfSpeech": "v", "meaningVi": "thu thập, quyên góp"},
                    {"word": "collector", "partOfSpeech": "n", "meaningVi": "người sưu tầm"},
                    {"word": "collectable", "partOfSpeech": "n", "meaningVi": "đồ sưu tầm"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["toll collection: việc thu phí cầu đường"],
                "needsReview": False
            },
            {
                "id": "exhibition",
                "word": "exhibition",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌeksɪˈbɪʃn/", "us": "/ˌeksɪˈbɪʃn/"},
                "frequency": 3,
                "meaningVi": "cuộc triển lãm, sự trưng bày",
                "exampleEn": "The art exhibition will run for the next two weeks.",
                "exampleVi": "Cuộc triển lãm nghệ thuật sẽ diễn ra trong hai tuần tới.",
                "derivatives": [
                    {"word": "exhibit", "partOfSpeech": "v/n", "meaningVi": "trưng bày/vật trưng bày"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "celebrity",
                "word": "celebrity",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/səˈlebrəti/", "us": "/səˈlebrəti/"},
                "frequency": 2,
                "meaningVi": "người nổi tiếng",
                "exampleEn": "Famous athlete Matt London was present at the game.",
                "exampleVi": "Vận động viên điền kinh nổi tiếng Matt London đã có mặt trong trận thi đấu đó.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "live-adj",
                "word": "live",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/laɪv/", "us": "/laɪv/"},
                "frequency": 1,
                "meaningVi": "trực tiếp (buổi diễn), sống động",
                "exampleEn": "The band will give a live performance tonight.",
                "exampleVi": "Ban nhạc sẽ có một buổi biểu diễn trực tiếp tối nay.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "live-v",
                "word": "live",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/lɪv/", "us": "/lɪv/"},
                "frequency": 1,
                "meaningVi": "sống, sinh sống",
                "exampleEn": "Many people choose to live in the suburbs.",
                "exampleVi": "Nhiều người chọn sinh sống ở vùng ngoại ô.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "popular",
                "word": "popular",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈpɒpjələ(r)/", "us": "/ˈpɑːpjələr/"},
                "frequency": 2,
                "meaningVi": "phổ biến, được yêu thích, đại chúng",
                "exampleEn": "The new comedy show is very popular.",
                "exampleVi": "Chương trình hài kịch mới đang rất được yêu thích.",
                "derivatives": [
                    {"word": "popularity", "partOfSpeech": "n", "meaningVi": "sự phổ biến"}
                ],
                "synonyms": [],
                "antonyms": ["unpopular"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "donation",
                "word": "donation",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dəʊˈneɪʃn/", "us": "/doʊˈneɪʃn/"},
                "frequency": 2,
                "meaningVi": "sự quyên góp, đồ quyên góp, hiến tặng",
                "exampleEn": "The charity relies on generous donations from the public.",
                "exampleVi": "Tổ chức từ thiện phụ thuộc vào sự quyên góp hào phóng của công chúng.",
                "derivatives": [
                    {"word": "donate", "partOfSpeech": "v", "meaningVi": "quyên góp, hiến tặng"},
                    {"word": "donor", "partOfSpeech": "n", "meaningVi": "người quyên góp"}
                ],
                "synonyms": ["grant", "contribution"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "improvise",
                "word": "improvise",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɪmprəvaɪz/", "us": "/ˈɪmprəvaɪz/"},
                "frequency": 2,
                "meaningVi": "ứng biến, ứng khẩu, tự biên tự diễn (không chuẩn bị trước)",
                "exampleEn": "The actor had to improvise when he forgot his lines.",
                "exampleVi": "Nam diễn viên đã phải ứng biến khi anh ấy quên lời thoại.",
                "derivatives": [
                    {"word": "improvisation", "partOfSpeech": "n", "meaningVi": "sự ứng biến"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "alumni",
                "word": "alumni",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈlʌmnaɪ/", "us": "/əˈlʌmnaɪ/"},
                "frequency": 2,
                "meaningVi": "cựu sinh viên, cựu học sinh",
                "exampleEn": "St. John's University alumni were invited to the graduation ceremony.",
                "exampleVi": "Các cựu sinh viên trường Đại học St. John đã được mời đến lễ tốt nghiệp.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "present-v",
                "word": "present",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/prɪˈzent/", "us": "/prɪˈzent/"},
                "frequency": 2,
                "meaningVi": "trình bày, giới thiệu, xuất trình",
                "exampleEn": "Please present valid tickets at the door.",
                "exampleVi": "Vui lòng xuất trình vé hợp lệ tại cửa ra vào.",
                "derivatives": [
                    {"word": "presentation", "partOfSpeech": "n", "meaningVi": "bài thuyết trình"},
                    {"word": "presenter", "partOfSpeech": "n", "meaningVi": "người thuyết trình"},
                    {"word": "presently", "partOfSpeech": "adv", "meaningVi": "hiện tại, bây giờ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["present A with B / present B to A: đưa/tặng B cho A"],
                "needsReview": False
            },
            {
                "id": "present-adj",
                "word": "present",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈpreznt/", "us": "/ˈpreznt/"},
                "frequency": 2,
                "meaningVi": "có mặt, hiện diện, hiện tại, hiện thời",
                "exampleEn": "The present owner of the resort intends to renovate it.",
                "exampleVi": "Người chủ hiện tại của khu nghỉ dưỡng có ý định cải tạo nó.",
                "derivatives": [],
                "synonyms": ["current"],
                "antonyms": ["absent"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "admission",
                "word": "admission",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ədˈmɪʃn/", "us": "/ədˈmɪʃn/"},
                "frequency": 3,
                "meaningVi": "sự nhận vào, thú nhận, phí vào cửa",
                "exampleEn": "Those wishing to visit the exhibit will be charged an extra admission fee.",
                "exampleVi": "Những người muốn tới thăm triển lãm sẽ bị tính thêm phí vào cửa.",
                "derivatives": [
                    {"word": "admit", "partOfSpeech": "v", "meaningVi": "thừa nhận, nhận vào"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["free admission: vào cửa miễn phí", "admission fee/price: phí vào cửa"],
                "needsReview": False
            },
            {
                "id": "banquet",
                "word": "banquet",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈbæŋkwɪt/", "us": "/ˈbæŋkwɪt/"},
                "frequency": 3,
                "meaningVi": "bữa tiệc lớn, tiệc chiêu đãi",
                "exampleEn": "The hotel has facilities for large-scale wedding banquets.",
                "exampleVi": "Khách sạn có cơ sở vật chất để tổ chức những tiệc cưới quy mô lớn.",
                "derivatives": [],
                "synonyms": ["feast"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "anniversary",
                "word": "anniversary",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌænɪˈvɜːsəri/", "us": "/ˌænɪˈvɜːrsəri/"},
                "frequency": 3,
                "meaningVi": "ngày kỷ niệm, lễ kỷ niệm",
                "exampleEn": "The company is celebrating its 10th anniversary.",
                "exampleVi": "Công ty đang kỷ niệm 10 năm ngày thành lập.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "required",
                "word": "required",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/rɪˈkwaɪəd/", "us": "/rɪˈkwaɪərd/"},
                "frequency": 3,
                "meaningVi": "được yêu cầu, bắt buộc, cần thiết",
                "exampleEn": "Submit the required documents to the office by Friday.",
                "exampleVi": "Hãy gửi các tài liệu được yêu cầu đến văn phòng trước thứ Sáu.",
                "derivatives": [
                    {"word": "require", "partOfSpeech": "v", "meaningVi": "yêu cầu"},
                    {"word": "requirement", "partOfSpeech": "n", "meaningVi": "yêu cầu"}
                ],
                "synonyms": ["compulsory", "mandatory"],
                "antonyms": ["optional"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "succeed",
                "word": "succeed",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/səkˈsiːd/", "us": "/səkˈsiːd/"},
                "frequency": 3,
                "meaningVi": "thành công; kế nghiệp, nối nghiệp",
                "exampleEn": "The campaign succeeded in raising money for the clinic.",
                "exampleVi": "Chiến dịch đã thành công trong việc gây quỹ cho phòng khám.",
                "derivatives": [
                    {"word": "success", "partOfSpeech": "n", "meaningVi": "sự thành công"},
                    {"word": "successful", "partOfSpeech": "adj", "meaningVi": "thành công"},
                    {"word": "successive", "partOfSpeech": "adj", "meaningVi": "kế tiếp, liên tục"},
                    {"word": "successively", "partOfSpeech": "adv", "meaningVi": "liên tiếp"}
                ],
                "synonyms": [],
                "antonyms": ["fail"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "rest-n",
                "word": "rest",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rest/", "us": "/rest/"},
                "frequency": 3,
                "meaningVi": "người/vật còn lại, phần còn lại; sự nghỉ ngơi",
                "exampleEn": "The rest of the day was spent relaxing on the beach.",
                "exampleVi": "Phần còn lại của ngày được dành để thư giãn trên bãi biển.",
                "derivatives": [],
                "synonyms": ["remainder"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "rest-v",
                "word": "rest",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rest/", "us": "/rest/"},
                "frequency": 3,
                "meaningVi": "nghỉ ngơi, tựa lên",
                "exampleEn": "The basketball team rested after a three-hour training session.",
                "exampleVi": "Đội bóng rổ đã nghỉ ngơi sau buổi tập kéo dài ba tiếng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "fund-raising",
                "word": "fund-raising",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈfʌndreɪzɪŋ/", "us": "/ˈfʌndreɪzɪŋ/"},
                "frequency": 3,
                "meaningVi": "sự gây quỹ",
                "exampleEn": "Auctions are a popular form of fund-raising.",
                "exampleVi": "Đấu giá là một hình thức gây quỹ phổ biến.",
                "derivatives": [
                    {"word": "fundraiser", "partOfSpeech": "n", "meaningVi": "buổi gây quỹ, người gây quỹ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "resume",
                "word": "resume",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈzjuːm/", "us": "/rɪˈzuːm/"},
                "frequency": 3,
                "meaningVi": "bắt đầu lại, tiếp tục (sau khi dừng)",
                "exampleEn": "The play will resume after a short intermission.",
                "exampleVi": "Vở kịch sẽ lại tiếp tục sau thời gian giải lao ngắn.",
                "derivatives": [
                    {"word": "resumption", "partOfSpeech": "n", "meaningVi": "sự tiếp tục lại"}
                ],
                "synonyms": ["restart", "reopen"],
                "antonyms": ["suspend", "pause"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "issue-n",
                "word": "issue",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɪʃuː/", "us": "/ˈɪʃuː/"},
                "frequency": 3,
                "meaningVi": "số báo, ấn bản; vấn đề, sự việc",
                "exampleEn": "Jack's cake recipe was in the April issue of Baker Monthly.",
                "exampleVi": "Công thức làm bánh của Jack có trong số tháng Tư của tạp chí Baker Monthly.",
                "derivatives": [],
                "synonyms": ["edition", "problem"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "issue-v",
                "word": "issue",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɪʃuː/", "us": "/ˈɪʃuː/"},
                "frequency": 3,
                "meaningVi": "phát hành, ban hành, đưa ra",
                "exampleEn": "The government issued a new regulation on trade.",
                "exampleVi": "Chính phủ đã ban hành một quy định mới về thương mại.",
                "derivatives": [],
                "synonyms": ["release", "distribute"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "subscription",
                "word": "subscription",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/səbˈskrɪpʃn/", "us": "/səbˈskrɪpʃn/"},
                "frequency": 3,
                "meaningVi": "sự đặt mua định kỳ, sự thuê bao (báo, tạp chí)",
                "exampleEn": "I would like to get a subscription to the Weekly Herald.",
                "exampleVi": "Tôi muốn đặt mua dài hạn tạp chí Weekly Herald.",
                "derivatives": [
                    {"word": "subscribe", "partOfSpeech": "v", "meaningVi": "đăng ký, đặt mua"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "appear",
                "word": "appear",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈpɪə(r)/", "us": "/əˈpɪr/"},
                "frequency": 3,
                "meaningVi": "xuất hiện, trình diện, có vẻ như",
                "exampleEn": "The novelist appeared at the bookstore to sign autographs.",
                "exampleVi": "Nhà văn đã xuất hiện ở hiệu sách để ký tặng.",
                "derivatives": [
                    {"word": "appearance", "partOfSpeech": "n", "meaningVi": "ngoại hình, sự xuất hiện"}
                ],
                "synonyms": [],
                "antonyms": ["disappear"],
                "toeicNotes": ["it appears that...: có vẻ như là...", "appear in court: trình diện tại tòa"],
                "needsReview": False
            },
            {
                "id": "accompany",
                "word": "accompany",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈkʌmpəni/", "us": "/əˈkʌmpəni/"},
                "frequency": 2,
                "meaningVi": "đi cùng, kèm theo, đồng hành",
                "exampleEn": "Mary accompanied her grandmother to the mall.",
                "exampleVi": "Mary đi cùng bà cô ấy tới trung tâm thương mại.",
                "derivatives": [],
                "synonyms": ["escort", "go with"],
                "antonyms": [],
                "toeicNotes": ["strong winds accompany rain: gió mạnh kèm theo mưa"],
                "needsReview": False
            },
            {
                "id": "edition",
                "word": "edition",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪˈdɪʃn/", "us": "/ɪˈdɪʃn/"},
                "frequency": 2,
                "meaningVi": "phiên bản, lần xuất bản, số lượng in",
                "exampleEn": "A revised edition of the economics book will be published soon.",
                "exampleVi": "Phiên bản có chỉnh sửa của cuốn sách kinh tế này sẽ sớm được xuất bản.",
                "derivatives": [],
                "synonyms": ["version", "issue"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "specifically",
                "word": "specifically",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/spəˈsɪfɪkli/", "us": "/spəˈsɪfɪkli/"},
                "frequency": 2,
                "meaningVi": "cụ thể, rõ ràng, đặc biệt là",
                "exampleEn": "The package terms specifically stated that guests would stay at a hotel.",
                "exampleVi": "Các điều khoản của gói du lịch đã nêu rõ rằng du khách sẽ ở tại khách sạn.",
                "derivatives": [
                    {"word": "specific", "partOfSpeech": "adj", "meaningVi": "cụ thể, rõ ràng"},
                    {"word": "specification", "partOfSpeech": "n", "meaningVi": "thông số kỹ thuật"}
                ],
                "synonyms": ["particularly"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "anonymous",
                "word": "anonymous",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/əˈnɒnɪməs/", "us": "/əˈnɑːnɪməs/"},
                "frequency": 2,
                "meaningVi": "ẩn danh, nặc danh, giấu tên",
                "exampleEn": "The charity received $6,000 from an anonymous donor.",
                "exampleVi": "Tổ chức từ thiện đã nhận được 6000 đô-la từ một người quyên góp ẩn danh.",
                "derivatives": [
                    {"word": "anonymity", "partOfSpeech": "n", "meaningVi": "sự ẩn danh"}
                ],
                "synonyms": ["nameless"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "commit",
                "word": "commit",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kəˈmɪt/", "us": "/kəˈmɪt/"},
                "frequency": 2,
                "meaningVi": "cam kết, giao phó, ủy thác, hứa",
                "exampleEn": "The store is committed to providing excellent customer service.",
                "exampleVi": "Cửa hàng luôn cam kết cung cấp dịch vụ khách hàng tuyệt hảo.",
                "derivatives": [
                    {"word": "commitment", "partOfSpeech": "n", "meaningVi": "sự tận tâm, cam kết"}
                ],
                "synonyms": ["dedicate", "devote"],
                "antonyms": [],
                "toeicNotes": ["be committed to -ing: tận tâm với, cam kết làm gì"],
                "needsReview": False
            },
            {
                "id": "informative",
                "word": "informative",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪnˈfɔːmətɪv/", "us": "/ɪnˈfɔːrmətɪv/"},
                "frequency": 2,
                "meaningVi": "nhiều thông tin, bổ ích, có kiến thức",
                "exampleEn": "The documentary was informative and interesting.",
                "exampleVi": "Bộ phim tài liệu này rất bổ ích và thú vị.",
                "derivatives": [
                    {"word": "inform", "partOfSpeech": "v", "meaningVi": "thông báo"},
                    {"word": "information", "partOfSpeech": "n", "meaningVi": "thông tin"}
                ],
                "synonyms": ["instructive"],
                "antonyms": ["uninformative"],
                "toeicNotes": ["informative brochure/booklet: cuốn sách/tài liệu hướng dẫn bổ ích"],
                "needsReview": False
            },
            {
                "id": "audience",
                "word": "audience",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɔːdiəns/", "us": "/ˈɑːdiəns/"},
                "frequency": 2,
                "meaningVi": "khán giả, thính giả, độc giả",
                "exampleEn": "The audience applauded the singer enthusiastically.",
                "exampleVi": "Khán giả cổ vũ cho ca sĩ rất nồng nhiệt.",
                "derivatives": [],
                "synonyms": ["spectators", "listeners"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "author",
                "word": "author",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɔːθə(r)/", "us": "/ˈɔːθər/"},
                "frequency": 2,
                "meaningVi": "tác giả, nhà văn",
                "exampleEn": "All of the author's short stories are popular.",
                "exampleVi": "Tất cả truyện ngắn của tác giả đó đều nổi tiếng.",
                "derivatives": [
                    {"word": "authorship", "partOfSpeech": "n", "meaningVi": "quyền tác giả"}
                ],
                "synonyms": ["writer"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "note-v",
                "word": "note",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/nəʊt/", "us": "/noʊt/"},
                "frequency": 2,
                "meaningVi": "lưu ý, ghi chú",
                "exampleEn": "Please note the intricate details of the architecture.",
                "exampleVi": "Xin hãy lưu ý các chi tiết phức tạp của công trình kiến trúc này.",
                "derivatives": [
                    {"word": "note", "partOfSpeech": "n", "meaningVi": "bản ghi nhớ, sự ghi chú"},
                    {"word": "notable", "partOfSpeech": "adj", "meaningVi": "đáng chú ý"}
                ],
                "synonyms": ["state"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "note-n",
                "word": "note",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/nəʊt/", "us": "/noʊt/"},
                "frequency": 2,
                "meaningVi": "bản ghi nhớ, lời ghi chú, bức thư ngắn",
                "exampleEn": "Leave a note on the desk if you go out.",
                "exampleVi": "Hãy để lại lời nhắn trên bàn nếu bạn đi ra ngoài.",
                "derivatives": [],
                "synonyms": ["memo"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "antique",
                "word": "antique",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ænˈtiːk/", "us": "/ænˈtiːk/"},
                "frequency": 2,
                "meaningVi": "đồ cổ",
                "exampleEn": "Antiques are popular for home decor.",
                "exampleVi": "Đồ cổ rất phổ biến trong việc trang trí nhà cửa.",
                "derivatives": [
                    {"word": "antique", "partOfSpeech": "adj", "meaningVi": "cổ xưa, thuộc về thời xưa"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "manuscript",
                "word": "manuscript",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈmænjuskrɪpt/", "us": "/ˈmænjuskrɪpt/"},
                "frequency": 2,
                "meaningVi": "bản viết tay, bản thảo",
                "exampleEn": "The author is working on several manuscripts.",
                "exampleVi": "Tác giả đó đang viết một vài bản thảo.",
                "derivatives": [],
                "synonyms": ["draft"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "beneficial",
                "word": "beneficial",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˌbenɪˈfɪʃl/", "us": "/ˌbenɪˈfɪʃl/"},
                "frequency": 2,
                "meaningVi": "có lợi, có ích",
                "exampleEn": "The organization's work is beneficial to the community.",
                "exampleVi": "Hoạt động của tổ chức đó có ích cho cộng đồng.",
                "derivatives": [
                    {"word": "benefit", "partOfSpeech": "n/v", "meaningVi": "lợi ích/có lợi"}
                ],
                "synonyms": ["advantageous", "helpful"],
                "antonyms": ["harmful"],
                "toeicNotes": ["be beneficial to: có lợi cho ai", "be beneficial for: có ích cho cái gì"],
                "needsReview": False
            },
            {
                "id": "upcoming",
                "word": "upcoming",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈʌpkʌmɪŋ/", "us": "/ˈʌpkʌmɪŋ/"},
                "frequency": 2,
                "meaningVi": "sắp tới, sắp diễn ra",
                "exampleEn": "A reporter spoke to a candidate for the upcoming election.",
                "exampleVi": "Phóng viên đã trao đổi với một ứng cử viên về cuộc bầu cử sắp tới.",
                "derivatives": [],
                "synonyms": ["forthcoming"],
                "antonyms": [],
                "toeicNotes": ["upcoming event: sự kiện sắp tới", "upcoming year: năm học sắp tới"],
                "needsReview": False
            },
            {
                "id": "lend",
                "word": "lend",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/lend/", "us": "/lend/"},
                "frequency": 2,
                "meaningVi": "cho mượn, cho vay",
                "exampleEn": "The library lends a variety of audio-visual materials.",
                "exampleVi": "Thư viện cho mượn rất nhiều loại tài liệu nghe nhìn.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["borrow"],
                "toeicNotes": ["Phân biệt: lend (cho mượn miễn phí), borrow (mượn miễn phí), rent (thuê trả tiền)"],
                "needsReview": False
            },
            {
                "id": "current",
                "word": "current",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈkʌrənt/", "us": "/ˈkɜːrənt/"},
                "frequency": 2,
                "meaningVi": "hiện thời, đang lưu hành, có hiệu lực",
                "exampleEn": "Current subscribers to the magazine will receive a free supplement.",
                "exampleVi": "Những người hiện đặt mua dài hạn tạp chí sẽ được nhận một cuốn phụ trương miễn phí.",
                "derivatives": [
                    {"word": "currently", "partOfSpeech": "adv", "meaningVi": "hiện thời, hiện nay"}
                ],
                "synonyms": ["present", "valid"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "local",
                "word": "local",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈlhəʊkl/", "us": "/ˈloʊkl/"},
                "frequency": 2,
                "meaningVi": "địa phương, cục bộ",
                "exampleEn": "The tournament will be held at the local high school.",
                "exampleVi": "Trận đấu sẽ được tổ chức tại trường trung học địa phương.",
                "derivatives": [
                    {"word": "locality", "partOfSpeech": "n", "meaningVi": "địa phương, vị trí"},
                    {"word": "locally", "partOfSpeech": "adv", "meaningVi": "mang tính địa phương"}
                ],
                "synonyms": [],
                "antonyms": ["global"],
                "toeicNotes": ["local high school: trường trung học địa phương"],
                "needsReview": False
            },
            {
                "id": "variety",
                "word": "variety",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/vəˈraɪəti/", "us": "/vəˈraɪəti/"},
                "frequency": 2,
                "meaningVi": "sự đa dạng, giống, loại",
                "exampleEn": "The newsstand sells a variety of magazines and newspapers.",
                "exampleVi": "Quầy báo bán nhiều loại báo và tạp chí.",
                "derivatives": [
                    {"word": "various", "partOfSpeech": "adj", "meaningVi": "đa dạng, khác nhau"},
                    {"word": "vary", "partOfSpeech": "v", "meaningVi": "thay đổi"}
                ],
                "synonyms": ["range"],
                "antonyms": [],
                "toeicNotes": ["a (large/wide) variety of + N (plural): rất nhiều thứ gì đó"],
                "needsReview": False
            },
            {
                "id": "advocate-n",
                "word": "advocate",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈædvəkət/", "us": "/ˈædvəkət/"},
                "frequency": 2,
                "meaningVi": "người ủng hộ, người biện hộ",
                "exampleEn": "The writer is an advocate of public education.",
                "exampleVi": "Nhà văn này là một người ủng hộ giáo dục công lập.",
                "derivatives": [
                    {"word": "advocacy", "partOfSpeech": "n", "meaningVi": "sự ủng hộ, vận động"}
                ],
                "synonyms": ["supporter"],
                "antonyms": ["opponent"],
                "toeicNotes": ["an advocate of: người ủng hộ của"],
                "needsReview": False
            },
            {
                "id": "advocate-v",
                "word": "advocate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈædvəkeɪt/", "us": "/ˈædvəkeɪt/"},
                "frequency": 2,
                "meaningVi": "ủng hộ, biện hộ, tán thành",
                "exampleEn": "Many experts advocate paying off debt as soon as possible.",
                "exampleVi": "Nhiều chuyên gia tán thành việc trả hết nợ càng sớm càng tốt.",
                "derivatives": [],
                "synonyms": ["support"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "contributor",
                "word": "contributor",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kənˈtrɪbjutə(r)/", "us": "/kənˈtrɪbjutər/"},
                "frequency": 2,
                "meaningVi": "người đóng góp, người cống hiến",
                "exampleEn": "The doctor is a regular contributor to the medical journal.",
                "exampleVi": "Bác sĩ đó là người thường xuyên đóng góp cho tạp chí y khoa.",
                "derivatives": [
                    {"word": "contribute", "partOfSpeech": "v", "meaningVi": "đóng góp"},
                    {"word": "contribution", "partOfSpeech": "n", "meaningVi": "sự đóng góp"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["contributor to: người đóng góp cho"],
                "needsReview": False
            },
            {
                "id": "defy",
                "word": "defy",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/dɪˈfaɪ/", "us": "/dɪˈfaɪ/"},
                "frequency": 2,
                "meaningVi": "thách thức, không tuân theo, bất chấp",
                "exampleEn": "The play defied all description.",
                "exampleVi": "Không lời nào có thể diễn tả được về vở kịch này.",
                "derivatives": [
                    {"word": "defiance", "partOfSpeech": "n", "meaningVi": "sự thách thức"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["defy description: không thể miêu tả được"],
                "needsReview": False
            },
            {
                "id": "fascinating",
                "word": "fascinating",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈfæsɪneɪtɪŋ/", "us": "/ˈfæsɪneɪtɪŋ/"},
                "frequency": 2,
                "meaningVi": "hấp dẫn, lôi cuốn, quyến rũ",
                "exampleEn": "Many fascinating pieces of art were on display.",
                "exampleVi": "Nhiều tác phẩm nghệ thuật hấp dẫn đã được trưng bày.",
                "derivatives": [
                    {"word": "fascinate", "partOfSpeech": "v", "meaningVi": "mê hoặc"}
                ],
                "synonyms": ["captivating"],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: fascinating (hấp dẫn - chủ động) và fascinated (bị hấp dẫn - bị động)"],
                "needsReview": False
            },
            {
                "id": "showing",
                "word": "showing",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈʃəʊɪŋ/", "us": "/ˈʃoʊɪŋ/"},
                "frequency": 2,
                "meaningVi": "sự trình diễn, buổi triển lãm, sự chiếu bóng",
                "exampleEn": "We attended the premiere showing of the Rita Garner movie.",
                "exampleVi": "Chúng tôi đã tham dự buổi công chiếu ra mắt phim của Rita Garner.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            }
        ]

    if day_num == 7:
        words_data = [
            {
                "id": "survey-n",
                "word": "survey",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈsɜːveɪ/", "us": "/ˈsɜːrveɪ/"},
                "frequency": 3,
                "meaningVi": "cuộc khảo sát, cuộc thăm dò",
                "exampleEn": "Customer surveys help to improve product quality.",
                "exampleVi": "Các cuộc khảo sát khách hàng giúp cải thiện chất lượng sản phẩm.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "survey-v",
                "word": "survey",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/səˈveɪ/", "us": "/sərˈveɪ/"},
                "frequency": 3,
                "meaningVi": "khảo sát, điều tra, thăm dò",
                "exampleEn": "The company surveyed 1,000 customers about their shopping habits.",
                "exampleVi": "Công ty đã khảo sát 1.000 khách hàng về thói quen mua sắm của họ.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "analysis",
                "word": "analysis",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈnæləsɪs/", "us": "/əˈnæləsɪs/"},
                "frequency": 3,
                "meaningVi": "sự phân tích",
                "exampleEn": "The latest market analysis shows an increase in used car purchases.",
                "exampleVi": "Phân tích thị trường mới nhất cho thấy sự gia tăng trong hoạt động mua bán xe hơi cũ.",
                "derivatives": [
                    {"word": "analyze", "partOfSpeech": "v", "meaningVi": "phân tích"},
                    {"word": "analyst", "partOfSpeech": "n", "meaningVi": "nhà phân tích"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["market analysis: phân tích thị trường", "reliable analysis: phân tích đáng tin cậy"],
                "needsReview": False
            },
            {
                "id": "respondent",
                "word": "respondent",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈspɒndənt/", "us": "/rɪˈspɑːndənt/"},
                "frequency": 2,
                "meaningVi": "người trả lời (khảo sát)",
                "exampleEn": "Almost all survey respondents rated the product highly.",
                "exampleVi": "Hầu như tất cả người trả lời khảo sát đều đánh giá cao sản phẩm.",
                "derivatives": [
                    {"word": "respond", "partOfSpeech": "v", "meaningVi": "phản hồi, đáp lại"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "monopoly",
                "word": "monopoly",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/məˈnɒpəli/", "us": "/məˈnɑːpəli/"},
                "frequency": 2,
                "meaningVi": "sự độc quyền, vật độc quyền",
                "exampleEn": "Panatronic has a virtual monopoly on the manufacture of digital recorders.",
                "exampleVi": "Panatronic gần như nắm độc quyền trong sản xuất thiết bị ghi âm kỹ thuật số.",
                "derivatives": [
                    {"word": "monopolize", "partOfSpeech": "v", "meaningVi": "giữ độc quyền, độc chiếm"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["have a monopoly on: nắm độc quyền về"],
                "needsReview": False
            },
            {
                "id": "competition",
                "word": "competition",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌkɒmpəˈtɪʃn/", "us": "/ˌkɑːmpəˈtɪʃn/"},
                "frequency": 3,
                "meaningVi": "sự cạnh tranh, cuộc thi, đối thủ cạnh tranh",
                "exampleEn": "Competition in the game software market has increased.",
                "exampleVi": "Cạnh tranh trong thị trường phần mềm trò chơi điện tử đang gia tăng.",
                "derivatives": [
                    {"word": "compete", "partOfSpeech": "v", "meaningVi": "cạnh tranh, tranh đua"},
                    {"word": "competitor", "partOfSpeech": "n", "meaningVi": "đối thủ cạnh tranh"},
                    {"word": "competitive", "partOfSpeech": "adj", "meaningVi": "mang tính cạnh tranh"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["compete for: cạnh tranh vì cái gì"],
                "needsReview": False
            },
            {
                "id": "consistently",
                "word": "consistently",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/kənˈsɪstəntli/", "us": "/kənˈsɪstəntli/"},
                "frequency": 3,
                "meaningVi": "nhất quán, luôn luôn, kiên định",
                "exampleEn": "The factory has consistently provided the highest grade products.",
                "exampleVi": "Nhà máy luôn cung cấp những sản phẩm cao cấp nhất.",
                "derivatives": [
                    {"word": "consistent", "partOfSpeech": "adj", "meaningVi": "nhất quán, nhất trí"}
                ],
                "synonyms": [],
                "antonyms": ["inconsistently"],
                "toeicNotes": ["consistently produce/provide: liên tục sản xuất/cung cấp"],
                "needsReview": False
            },
            {
                "id": "demand-n",
                "word": "demand",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈmɑːnd/", "us": "/dɪˈmænd/"},
                "frequency": 3,
                "meaningVi": "nhu cầu",
                "exampleEn": "The company could not meet the increased demand for mobile devices.",
                "exampleVi": "Công ty không thể đáp ứng được nhu cầu ngày càng tăng đối với các thiết bị di động.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["supply"],
                "toeicNotes": ["demand for: nhu cầu về"],
                "needsReview": False
            },
            {
                "id": "demand-v",
                "word": "demand",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/dɪˈmɑːnd/", "us": "/dɪˈmænd/"},
                "frequency": 3,
                "meaningVi": "yêu cầu, đòi hỏi",
                "exampleEn": "Mr. Hawkesby demanded that the clause be removed.",
                "exampleVi": "Ông Hawkesby đã yêu cầu bỏ điều khoản này.",
                "derivatives": [
                    {"word": "demanding", "partOfSpeech": "adj", "meaningVi": "đòi hỏi khắt khe"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["demand that + S + V(nguyên thể): đòi hỏi ai phải làm gì"],
                "needsReview": False
            },
            {
                "id": "do-one-utmost",
                "word": "do one's utmost",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/duː wʌnz ˈʌtməʊst/", "us": "/duː wʌnz ˈʌtmoʊst/"},
                "frequency": 2,
                "meaningVi": "cố gắng hết sức, làm hết sức mình",
                "exampleEn": "Sun Manufacturing does its utmost to ensure the quality of its products.",
                "exampleVi": "Sun Manufacturing luôn cố gắng hết sức để đảm bảo chất lượng sản phẩm của mình.",
                "derivatives": [],
                "synonyms": ["do one's best"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "expand",
                "word": "expand",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪkˈspænd/", "us": "/ɪkˈspænd/"},
                "frequency": 2,
                "meaningVi": "mở rộng, phát triển",
                "exampleEn": "Brahe Optics has expanded its marketing and sales division.",
                "exampleVi": "Brahe Optics đã mở rộng bộ phận bán hàng và marketing của mình.",
                "derivatives": [
                    {"word": "expansion", "partOfSpeech": "n", "meaningVi": "sự mở rộng"},
                    {"word": "expansive", "partOfSpeech": "adj", "meaningVi": "rộng rãi, có thể mở rộng"}
                ],
                "synonyms": [],
                "antonyms": ["contract", "shrink"],
                "toeicNotes": ["expand the market/division: mở rộng thị trường/bộ phận"],
                "needsReview": False
            },
            {
                "id": "advanced",
                "word": "advanced",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ədˈvɑːnst/", "us": "/ədˈvænst/"},
                "frequency": 2,
                "meaningVi": "tiên tiến, cao cấp, đi trước",
                "exampleEn": "Modern cell phones are very advanced compared to those from a decade ago.",
                "exampleVi": "Điện thoại di động hiện đại tiên tiến hơn nhiều so với những chiếc điện thoại cách đây một thập kỷ.",
                "derivatives": [
                    {"word": "advance", "partOfSpeech": "v/n", "meaningVi": "tiến bộ/sự tiến bộ"},
                    {"word": "advancement", "partOfSpeech": "n", "meaningVi": "sự thăng tiến, phát triển"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["in the advanced stages of: ở những giai đoạn tiên tiến/cuối của"],
                "needsReview": False
            },
            {
                "id": "postpone",
                "word": "postpone",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/pəʊˈspəʊn/", "us": "/poʊˈspoʊn/"},
                "frequency": 2,
                "meaningVi": "trì hoãn, hoãn lại",
                "exampleEn": "Organizers postponed the conference on management strategies because of bad weather.",
                "exampleVi": "Do thời tiết xấu, ban tổ chức đã hoãn cuộc hội thảo về chiến lược quản lý.",
                "derivatives": [],
                "synonyms": ["delay", "put off"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "additional",
                "word": "additional",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/əˈdɪʃənl/", "us": "/əˈdɪʃənl/"},
                "frequency": 3,
                "meaningVi": "thêm vào, bổ sung",
                "exampleEn": "Several investors decided to purchase additional stocks.",
                "exampleVi": "Một số nhà đầu tư đã quyết định mua thêm cổ phiếu.",
                "derivatives": [
                    {"word": "addition", "partOfSpeech": "n", "meaningVi": "sự thêm vào"},
                    {"word": "add", "partOfSpeech": "v", "meaningVi": "thêm vào"}
                ],
                "synonyms": ["extra", "further"],
                "antonyms": [],
                "toeicNotes": ["additional information/detail: thông tin/chi tiết bổ sung"],
                "needsReview": False
            },
            {
                "id": "appreciate",
                "word": "appreciate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈpriːʃieɪt/", "us": "/əˈpriːʃieɪt/"},
                "frequency": 3,
                "meaningVi": "đánh giá cao, cảm kích, hiểu sâu sắc, thưởng thức",
                "exampleEn": "Benson Co. appreciates your continued business.",
                "exampleVi": "Công ty Benson rất cảm kích sự hợp tác liên tục của bạn.",
                "derivatives": [
                    {"word": "appreciation", "partOfSpeech": "n", "meaningVi": "sự cảm kích, đánh giá cao"},
                    {"word": "appreciative", "partOfSpeech": "adj", "meaningVi": "biết thưởng thức, đánh giá cao"}
                ],
                "synonyms": ["value"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "demonstration",
                "word": "demonstration",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌdemənˈstreɪʃn/", "us": "/ˌdemənˈstreɪʃn/"},
                "frequency": 3,
                "meaningVi": "sự thể hiện, sự minh họa, sự thuyết minh",
                "exampleEn": "The salesclerk offered to provide a demonstration on how to use the photocopier.",
                "exampleVi": "Nhân viên bán hàng đã đề nghị trình bày minh họa cách sử dụng máy photocopy.",
                "derivatives": [
                    {"word": "demonstrate", "partOfSpeech": "v", "meaningVi": "chứng minh, minh họa"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "buy",
                "word": "buy",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/baɪ/", "us": "/baɪ/"},
                "frequency": 3,
                "meaningVi": "mua",
                "exampleEn": "The acquisitions department buys all of the office equipment.",
                "exampleVi": "Bộ phận mua lại sẽ mua tất cả thiết bị văn phòng.",
                "derivatives": [],
                "synonyms": ["purchase"],
                "antonyms": ["sell"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "examine",
                "word": "examine",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪɡˈzæmɪn/", "us": "/ɪɡˈzæmɪn/"},
                "frequency": 3,
                "meaningVi": "xem xét, kiểm tra, nghiên cứu, điều tra",
                "exampleEn": "Research and Development will examine food consumption trends in foreign markets.",
                "exampleVi": "Phòng Nghiên cứu và Phát triển sẽ điều tra xu hướng tiêu thụ thực phẩm ở các thị trường nước ngoài.",
                "derivatives": [
                    {"word": "examination", "partOfSpeech": "n", "meaningVi": "sự xem xét, kỳ thi"}
                ],
                "synonyms": ["investigate", "check out"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "effective",
                "word": "effective",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪˈfektɪv/", "us": "/ɪˈfektɪv/"},
                "frequency": 3,
                "meaningVi": "hiệu quả, có hiệu lực, có tác dụng",
                "exampleEn": "An effective advertising campaign is one that people remember for a long time.",
                "exampleVi": "Một chiến dịch quảng cáo hiệu quả phải là chiến dịch khiến mọi người ghi nhớ rất lâu.",
                "derivatives": [
                    {"word": "effectively", "partOfSpeech": "adv", "meaningVi": "một cách hiệu quả"},
                    {"word": "effectiveness", "partOfSpeech": "n", "meaningVi": "sự hiệu quả"}
                ],
                "synonyms": ["efficient", "valid"],
                "antonyms": ["ineffective"],
                "toeicNotes": ["run effectively: hoạt động hiệu quả", "effective as of + ngày: có hiệu lực từ ngày"],
                "needsReview": False
            },
            {
                "id": "like-v",
                "word": "like",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/laɪk/", "us": "/laɪk/"},
                "frequency": 3,
                "meaningVi": "yêu thích, thích",
                "exampleEn": "Consumers like products that look high-end but are less expensive.",
                "exampleVi": "Người tiêu dùng thích những sản phẩm trông cao cấp nhưng không đắt đỏ.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["dislike"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "like-prep",
                "word": "like",
                "partOfSpeech": "prep",
                "pronunciation": {"uk": "/laɪk/", "us": "/laɪk/"},
                "frequency": 3,
                "meaningVi": "như, giống như",
                "exampleEn": "He wants a campaign like the one we ran last year.",
                "exampleVi": "Anh ấy muốn có một chiến dịch giống như chiến dịch chúng ta chạy năm ngoái.",
                "derivatives": [
                    {"word": "likeness", "partOfSpeech": "n", "meaningVi": "sự giống nhau"}
                ],
                "synonyms": ["such as"],
                "antonyms": ["unlike"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "especially",
                "word": "especially",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ɪˈspeʃəli/", "us": "/ɪˈspeʃəli/"},
                "frequency": 3,
                "meaningVi": "đặc biệt, nhất là",
                "exampleEn": "Manufacturers of large vehicles are facing an especially difficult year for sales.",
                "exampleVi": "Các nhà sản xuất phương tiện vận tải lớn đang phải đối mặt với một năm kinh doanh đặc biệt khó khăn.",
                "derivatives": [],
                "synonyms": ["particularly"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "closely",
                "word": "closely",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈkləʊsli/", "us": "/ˈkloʊsli/"},
                "frequency": 2,
                "meaningVi": "chặt chẽ, kỹ lượng, sát sao",
                "exampleEn": "Marketing departments monitor the latest trends closely.",
                "exampleVi": "Bộ phận marketing luôn theo dõi sát sao các xu hướng mới nhất.",
                "derivatives": [
                    {"word": "close", "partOfSpeech": "adj", "meaningVi": "gần gũi, chặt chẽ"}
                ],
                "synonyms": ["carefully"],
                "antonyms": [],
                "toeicNotes": ["closely watch/examine: quan sát/điều tra kỹ lưỡng"],
                "needsReview": False
            },
            {
                "id": "reserve",
                "word": "reserve",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈzɜːv/", "us": "/rɪˈzɜːrv/"},
                "frequency": 2,
                "meaningVi": "đặt trước, dự trữ, để dành",
                "exampleEn": "The secretary will reserve hotel rooms for anyone going to the convention.",
                "exampleVi": "Thư ký sẽ đặt trước phòng khách sạn cho những người đi dự hội nghị.",
                "derivatives": [
                    {"word": "reservation", "partOfSpeech": "n", "meaningVi": "sự đặt trước"},
                    {"word": "reserved", "partOfSpeech": "adj", "meaningVi": "dè dặt, kín đáo"}
                ],
                "synonyms": ["book"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "cooperate",
                "word": "cooperate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/kəʊˈɒpəreɪt/", "us": "/koʊˈɑːpəreɪt/"},
                "frequency": 2,
                "meaningVi": "hợp tác, chung sức",
                "exampleEn": "The two companies cooperated on developing the promotional campaign.",
                "exampleVi": "Hai công ty đã hợp tác để phát triển chiến dịch quảng bá.",
                "derivatives": [
                    {"word": "cooperation", "partOfSpeech": "n", "meaningVi": "sự hợp tác"},
                    {"word": "cooperative", "partOfSpeech": "adj", "meaningVi": "hợp tác, tập thể"}
                ],
                "synonyms": ["collaborate"],
                "antonyms": [],
                "toeicNotes": ["cooperate with sb: hợp tác với ai", "cooperate on sth: hợp tác về việc gì"],
                "needsReview": False
            },
            {
                "id": "very",
                "word": "very",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈveri/", "us": "/ˈveri/"},
                "frequency": 2,
                "meaningVi": "rất, hết sức",
                "exampleEn": "The survey was very effective at identifying the target market.",
                "exampleVi": "Cuộc khảo sát rất hiệu quả trong việc xác định thị trường mục tiêu.",
                "derivatives": [],
                "synonyms": ["extremely"],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: very (nhấn mạnh tính từ/trạng từ thường) và far (nhấn mạnh so sánh hơn hoặc too)"],
                "needsReview": False
            },
            {
                "id": "consecutive",
                "word": "consecutive",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/kənˈsekjətɪv/", "us": "/kənˈsekjətɪv/"},
                "frequency": 2,
                "meaningVi": "liên tiếp, liên tục, liền nhau",
                "exampleEn": "The Barkley Company achieved high sales growth for the third consecutive year.",
                "exampleVi": "Công ty Barkley đã đạt mức tăng trưởng cao về doanh số năm thứ ba liên tiếp.",
                "derivatives": [
                    {"word": "consecutively", "partOfSpeech": "adv", "meaningVi": "liên tiếp"}
                ],
                "synonyms": ["successive"],
                "antonyms": [],
                "toeicNotes": ["for the third consecutive year: năm thứ ba liên tiếp", "for three consecutive years: trong ba năm liên tiếp"],
                "needsReview": False
            },
            {
                "id": "expectation",
                "word": "expectation",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌekspekˈteɪʃn/", "us": "/ˌekspekˈteɪʃn/"},
                "frequency": 2,
                "meaningVi": "sự kỳ vọng, dự kiến, mong đợi",
                "exampleEn": "The expectation is that costs will be cut.",
                "exampleVi": "Dự kiến là chi phí sẽ được cắt giảm.",
                "derivatives": [
                    {"word": "expect", "partOfSpeech": "v", "meaningVi": "kỳ vọng, mong chờ"}
                ],
                "synonyms": ["anticipation"],
                "antonyms": [],
                "toeicNotes": ["meet/surpass expectations: đáp ứng/vượt mong đợi", "above/beyond expectations: vượt ngoài dự kiến"],
                "needsReview": False
            },
            {
                "id": "publicize",
                "word": "publicize",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈpʌblɪsaɪz/", "us": "/ˈpʌblɪsaɪz/"},
                "frequency": 2,
                "meaningVi": "quảng cáo, công khai, đưa ra công chúng",
                "exampleEn": "New regulations are publicized on the government website.",
                "exampleVi": "Những quy định mới được công khai trên trang web của chính phủ.",
                "derivatives": [
                    {"word": "public", "partOfSpeech": "adj/n", "meaningVi": "công cộng/công chúng"},
                    {"word": "publicity", "partOfSpeech": "n", "meaningVi": "sự công khai, quảng cáo"}
                ],
                "synonyms": ["promote", "advertise"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "raise",
                "word": "raise",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/reɪz/", "us": "/reɪz/"},
                "frequency": 2,
                "meaningVi": "nâng lên, tăng lên; đề xuất, nêu ra",
                "exampleEn": "We used mass-mailing methods to raise awareness of our brand.",
                "exampleVi": "Chúng tôi đã sử dụng phương thức gửi thư hàng loạt để nâng cao sự nhận biết về thương hiệu của mình.",
                "derivatives": [
                    {"word": "raise", "partOfSpeech": "n", "meaningVi": "sự tăng lương"}
                ],
                "synonyms": ["voice"],
                "antonyms": ["lower", "reduce"],
                "toeicNotes": ["Phân biệt: raise (ngoại động từ, cần tân ngữ) và rise (nội động từ, tự tăng lên, không cần tân ngữ)", "Phân biệt: raise (tăng giá/nêu câu hỏi) và lift (nâng vật nặng lên)"],
                "needsReview": False
            },
            {
                "id": "extremely",
                "word": "extremely",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ɪkˈstriːmli/", "us": "/ɪkˈstriːmli/"},
                "frequency": 2,
                "meaningVi": "cực kỳ, vô cùng",
                "exampleEn": "Internet service providers struggle to survive in today's extremely competitive market.",
                "exampleVi": "Các nhà cấp dịch vụ Internet phải đấu tranh để tồn tại trong thị trường vô cùng cạnh tranh ngày nay.",
                "derivatives": [
                    {"word": "extreme", "partOfSpeech": "adj/n", "meaningVi": "cực kỳ/cực đoan"}
                ],
                "synonyms": ["very"],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: extremely (nhấn mạnh mức độ tuyệt đối) và exclusively (độc quyền, hạn định trong phạm vi)"],
                "needsReview": False
            },
            {
                "id": "affect",
                "word": "affect",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈfekt/", "us": "/əˈfekt/"},
                "frequency": 2,
                "meaningVi": "ảnh hưởng, tác động",
                "exampleEn": "The frozen-food industry can affect the canned goods market.",
                "exampleVi": "Ngành thực phẩm đông lạnh có thể ảnh hưởng đến thị trường đồ đóng hộp.",
                "derivatives": [],
                "synonyms": ["influence"],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: affect (động từ - có ảnh hưởng đến) và effect (danh từ - có hiệu lực, tác động)"],
                "needsReview": False
            },
            {
                "id": "target-n",
                "word": "target",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈtɑːɡɪt/", "us": "/ˈtɑːrɡɪt/"},
                "frequency": 2,
                "meaningVi": "mục tiêu, mục đích",
                "exampleEn": "Sales for this quarter are right on target.",
                "exampleVi": "Doanh số bán hàng của quý này đúng như mục tiêu.",
                "derivatives": [],
                "synonyms": ["goal", "aim"],
                "antonyms": [],
                "toeicNotes": ["on target: đúng mục tiêu"],
                "needsReview": False
            },
            {
                "id": "target-v",
                "word": "target",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈtɑːɡɪt/", "us": "/ˈtɑːrɡɪt/"},
                "frequency": 2,
                "meaningVi": "nhắm tới, hướng tới",
                "exampleEn": "The advertisement targets the age range of 25-40 years.",
                "exampleVi": "Quảng cáo này nhắm tới đối tượng trong độ tuổi từ 25 đến 40.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "campaign",
                "word": "campaign",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kæmˈpeɪn/", "us": "/kæmˈpeɪn/"},
                "frequency": 2,
                "meaningVi": "chiến dịch, đợt vận động",
                "exampleEn": "The mayor's election campaign focused on his strong record in office.",
                "exampleVi": "Chiến dịch bầu cử của thị trưởng tập trung vào những thành tích tốt của ông lúc đương nhiệm.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["advertising campaign: chiến dịch quảng cáo"],
                "needsReview": False
            },
            {
                "id": "probable",
                "word": "probable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈprɒbəbl/", "us": "/ˈprɑːbəbl/"},
                "frequency": 2,
                "meaningVi": "nhiều khả năng, có thể xảy ra, chắc hẳn",
                "exampleEn": "One of the probable causes for low sales was the lack of promotion.",
                "exampleVi": "Một trong những nguyên nhân nhiều khả năng gây ra doanh số thấp là việc không có hoạt động quảng bá.",
                "derivatives": [
                    {"word": "probably", "partOfSpeech": "adv", "meaningVi": "chắc chắn, có lẽ"}
                ],
                "synonyms": [],
                "antonyms": ["improbable"],
                "toeicNotes": ["Phân biệt: probable (có triển vọng xảy ra) và convincing (có sức thuyết phục người khác tin)"],
                "needsReview": False
            },
            {
                "id": "focus-v",
                "word": "focus",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈfəʊkəs/", "us": "/ˈfoʊkəs/"},
                "frequency": 2,
                "meaningVi": "tập trung",
                "exampleEn": "Management decided to focus resources on expanding its business.",
                "exampleVi": "Ban quản lý đã quyết định tập trung các nguồn lực vào việc mở rộng kinh doanh.",
                "derivatives": [
                    {"word": "focus", "partOfSpeech": "n", "meaningVi": "tiêu điểm, trọng tâm"}
                ],
                "synonyms": ["concentrate"],
                "antonyms": [],
                "toeicNotes": ["focus A on B: tập trung A vào B", "be focused on: được tập trung vào"],
                "needsReview": False
            },
            {
                "id": "focus-n",
                "word": "focus",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈfəʊkəs/", "us": "/ˈfoʊkəs/"},
                "frequency": 2,
                "meaningVi": "trọng tâm, tiêu điểm",
                "exampleEn": "The main focus of the meeting was the new budget.",
                "exampleVi": "Trọng tâm chính của cuộc họp là ngân sách mới.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "seasonal",
                "word": "seasonal",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈsiːzənl/", "us": "/ˈsiːzənl/"},
                "frequency": 2,
                "meaningVi": "theo mùa, mang tính thời vụ",
                "exampleEn": "The sugarcane industry is vulnerable to seasonal variations.",
                "exampleVi": "Ngành sản xuất đường mía rất dễ bị tác động bởi những thay đổi theo mùa.",
                "derivatives": [
                    {"word": "season", "partOfSpeech": "n", "meaningVi": "mùa"},
                    {"word": "seasonally", "partOfSpeech": "adv", "meaningVi": "theo từng mùa"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["seasonal variation/demand/change: sự thay đổi/nhu cầu theo mùa", "Phân biệt: seasonal (theo mùa) và seasoned (dày dạn kinh nghiệm, lão luyện)"],
                "needsReview": False
            },
            {
                "id": "impact",
                "word": "impact",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɪmpækt/", "us": "/ˈɪmpækt/"},
                "frequency": 2,
                "meaningVi": "sự tác động, sự ảnh hưởng, va chạm",
                "exampleEn": "Price fluctuations had a major impact on the market.",
                "exampleVi": "Những biến động về giá cả có tác động lớn đến thị trường.",
                "derivatives": [],
                "synonyms": ["influence", "effect"],
                "antonyms": [],
                "toeicNotes": ["have an impact on: có tác động/ảnh hưởng đến"],
                "needsReview": False
            },
            {
                "id": "comparison",
                "word": "comparison",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kəmˈpærɪsn/", "us": "/kəmˈpærɪsn/"},
                "frequency": 2,
                "meaningVi": "sự so sánh",
                "exampleEn": "Online advertising is cheaper in comparison with television.",
                "exampleVi": "Quảng cáo trên tivi rẻ hơn so với quảng cáo trên mạng.",
                "derivatives": [
                    {"word": "compare", "partOfSpeech": "v", "meaningVi": "so sánh"},
                    {"word": "comparable", "partOfSpeech": "adj", "meaningVi": "có thể so sánh"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["in comparison with: so sánh với"],
                "needsReview": False
            },
            {
                "id": "gap",
                "word": "gap",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɡæp/", "us": "/ɡæp/"},
                "frequency": 2,
                "meaningVi": "lỗ hổng, kẽ hở, khoảng trống, khoảng cách",
                "exampleEn": "Severe deficits can occur when there is a huge gap between exports and imports.",
                "exampleVi": "Thâm hụt nghiêm trọng có thể xảy ra khi có một khoảng cách lớn giữa xuất khẩu và nhập khẩu.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["gap between A and B: khoảng trống giữa A và B", "generation gap: khoảng cách thế hệ", "Phân biệt: gap (khoảng trống, lỗ hổng) và hole (lỗ thủng)"],
                "needsReview": False
            },
            {
                "id": "mounting",
                "word": "mounting",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈmaʊntɪŋ/", "us": "/ˈmaʊntɪŋ/"},
                "frequency": 2,
                "meaningVi": "tăng dần lên",
                "exampleEn": "There is mounting pressure from management to increase productivity.",
                "exampleVi": "Áp lực từ ban quản lý ngày càng tăng đối với việc phải nâng cao năng suất.",
                "derivatives": [
                    {"word": "mount", "partOfSpeech": "v", "meaningVi": "dựng lên, tăng lên"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["mounting pressure: áp lực ngày càng tăng", "mounting tension: căng thẳng tăng dần"],
                "needsReview": False
            },
            {
                "id": "reflective",
                "word": "reflective",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/rɪˈflektɪv/", "us": "/rɪˈflektɪv/"},
                "frequency": 2,
                "meaningVi": "phản chiếu, phản ánh",
                "exampleEn": "Shrinking profits are reflective of the current state of the company.",
                "exampleVi": "Lợi nhuận ngày càng thu nhỏ lại phản ánh tình trạng hiện tại của công ty.",
                "derivatives": [
                    {"word": "reflect", "partOfSpeech": "v", "meaningVi": "phản chiếu, phản ánh"},
                    {"word": "reflection", "partOfSpeech": "n", "meaningVi": "sự phản chiếu, phản ánh"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["be reflective of: phản ánh cái gì"],
                "needsReview": False
            }
        ]

    if day_num == 8:
        words_data = [
            {
                "id": "advertisement",
                "word": "advertisement",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ədˈvɜːtɪsmənt/", "us": "/ˌædvərˈtaɪzmənt/"},
                "frequency": 3,
                "meaningVi": "quảng cáo",
                "exampleEn": "Sales have been propelled by the new advertisement.",
                "exampleVi": "Doanh số bán hàng đã được thúc đẩy bởi quảng cáo mới này.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "marginal",
                "word": "marginal",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈmɑːdʒɪnl/", "us": "/ˈmɑːrdʒɪnl/"},
                "frequency": 2,
                "meaningVi": "không đáng kể, ở mép, sát giới hạn",
                "exampleEn": "Customers showed only marginal interest in the new tablet computer.",
                "exampleVi": "Người tiêu dùng tỏ ra không mấy quan tâm đến sản phẩm máy tính bảng mới.",
                "derivatives": [
                    {"word": "margin", "partOfSpeech": "n", "meaningVi": "lề, mép, giới hạn, biên, sự chênh lệch"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: marginal (xung quanh, gần ranh giới) và approximate (xấp xỉ, gần đúng)"],
                "needsReview": False
            },
            {
                "id": "customer",
                "word": "customer",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈkʌstəmə(r)//", "us": "/ˈkʌstəmər/"},
                "frequency": 3,
                "meaningVi": "khách hàng, người tiêu dùng",
                "exampleEn": "Telephone representatives should make the needs of customers their priority.",
                "exampleVi": "Nhân viên bán hàng trên điện thoại nên đặt nhu cầu của khách hàng là ưu tiên hàng đầu.",
                "derivatives": [],
                "synonyms": ["patron"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "influence-v",
                "word": "influence",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɪnfluəns/", "us": "/ˈɪnfluəns/"},
                "frequency": 2,
                "meaningVi": "ảnh hưởng, tác động, chi phối",
                "exampleEn": "Demand for housing directly influences the cost of homes.",
                "exampleVi": "Nhu cầu về nhà ở ảnh hưởng trực tiếp tới giá nhà.",
                "derivatives": [
                    {"word": "influential", "partOfSpeech": "adj", "meaningVi": "có ảnh hưởng"}
                ],
                "synonyms": ["affect"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "influence-n",
                "word": "influence",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɪnfluəns/", "us": "/ˈɪnfluəns/"},
                "frequency": 2,
                "meaningVi": "sự ảnh hưởng, tác dụng",
                "exampleEn": "Product reviews have a profound influence on sales.",
                "exampleVi": "Những đánh giá về sản phẩm có tác động rất lớn đến việc bán hàng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["have an influence on: có ảnh hưởng tới"],
                "needsReview": False
            },
            {
                "id": "instantly",
                "word": "instantly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈɪnstəntli/", "us": "/ˈɪnstəntli/"},
                "frequency": 3,
                "meaningVi": "ngay lập tức",
                "exampleEn": "The brand logo should be instantly recognizable.",
                "exampleVi": "Logo của thương hiệu cần được dễ dàng nhận diện ngay lập tức.",
                "derivatives": [
                    {"word": "instance", "partOfSpeech": "n", "meaningVi": "ví dụ"},
                    {"word": "instant", "partOfSpeech": "adj", "meaningVi": "ngay lập tức"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: instantly (ngay tức thì), urgently (khẩn cấp), hastily (vội vàng)"],
                "needsReview": False
            },
            {
                "id": "creative",
                "word": "creative",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/kriˈeɪtɪv/", "us": "/kriˈeɪtɪv/"},
                "frequency": 2,
                "meaningVi": "sáng tạo",
                "exampleEn": "Mr. Beaumont came up with a creative idea.",
                "exampleVi": "Ông Beaumont đã nảy ra một ý tưởng sáng tạo.",
                "derivatives": [
                    {"word": "create", "partOfSpeech": "v", "meaningVi": "tạo ra"},
                    {"word": "creativity", "partOfSpeech": "n", "meaningVi": "sự sáng tạo"},
                    {"word": "creatively", "partOfSpeech": "adv", "meaningVi": "một cách sáng tạo"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "aggressively",
                "word": "aggressively",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/əˈɡresɪvli/", "us": "/əˈɡresɪvli/"},
                "frequency": 3,
                "meaningVi": "xông xáo, tích cực, quyết liệt",
                "exampleEn": "The best sales representatives aggressively seek out potential clients.",
                "exampleVi": "Những nhân viên bán hàng tốt nhất luôn tích cực tìm kiếm các khách hàng tiềm năng.",
                "derivatives": [
                    {"word": "aggressive", "partOfSpeech": "adj", "meaningVi": "xông xáo, chủ động, quyết liệt"}
                ],
                "synonyms": [],
                "antonyms": ["passively"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "aim-v",
                "word": "aim",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/eɪm/", "us": "/eɪm/"},
                "frequency": 3,
                "meaningVi": "nhắm tới, có mục đích",
                "exampleEn": "Sport Apparel developed athletic gear aimed at teenagers.",
                "exampleVi": "Sport Apparel đã phát triển những dụng cụ thể thao nhằm tới đối tượng thanh thiếu niên.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["aim to do: định làm gì", "aimed at: nhằm mục tiêu vào (đối tượng)"],
                "needsReview": False
            },
            {
                "id": "aim-n",
                "word": "aim",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/eɪm/", "us": "/eɪm/"},
                "frequency": 3,
                "meaningVi": "mục tiêu, mục đích",
                "exampleEn": "The division head will outline the aims of the marketing strategy.",
                "exampleVi": "Trưởng bộ phận sẽ vạch ra các mục tiêu của chiến lược marketing này.",
                "derivatives": [],
                "synonyms": ["intention"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "strategy",
                "word": "strategy",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈstrætədʒi/", "us": "/ˈstrætədʒi/"},
                "frequency": 2,
                "meaningVi": "chiến lược",
                "exampleEn": "Management's strategy for expansion has been successful.",
                "exampleVi": "Chiến dịch mở rộng của ban quản lý đã thành công.",
                "derivatives": [
                    {"word": "strategic", "partOfSpeech": "adj", "meaningVi": "có tính chiến lược"},
                    {"word": "strategically", "partOfSpeech": "adv", "meaningVi": "có chiến lược"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "indicate",
                "word": "indicate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɪndɪkeɪt/", "us": "/ˈɪndɪkeɪt/"},
                "frequency": 3,
                "meaningVi": "biểu thị, cho biết, chỉ ra",
                "exampleEn": "Studies indicate that consumers prefer attractively packaged products.",
                "exampleVi": "Các nghiên cứu chỉ ra rằng người tiêu dùng thích những sản phẩm được đóng gói bắt mắt.",
                "derivatives": [
                    {"word": "indicative", "partOfSpeech": "adj", "meaningVi": "tỏ ra, chỉ ra"},
                    {"word": "indication", "partOfSpeech": "n", "meaningVi": "sự biểu thị, dấu hiệu"},
                    {"word": "indicator", "partOfSpeech": "n", "meaningVi": "chỉ số, chỉ tiêu"}
                ],
                "synonyms": ["show"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "attract",
                "word": "attract",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈtrækt/", "us": "/əˈtrækt/"},
                "frequency": 3,
                "meaningVi": "thu hút, lôi cuốn",
                "exampleEn": "The automaker is making an effort to attract younger buyers.",
                "exampleVi": "Nhà sản xuất xe ô tô đang nỗ lực để thu hút những người tiêu dùng trẻ tuổi.",
                "derivatives": [
                    {"word": "attractive", "partOfSpeech": "adj", "meaningVi": "thu hút, hấp dẫn"},
                    {"word": "attraction", "partOfSpeech": "n", "meaningVi": "sức hút, sự hấp dẫn"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "experience-n",
                "word": "experience",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪkˈspɪəriəns/", "us": "/ɪkˈspɪəriəns/"},
                "frequency": 3,
                "meaningVi": "kinh nghiệm, sự trải nghiệm",
                "exampleEn": "All of the invited guests had a pleasant experience at the store opening.",
                "exampleVi": "Tất cả khách mời đã có trải nghiệm vui vẻ trong ngày khai trương cửa hàng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "experience-v",
                "word": "experience",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪkˈspɪəriəns/", "us": "/ɪkˈspɪəriəns/"},
                "frequency": 3,
                "meaningVi": "trải nghiệm, trải qua",
                "exampleEn": "Customers can experience the new service free for a limited time.",
                "exampleVi": "Khách hàng có thể trải nghiệm dịch vụ mới miễn phí trong một khoảng thời gian giới hạn.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "analyze",
                "word": "analyze",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈænəlaɪz/", "us": "/ˈænəlaɪz/"},
                "frequency": 3,
                "meaningVi": "phân tích",
                "exampleEn": "Researchers were asked to analyze the survey data.",
                "exampleVi": "Các nhà nghiên cứu đã được yêu cầu phân tích các dữ liệu khảo sát.",
                "derivatives": [
                    {"word": "analysis", "partOfSpeech": "n", "meaningVi": "sự phân tích"},
                    {"word": "analyst", "partOfSpeech": "n", "meaningVi": "nhà phân tích"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "introduce",
                "word": "introduce",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˌɪntrəˈdjuːs/", "us": "/ˌɪntrəˈduːs/"},
                "frequency": 3,
                "meaningVi": "giới thiệu, đưa ra",
                "exampleEn": "ElectroLife introduced a new line of vacuum cleaners.",
                "exampleVi": "ElectroLife đã giới thiệu một dòng sản phẩm máy hút bụi mới.",
                "derivatives": [
                    {"word": "introduction", "partOfSpeech": "n", "meaningVi": "sự giới thiệu"},
                    {"word": "introductory", "partOfSpeech": "adj", "meaningVi": "để giới thiệu"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "advise",
                "word": "advise",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ədˈvaɪz/", "us": "/ədˈvaɪz/"},
                "frequency": 3,
                "meaningVi": "khuyên bảo, khuyên nhủ, tư vấn",
                "exampleEn": "Coburn Law Firm advises clients on intellectual property matters.",
                "exampleVi": "Hãng Luật Coburn tư vấn cho khách hàng về các vấn đề sở hữu trí tuệ.",
                "derivatives": [
                    {"word": "advice", "partOfSpeech": "n", "meaningVi": "lời khuyên"},
                    {"word": "advisor", "partOfSpeech": "n", "meaningVi": "người cố vấn"},
                    {"word": "advisory", "partOfSpeech": "adj", "meaningVi": "tư vấn, khuyến cáo"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["advise A to do: khuyên A làm gì", "advise A on B: tư vấn cho A về B"],
                "needsReview": False
            },
            {
                "id": "subscribe",
                "word": "subscribe",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/səbˈskraɪb/", "us": "/səbˈskraɪb/"},
                "frequency": 3,
                "meaningVi": "đăng ký, đặt mua dài hạn (báo, tạp chí)",
                "exampleEn": "Subscribing to the monthly fashion magazine costs only $40 a year.",
                "exampleVi": "Đặt mua dài hạn tạp chí thời trang hằng tháng chỉ tốn 40 đô-la một năm.",
                "derivatives": [
                    {"word": "subscription", "partOfSpeech": "n", "meaningVi": "sự đặt mua định kỳ"},
                    {"word": "subscriber", "partOfSpeech": "n", "meaningVi": "người đặt mua định kỳ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "absence",
                "word": "absence",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈæbsəns/", "us": "/ˈæbsəns/"},
                "frequency": 3,
                "meaningVi": "sự vắng mặt, sự nghỉ phép, sự thiếu",
                "exampleEn": "The absence of competition will help product sales.",
                "exampleVi": "Không có cạnh tranh sẽ có lợi cho việc bán sản phẩm.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["presence"],
                "toeicNotes": ["during/in one's absence: trong lúc ai đó vắng mặt"],
                "needsReview": False
            },
            {
                "id": "means",
                "word": "means",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/miːnz/", "us": "/miːnz/"},
                "frequency": 3,
                "meaningVi": "phương tiện, cách thức",
                "exampleEn": "Direct surveys are one means of gathering consumer feedback.",
                "exampleVi": "Khảo sát trực tiếp là một trong những cách để thu thập phản hồi của khách hàng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["by means of: bằng phương tiện/cách", "Phân biệt: means of (phương pháp/phương tiện cho cái gì) và instrument for (công cụ để làm gì)"],
                "needsReview": False
            },
            {
                "id": "prefer",
                "word": "prefer",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/prɪˈfɜː(r)/", "us": "/prɪˈfɜːr/"},
                "frequency": 3,
                "meaningVi": "thích hơn (những cái khác)",
                "exampleEn": "Customers prefer Luster Shampoo to any other competing brand.",
                "exampleVi": "Người tiêu dùng thích dầu gội Luster hơn các thương hiệu cạnh tranh khác.",
                "derivatives": [
                    {"word": "preferable", "partOfSpeech": "adj", "meaningVi": "được ưa thích hơn"},
                    {"word": "preference", "partOfSpeech": "n", "meaningVi": "sự ưa thích hơn"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["prefer A to B: thích A hơn B"],
                "needsReview": False
            },
            {
                "id": "advantage",
                "word": "advantage",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ədˈvɑːntɪdʒ/", "us": "/ədˈvæntɪdʒ/"},
                "frequency": 3,
                "meaningVi": "lợi ích, lợi thế",
                "exampleEn": "One advantage of consumer testing is the development of marketing insight.",
                "exampleVi": "Một lợi ích của hoạt động thử nghiệm với người tiêu dùng là có được hiểu biết thấu đáo về marketing.",
                "derivatives": [
                    {"word": "advantageous", "partOfSpeech": "adj", "meaningVi": "có lợi, thuận lợi"}
                ],
                "synonyms": [],
                "antonyms": ["disadvantage"],
                "toeicNotes": ["take advantage of: lợi dụng, tận dụng", "Phân biệt: advantage (điểm mạnh, ưu thế so với người khác) và benefit (lợi ích mang lại từ cái gì)"],
                "needsReview": False
            },
            {
                "id": "forward-adv",
                "word": "forward",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈfɔːwəd/", "us": "/ˈfɔːrwərd/"},
                "frequency": 3,
                "meaningVi": "về phía trước, tiến bộ",
                "exampleEn": "Our company's research program has moved forward substantially.",
                "exampleVi": "Chương trình nghiên cứu của công ty chúng tôi đã tiến triển đáng kể.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["backward"],
                "toeicNotes": ["a huge step forward: một bước tiến lớn", "look forward to -ing: mong đợi làm gì"],
                "needsReview": False
            },
            {
                "id": "forward-v",
                "word": "forward",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈfɔːwəd/", "us": "/ˈfɔːrwərd/"},
                "frequency": 3,
                "meaningVi": "chuyển tiếp (đồ vật, thông tin)",
                "exampleEn": "Please forward your e-mail to the accounting manager.",
                "exampleVi": "Vui lòng chuyển tiếp email cho trưởng phòng kế toán.",
                "derivatives": [],
                "synonyms": ["send", "redirect"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "contemporary",
                "word": "contemporary",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/kənˈtempərəri/", "us": "/kənˈtempəreri/"},
                "frequency": 2,
                "meaningVi": "đương thời, hiện đại",
                "exampleEn": "Advertising messages change over time to reflect contemporary attitudes.",
                "exampleVi": "Các thông điệp quảng cáo thay đổi theo thời gian để phản ánh những quan điểm đương thời.",
                "derivatives": [],
                "synonyms": ["modern"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "discussion",
                "word": "discussion",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈskʌʃn/", "us": "/dɪˈskʌʃn/"},
                "frequency": 3,
                "meaningVi": "sự thảo luận, sự tranh luận",
                "exampleEn": "A discussion was held to decide how to promote the product.",
                "exampleVi": "Một cuộc thảo luận đã được tổ chức để quyết định cách thức quảng bá sản phẩm.",
                "derivatives": [
                    {"word": "discuss", "partOfSpeech": "v", "meaningVi": "thảo luận"}
                ],
                "synonyms": ["debate", "conversation"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "initial",
                "word": "initial",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪˈnɪʃl/", "us": "/ɪˈnɪʃl/"},
                "frequency": 2,
                "meaningVi": "ban đầu, lúc đầu",
                "exampleEn": "Initial findings show that customers are satisfied with the service.",
                "exampleVi": "Những kết quả ban đầu cho thấy người tiêu dùng hài lòng với dịch vụ này.",
                "derivatives": [
                    {"word": "initiate", "partOfSpeech": "v", "meaningVi": "đề xướng, khởi xướng"},
                    {"word": "initially", "partOfSpeech": "adv", "meaningVi": "vào lúc đầu"}
                ],
                "synonyms": [],
                "antonyms": ["final"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "steadily",
                "word": "steadily",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈstedəli/", "us": "/ˈstedəli/"},
                "frequency": 2,
                "meaningVi": "vững chắc, kiên định, tăng dần đều",
                "exampleEn": "Product sales steadily increased as time passed.",
                "exampleVi": "Lượng sản phẩm bán ra tăng ổn định theo thời gian.",
                "derivatives": [
                    {"word": "steady", "partOfSpeech": "adj", "meaningVi": "ổn định, kiên định"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "necessarily",
                "word": "necessarily",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈnesəsərəli/", "us": "/ˌnesəˈserəli/"},
                "frequency": 2,
                "meaningVi": "tất yếu, nhất thiết",
                "exampleEn": "Increased production does not necessarily lead to greater revenues.",
                "exampleVi": "Sản lượng tăng không nhất thiết dẫn đến doanh thu tăng.",
                "derivatives": [
                    {"word": "necessary", "partOfSpeech": "adj", "meaningVi": "cần thiết"},
                    {"word": "necessitate", "partOfSpeech": "v", "meaningVi": "bắt phải, đòi hỏi"},
                    {"word": "necessity", "partOfSpeech": "n", "meaningVi": "sự cần thiết"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["not necessarily: không nhất thiết phải"],
                "needsReview": False
            },
            {
                "id": "resolve",
                "word": "resolve",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈzɒlv/", "us": "/rɪˈzɑːlv/"},
                "frequency": 2,
                "meaningVi": "giải quyết, kiên quyết",
                "exampleEn": "The new facial cream promises to resolve 90 percent of common skin problems.",
                "exampleVi": "Loại kem dưỡng da mới hứa hẹn sẽ giải quyết được 90% những vấn đề thường gặp về da.",
                "derivatives": [
                    {"word": "resolution", "partOfSpeech": "n", "meaningVi": "sự giải quyết, quyết định"}
                ],
                "synonyms": ["solve", "settle"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "detect",
                "word": "detect",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/dɪˈtekt/", "us": "/dɪˈtekt/"},
                "frequency": 2,
                "meaningVi": "phát hiện ra, khám phá ra, nhận ra",
                "exampleEn": "Only a few people detected any actual differences between the two models.",
                "exampleVi": "Chỉ một vài người nhận ra những khác biệt thực sự giữa hai mẫu này.",
                "derivatives": [
                    {"word": "detection", "partOfSpeech": "n", "meaningVi": "sự phát hiện"},
                    {"word": "detective", "partOfSpeech": "n/adj", "meaningVi": "thám tử/thuộc thám tử"}
                ],
                "synonyms": ["discover", "notice"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "intensify",
                "word": "intensify",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈtensɪfaɪ/", "us": "/ɪnˈtensɪfaɪ/"},
                "frequency": 2,
                "meaningVi": "làm tăng lên, tăng cường, gia tăng",
                "exampleEn": "The movie studio intensified its promotional activities to draw in a wider audience.",
                "exampleVi": "Hãng phim đã tăng cường các hoạt động quảng bá để thu hút một lượng lớn khán giả.",
                "derivatives": [
                    {"word": "intense", "partOfSpeech": "adj", "meaningVi": "mạnh, cực kỳ"},
                    {"word": "intensive", "partOfSpeech": "adj", "meaningVi": "chuyên sâu, tập trung"}
                ],
                "synonyms": [],
                "antonyms": ["weaken", "diminish"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "favorably",
                "word": "favorably",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈfeɪvərəbli/", "us": "/ˈfeɪvərəbli/"},
                "frequency": 2,
                "meaningVi": "thuận lợi, tốt đẹp, có thiện chí",
                "exampleEn": "The product demonstration was favorably received by consumers.",
                "exampleVi": "Buổi trưng bày giới thiệu sản phẩm đã được khách hàng nồng nhiệt đón nhận.",
                "derivatives": [
                    {"word": "favor", "partOfSpeech": "n/v", "meaningVi": "thiện chí/ủng hộ"},
                    {"word": "favorable", "partOfSpeech": "adj", "meaningVi": "thuận lợi"},
                    {"word": "favored", "partOfSpeech": "adj", "meaningVi": "được ưa chuộng"}
                ],
                "synonyms": [],
                "antonyms": ["unfavorably"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "cover",
                "word": "cover",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈkʌvə(r)/", "us": "/ˈkʌvər/"},
                "frequency": 2,
                "meaningVi": "bao gồm, thanh toán (chi phí), che phủ, xử lý (tin tức)",
                "exampleEn": "The firm's budget is large enough to cover marketing expenses for a year.",
                "exampleVi": "Ngân sách của công ty đủ lớn để thanh toán chi phí marketing trong một năm.",
                "derivatives": [
                    {"word": "coverage", "partOfSpeech": "n", "meaningVi": "sự phủ sóng, tin tức, phạm vi"}
                ],
                "synonyms": ["include", "pay", "report on"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "less",
                "word": "less",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/les/", "us": "/les/"},
                "frequency": 2,
                "meaningVi": "ít hơn, kém hơn",
                "exampleEn": "Less competition among insurance companies led to higher premiums.",
                "exampleVi": "Ít sự cạnh tranh hơn giữa các công ty bảo hiểm đã dẫn đến việc tăng phí bảo hiểm.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["more"],
                "toeicNotes": ["Phân biệt: less (nói về số lượng, mức độ ít hơn) và lesser (kém quan trọng hơn, ít giá trị hơn)"],
                "needsReview": False
            },
            {
                "id": "majority",
                "word": "majority",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/məˈdʒɒrəti/", "us": "/məˈdʒɔːrəti/"},
                "frequency": 2,
                "meaningVi": "đa số, phần lớn, số đông",
                "exampleEn": "The majority of registered clients pay their dues regularly.",
                "exampleVi": "Đa số các khách hàng đã đăng ký đều trả phí rất đều đặn.",
                "derivatives": [
                    {"word": "major", "partOfSpeech": "adj/n", "meaningVi": "chủ yếu/chuyên ngành"}
                ],
                "synonyms": [],
                "antonyms": ["minority"],
                "toeicNotes": ["a/the majority of + N(plural): đa số", "Phân biệt: majority (có mạo từ a/the) và most of the (không sử dụng mạo từ trước most)"],
                "needsReview": False
            },
            {
                "id": "adopt",
                "word": "adopt",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈdɒpt/", "us": "/əˈdɑːpt/"},
                "frequency": 2,
                "meaningVi": "thông qua, lựa chọn, làm theo, nhận nuôi",
                "exampleEn": "Plenty of research must be done before adopting a particular marketing strategy.",
                "exampleVi": "Cần phải thực hiện nhiều cuộc nghiên cứu trước khi thông qua một chiến lược marketing nhất định.",
                "derivatives": [
                    {"word": "adoption", "partOfSpeech": "n", "meaningVi": "sự chấp nhận, nhận nuôi"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "largely",
                "word": "largely",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈlɑːdʒli/", "us": "/ˈlɑːrdʒli/"},
                "frequency": 2,
                "meaningVi": "phần lớn, đa phần, trên quy mô lớn",
                "exampleEn": "Public reaction to the charity foundation was largely positive.",
                "exampleVi": "Phản ứng của công chúng đối với tổ chức từ thiện này đa phần là tích cực.",
                "derivatives": [
                    {"word": "large", "partOfSpeech": "adj", "meaningVi": "lớn"}
                ],
                "synonyms": ["mostly", "mainly"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "disregard",
                "word": "disregard",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˌdɪsrɪˈɡɑːd/", "us": "/ˌdɪsrɪˈɡɑːrd/"},
                "frequency": 2,
                "meaningVi": "xem nhẹ, không đếm xỉa đến, lờ đi",
                "exampleEn": "The company should not disregard customers' opinions if it wants to improve service quality.",
                "exampleVi": "Công ty không nên xem nhẹ ý kiến của khách hàng nếu muốn cải thiện chất lượng dịch vụ.",
                "derivatives": [
                    {"word": "disregard", "partOfSpeech": "n", "meaningVi": "sự bỏ qua, sự lơ là"}
                ],
                "synonyms": ["ignore"],
                "antonyms": ["consider", "respect"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "effort",
                "word": "effort",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈefət/", "us": "/ˈefərt/"},
                "frequency": 2,
                "meaningVi": "sự cố gắng, sự nỗ lực",
                "exampleEn": "TV commercials were run in an effort to broaden consumer awareness of new brands.",
                "exampleVi": "Quảng cáo được phát trên truyền hình với nỗ lực nhằm tăng cường sự nhận diện của người tiêu dùng đối với những thương hiệu mới.",
                "derivatives": [],
                "synonyms": ["endeavor"],
                "antonyms": [],
                "toeicNotes": ["in an effort to do: trong nỗ lực làm gì", "make an effort: nỗ lực"],
                "needsReview": False
            },
            {
                "id": "incentive",
                "word": "incentive",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪnˈsentɪv/", "us": "/ɪnˈsentɪv/"},
                "frequency": 2,
                "meaningVi": "sự khích lệ, ưu đãi, khuyến khích",
                "exampleEn": "Financial incentives such as coupons may encourage purchases.",
                "exampleVi": "Những ưu đãi về tài chính như phiếu giảm giá có thể khuyến khích việc mua hàng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["financial incentives: ưu đãi tài chính", "extra incentives: phần thưởng thêm", "Phân biệt: incentive (tiền khuyến khích), budget (ngân sách), earning (thu nhập)"],
                "needsReview": False
            },
            {
                "id": "need-n",
                "word": "need",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/niːd/", "us": "/niːd/"},
                "frequency": 2,
                "meaningVi": "nhu cầu, sự cần thiết",
                "exampleEn": "The company is in need of an untapped market.",
                "exampleVi": "Công ty đang cần một thị trường chưa được khai thác.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["in need of: đang cần cái gì", "meet the needs of: đáp ứng nhu cầu của"],
                "needsReview": False
            },
            {
                "id": "need-v",
                "word": "need",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/niːd/", "us": "/niːd/"},
                "frequency": 2,
                "meaningVi": "cần, muốn",
                "exampleEn": "We need to scrutinize each transaction for potential errors.",
                "exampleVi": "Chúng tôi cần xem xét kỹ lưỡng từng giao dịch để tìm các lỗi có thể xảy ra.",
                "derivatives": [
                    {"word": "needy", "partOfSpeech": "adj", "meaningVi": "nghèo túng, thiếu thốn"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "mastermind",
                "word": "mastermind",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈmɑːstəmaɪnd/", "us": "/ˈmæstərmaɪnd/"},
                "frequency": 2,
                "meaningVi": "quân sư, đạo diễn, người tổ chức, bộ óc",
                "exampleEn": "Mr. Dane is the mastermind behind the innovative design.",
                "exampleVi": "Ông Dane chính là bộ óc đằng sau thiết kế sáng tạo đó.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            }
        ]

    if day_num == 9:
        words_data = [
            {
                "id": "stagnant",
                "word": "stagnant",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈstæɡnənt/", "us": "/ˈstæɡnənt/"},
                "frequency": 2,
                "meaningVi": "trì trệ, uể oải, lờ đờ, đình trệ",
                "exampleEn": "Profits are down this year as sales have been stagnant.",
                "exampleVi": "Lợi nhuận năm nay giảm là do việc kinh doanh trì trệ.",
                "derivatives": [
                    {"word": "stagnate", "partOfSpeech": "v", "meaningVi": "đình trệ, đình đốn"}
                ],
                "synonyms": ["sluggish"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "dramatically",
                "word": "dramatically",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/drəˈmætɪkli/", "us": "/drəˈmætɪkli/"},
                "frequency": 3,
                "meaningVi": "đột ngột, đáng kể, kịch tính",
                "exampleEn": "Interest rates climbed dramatically.",
                "exampleVi": "Lãi suất đã đột ngột tăng.",
                "derivatives": [
                    {"word": "dramatic", "partOfSpeech": "adj", "meaningVi": "kịch tính, đột ngột"}
                ],
                "synonyms": ["substantially"],
                "antonyms": [],
                "toeicNotes": ["increase/grow/climb dramatically: tăng lên đột ngột/đáng kể"],
                "needsReview": False
            },
            {
                "id": "brisk",
                "word": "brisk",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/brɪsk/", "us": "/brɪsk/"},
                "frequency": 2,
                "meaningVi": "sôi động, phát đạt, nhanh nhẹn, trong lành (thời tiết)",
                "exampleEn": "A brisk market is developing in online shopping.",
                "exampleVi": "Một thị trường sôi động đang phát triển trên môi trường mua sắm trực tuyến.",
                "derivatives": [],
                "synonyms": ["strong", "lively", "quick", "rapid"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "unstable",
                "word": "unstable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/uânˈsteɪbl/", "us": "/ʌnˈsteɪbl/"},
                "frequency": 2,
                "meaningVi": "không ổn định, không bền vững",
                "exampleEn": "Gas prices have been unstable in recent years.",
                "exampleVi": "Giá xăng dầu không ổn định trong những năm gần đây.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["stable"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "rapidly",
                "word": "rapidly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈræpɪdli/", "us": "/ˈræpɪdli/"},
                "frequency": 3,
                "meaningVi": "nhanh chóng, mau lẹ",
                "exampleEn": "Energy demand increased rapidly.",
                "exampleVi": "Nhu cầu về năng lượng tăng lên nhanh chóng.",
                "derivatives": [
                    {"word": "rapid", "partOfSpeech": "adj", "meaningVi": "nhanh chóng"},
                    {"word": "rapidity", "partOfSpeech": "n", "meaningVi": "sự nhanh chóng"}
                ],
                "synonyms": ["quickly", "swiftly"],
                "antonyms": ["slowly"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "soar",
                "word": "soar",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/sɔː(r)/", "us": "/sɔːr/"},
                "frequency": 2,
                "meaningVi": "bay vút lên, tăng vọt",
                "exampleEn": "Interest rates have soared due to inflation.",
                "exampleVi": "Lãi suất tăng vọt lên do lạm phát.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": ["plummet"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "assert",
                "word": "assert",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈsɜːt/", "us": "/əˈsɜːrt/"},
                "frequency": 2,
                "meaningVi": "khẳng định, quả quyết, đòi quyền lợi",
                "exampleEn": "The report asserts that corporate growth will continue.",
                "exampleVi": "Báo cáo khẳng định rằng công ty sẽ tiếp tục tăng trưởng.",
                "derivatives": [
                    {"word": "assertion", "partOfSpeech": "n", "meaningVi": "sự khẳng định"},
                    {"word": "assertive", "partOfSpeech": "adj", "meaningVi": "quả quyết, quyết đoán"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "boost",
                "word": "boost",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/buːst/", "us": "/buːst/"},
                "frequency": 2,
                "meaningVi": "thúc đẩy, nâng lên, tăng cường",
                "exampleEn": "The real estate industry has helped boost the economy.",
                "exampleVi": "Ngành bất động sản đã giúp thúc đẩy nền kinh tế.",
                "derivatives": [
                    {"word": "boost", "partOfSpeech": "n", "meaningVi": "sự tăng lên, sự thúc đẩy"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "analyst",
                "word": "analyst",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈænəlɪst/", "us": "/ˈænəlɪst/"},
                "frequency": 3,
                "meaningVi": "nhà phân tích, người phân tích",
                "exampleEn": "Analysts recommend buying stock in energy companies.",
                "exampleVi": "Các nhà phân tích khuyên nên mua cổ phiếu của các công ty năng lượng.",
                "derivatives": [
                    {"word": "analyze", "partOfSpeech": "v", "meaningVi": "phân tích"},
                    {"word": "analysis", "partOfSpeech": "n", "meaningVi": "sự phân tích"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["financial analyst: nhà phân tích tài chính", "market analyst: nhà phân tích thị trường"],
                "needsReview": False
            },
            {
                "id": "potential-adj",
                "word": "potential",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/pəˈtenʃl/", "us": "/pəˈtenʃl/"},
                "frequency": 2,
                "meaningVi": "tiềm năng, có khả năng",
                "exampleEn": "Potential earnings from the trade deal could reach billions of dollars.",
                "exampleVi": "Nguồn thu nhập tiềm năng từ giao dịch thương mại này có thể lên tới hàng tỷ đô-la.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "potential-n",
                "word": "potential",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/pəˈtenʃl/", "us": "/pəˈtenʃl/"},
                "frequency": 2,
                "meaningVi": "tiềm lực, tiềm năng",
                "exampleEn": "The newly formed company has great potential to succeed.",
                "exampleVi": "Công ty mới thành lập đó có tiềm năng thành công rất lớn.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "pleased",
                "word": "pleased",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/pliːzd/", "us": "/pliːzd/"},
                "frequency": 3,
                "meaningVi": "hài lòng, vui mừng",
                "exampleEn": "Investors are pleased with the market's performance.",
                "exampleVi": "Nhà đầu tư rất hài lòng với hiệu quả của thị trường đó.",
                "derivatives": [],
                "synonyms": ["satisfied", "happy"],
                "antonyms": ["displeased"],
                "toeicNotes": ["be pleased to do: sẵn lòng làm gì", "be pleased with: hài lòng với"],
                "needsReview": False
            },
            {
                "id": "remain",
                "word": "remain",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈmeɪn/", "us": "/rɪˈmeɪn/"},
                "frequency": 3,
                "meaningVi": "vẫn, duy trì, còn như cũ",
                "exampleEn": "The cost of living will remain stable over the next decade.",
                "exampleVi": "Chi phí sinh hoạt vẫn sẽ ổn định trong thập kỷ tới.",
                "derivatives": [
                    {"word": "remainder", "partOfSpeech": "n", "meaningVi": "phần còn lại"},
                    {"word": "remaining", "partOfSpeech": "adj", "meaningVi": "còn lại"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["remain steady/stable/the same: duy trì ổn định/như cũ", "remain to be seen: vẫn còn phải chờ xem"],
                "needsReview": False
            },
            {
                "id": "limited",
                "word": "limited",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈlɪmɪtɪd/", "us": "/ˈlɪmɪtɪd/"},
                "frequency": 3,
                "meaningVi": "hạn chế, bị giới hạn",
                "exampleEn": "The island nation has limited natural resources.",
                "exampleVi": "Quốc đảo này có nguồn tài nguyên thiên nhiên hạn chế.",
                "derivatives": [
                    {"word": "limit", "partOfSpeech": "v/n", "meaningVi": "giới hạn/sự giới hạn"},
                    {"word": "limitation", "partOfSpeech": "n", "meaningVi": "sự hạn chế"}
                ],
                "synonyms": ["restricted"],
                "antonyms": ["unlimited"],
                "toeicNotes": ["limited offer: ưu đãi có giới hạn", "for a limited time: trong thời gian giới hạn"],
                "needsReview": False
            },
            {
                "id": "costly",
                "word": "costly",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈkɒstli/", "us": "/ˈkɔːstli/"},
                "frequency": 3,
                "meaningVi": "tốn kém, đắt đỏ",
                "exampleEn": "Starting a business is costly.",
                "exampleVi": "Khởi nghiệp sẽ rất tốn kém.",
                "derivatives": [
                    {"word": "cost", "partOfSpeech": "n/v", "meaningVi": "chi phí/trị giá"}
                ],
                "synonyms": ["expensive"],
                "antonyms": ["cheap", "inexpensive"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "particular",
                "word": "particular",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/pəˈtɪkjələ(r)/", "us": "/pərˈtɪkjələr/"},
                "frequency": 3,
                "meaningVi": "đặc biệt, riêng biệt, cụ thể, chi tiết",
                "exampleEn": "Import taxes are higher for particular products that are luxury goods.",
                "exampleVi": "Một số sản phẩm đặc biệt như là hàng xa xỉ bị áp thuế nhập khẩu cao hơn.",
                "derivatives": [
                    {"word": "particularly", "partOfSpeech": "adv", "meaningVi": "đặc biệt, cá biệt"}
                ],
                "synonyms": ["specific"],
                "antonyms": [],
                "toeicNotes": ["in particular: nói riêng, đặc biệt"],
                "needsReview": False
            },
            {
                "id": "drastic",
                "word": "drastic",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈdræstɪk/", "us": "/ˈdræstɪk/"},
                "frequency": 3,
                "meaningVi": "mạnh mẽ, quyết liệt, triệt để",
                "exampleEn": "Resolving the financial crisis will require drastic action.",
                "exampleVi": "Giải quyết khủng hoảng tài chính đòi hỏi phải có những hành động quyết liệt.",
                "derivatives": [
                    {"word": "drastically", "partOfSpeech": "adv", "meaningVi": "quyết liệt, triệt để"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["drastic reform: cải cách triệt để"],
                "needsReview": False
            },
            {
                "id": "evenly",
                "word": "evenly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈiːvnli/", "us": "/ˈiːvnli/"},
                "frequency": 2,
                "meaningVi": "ngang nhau, đều, công bằng",
                "exampleEn": "Economic wealth is not evenly distributed.",
                "exampleVi": "Sự giàu có về kinh tế không được phân chia đều.",
                "derivatives": [
                    {"word": "even", "partOfSpeech": "adj", "meaningVi": "đều, bằng phẳng, chẵn"}
                ],
                "synonyms": ["equally"],
                "antonyms": ["unevenly"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "evidence",
                "word": "evidence",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈevɪdəns/", "us": "/ˈevɪdəns/"},
                "frequency": 3,
                "meaningVi": "bằng chứng, chứng cứ, dấu hiệu",
                "exampleEn": "The latest employment data shows evidence that the economy is improving.",
                "exampleVi": "Dữ liệu về việc làm mới nhất cho thấy bằng chứng rằng nền kinh tế đang cải thiện.",
                "derivatives": [
                    {"word": "evident", "partOfSpeech": "adj", "meaningVi": "rõ ràng, hiển nhiên"},
                    {"word": "evidently", "partOfSpeech": "adv", "meaningVi": "hiển nhiên, rõ ràng"}
                ],
                "synonyms": ["proof"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "prospect",
                "word": "prospect",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈprɒspekt/", "us": "/ˈprɑːspekt/"},
                "frequency": 3,
                "meaningVi": "viễn cảnh, triển vọng, khả năng thành công",
                "exampleEn": "Bolton Industries is facing the prospect of having to reduce its workforce.",
                "exampleVi": "Bolton Industries đang đối mặt với viễn cảnh phải cắt giảm nhân lực.",
                "derivatives": [
                    {"word": "prospective", "partOfSpeech": "adj", "meaningVi": "tương lai, có triển vọng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "lead",
                "word": "lead",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/liːd/", "us": "/liːd/"},
                "frequency": 3,
                "meaningVi": "dẫn dắt, chỉ huy, dẫn đến",
                "exampleEn": "Growing oil markets will lead to economic improvement.",
                "exampleVi": "Sự phát triển của thị trường dầu khí sẽ dẫn tới những cải thiện về kinh tế.",
                "derivatives": [
                    {"word": "leading", "partOfSpeech": "adj", "meaningVi": "dẫn đầu, hàng đầu"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["lead to: dẫn đến", "leading brand/company/figure: thương hiệu/công ty/nhân vật hàng đầu"],
                "needsReview": False
            },
            {
                "id": "fall-v",
                "word": "fall",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/fɔːl/", "us": "/fɔːl/"},
                "frequency": 2,
                "meaningVi": "giảm xuống, hạ xuống, rơi",
                "exampleEn": "The rate of unemployment has fallen steadily this quarter.",
                "exampleVi": "Tỷ lệ thất nghiệp đã giảm đều trong quý này.",
                "derivatives": [],
                "synonyms": ["decrease", "drop"],
                "antonyms": ["rise", "increase"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "fall-n",
                "word": "fall",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/fɔːl/", "us": "/fɔːl/"},
                "frequency": 2,
                "meaningVi": "sự giảm, sự rơi, sự sụp đổ",
                "exampleEn": "A sharp fall in prices was observed.",
                "exampleVi": "Sự giảm giá mạnh đã được ghi nhận.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "period",
                "word": "period",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈpɪəriəd/", "us": "/ˈpɪriəd/"},
                "frequency": 3,
                "meaningVi": "thời kỳ, giai đoạn, khoảng thời gian",
                "exampleEn": "For a period of three years, the company underwent rapid expansion.",
                "exampleVi": "Trong khoảng thời gian ba năm, công ty đã nhanh chóng mở rộng.",
                "derivatives": [
                    {"word": "periodic", "partOfSpeech": "adj", "meaningVi": "định kỳ"},
                    {"word": "periodically", "partOfSpeech": "adv", "meaningVi": "định kỳ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "indicator",
                "word": "indicator",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɪndɪkeɪtə(r)/", "us": "/ˈɪndɪkeɪtər/"},
                "frequency": 3,
                "meaningVi": "chỉ số, công cụ chỉ thị",
                "exampleEn": "Current economic indicators show rising growth in mining.",
                "exampleVi": "Các chỉ số kinh tế hiện tại cho thấy sự phát triển ngày càng tăng trong ngành khai thác mỏ.",
                "derivatives": [
                    {"word": "indicate", "partOfSpeech": "v", "meaningVi": "chỉ ra"},
                    {"word": "indication", "partOfSpeech": "n", "meaningVi": "sự biểu thị"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["economic indicator: chỉ số kinh tế"],
                "needsReview": False
            },
            {
                "id": "industry",
                "word": "industry",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɪndəstri/", "us": "/ˈɪndəstri/"},
                "frequency": 3,
                "meaningVi": "ngành công nghiệp, ngành sản xuất, sự cần cù",
                "exampleEn": "Jobs in the newspaper industry are declining rapidly.",
                "exampleVi": "Việc làm trong ngành báo chí đang giảm nhanh chóng.",
                "derivatives": [
                    {"word": "industrial", "partOfSpeech": "adj", "meaningVi": "thuộc công nghiệp"},
                    {"word": "industrious", "partOfSpeech": "adj", "meaningVi": "cần cù, siêng năng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "likely",
                "word": "likely",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈlaɪkli/", "us": "/ˈlaɪkli/"},
                "frequency": 2,
                "meaningVi": "có khả năng xảy ra, có thể, chắc hẳn",
                "exampleEn": "The new CEO is likely to confront major challenges.",
                "exampleVi": "Vị giám đốc điều hành mới có khả năng sẽ phải đối mặt với những thách thức lớn.",
                "derivatives": [
                    {"word": "likelihood", "partOfSpeech": "n", "meaningVi": "sự có thể xảy ra"}
                ],
                "synonyms": [],
                "antonyms": ["unlikely"],
                "toeicNotes": ["be likely to do: có khả năng làm gì", "Phân biệt: likely (có khả năng xảy ra trong thực tế, thường có chủ ngữ là người) và possible (có khả năng thành hiện thực, chủ ngữ thường không phải người)"],
                "needsReview": False
            },
            {
                "id": "boom",
                "word": "boom",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/buːm/", "us": "/buːm/"},
                "frequency": 2,
                "meaningVi": "sự bùng nổ, sự phát triển nhanh chóng",
                "exampleEn": "Land developers are taking advantage of the housing boom.",
                "exampleVi": "Các nhà phát triển dự án bất động sản đang tận dụng sự bùng nổ của thị trường nhà đất.",
                "derivatives": [
                    {"word": "boom", "partOfSpeech": "v", "meaningVi": "phát triển nhanh vọt"}
                ],
                "synonyms": [],
                "antonyms": ["slump", "depression"],
                "toeicNotes": ["housing boom: sự bùng nổ nhà đất"],
                "needsReview": False
            },
            {
                "id": "director",
                "word": "director",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/daɪˈrektə(r)/", "us": "/daɪˈrektər/"},
                "frequency": 2,
                "meaningVi": "giám đốc, người chỉ đạo",
                "exampleEn": "The company directors are discussing a new business strategy.",
                "exampleVi": "Ban giám đốc công ty đang thảo luận về một chiến lược kinh doanh mới.",
                "derivatives": [
                    {"word": "direct", "partOfSpeech": "v/adj", "meaningVi": "chỉ đạo/trực tiếp"},
                    {"word": "direction", "partOfSpeech": "n", "meaningVi": "sự chỉ đạo, hướng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "substitute-n",
                "word": "substitute",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈsʌbstɪtjuːt/", "us": "/ˈsʌbstɪtuːt/"},
                "frequency": 2,
                "meaningVi": "người thay thế, vật thay thế",
                "exampleEn": "Corn syrup is used as a substitute for sugar in many food products.",
                "exampleVi": "Xi-rô ngô được sử dụng như một nguyên liệu thay thế cho đường trong nhiều loại thực phẩm.",
                "derivatives": [],
                "synonyms": ["replacement"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "substitute-v",
                "word": "substitute",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈsʌbstɪtjuːt/", "us": "/ˈsʌbstɪtuːt/"},
                "frequency": 2,
                "meaningVi": "thay thế",
                "exampleEn": "Ms. Ohara will be substituting for the project manager this week.",
                "exampleVi": "Cô Ohara sẽ thay thế người quản lý dự án trong tuần này.",
                "derivatives": [],
                "synonyms": ["replace"],
                "antonyms": [],
                "toeicNotes": ["substitute A with B: thay thế A bằng B", "substitute B for A: thay thế B cho A"],
                "needsReview": False
            },
            {
                "id": "consequence",
                "word": "consequence",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈkɒnsɪkwəns/", "us": "/ˈkɑːnsəkwens/"},
                "frequency": 2,
                "meaningVi": "hậu quả, kết quả, hệ quả",
                "exampleEn": "Profits grew as a consequence of increased business.",
                "exampleVi": "Lợi nhuận tăng là kết quả của việc kinh doanh được cải thiện.",
                "derivatives": [
                    {"word": "consequential", "partOfSpeech": "adj", "meaningVi": "thuộc hệ quả, tự phụ"}
                ],
                "synonyms": ["result", "outcome"],
                "antonyms": [],
                "toeicNotes": ["as a consequence of: là kết quả của, do hậu quả của"],
                "needsReview": False
            },
            {
                "id": "fairly",
                "word": "fairly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈfeəli/", "us": "/ˈferli/"},
                "frequency": 2,
                "meaningVi": "khá, công bằng, ngay thẳng",
                "exampleEn": "Concerns over the bankruptcy are fairly widespread.",
                "exampleVi": "Những lo ngại về việc phá sản là khá phổ biến.",
                "derivatives": [
                    {"word": "fair", "partOfSpeech": "adj", "meaningVi": "công bằng, trung thực"}
                ],
                "synonyms": ["quite", "reasonably", "equally"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "economical",
                "word": "economical",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˌiːkəˈnɒmɪkl/", "us": "/ˌiːkəˈnɑːmɪkl/"},
                "frequency": 2,
                "meaningVi": "tiết kiệm, mang tính kinh tế",
                "exampleEn": "Companies are searching for economical ways to utilize energy.",
                "exampleVi": "Các công ty đang tìm kiếm những giải pháp tiết kiệm trong việc sử dụng năng lượng.",
                "derivatives": [
                    {"word": "economy", "partOfSpeech": "n", "meaningVi": "nền kinh tế"},
                    {"word": "economic", "partOfSpeech": "adj", "meaningVi": "thuộc kinh tế"},
                    {"word": "economics", "partOfSpeech": "n", "meaningVi": "kinh tế học"}
                ],
                "synonyms": ["thrifty", "saving"],
                "antonyms": ["extravagant"],
                "toeicNotes": ["Phân biệt: economical (tiết kiệm, kinh tế) và economic (thuộc về nền kinh tế, kinh tế)"],
                "needsReview": False
            },
            {
                "id": "thrive",
                "word": "thrive",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/θraɪv/", "us": "/θraɪv/"},
                "frequency": 2,
                "meaningVi": "phát triển mạnh, thịnh vượng, phát đạt",
                "exampleEn": "The delivery service industry is thriving.",
                "exampleVi": "Ngành dịch vụ giao hàng đang phát triển mạnh.",
                "derivatives": [],
                "synonyms": ["prosper", "flourish"],
                "antonyms": ["fail", "decline"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "implication",
                "word": "implication",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌɪmplɪˈkeɪʃn/", "us": "/ˌimplɪˈkeɪʃn/"},
                "frequency": 2,
                "meaningVi": "sự liên quan, sự dính líu, hàm ý ngụ ý",
                "exampleEn": "The Supreme Court ruling has implications for small businesses.",
                "exampleVi": "Phán quyết của tòa án tối cao có liên quan đến các doanh nghiệp nhỏ.",
                "derivatives": [
                    {"word": "implicate", "partOfSpeech": "v", "meaningVi": "ngụ ý, ám chỉ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "wane-n",
                "word": "wane",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/weɪn/", "us": "/weɪn/"},
                "frequency": 2,
                "meaningVi": "sự suy giảm, sự hao mòn",
                "exampleEn": "Consumer spending is on the wane.",
                "exampleVi": "Chiêu tiêu của người tiêu dùng đang giảm dần.",
                "derivatives": [],
                "synonyms": ["decline", "diminution"],
                "antonyms": ["wax"],
                "toeicNotes": ["on the wane: đang trên đà suy giảm"],
                "needsReview": False
            },
            {
                "id": "wane-v",
                "word": "wane",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/weɪn/", "us": "/weɪn/"},
                "frequency": 2,
                "meaningVi": "suy giảm, yếu đi, tàn tạ",
                "exampleEn": "Her popularity began to wane after the scandal.",
                "exampleVi": "Sự nổi tiếng của cô ấy bắt đầu giảm sút sau vụ bê bối.",
                "derivatives": [],
                "synonyms": ["decline", "fade"],
                "antonyms": ["grow", "increase"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "prosperity",
                "word": "prosperity",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/prɒˈsperəti/", "us": "/prɑːˈsperəti/"},
                "frequency": 2,
                "meaningVi": "sự thịnh vượng, sự phát đạt",
                "exampleEn": "Strong economic growth is a prerequisite for national prosperity.",
                "exampleVi": "Tăng trưởng kinh tế mạnh mẽ là điều kiện tiên quyết cho sự thịnh vượng quốc gia.",
                "derivatives": [
                    {"word": "prosper", "partOfSpeech": "v", "meaningVi": "thành công, phát đạt"},
                    {"word": "prosperous", "partOfSpeech": "adj", "meaningVi": "thịnh vượng, khấm khá"}
                ],
                "synonyms": ["wealth", "affluence"],
                "antonyms": ["poverty"],
                "toeicNotes": ["in times of prosperity: trong thời kỳ thịnh vượng"],
                "needsReview": False
            },
            {
                "id": "depression",
                "word": "depression",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈpreʃn/", "us": "/dɪˈpreʃn/"},
                "frequency": 2,
                "meaningVi": "tình trạng suy thoái (kinh tế), sự trầm cảm",
                "exampleEn": "The entire industry is going through an economic depression.",
                "exampleVi": "Toàn bộ ngành công nghiệp đang trải qua thời kỳ suy thoái kinh tế.",
                "derivatives": [],
                "synonyms": ["slump", "recession"],
                "antonyms": ["boom", "prosperity"],
                "toeicNotes": ["economic depression: suy thoái kinh tế"],
                "needsReview": False
            },
            {
                "id": "dwindle",
                "word": "dwindle",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈdwɪndl/", "us": "/ˈdwɪndl/"},
                "frequency": 2,
                "meaningVi": "giảm bớt, thu nhỏ, nhỏ lại",
                "exampleEn": "The company's profits dwindled in the 1990s.",
                "exampleVi": "Lợi nhuận của công ty đã sụt giảm trong những năm 1990.",
                "derivatives": [],
                "synonyms": ["diminish", "decrease", "shrink"],
                "antonyms": ["grow", "increase"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "impede",
                "word": "impede",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪmˈpiːd/", "us": "/ɪmˈpiːd/"},
                "frequency": 2,
                "meaningVi": "cản trở, ngăn trở",
                "exampleEn": "Natural calamities in the summer will impede national growth.",
                "exampleVi": "Thiên tai vào mùa hè sẽ cản trở sự tăng trưởng của quốc gia.",
                "derivatives": [
                    {"word": "impediment", "partOfSpeech": "n", "meaningVi": "sự cản trở, trở ngại"}
                ],
                "synonyms": ["hinder", "obstruct"],
                "antonyms": ["facilitate"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "promising",
                "word": "promising",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈprɒmɪsɪŋ/", "us": "/ˈprɑːmɪsɪŋ/"},
                "frequency": 2,
                "meaningVi": "đầy hứa hẹn, đầy triển vọng",
                "exampleEn": "Many people find promising careers in health and technology.",
                "exampleVi": "Nhiều người tìm thấy những nghề nghiệp đầy triển vọng trong ngành y tế và công nghệ.",
                "derivatives": [
                    {"word": "promise", "partOfSpeech": "v/n", "meaningVi": "hứa/lời hứa"}
                ],
                "synonyms": ["hopeful", "encouraging"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "adversity",
                "word": "adversity",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ədˈvɜːsəti/", "us": "/ədˈvɜːrsəti/"},
                "frequency": 2,
                "meaningVi": "hoàn cảnh khó khăn, nghịch cảnh, tai họa",
                "exampleEn": "In spite of the adversity he faced, Mike managed to find a job.",
                "exampleVi": "Bất chấp nghịch cảnh phải đối mặt, Mike vẫn xoay xở tìm được một công việc.",
                "derivatives": [
                    {"word": "adverse", "partOfSpeech": "adj", "meaningVi": "bất lợi, ngược lại"}
                ],
                "synonyms": ["difficulty", "hardship"],
                "antonyms": ["prosperity", "good fortune"],
                "toeicNotes": [],
                "needsReview": False
            }
        ]

    if day_num == 10:
        words_data = [
            {
                "id": "purchase-v",
                "word": "purchase",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈpɜːtʃəs/", "us": "/ˈpɜːrtʃəs/"},
                "frequency": 3,
                "meaningVi": "mua, sắm",
                "exampleEn": "The customer purchased a laptop computer.",
                "exampleVi": "Vị khách đã mua một chiếc máy tính xách tay.",
                "derivatives": [],
                "synonyms": ["buy"],
                "antonyms": ["sell"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "purchase-n",
                "word": "purchase",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈpɜːtʃəs/", "us": "/ˈpɜːrtʃəs/"},
                "frequency": 3,
                "meaningVi": "việc mua hàng, món đồ mua được",
                "exampleEn": "For every purchase of $100 or more, customers will receive a raffle ticket.",
                "exampleVi": "Với mỗi lần mua hàng giá trị từ 100 đô-la trở lên, khách hàng sẽ nhận được một tấm vé số.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["within ~ days of purchase: trong vòng ~ ngày kể từ ngày mua hàng"],
                "needsReview": False
            },
            {
                "id": "installment",
                "word": "installment",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪnˈstɔːlmənt/", "us": "/ɪnˈstɔːlmənt/"},
                "frequency": 2,
                "meaningVi": "sự trả góp, tiền trả góp",
                "exampleEn": "The shop allows buyers to pay for furniture in monthly installments.",
                "exampleVi": "Cửa hàng cho phép khách trả tiền mua đồ nội thất bằng hình thức trả góp theo tháng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["pay in monthly installments: trả góp hàng tháng"],
                "needsReview": False
            },
            {
                "id": "affordable",
                "word": "affordable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/əˈfɔːdəbl/", "us": "/əˈfɔːrdəbl/"},
                "frequency": 2,
                "meaningVi": "(giá cả) phải chăng, có thể chi trả được",
                "exampleEn": "Toyama launched an affordable mid-range sedan.",
                "exampleVi": "Toyama đã ra mắt một mẫu xe sedan tầm trung với mức giá hợp lý.",
                "derivatives": [
                    {"word": "afford", "partOfSpeech": "v", "meaningVi": "có đủ khả năng chi trả"},
                    {"word": "affordability", "partOfSpeech": "n", "meaningVi": "tính hợp lý về giá cả"},
                    {"word": "affordably", "partOfSpeech": "adv", "meaningVi": "ở mức giá phải chăng"}
                ],
                "synonyms": ["reasonable", "inexpensive"],
                "antonyms": ["expensive", "costly"],
                "toeicNotes": ["at an affordable price/rate: với mức giá hợp lý"],
                "needsReview": False
            },
            {
                "id": "exactly",
                "word": "exactly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ɪɡˈzæktli/", "us": "/ɪɡˈzæktli/"},
                "frequency": 3,
                "meaningVi": "chính xác, đúng",
                "exampleEn": "The sales representatives help customers decide exactly what style fits them best.",
                "exampleVi": "Nhân viên bán hàng giúp người mua xác định chính xác phong cách phù hợp với họ.",
                "derivatives": [
                    {"word": "exact", "partOfSpeech": "adj", "meaningVi": "chính xác"}
                ],
                "synonyms": ["precisely"],
                "antonyms": ["inaccurately"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "auction",
                "word": "auction",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɔːkʃn/", "us": "/ˈɑːkʃn/"},
                "frequency": 2,
                "meaningVi": "cuộc đấu giá, sự bán đấu giá",
                "exampleEn": "A number of antique pieces will be sold at the auction.",
                "exampleVi": "Nhiều món đồ cổ sẽ được bán tại buổi đấu giá.",
                "derivatives": [
                    {"word": "auctioneer", "partOfSpeech": "n", "meaningVi": "người điều hành bán đấu giá"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["sell at auction: bán đấu giá"],
                "needsReview": False
            },
            {
                "id": "authentic",
                "word": "authentic",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɔːˈθentɪk/", "us": "/ɑːˈθentɪk/"},
                "frequency": 2,
                "meaningVi": "thật, đích thực, đáng tin",
                "exampleEn": "The new downtown restaurant serves authentic Spanish cuisine.",
                "exampleVi": "Nhà hàng mới ở trung tâm thành phố phục vụ các món Tây Ban Nha đích thực.",
                "derivatives": [
                    {"word": "authenticity", "partOfSpeech": "n", "meaningVi": "tính xác thực, tính chân thật"}
                ],
                "synonyms": ["genuine", "real"],
                "antonyms": ["fake", "counterfeit"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "charge-n",
                "word": "charge",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/tʃɑːdʒ/", "us": "/tʃɑːrdʒ/"},
                "frequency": 3,
                "meaningVi": "tiền phải trả, phí, nhiệm vụ, trách nhiệm",
                "exampleEn": "The price includes shipping and handling charges.",
                "exampleVi": "Giá này đã bao gồm phí vận chuyển và xử lý.",
                "derivatives": [],
                "synonyms": ["expense", "fee", "cost"],
                "antonyms": [],
                "toeicNotes": ["free of charge: miễn phí", "in charge of: chịu trách nhiệm, đảm nhiệm", "additional charge: chi phí phát sinh thêm"],
                "needsReview": False
            },
            {
                "id": "charge-v",
                "word": "charge",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/tʃɑːdʒ/", "us": "/tʃɑːrdʒ/"},
                "frequency": 3,
                "meaningVi": "thu phí, tính phí, ghi nợ vào thẻ",
                "exampleEn": "The phone company charges high fees for installations.",
                "exampleVi": "Công ty viễn thông đó thu phí lắp đặt cao.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["charge A to B: tính khoản phí A vào B"],
                "needsReview": False
            },
            {
                "id": "notice-n",
                "word": "notice",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈnəʊtɪs/", "us": "/ˈnəʊtɪs/"},
                "frequency": 3,
                "meaningVi": "thông báo, yết thị, sự chú ý",
                "exampleEn": "The prices listed in the catalog are effective until further notice.",
                "exampleVi": "Giá ghi trong danh mục có hiệu lực cho đến khi có thông báo thêm.",
                "derivatives": [
                    {"word": "notify", "partOfSpeech": "v", "meaningVi": "thông báo, báo tin"},
                    {"word": "notification", "partOfSpeech": "n", "meaningVi": "sự thông báo"},
                    {"word": "noticeable", "partOfSpeech": "adj", "meaningVi": "đáng chú ý"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["until further notice: cho đến khi có thông báo mới", "give two weeks' notice: thông báo trước hai tuần"],
                "needsReview": False
            },
            {
                "id": "notice-v",
                "word": "notice",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈnəʊtɪs/", "us": "/ˈnəʊtɪs/"},
                "frequency": 3,
                "meaningVi": "chú ý, nhận biết, nhận ra",
                "exampleEn": "The customer noticed a flaw in the display item.",
                "exampleVi": "Khách hàng nhận ra một vết lỗi trên sản phẩm trưng bày.",
                "derivatives": [],
                "synonyms": ["observe", "spot"],
                "antonyms": ["ignore"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "experienced",
                "word": "experienced",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ɪkˈspɪəriənst/", "us": "/ɪkˈspɪriənst/"},
                "frequency": 3,
                "meaningVi": "có kinh nghiệm, lão luyện",
                "exampleEn": "Bill is the most experienced salesperson in the store.",
                "exampleVi": "Bill là nhân viên bán hàng có kinh nghiệm nhất ở cửa hàng.",
                "derivatives": [
                    {"word": "experience", "partOfSpeech": "n/v", "meaningVi": "kinh nghiệm/trải nghiệm"}
                ],
                "synonyms": ["expert", "seasoned"],
                "antonyms": ["inexperienced"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "instruction",
                "word": "instruction",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪnˈstrʌkʃn/", "us": "/ɪnˈstrʌkʃn/"},
                "frequency": 3,
                "meaningVi": "lời chỉ dẫn, hướng dẫn",
                "exampleEn": "The receipt gives instructions for returning or exchanging items.",
                "exampleVi": "Biên lai có cung cấp hướng dẫn cách đổi trả sản phẩm.",
                "derivatives": [
                    {"word": "instruct", "partOfSpeech": "v", "meaningVi": "hướng dẫn, chỉ bảo"},
                    {"word": "instructional", "partOfSpeech": "adj", "meaningVi": "thuộc hướng dẫn"}
                ],
                "synonyms": ["directions", "guidance"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "expert-n",
                "word": "expert",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈekspɜːt/", "us": "/ˈekspɜːrt/"},
                "frequency": 2,
                "meaningVi": "chuyên gia",
                "exampleEn": "A personal shopper is an expert at finding bargains for customers.",
                "exampleVi": "Chuyên viên tư vấn mua sắm cá nhân chính là chuyên gia trong việc tìm ra những món hời cho khách hàng.",
                "derivatives": [
                    {"word": "expertly", "partOfSpeech": "adv", "meaningVi": "một cách thành thạo, chuyên nghiệp"}
                ],
                "synonyms": ["specialist"],
                "antonyms": ["novice", "amateur"],
                "toeicNotes": ["expert at/in: chuyên gia về lĩnh vực gì"],
                "needsReview": False
            },
            {
                "id": "expert-adj",
                "word": "expert",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈekspɜːt/", "us": "/ˈekspɜːrt/"},
                "frequency": 2,
                "meaningVi": "về mặt chuyên môn, thành thạo, lão luyện",
                "exampleEn": "An expert designer created the layout of the store.",
                "exampleVi": "Nhà thiết kế có chuyên môn đã lên bố cục cho cửa hàng.",
                "derivatives": [],
                "synonyms": ["skillful", "proficient"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "warranty",
                "word": "warranty",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈwɒrənti/", "us": "/ˈwɔːrənti/"},
                "frequency": 3,
                "meaningVi": "giấy bảo hành, sự bảo hành",
                "exampleEn": "The computer is under warranty for two years.",
                "exampleVi": "Máy tính được bảo hành trong vòng 2 năm.",
                "derivatives": [],
                "synonyms": ["guarantee"],
                "antonyms": [],
                "toeicNotes": ["under warranty: trong thời gian bảo hành"],
                "needsReview": False
            },
            {
                "id": "refund-n",
                "word": "refund",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈriːfʌnd/", "us": "/ˈriːfʌnd/"},
                "frequency": 3,
                "meaningVi": "sự hoàn tiền, tiền trả lại",
                "exampleEn": "Buyers can get a full refund for a defective product.",
                "exampleVi": "Người mua có thể được hoàn trả toàn bộ tiền nếu sản phẩm bị lỗi.",
                "derivatives": [
                    {"word": "refundable", "partOfSpeech": "adj", "meaningVi": "có thể hoàn trả"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["a full refund: hoàn tiền toàn bộ", "provide a refund: hoàn lại tiền"],
                "needsReview": False
            },
            {
                "id": "refund-v",
                "word": "refund",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈfʌnd/", "us": "/rɪˈfʌnd/"},
                "frequency": 3,
                "meaningVi": "hoàn tiền, trả lại tiền",
                "exampleEn": "The store will refund the purchase price if you have a valid receipt.",
                "exampleVi": "Cửa hàng sẽ hoàn lại tiền mua nếu bạn có hóa đơn hợp lệ.",
                "derivatives": [],
                "synonyms": ["reimburse", "pay back"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "subscriber",
                "word": "subscriber",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/səbˈskraɪbə(r)/", "us": "/səbˈskraɪbər/"},
                "frequency": 3,
                "meaningVi": "người đăng ký, người theo dõi, người đặt mua dài hạn",
                "exampleEn": "The website now has millions of subscribers.",
                "exampleVi": "Trang web này hiện có hàng triệu người theo dõi.",
                "derivatives": [
                    {"word": "subscribe", "partOfSpeech": "v", "meaningVi": "đăng ký, mua dài hạn"},
                    {"word": "subscription", "partOfSpeech": "n", "meaningVi": "sự mua định kỳ"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "delivery",
                "word": "delivery",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈlɪvəri/", "us": "/dɪˈlɪvəri/"},
                "frequency": 3,
                "meaningVi": "sự giao hàng, sự phân phát",
                "exampleEn": "We guarantee delivery within three days.",
                "exampleVi": "Chúng tôi cam đoan sẽ giao hàng trong vòng ba ngày.",
                "derivatives": [
                    {"word": "deliver", "partOfSpeech": "v", "meaningVi": "giao hàng"}
                ],
                "synonyms": ["shipment"],
                "antonyms": [],
                "toeicNotes": ["express delivery: giao hàng hỏa tốc"],
                "needsReview": False
            },
            {
                "id": "price-n",
                "word": "price",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/praɪs/", "us": "/praɪs/"},
                "frequency": 3,
                "meaningVi": "giá, giá cả",
                "exampleEn": "The new color printer has a retail price of only $150.99.",
                "exampleVi": "Chiếc máy in màu mới có giá bán lẻ là 150,99 đô-la.",
                "derivatives": [
                    {"word": "pricey", "partOfSpeech": "adj", "meaningVi": "đắt đỏ"}
                ],
                "synonyms": ["cost", "rate"],
                "antonyms": [],
                "toeicNotes": ["a reduced price: giá đã giảm", "retail price: giá bán lẻ", "wholesale price: giá bán sỉ"],
                "needsReview": False
            },
            {
                "id": "price-v",
                "word": "price",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/praɪs/", "us": "/praɪs/"},
                "frequency": 3,
                "meaningVi": "định giá, đặt giá",
                "exampleEn": "The merchandise was priced reasonably to attract customers.",
                "exampleVi": "Hàng hóa được định giá hợp lý để thu hút khách hàng.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "receipt",
                "word": "receipt",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈsiːt/", "us": "/rɪˈsiːt/"},
                "frequency": 3,
                "meaningVi": "biên lai, hóa đơn",
                "exampleEn": "The original receipt is required for all refunds.",
                "exampleVi": "Mọi khoản hoàn lại đều cần phải có biên lai gốc.",
                "derivatives": [
                    {"word": "receive", "partOfSpeech": "v", "meaningVi": "nhận"}
                ],
                "synonyms": ["proof of purchase"],
                "antonyms": [],
                "toeicNotes": ["original/valid receipt: biên lai gốc/hợp lệ"],
                "needsReview": False
            },
            {
                "id": "offer-v",
                "word": "offer",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɒfə(r)/", "us": "/ˈɔːfər/"},
                "frequency": 3,
                "meaningVi": "cung cấp, tạo cơ hội, tặng",
                "exampleEn": "Z-Mart offers $25 gift cards to customers signing up for membership.",
                "exampleVi": "Z-Mart tặng thẻ quà tặng trị giá 25 đô-la cho những khách hàng đăng ký làm hội viên.",
                "derivatives": [],
                "synonyms": ["provide", "present"],
                "antonyms": [],
                "toeicNotes": ["offer A B / offer B to A: cung cấp B cho A"],
                "needsReview": False
            },
            {
                "id": "offer-n",
                "word": "offer",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈɒfə(r)/", "us": "/ˈɔːfər/"},
                "frequency": 3,
                "meaningVi": "lời đề nghị, đề xuất, ưu đãi",
                "exampleEn": "The supermarket entices customers with promotional offers.",
                "exampleVi": "Siêu thị thu hút khách hàng bằng các ưu đãi khuyến mại.",
                "derivatives": [],
                "synonyms": ["proposal", "discount"],
                "antonyms": [],
                "toeicNotes": ["promotional offer: ưu đãi khuyến mại", "job offer: lời mời làm việc"],
                "needsReview": False
            },
            {
                "id": "carefully",
                "word": "carefully",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈkeəfəli/", "us": "/ˈkerfəli/"},
                "frequency": 2,
                "meaningVi": "một cách cẩn thận, thận trọng",
                "exampleEn": "Please follow the installation directions carefully.",
                "exampleVi": "Vui lòng làm theo hướng dẫn cài đặt một cách cẩn thận.",
                "derivatives": [
                    {"word": "care", "partOfSpeech": "n/v", "meaningVi": "sự chăm sóc/quan tâm"},
                    {"word": "careful", "partOfSpeech": "adj", "meaningVi": "cẩn thận"}
                ],
                "synonyms": ["cautiously"],
                "antonyms": ["carelessly"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "benefit-n",
                "word": "benefit",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈbenɪfɪt/", "us": "/ˈbenɪfɪt/"},
                "frequency": 3,
                "meaningVi": "lợi ích, tác dụng, ưu đãi",
                "exampleEn": "The Shoppers' Club offers many benefits to its members.",
                "exampleVi": "Shoppers Club cung cấp nhiều ưu đãi cho các hội viên.",
                "derivatives": [
                    {"word": "beneficial", "partOfSpeech": "adj", "meaningVi": "có lợi"},
                    {"word": "beneficiary", "partOfSpeech": "n", "meaningVi": "người thụ hưởng"}
                ],
                "synonyms": ["advantage"],
                "antonyms": ["disadvantage", "drawback"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "benefit-v",
                "word": "benefit",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈbenɪfɪt/", "us": "/ˈbenɪfɪt/"},
                "frequency": 3,
                "meaningVi": "được hưởng lợi, giúp ích cho",
                "exampleEn": "NBC Mart shoppers benefit from various coupons and free delivery service.",
                "exampleVi": "Người mua hàng tại NBC Mart được hưởng lợi từ các phiếu giảm giá và dịch vụ giao hàng miễn phí.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["benefit from: hưởng lợi từ"],
                "needsReview": False
            },
            {
                "id": "exclusively",
                "word": "exclusively",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ɪkˈskluːsɪvli/", "us": "/ɪkˈskluːsɪvli/"},
                "frequency": 2,
                "meaningVi": "dành riêng, độc quyền",
                "exampleEn": "A 10 percent discount is available exclusively to Premium Club members.",
                "exampleVi": "Mức giảm giá 10% chỉ dành cho hội viên của Premium Club.",
                "derivatives": [
                    {"word": "exclusive", "partOfSpeech": "adj", "meaningVi": "dành riêng, độc quyền"},
                    {"word": "exclude", "partOfSpeech": "v", "meaningVi": "loại trừ"}
                ],
                "synonyms": ["solely", "only"],
                "antonyms": [],
                "toeicNotes": ["available exclusively online: chỉ có trên mạng", "sell exclusively: bán độc quyền"],
                "needsReview": False
            },
            {
                "id": "description",
                "word": "description",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈskrɪpʃn/", "us": "/dɪˈskrɪpʃn/"},
                "frequency": 3,
                "meaningVi": "sự miêu tả, sự mô tả",
                "exampleEn": "Call customer service for a more extensive description of any of the equipment.",
                "exampleVi": "Hãy gọi tới dịch vụ khách hàng để có thêm mô tả chi tiết về các thiết bị.",
                "derivatives": [
                    {"word": "describe", "partOfSpeech": "v", "meaningVi": "mô tả, miêu tả"}
                ],
                "synonyms": ["account", "explanation"],
                "antonyms": [],
                "toeicNotes": ["job description: bản mô tả công việc"],
                "needsReview": False
            },
            {
                "id": "relatively",
                "word": "relatively",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈrelətɪvli/", "us": "/ˈrelətɪvli/"},
                "frequency": 3,
                "meaningVi": "tương đối, vừa phải, có liên quan",
                "exampleEn": "McCoy's has a relatively lenient return policy compared to similar stores.",
                "exampleVi": "McCoy's có chính sách hoàn trả tương đối thoải mái so với các cửa hàng khác.",
                "derivatives": [
                    {"word": "relative", "partOfSpeech": "adj", "meaningVi": "tương đối, có liên quan"},
                    {"word": "relate", "partOfSpeech": "v", "meaningVi": "liên quan"}
                ],
                "synonyms": ["comparatively", "moderately"],
                "antonyms": [],
                "toeicNotes": ["relatively lenient/low: tương đối nới lỏng/thấp"],
                "needsReview": False
            },
            {
                "id": "spare-v",
                "word": "spare",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/speə(r)/", "us": "/sper/"},
                "frequency": 2,
                "meaningVi": "để dành, miễn cho, không tiếc",
                "exampleEn": "The shopping mall spared no expense on the 10th anniversary promotion.",
                "exampleVi": "Trung tâm mua sắm đã không tiếc chi phí cho chương trình khuyến mãi kỷ niệm 10 năm thành lập.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["spare no expense: không tiếc chi phí"],
                "needsReview": False
            },
            {
                "id": "spare-adj",
                "word": "spare",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/speə(r)/", "us": "/sper/"},
                "frequency": 2,
                "meaningVi": "dự trữ, dự phòng, rảnh rỗi",
                "exampleEn": "Customers may order spare parts at the service counter.",
                "exampleVi": "Khách hàng có thể đặt mua phụ tùng dự phòng tại quầy dịch vụ.",
                "derivatives": [],
                "synonyms": ["extra", "reserve"],
                "antonyms": [],
                "toeicNotes": ["spare parts: phụ tùng thay thế/dự phòng"],
                "needsReview": False
            },
            {
                "id": "preparation",
                "word": "preparation",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌprepəˈreɪʃn/", "us": "/ˌprepəˈreɪʃn/"},
                "frequency": 2,
                "meaningVi": "sự chuẩn bị, khâu chuẩn bị",
                "exampleEn": "Preparations are under way for the department store's grand opening.",
                "exampleVi": "Khâu chuẩn bị cho buổi khai trương khu mua sắm đang được tiến hành.",
                "derivatives": [
                    {"word": "prepare", "partOfSpeech": "v", "meaningVi": "chuẩn bị"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["preparations are under way: công tác chuẩn bị đang tiến hành"],
                "needsReview": False
            },
            {
                "id": "area",
                "word": "area",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈeəriə/", "us": "/ˈeriə/"},
                "frequency": 3,
                "meaningVi": "khu vực, vùng, lĩnh vực",
                "exampleEn": "There are excellent retail stores in this area.",
                "exampleVi": "Có những cửa hàng bán lẻ rất tốt trong khu vực này.",
                "derivatives": [],
                "synonyms": ["region", "zone"],
                "antonyms": [],
                "toeicNotes": ["Phân biệt: area (vùng/khu vực của thành phố, quốc gia) và site (bãi đất, địa điểm xây dựng/dùng cho mục đích cụ thể)"],
                "needsReview": False
            },
            {
                "id": "clearance",
                "word": "clearance",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈklɪərəns/", "us": "/ˈklɪrəns/"},
                "frequency": 3,
                "meaningVi": "sự dọn sạch, sự xả hàng kho, sự cấp phép",
                "exampleEn": "There is usually a clearance sale for winter clothes in March.",
                "exampleVi": "Vào tháng Ba thường có chương trình xả hàng dọn kho quần áo mùa đông.",
                "derivatives": [
                    {"word": "clear", "partOfSpeech": "v/adj", "meaningVi": "dọn dẹp/rõ ràng"}
                ],
                "synonyms": ["authorization"],
                "antonyms": [],
                "toeicNotes": ["clearance sale: bán xả hàng toàn bộ/dọn kho"],
                "needsReview": False
            },
            {
                "id": "alter",
                "word": "alter",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɔːltə(r)/", "us": "/ˈɔːltər/"},
                "frequency": 3,
                "meaningVi": "thay đổi, điều chỉnh, sửa đổi",
                "exampleEn": "The customer asked that the length of his pants be altered.",
                "exampleVi": "Vị khách đã yêu cầu điều chỉnh chiều dài chiếc quần.",
                "derivatives": [
                    {"word": "alteration", "partOfSpeech": "n", "meaningVi": "sự thay đổi, điều chỉnh"}
                ],
                "synonyms": ["change", "modify", "adjust"],
                "antonyms": ["preserve"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "apply",
                "word": "apply",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈplaɪ/", "us": "/əˈplaɪ/"},
                "frequency": 2,
                "meaningVi": "nộp đơn, ứng tuyển, áp dụng",
                "exampleEn": "The cashier applied the discount to all the items.",
                "exampleVi": "Nhân viên thu ngân đã áp dụng mức giảm giá cho tất cả sản phẩm.",
                "derivatives": [
                    {"word": "application", "partOfSpeech": "n", "meaningVi": "đơn xin, sự áp dụng"},
                    {"word": "applicant", "partOfSpeech": "n", "meaningVi": "ứng viên"},
                    {"word": "applicable", "partOfSpeech": "adj", "meaningVi": "có thể áp dụng"}
                ],
                "synonyms": ["put into effect", "put to use"],
                "antonyms": [],
                "toeicNotes": ["apply for: nộp đơn xin việc/vị trí", "apply A to B: áp dụng A vào B"],
                "needsReview": False
            },
            {
                "id": "mutually",
                "word": "mutually",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈmjuːtʃuəli/", "us": "/ˈmjuːtʃuəli/"},
                "frequency": 2,
                "meaningVi": "lẫn nhau, qua lại, với nhau",
                "exampleEn": "The couple and dealer reached a mutually agreeable price for the car.",
                "exampleVi": "Cặp vợ chồng và người bán hàng đã thống nhất được một mức giá xe hợp lý với cả hai bên.",
                "derivatives": [
                    {"word": "mutual", "partOfSpeech": "adj", "meaningVi": "lẫn nhau, chung"}
                ],
                "synonyms": ["reciprocally"],
                "antonyms": [],
                "toeicNotes": ["mutually agreeable/beneficial: thỏa thuận/có lợi cho cả hai bên"],
                "needsReview": False
            },
            {
                "id": "method",
                "word": "method",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈmeθəd/", "us": "/ˈmeθəd/"},
                "frequency": 3,
                "meaningVi": "phương pháp, cách thức",
                "exampleEn": "In recent years, debit cards have become a popular method of payment.",
                "exampleVi": "Trong những năm gần đây, thẻ ghi nợ đã trở thành một phương thức thanh toán phổ biến.",
                "derivatives": [
                    {"word": "methodical", "partOfSpeech": "adj", "meaningVi": "có phương pháp, ngăn nắp"}
                ],
                "synonyms": ["approach", "manner", "way"],
                "antonyms": [],
                "toeicNotes": ["method of payment: phương thức thanh toán"],
                "needsReview": False
            },
            {
                "id": "acceptable",
                "word": "acceptable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/əkˈseptəbl/", "us": "/əkˈseptəbl/"},
                "frequency": 2,
                "meaningVi": "có thể chấp nhận được, tạm được, ổn",
                "exampleEn": "Jenson Fashions sells clothes that are acceptable as business attire.",
                "exampleVi": "Jenson Fashions bán những bộ đồ phù hợp với trang phục công sở.",
                "derivatives": [
                    {"word": "accept", "partOfSpeech": "v", "meaningVi": "chấp nhận"},
                    {"word": "acceptance", "partOfSpeech": "n", "meaningVi": "sự chấp nhận"}
                ],
                "synonyms": ["satisfactory", "fine"],
                "antonyms": ["unacceptable"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "desire-n",
                "word": "desire",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈzaɪə(r)/", "us": "/dɪˈzaɪər/"},
                "frequency": 2,
                "meaningVi": "niềm mong muốn, khát khao",
                "exampleEn": "Effective advertising can create a desire in consumers to buy goods they do not need.",
                "exampleVi": "Quảng cáo hiệu quả có thể khiến người tiêu dùng hình thành mong muốn mua những sản phẩm mà họ không cần.",
                "derivatives": [
                    {"word": "desirable", "partOfSpeech": "adj", "meaningVi": "đáng khao khát"},
                    {"word": "undesirable", "partOfSpeech": "adj", "meaningVi": "không mong muốn"}
                ],
                "synonyms": ["wish", "want"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "desire-v",
                "word": "desire",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/dɪˈzaɪə(r)/", "us": "/dɪˈzaɪər/"},
                "frequency": 2,
                "meaningVi": "ao ước, mơ ước, thèm muốn",
                "exampleEn": "Many people desire the latest electronic devices.",
                "exampleVi": "Nhiều người ao ước được sở hữu những thiết bị điện tử mới nhất.",
                "derivatives": [],
                "synonyms": ["wish", "crave"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "redeemable",
                "word": "redeemable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/rɪˈdiːməbl/", "us": "/rɪˈdiːməbl/"},
                "frequency": 2,
                "meaningVi": "có thể quy đổi, có thể chuộc lại",
                "exampleEn": "Store gift vouchers are redeemable at any branch.",
                "exampleVi": "Phiếu mua hàng của cửa hàng có thể quy đổi được tại bất cứ chi nhánh nào.",
                "derivatives": [
                    {"word": "redeem", "partOfSpeech": "v", "meaningVi": "chuộc lại, quy đổi"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["redeemable at: có thể quy đổi/sử dụng tại"],
                "needsReview": False
            },
            {
                "id": "officially",
                "word": "officially",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/əˈfɪʃəli/", "us": "/əˈfɪʃəli/"},
                "frequency": 2,
                "meaningVi": "chính thức, trịnh trọng",
                "exampleEn": "The online store will officially open next month.",
                "exampleVi": "Cửa hàng trực tuyến sẽ chính thức mở vào tháng tới.",
                "derivatives": [
                    {"word": "official", "partOfSpeech": "adj/n", "meaningVi": "chính thức/quan chức"}
                ],
                "synonyms": ["formally"],
                "antonyms": ["unofficially"],
                "toeicNotes": ["officially open: chính thức mở cửa/khai trương"],
                "needsReview": False
            },
            {
                "id": "consumption",
                "word": "consumption",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kənˈsʌmpʃn/", "us": "/kənˈsʌmpʃn/"},
                "frequency": 2,
                "meaningVi": "sự tiêu thụ, sự tiêu dùng",
                "exampleEn": "Consumption of high-end products like home theaters has increased recently.",
                "exampleVi": "Việc tiêu dùng các sản phẩm cao cấp như rạp chiếu phim tại gia ngày càng tăng trong thời gian gần đây.",
                "derivatives": [
                    {"word": "consume", "partOfSpeech": "v", "meaningVi": "tiêu thụ"},
                    {"word": "consumer", "partOfSpeech": "n", "meaningVi": "người tiêu dùng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "qualify",
                "word": "qualify",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈkwɒlɪfaɪ/", "us": "/ˈkwɑːlɪfaɪ/"},
                "frequency": 2,
                "meaningVi": "đủ điều kiện, đủ khả năng, cấp chứng chỉ",
                "exampleEn": "Clients need a regular income to qualify for credit cards.",
                "exampleVi": "Để đủ điều kiện làm thẻ tín dụng, khách hàng cần có thu nhập ổn định.",
                "derivatives": [
                    {"word": "qualification", "partOfSpeech": "n", "meaningVi": "bằng cấp, năng lực"},
                    {"word": "qualified", "partOfSpeech": "adj", "meaningVi": "đủ trình độ, đủ điều kiện"}
                ],
                "synonyms": [],
                "antonyms": ["disqualify"],
                "toeicNotes": ["qualify for: đủ điều kiện cho/làm cái gì"],
                "needsReview": False
            },
            {
                "id": "fabric",
                "word": "fabric",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈfæbrɪk/", "us": "/ˈfæbrɪk/"},
                "frequency": 2,
                "meaningVi": "vải, chất liệu vải",
                "exampleEn": "The manufacturer's garments are made of natural fabric only.",
                "exampleVi": "Các sản phẩm may mặc của nhà sản xuất này đều chỉ được làm từ vải tự nhiên.",
                "derivatives": [],
                "synonyms": ["cloth", "material"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "valid",
                "word": "valid",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈvælɪd/", "us": "/ˈvælɪd/"},
                "frequency": 2,
                "meaningVi": "có hiệu lực, hợp lệ",
                "exampleEn": "A valid receipt must be presented.",
                "exampleVi": "Cần phải xuất trình hóa đơn hợp lệ.",
                "derivatives": [
                    {"word": "validate", "partOfSpeech": "v", "meaningVi": "xác nhận hiệu lực"},
                    {"word": "validity", "partOfSpeech": "n", "meaningVi": "giá trị pháp lý, hiệu lực"}
                ],
                "synonyms": ["effective", "good", "legitimate"],
                "antonyms": ["invalid"],
                "toeicNotes": ["be valid for + time: có hiệu lực trong khoảng thời gian", "valid receipt: hóa đơn hợp lệ"],
                "needsReview": False
            },
            {
                "id": "vendor",
                "word": "vendor",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈvendə(r)/", "us": "/ˈvendər/"},
                "frequency": 2,
                "meaningVi": "người bán hàng, đại lý cung cấp, máy bán hàng",
                "exampleEn": "Software vendors have been instructed to sell the product at a specific retail price.",
                "exampleVi": "Các nhà cung cấp phần mềm đã được hướng dẫn bán sản phẩm với giá bán lẻ cụ thể.",
                "derivatives": [],
                "synonyms": ["seller", "supplier"],
                "antonyms": ["buyer", "customer"],
                "toeicNotes": [],
                "needsReview": False
            }
        ]

    if day_num == 11:
        words_data = [
            {
                "id": "research-n",
                "word": "research",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈsɜːtʃ/", "us": "/ˈriːsɜːrtʃ/"},
                "frequency": 3,
                "meaningVi": "sự nghiên cứu, cuộc điều tra",
                "exampleEn": "The company started a research program into developing GPS technology.",
                "exampleVi": "Công ty đã bắt đầu một chương trình nghiên cứu về việc phát triển hệ thống định vị toàn cầu (GPS).",
                "derivatives": [
                    {"word": "researcher", "partOfSpeech": "n", "meaningVi": "nhà nghiên cứu"}
                ],
                "synonyms": ["study", "investigation"],
                "antonyms": [],
                "toeicNotes": ["research on: nghiên cứu về"],
                "needsReview": False
            },
            {
                "id": "research-v",
                "word": "research",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/rɪˈsɜːtʃ/", "us": "/ˈriːsɜːrtʃ/"},
                "frequency": 3,
                "meaningVi": "nghiên cứu, điều tra",
                "exampleEn": "Scientists are researching new energy sources.",
                "exampleVi": "Các nhà khoa học đang nghiên cứu các nguồn năng lượng mới.",
                "derivatives": [],
                "synonyms": ["investigate"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "devise",
                "word": "devise",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/dɪˈvaɪz/", "us": "/dɪˈvaɪz/"},
                "frequency": 2,
                "meaningVi": "phát minh, chế tạo, nghĩ ra",
                "exampleEn": "The firm devised a more efficient network system.",
                "exampleVi": "Công ty đã tạo ra một hệ thống mạng lưới hiệu quả hơn.",
                "derivatives": [
                    {"word": "device", "partOfSpeech": "n", "meaningVi": "thiết bị"}
                ],
                "synonyms": ["contrive", "invent", "create"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "revolutionary",
                "word": "revolutionary",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˌrevəˈluːʃənəri/", "us": "/ˌrevəˈluːʃəneri/"},
                "frequency": 2,
                "meaningVi": "mang tính cách mạng, cải cách",
                "exampleEn": "The car's revolutionary new engine surpasses those of the competition.",
                "exampleVi": "Động cơ mới mang tính cách mạng của chiếc xe này vượt trội hơn các loại xe khác trong cuộc đua.",
                "derivatives": [
                    {"word": "revolution", "partOfSpeech": "n", "meaningVi": "cuộc cách mạng"}
                ],
                "synonyms": ["groundbreaking"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "innovative",
                "word": "innovative",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈɪnəveɪtɪv/", "us": "/ˈɪnəveɪtɪv/"},
                "frequency": 2,
                "meaningVi": "tân tiến, đổi mới, sáng tạo",
                "exampleEn": "Simpson & Associates provides clients with innovative solutions to their needs.",
                "exampleVi": "Simpsons & Associates cung cấp cho khách hàng những giải pháp tân tiến nhất phù hợp với nhu cầu của họ.",
                "derivatives": [
                    {"word": "innovate", "partOfSpeech": "v", "meaningVi": "đổi mới, cách tân"},
                    {"word": "innovation", "partOfSpeech": "n", "meaningVi": "sự đổi mới, sự cách tân"}
                ],
                "synonyms": ["inventive", "cutting-edge"],
                "antonyms": ["unimaginative"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "feature-n",
                "word": "feature",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈfiːtʃə(r)/", "us": "/ˈfiːtʃər/"},
                "frequency": 3,
                "meaningVi": "đặc điểm, tính năng",
                "exampleEn": "The latest dryer has several new features.",
                "exampleVi": "Chiếc máy sấy mới nhất có một vài tính năng mới.",
                "derivatives": [],
                "synonyms": ["characteristic", "attribute"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "feature-v",
                "word": "feature",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈfiːtʃə(r)/", "us": "/ˈfiːtʃər/"},
                "frequency": 3,
                "meaningVi": "có tính năng, có đặc trưng, có mặt (sản phẩm)",
                "exampleEn": "This refrigerator model features high energy efficiency.",
                "exampleVi": "Mẫu tủ lạnh này có tính năng cực kỳ tiết kiệm năng lượng.",
                "derivatives": [],
                "synonyms": ["highlight", "include"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "inspiration",
                "word": "inspiration",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌɪnspəˈreɪʃn/", "us": "/ˌɪnspəˈreɪʃn/"},
                "frequency": 2,
                "meaningVi": "cảm hứng, nguồn cảm hứng",
                "exampleEn": "The new fashion designer draws her inspiration from traditional attire.",
                "exampleVi": "Nhà thiết kế thời trang mới đã lấy cảm hứng từ các trang phục truyền thống.",
                "derivatives": [
                    {"word": "inspire", "partOfSpeech": "v", "meaningVi": "truyền cảm hứng"},
                    {"word": "inspirational", "partOfSpeech": "adj", "meaningVi": "gây cảm hứng"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["draw inspiration from: lấy cảm hứng từ"],
                "needsReview": False
            },
            {
                "id": "sufficiently",
                "word": "sufficiently",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/səˈfɪʃntli/", "us": "/səˈfɪʃntli/"},
                "frequency": 2,
                "meaningVi": "đủ, đầy đủ, thỏa đáng",
                "exampleEn": "The containers are sufficiently strong to resist breakage.",
                "exampleVi": "Các thùng chứa đủ chắc chắn để không bị vỡ.",
                "derivatives": [
                    {"word": "sufficient", "partOfSpeech": "adj", "meaningVi": "đầy đủ"},
                    {"word": "sufficiency", "partOfSpeech": "n", "meaningVi": "sự đầy đủ"}
                ],
                "synonyms": ["adequately", "enough"],
                "antonyms": ["insufficiently"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "patent-n",
                "word": "patent",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈpætnt/", "us": "/ˈpætnt/"},
                "frequency": 2,
                "meaningVi": "bằng sáng chế, giấy đăng ký sáng chế",
                "exampleEn": "The lawyers submitted the paperwork for a patent application.",
                "exampleVi": "Các luật sư đã trình giấy tờ để xin cấp bằng sáng chế.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["patent application: đơn xin cấp bằng sáng chế"],
                "needsReview": False
            },
            {
                "id": "patent-v",
                "word": "patent",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈpætnt/", "us": "/ˈpætnt/"},
                "frequency": 2,
                "meaningVi": "lấy bằng sáng chế, cấp bằng sáng chế",
                "exampleEn": "The company patented the new solar panel technology.",
                "exampleVi": "Công ty đã lấy bằng sáng chế cho công nghệ pin năng lượng mặt trời mới.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "envision",
                "word": "envision",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈvɪʒn/", "us": "/ɪnˈvɪʒn/"},
                "frequency": 2,
                "meaningVi": "hình dung, mường tượng",
                "exampleEn": "Management envisions its latest product being sold in stores across the country.",
                "exampleVi": "Ban lãnh đạo hình dung rằng sản phẩm mới nhất của họ sẽ được bày bán ở các cửa hàng trên cả nước.",
                "derivatives": [],
                "synonyms": ["imagine", "picture", "foresee"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "extend",
                "word": "extend",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪkˈstend/", "us": "/ɪkˈstend/"},
                "frequency": 3,
                "meaningVi": "mở rộng, kéo dài, gia hạn, giơ ra, bày tỏ",
                "exampleEn": "The CEO extended his thanks to the research team for their great work.",
                "exampleVi": "Vị giám đốc điều hành bày tỏ sự biết ơn đối với nhóm nghiên cứu vì đã làm việc rất tốt.",
                "derivatives": [
                    {"word": "extent", "partOfSpeech": "n", "meaningVi": "quy mô, phạm vi"},
                    {"word": "extension", "partOfSpeech": "n", "meaningVi": "sự gia hạn, mở rộng"},
                    {"word": "extensive", "partOfSpeech": "adj", "meaningVi": "rộng lớn"}
                ],
                "synonyms": ["lengthen", "offer", "expand"],
                "antonyms": ["shorten"],
                "toeicNotes": ["extend a deadline: gia hạn thời hạn", "extend thanks to: gửi lời cảm ơn tới"],
                "needsReview": False
            },
            {
                "id": "following",
                "word": "following",
                "partOfSpeech": "prep",
                "pronunciation": {"uk": "/ˈfɒləʊɪŋ/", "us": "/ˈfɑːləʊɪŋ/"},
                "frequency": 3,
                "meaningVi": "sau, tiếp theo",
                "exampleEn": "The software was launched following months of research.",
                "exampleVi": "Phần mềm này đã được ra mắt sau hàng tháng trời nghiên cứu.",
                "derivatives": [],
                "synonyms": ["after"],
                "antonyms": ["preceding"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "intend",
                "word": "intend",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈtend/", "us": "/ɪnˈtend/"},
                "frequency": 3,
                "meaningVi": "dự định, có ý định",
                "exampleEn": "Beauford Incorporated intends to release its new appliances this fall.",
                "exampleVi": "Tập đoàn Beauford dự định ra mắt thiết bị gia dụng mới vào mùa thu này.",
                "derivatives": [
                    {"word": "intention", "partOfSpeech": "n", "meaningVi": "mong muốn, ý định"},
                    {"word": "intent", "partOfSpeech": "n", "meaningVi": "ý định, mục đích"}
                ],
                "synonyms": ["plan", "aim"],
                "antonyms": [],
                "toeicNotes": ["intend to do: định làm gì"],
                "needsReview": False
            },
            {
                "id": "grant-v",
                "word": "grant",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɡrɑːnt/", "us": "/ɡrænt/"},
                "frequency": 3,
                "meaningVi": "ban, cấp, thừa nhận, công nhận",
                "exampleEn": "The patent for the handheld computer was granted on April 27.",
                "exampleVi": "Bằng sáng chế máy tính cầm tay đã được cấp vào ngày 27 tháng Tư.",
                "derivatives": [],
                "synonyms": ["allow", "award"],
                "antonyms": ["deny", "refuse"],
                "toeicNotes": ["take ~ for granted: coi điều gì là hiển nhiên"],
                "needsReview": False
            },
            {
                "id": "grant-n",
                "word": "grant",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɡrɑːnt/", "us": "/ɡrænt/"},
                "frequency": 3,
                "meaningVi": "sự ban cấp, tiền trợ cấp, khoản tài trợ",
                "exampleEn": "The research team will receive a government grant of up to $4,000.",
                "exampleVi": "Nhóm nghiên cứu sẽ được nhận một khoản trợ cấp chính phủ lên tới 4000 đô-la.",
                "derivatives": [],
                "synonyms": ["subsidy", "allowance"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "allow",
                "word": "allow",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈlaʊ/", "us": "/əˈlaʊ/"},
                "frequency": 3,
                "meaningVi": "cho phép, phê duyệt, chấp thuận",
                "exampleEn": "The program's new feature allows users to conduct advanced searches.",
                "exampleVi": "Tính năng mới của chương trình này cho phép người dùng thực hiện các tìm kiếm nâng cao.",
                "derivatives": [
                    {"word": "allowable", "partOfSpeech": "adj", "meaningVi": "có thể chấp nhận"},
                    {"word": "allowance", "partOfSpeech": "n", "meaningVi": "sự cho phép, tiền trợ cấp"}
                ],
                "synonyms": ["permit", "enable"],
                "antonyms": ["forbid", "prohibit"],
                "toeicNotes": ["allow sb to do: cho phép ai làm gì"],
                "needsReview": False
            },
            {
                "id": "inspect",
                "word": "inspect",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈspekt/", "us": "/ɪnˈspekt/"},
                "frequency": 2,
                "meaningVi": "kiểm tra, thanh tra, giám định",
                "exampleEn": "The head researcher inspects all equipments and chemicals in the laboratory daily to ensure safety.",
                "exampleVi": "Trưởng nhóm nghiên cứu phải kiểm tra toàn bộ thiết bị và hóa chất trong phòng thí nghiệm hằng ngày để đảm bảo an toàn.",
                "derivatives": [
                    {"word": "inspection", "partOfSpeech": "n", "meaningVi": "sự kiểm tra, thanh tra"},
                    {"word": "inspector", "partOfSpeech": "n", "meaningVi": "thanh tra viên"}
                ],
                "synonyms": ["examine", "check", "scrutinize"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "improve",
                "word": "improve",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪmˈpruːv/", "us": "/ɪmˈpruːv/"},
                "frequency": 2,
                "meaningVi": "cải thiện, cải tiến, nâng cao",
                "exampleEn": "A variety of incentives can improve staff productivity.",
                "exampleVi": "Việc khích lệ động viên với nhiều hình thức có thể cải thiện năng suất lao động của nhân viên.",
                "derivatives": [
                    {"word": "improvement", "partOfSpeech": "n", "meaningVi": "sự cải tiến, sự nâng cao"}
                ],
                "synonyms": ["upgrade", "enhance"],
                "antonyms": ["worsen", "impair"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "increasingly",
                "word": "increasingly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ɪnˈkriːsɪŋli/", "us": "/ɪnˈkriːsɪŋli/"},
                "frequency": 3,
                "meaningVi": "ngày càng tăng, gia tăng",
                "exampleEn": "Technology is becoming an increasingly important factor in the nation's economy.",
                "exampleVi": "Khoa học kỹ thuật đang trở thành một nhân tố ngày càng quan trọng trong nền kinh tế quốc gia.",
                "derivatives": [
                    {"word": "increase", "partOfSpeech": "v/n", "meaningVi": "tăng/sự tăng lên"},
                    {"word": "increasing", "partOfSpeech": "adj", "meaningVi": "ngày càng tăng"}
                ],
                "synonyms": ["progressively", "more and more"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "invest",
                "word": "invest",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪnˈvest/", "us": "/ɪnˈvest/"},
                "frequency": 2,
                "meaningVi": "đầu tư",
                "exampleEn": "Lamont Manufacturing invested millions of dollars in improving its assembly line.",
                "exampleVi": "Lamont Manufacturing đã đầu tư hàng triệu đô-la vào việc cải tiến dây chuyền lắp ráp.",
                "derivatives": [
                    {"word": "investment", "partOfSpeech": "n", "meaningVi": "sự đầu tư, khoản đầu tư"},
                    {"word": "investor", "partOfSpeech": "n", "meaningVi": "nhà đầu tư"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["invest in: đầu tư vào cái gì"],
                "needsReview": False
            },
            {
                "id": "various",
                "word": "various",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈveəriəs/", "us": "/ˈveriəs/"},
                "frequency": 3,
                "meaningVi": "nhiều, đa dạng, khác nhau",
                "exampleEn": "This car has various features not included in older models.",
                "exampleVi": "Chiếc xe hơi này có những tính năng đa dạng mà các mẫu xe cũ không có.",
                "derivatives": [
                    {"word": "vary", "partOfSpeech": "v", "meaningVi": "thay đổi, làm cho khác"},
                    {"word": "variety", "partOfSpeech": "n", "meaningVi": "sự đa dạng"}
                ],
                "synonyms": ["diverse", "assorted"],
                "antonyms": ["same", "similar"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "upgrade-n",
                "word": "upgrade",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈʌpɡreɪd/", "us": "/ˈʌpɡreɪd/"},
                "frequency": 3,
                "meaningVi": "sự nâng cấp, bản cải tiến",
                "exampleEn": "Special customers are eligible for one free computer upgrade.",
                "exampleVi": "Các khách hàng đặc biệt sẽ được hưởng một gói nâng cấp máy tính miễn phí.",
                "derivatives": [],
                "synonyms": ["improvement"],
                "antonyms": ["downgrade"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "upgrade-v",
                "word": "upgrade",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˌʌpˈɡreɪd/", "us": "/ˌʌpˈɡreɪd/"},
                "frequency": 3,
                "meaningVi": "nâng cấp, cải tiến",
                "exampleEn": "Gina just upgraded her cell phone software.",
                "exampleVi": "Gina vừa mới nâng cấp phần mềm điện thoại.",
                "derivatives": [],
                "synonyms": ["update", "enhance"],
                "antonyms": ["downgrade"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "manual-n",
                "word": "manual",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈmænjuəl/", "us": "/ˈmænjuəl/"},
                "frequency": 3,
                "meaningVi": "sách hướng dẫn, sổ tay hướng dẫn",
                "exampleEn": "Rachel is writing the product manual for the new air conditioner.",
                "exampleVi": "Rachel đang viết hướng dẫn sử dụng cho sản phẩm điều hòa mới.",
                "derivatives": [],
                "synonyms": ["handbook", "guide"],
                "antonyms": [],
                "toeicNotes": ["instruction manual: sách hướng dẫn sử dụng"],
                "needsReview": False
            },
            {
                "id": "manual-adj",
                "word": "manual",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈmænjuəl/", "us": "/ˈmænjuəl/"},
                "frequency": 3,
                "meaningVi": "(thuộc) tay, làm bằng tay, thủ công",
                "exampleEn": "The workers perform manual labor in the factory.",
                "exampleVi": "Công nhân làm công việc lao động thủ công trong nhà máy.",
                "derivatives": [],
                "synonyms": ["hand-operated"],
                "antonyms": ["automatic"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "explore",
                "word": "explore",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪkˈsplɔː(r)/", "us": "/ɪkˈsplɔːr/"},
                "frequency": 2,
                "meaningVi": "khám phá, tìm tòi, thăm dò",
                "exampleEn": "Clients seeking company information can explore our website.",
                "exampleVi": "Khách hàng muốn biết thêm thông tin về công ty có thể tìm hiểu trên trang web của chúng tôi.",
                "derivatives": [
                    {"word": "exploration", "partOfSpeech": "n", "meaningVi": "sự thăm dò, khám phá"},
                    {"word": "exploratory", "partOfSpeech": "adj", "meaningVi": "nhằm khám phá"}
                ],
                "synonyms": ["investigate", "examine"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "response",
                "word": "response",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/rɪˈspɒns/", "us": "/rɪˈspɑːns/"},
                "frequency": 3,
                "meaningVi": "sự phản hồi, câu trả lời, sự hưởng ứng",
                "exampleEn": "Those testing the new microwave are asked to submit written responses to some questions.",
                "exampleVi": "Những người dùng thử sản phẩm lò vi sóng mới được yêu cầu viết câu trả lời cho một số câu hỏi.",
                "derivatives": [
                    {"word": "respond", "partOfSpeech": "v", "meaningVi": "trả lời, phản hồi"}
                ],
                "synonyms": ["reply", "answer"],
                "antonyms": [],
                "toeicNotes": ["in response to: để đáp lại, phản hồi về"],
                "needsReview": False
            },
            {
                "id": "appearance",
                "word": "appearance",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˈpɪərəns/", "us": "/əˈpɪrəns/"},
                "frequency": 3,
                "meaningVi": "sự xuất hiện, diện mạo, vẻ ngoài",
                "exampleEn": "The design team completely modernized the product's appearance.",
                "exampleVi": "Nhóm thiết kế đã đổi mới hoàn toàn mẫu mã của sản phẩm.",
                "derivatives": [
                    {"word": "appear", "partOfSpeech": "v", "meaningVi": "xuất hiện, hình như"},
                    {"word": "apparently", "partOfSpeech": "adv", "meaningVi": "hiển nhiên, rõ ràng"}
                ],
                "synonyms": ["outlook", "look", "aspect"],
                "antonyms": ["disappearance"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "successful",
                "word": "successful",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/səkˈsesfl/", "us": "/səkˈsesfl/"},
                "frequency": 3,
                "meaningVi": "thành công, thành đạt",
                "exampleEn": "The floor lamps are the company's most successful product.",
                "exampleVi": "Đèn sàn là sản phẩm thành công nhất của công ty.",
                "derivatives": [
                    {"word": "succeed", "partOfSpeech": "v", "meaningVi": "thành công"},
                    {"word": "success", "partOfSpeech": "n", "meaningVi": "sự thành công"},
                    {"word": "successfully", "partOfSpeech": "adv", "meaningVi": "thành công"}
                ],
                "synonyms": ["prosperous", "effective"],
                "antonyms": ["unsuccessful", "failing"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "hold",
                "word": "hold",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/həʊld/", "us": "/həʊld/"},
                "frequency": 3,
                "meaningVi": "cầm, giữ, tổ chức, chứa được",
                "exampleEn": "The washing machine holds up to three kilograms of laundry.",
                "exampleVi": "Chiếc máy giặt này giặt được tới 3 kg quần áo.",
                "derivatives": [],
                "synonyms": ["contain", "conduct", "host"],
                "antonyms": [],
                "toeicNotes": ["hold a meeting/conference: tổ chức cuộc họp/hội nghị"],
                "needsReview": False
            },
            {
                "id": "advance-n",
                "word": "advance",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ədˈvɑːns/", "us": "/ədˈvæns/"},
                "frequency": 3,
                "meaningVi": "thành tựu, sự tiến bộ, sự phát triển",
                "exampleEn": "The product development team researches advances in computer technology.",
                "exampleVi": "Bộ phận cải tiến sản phẩm nghiên cứu những thành tựu trong công nghệ tin học.",
                "derivatives": [
                    {"word": "advancement", "partOfSpeech": "n", "meaningVi": "sự thăng tiến, sự cải tiến"},
                    {"word": "advanced", "partOfSpeech": "adj", "meaningVi": "tiên tiến, cao cấp"}
                ],
                "synonyms": ["breakthrough", "progress"],
                "antonyms": ["setback"],
                "toeicNotes": ["in advance: trước (thời gian)", "in advance of: trước ai/cái gì", "advance in: sự cải tiến về"],
                "needsReview": False
            },
            {
                "id": "advance-v",
                "word": "advance",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ədˈvɑːns/", "us": "/ədˈvæns/"},
                "frequency": 3,
                "meaningVi": "tiến lên, thúc đẩy, đề xuất",
                "exampleEn": "Medical technology has advanced rapidly over the past decade.",
                "exampleVi": "Công nghệ y tế đã tiến bộ nhanh chóng trong thập kỷ qua.",
                "derivatives": [],
                "synonyms": ["progress", "further"],
                "antonyms": ["recede"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "reliable",
                "word": "reliable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/rɪˈlaɪəbl/", "us": "/rɪˈlaɪəbl/"},
                "frequency": 3,
                "meaningVi": "đáng tin cậy",
                "exampleEn": "Tests indicate that Branco's products are reliable and efficient.",
                "exampleVi": "Các thử nghiệm đã chỉ ra rằng những sản phẩm của Branco rất đáng tin cậy và hiệu quả.",
                "derivatives": [
                    {"word": "rely", "partOfSpeech": "v", "meaningVi": "tin tưởng, nhờ cậy"},
                    {"word": "reliability", "partOfSpeech": "n", "meaningVi": "sự đáng tin, độ tin cậy"}
                ],
                "synonyms": ["trustworthy", "dependable"],
                "antonyms": ["unreliable"],
                "toeicNotes": ["Phân biệt: reliable (đáng tin cậy) và reliant (dựa vào, phụ thuộc vào)"],
                "needsReview": False
            },
            {
                "id": "quality",
                "word": "quality",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈkwɒləti/", "us": "/ˈkwɑːləti/"},
                "frequency": 3,
                "meaningVi": "chất lượng, phẩm chất",
                "exampleEn": "The quality control division inspects samples of all items.",
                "exampleVi": "Bộ phận kiểm soát chất lượng kiểm tra mẫu của toàn bộ sản phẩm.",
                "derivatives": [],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["quality control: kiểm soát chất lượng"],
                "needsReview": False
            },
            {
                "id": "domestic",
                "word": "domestic",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/dəˈmestɪk/", "us": "/dəˈmestɪk/"},
                "frequency": 2,
                "meaningVi": "trong nước, nội địa, (thuộc) gia đình",
                "exampleEn": "Slow sales in the domestic market forced companies to expand overseas.",
                "exampleVi": "Tốc độ bán chậm trong nước đã buộc các công ty phải mở rộng ra nước ngoài.",
                "derivatives": [
                    {"word": "domestically", "partOfSpeech": "adv", "meaningVi": "trong nước, nội địa"}
                ],
                "synonyms": ["internal", "national"],
                "antonyms": ["foreign", "international"],
                "toeicNotes": ["domestic market: thị trường trong nước"],
                "needsReview": False
            },
            {
                "id": "development",
                "word": "development",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈveləpmənt/", "us": "/dɪˈveləpmənt/"},
                "frequency": 3,
                "meaningVi": "sự phát triển, sự tiến triển",
                "exampleEn": "The project is in the final stage of development.",
                "exampleVi": "Dự án đang ở giai đoạn phát triển cuối cùng.",
                "derivatives": [
                    {"word": "develop", "partOfSpeech": "v", "meaningVi": "phát triển"},
                    {"word": "developer", "partOfSpeech": "n", "meaningVi": "người/nhà phát triển"},
                    {"word": "developing", "partOfSpeech": "adj", "meaningVi": "đang phát triển"}
                ],
                "synonyms": ["growth", "evolution"],
                "antonyms": [],
                "toeicNotes": ["be under development: đang được phát triển"],
                "needsReview": False
            },
            {
                "id": "availability",
                "word": "availability",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/əˌveɪləˈbɪləti/", "us": "/əˌveɪləˈbɪləti/"},
                "frequency": 2,
                "meaningVi": "sự có sẵn, sự sẵn sàng cung cấp",
                "exampleEn": "Availability of product depends on market demand and supply.",
                "exampleVi": "Sự có mặt của sản phẩm phụ thuộc vào cung và cầu của thị trường.",
                "derivatives": [
                    {"word": "available", "partOfSpeech": "adj", "meaningVi": "có sẵn, sẵn sàng"}
                ],
                "synonyms": [],
                "antonyms": ["unavailability"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "update-n",
                "word": "update",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈʌpdeɪt/", "us": "/ˈʌpdeɪt/"},
                "frequency": 3,
                "meaningVi": "sự cập nhật, bản nâng cấp",
                "exampleEn": "The website update includes information on the latest hair styling appliances.",
                "exampleVi": "Việc cập nhật trang web bao gồm cả thông tin về những thiết bị tạo mẫu tóc mới nhất.",
                "derivatives": [
                    {"word": "updated", "partOfSpeech": "adj", "meaningVi": "đã cập nhật"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "update-v",
                "word": "update",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˌʌpˈdeɪt/", "us": "/ˌʌpˈdeɪt/"},
                "frequency": 3,
                "meaningVi": "cập nhật, nâng cấp",
                "exampleEn": "The factory updated the software of its equipment to speed up production.",
                "exampleVi": "Nhà máy đã nâng cấp phần mềm của thiết bị để đẩy nhanh tốc độ sản xuất.",
                "derivatives": [],
                "synonyms": ["upgrade", "modernize"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "accurate",
                "word": "accurate",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈækjərət/", "us": "/ˈækjərət/"},
                "frequency": 3,
                "meaningVi": "đúng, chính xác, xác đáng",
                "exampleEn": "The new accounting software is accurate and precise.",
                "exampleVi": "Phần mềm kế toán mới rất đúng và chính xác.",
                "derivatives": [
                    {"word": "accuracy", "partOfSpeech": "n", "meaningVi": "độ chính xác"},
                    {"word": "accurately", "partOfSpeech": "adv", "meaningVi": "chính xác"}
                ],
                "synonyms": ["precise", "correct"],
                "antonyms": ["inaccurate"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "complicated",
                "word": "complicated",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈkɒmplɪkeɪtɪd/", "us": "/ˈkɑːmplɪkeɪtɪd/"},
                "frequency": 2,
                "meaningVi": "phức tạp, rắc rối",
                "exampleEn": "Project delays often create a complicated situation for the public relations department.",
                "exampleVi": "Việc trì hoãn dự án thường tạo ra tình huống rắc rối cho bộ phận quan hệ công chúng.",
                "derivatives": [
                    {"word": "complicate", "partOfSpeech": "v", "meaningVi": "làm rắc rối, làm phức tạp"}
                ],
                "synonyms": ["complex", "intricate"],
                "antonyms": ["simple", "straightforward"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "accomplished",
                "word": "accomplished",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/əˈkʌmplɪʃt/", "us": "/əˈkɑːmplɪʃt/"},
                "frequency": 2,
                "meaningVi": "hoàn hảo, tài năng, thành thạo",
                "exampleEn": "The accomplished chemist has been hired to develop a flexible battery.",
                "exampleVi": "Nhà hóa học tài năng đó đã được thuê để phát triển một loại pin dẻo.",
                "derivatives": [
                    {"word": "accomplish", "partOfSpeech": "v", "meaningVi": "hoàn thành, đạt được"},
                    {"word": "accomplishment", "partOfSpeech": "n", "meaningVi": "thành tựu, sự hoàn thành"}
                ],
                "synonyms": ["skilled", "talented", "proficient"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "inquiry",
                "word": "inquiry",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪnˈkwaɪəri/", "us": "/ˈɪnkwəri/"},
                "frequency": 2,
                "meaningVi": "câu hỏi giải đáp, sự điều tra, thắc mắc",
                "exampleEn": "Please call our customer representatives for service inquiries.",
                "exampleVi": "Vui lòng liên hệ nhân viên chăm sóc khách hàng để được giải đáp các câu hỏi về dịch vụ.",
                "derivatives": [
                    {"word": "inquire", "partOfSpeech": "v", "meaningVi": "hỏi, điều tra"}
                ],
                "synonyms": ["question", "query"],
                "antonyms": [],
                "toeicNotes": ["service inquiries: thắc mắc về dịch vụ"],
                "needsReview": False
            },
            {
                "id": "indication",
                "word": "indication",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌɪndɪˈkeɪʃn/", "us": "/ˌɪndɪˈkeɪʃn/"},
                "frequency": 2,
                "meaningVi": "biểu hiện, dấu hiệu, sự chỉ dẫn",
                "exampleEn": "Uneven printing is an indication of a technical fault.",
                "exampleVi": "In không đều màu là một dấu hiệu của lỗi kỹ thuật.",
                "derivatives": [
                    {"word": "indicate", "partOfSpeech": "v", "meaningVi": "chỉ ra, biểu thị"},
                    {"word": "indicative", "partOfSpeech": "adj", "meaningVi": "tỏ ra"}
                ],
                "synonyms": ["sign", "symptom", "mark"],
                "antonyms": [],
                "toeicNotes": ["indication of: dấu hiệu của"],
                "needsReview": False
            },
            {
                "id": "manufacturer",
                "word": "manufacturer",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌmænjuˈfæktʃərə(r)/", "us": "/ˌmænjuˈfæktʃərər/"},
                "frequency": 2,
                "meaningVi": "nhà sản xuất, chủ xí nghiệp",
                "exampleEn": "The manufacturer guarantees all its products for up to one year.",
                "exampleVi": "Nhà sản xuất bảo hành toàn bộ sản phẩm của họ lên tới một năm.",
                "derivatives": [
                    {"word": "manufacture", "partOfSpeech": "v/n", "meaningVi": "sản xuất/sự sản xuất"}
                ],
                "synonyms": ["maker", "producer"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "compatible",
                "word": "compatible",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/kəmˈpætəbl/", "us": "/kəmˈpætəbl/"},
                "frequency": 2,
                "meaningVi": "tương thích, thích hợp",
                "exampleEn": "The remote control is compatible with all models.",
                "exampleVi": "Chiếc điều khiển từ xa này tương thích với mọi mẫu sản phẩm.",
                "derivatives": [
                    {"word": "compatibility", "partOfSpeech": "n", "meaningVi": "tính tương thích"}
                ],
                "synonyms": ["matching", "harmonious"],
                "antonyms": ["incompatible"],
                "toeicNotes": ["be compatible with: tương thích với"],
                "needsReview": False
            },
            {
                "id": "superior",
                "word": "superior",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/suːˈpɪəriə(r)/", "us": "/suːˈpɪriər/"},
                "frequency": 2,
                "meaningVi": "cao cấp hơn, vượt trội, tốt hơn",
                "exampleEn": "The company's latest television is superior to those on the market today.",
                "exampleVi": "Chiếc tivi mới nhất của công ty cao cấp hơn các sản phẩm tivi hiện có trên thị trường.",
                "derivatives": [
                    {"word": "superiority", "partOfSpeech": "n", "meaningVi": "sự vượt trội, ưu việt"}
                ],
                "synonyms": ["excellent", "better"],
                "antonyms": ["inferior"],
                "toeicNotes": ["be superior to: tốt hơn/vượt trội hơn cái gì"],
                "needsReview": False
            },
            {
                "id": "absolute",
                "word": "absolute",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈæbsəluːt/", "us": "/ˈæbsəluːt/"},
                "frequency": 2,
                "meaningVi": "tuyệt đối, hoàn toàn, thuần túy",
                "exampleEn": "The latest technology keeps production costs to an absolute minimum.",
                "exampleVi": "Công nghệ tiên tiến giúp giảm chi phí sản xuất xuống mức thấp nhất.",
                "derivatives": [
                    {"word": "absolutely", "partOfSpeech": "adv", "meaningVi": "hoàn toàn, tuyệt đối"}
                ],
                "synonyms": ["complete", "total", "utter"],
                "antonyms": ["relative", "partial"],
                "toeicNotes": ["to an absolute minimum: xuống mức tối thiểu"],
                "needsReview": False
            },
            {
                "id": "broaden",
                "word": "broaden",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈbrɔːdn/", "us": "/ˈbrɔːdn/"},
                "frequency": 2,
                "meaningVi": "mở rộng",
                "exampleEn": "The new CEO is broadening the scope of the company's research.",
                "exampleVi": "Vị giám đốc điều hành mới đang mở rộng phạm vi nghiên cứu của công ty.",
                "derivatives": [
                    {"word": "broad", "partOfSpeech": "adj", "meaningVi": "rộng"},
                    {"word": "breadth", "partOfSpeech": "n", "meaningVi": "bề rộng"}
                ],
                "synonyms": ["widen", "expand"],
                "antonyms": ["narrow"],
                "toeicNotes": ["broaden the scope: mở rộng phạm vi"],
                "needsReview": False
            },
            {
                "id": "corrosion",
                "word": "corrosion",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kəˈrəʊʒn/", "us": "/kəˈrəʊʒn/"},
                "frequency": 2,
                "meaningVi": "sự ăn mòn (kim loại), gỉ sét",
                "exampleEn": "This steel roof is designed to be resistant to corrosion from the weather.",
                "exampleVi": "Loại mái tôn này được thiết kế để không bị ăn mòn do thời tiết.",
                "derivatives": [
                    {"word": "corrode", "partOfSpeech": "v", "meaningVi": "ăn mòn, bào mòn"}
                ],
                "synonyms": ["rust", "decay"],
                "antonyms": [],
                "toeicNotes": ["resistant to corrosion: chống ăn mòn"],
                "needsReview": False
            }
        ]












    # Generate Quiz questions (Fill-in-the-blank)
    quiz_questions = []
    eligible_quiz_words = [w for w in words_data if w["exampleEn"] and w["word"] in w["exampleEn"].lower()]
    
    if len(eligible_quiz_words) >= 4:
        for qw in eligible_quiz_words[:10]:
            pattern_word = re.compile(re.escape(qw["word"]), re.IGNORECASE)
            masked_sentence = pattern_word.sub("___", qw["exampleEn"])
            
            correct_opt = qw["word"]
            other_words = [w["word"] for w in words_data if w["word"] != correct_opt]
            opts = [correct_opt] + random.sample(other_words, min(3, len(other_words)))
            random.shuffle(opts)
            
            quiz_questions.append({
                "q": masked_sentence,
                "a": correct_opt,
                "options": opts
            })

    if day_num == 12:
        words_data = [
            {
                "id": "equipment",
                "word": "equipment",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪˈkwɪpmənt/", "us": "/ɪˈkwɪpmənt/"},
                "frequency": 3,
                "meaningVi": "máy móc, trang thiết bị",
                "exampleEn": "The company uses special equipment to load large crates onto freight trucks.",
                "exampleVi": "Công ty sử dụng một thiết bị đặc biệt để chất những thùng hàng lớn lên xe tải chở hàng.",
                "derivatives": [
                    {"word": "equip", "partOfSpeech": "v", "meaningVi": "trang bị"}
                ],
                "synonyms": ["machinery", "apparatus"],
                "antonyms": [],
                "toeicNotes": ["office equipment: thiết bị văn phòng", "lưu ý: equipment là danh từ không đếm được, không dùng a/an"],
                "needsReview": False
            },
            {
                "id": "automate",
                "word": "automate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɔːtəmeɪt/", "us": "/ˈɔːtəmeɪt/"},
                "frequency": 1,
                "meaningVi": "tự động hóa",
                "exampleEn": "The production plant will be fully automated by next year.",
                "exampleVi": "Xưởng sản xuất sẽ được tự động hóa hoàn toàn vào năm sau.",
                "derivatives": [
                    {"word": "automation", "partOfSpeech": "n", "meaningVi": "sự tự động hóa"},
                    {"word": "automatic", "partOfSpeech": "adj", "meaningVi": "tự động"}
                ],
                "synonyms": [],
                "antonyms": ["manual"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "specification",
                "word": "specification",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌspesɪfɪˈkeɪʃn/", "us": "/ˌspesɪfɪˈkeɪʃn/"},
                "frequency": 1,
                "meaningVi": "chi tiết, đặc điểm, chỉ dẫn/yêu cầu kỹ thuật",
                "exampleEn": "The quality control team checks if all items meet product specifications.",
                "exampleVi": "Đội ngũ kiểm soát chất lượng kiểm tra liệu tất cả sản phẩm có đáp ứng đủ yêu cầu kỹ thuật không.",
                "derivatives": [
                    {"word": "specify", "partOfSpeech": "v", "meaningVi": "chỉ rõ, ghi rõ"},
                    {"word": "specific", "partOfSpeech": "adj", "meaningVi": "cụ thể, chi tiết"}
                ],
                "synonyms": ["manual", "instructions"],
                "antonyms": [],
                "toeicNotes": ["meet specifications: đáp ứng các tiêu chuẩn/yêu cầu kỹ thuật"],
                "needsReview": False
            },
            {
                "id": "properly",
                "word": "properly",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈprɒpəli/", "us": "/ˈprɑːpərli/"},
                "frequency": 3,
                "meaningVi": "đúng đắn, thích đáng, hợp lệ",
                "exampleEn": "Machinery must be well-maintained to operate properly.",
                "exampleVi": "Máy móc cần được bảo dưỡng tốt để có thể hoạt động ổn định.",
                "derivatives": [
                    {"word": "proper", "partOfSpeech": "adj", "meaningVi": "đúng, thích hợp"}
                ],
                "synonyms": ["correctly", "appropriately"],
                "antonyms": ["improperly"],
                "toeicNotes": ["operate properly: hoạt động ổn định / đúng chức năng"],
                "needsReview": False
            },
            {
                "id": "safety",
                "word": "safety",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈseɪfti/", "us": "/ˈseɪfti/"},
                "frequency": 1,
                "meaningVi": "sự an toàn, tính an toàn",
                "exampleEn": "Factory supervisors prioritize safety over speed.",
                "exampleVi": "Giám sát viên nhà máy ưu tiên yếu tố an toàn hơn là tốc độ.",
                "derivatives": [
                    {"word": "safe", "partOfSpeech": "adj", "meaningVi": "an toàn"},
                    {"word": "safely", "partOfSpeech": "adv", "meaningVi": "một cách an toàn"}
                ],
                "synonyms": ["security"],
                "antonyms": ["danger"],
                "toeicNotes": ["safety precautions / regulations: các biện pháp / quy tắc an toàn"],
                "needsReview": False
            },
            {
                "id": "precaution",
                "word": "precaution",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/prɪˈkɔːʃn/", "us": "/prɪˈkɔːʃn/"},
                "frequency": 2,
                "meaningVi": "sự phòng ngừa, sự đề phòng",
                "exampleEn": "After the accident, the company introduced stricter safety precautions.",
                "exampleVi": "Sau vụ tai nạn đó, công ty đã đưa ra những biện pháp đảm bảo an toàn nghiêm ngặt hơn.",
                "derivatives": [
                    {"word": "precautious", "partOfSpeech": "adj", "meaningVi": "thận trọng, phòng xa"}
                ],
                "synonyms": ["safeguard", "protection"],
                "antonyms": [],
                "toeicNotes": ["take precautions: thực hiện các biện pháp phòng ngừa"],
                "needsReview": False
            },
            {
                "id": "operate",
                "word": "operate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈɒpəreɪt/", "us": "/ˈɑːpəreɪt/"},
                "frequency": 3,
                "meaningVi": "vận hành, hoạt động",
                "exampleEn": "The assembly line operates round the clock.",
                "exampleVi": "Dây chuyền lắp ráp vận hành suốt ngày đêm.",
                "derivatives": [
                    {"word": "operation", "partOfSpeech": "n", "meaningVi": "sự vận hành"},
                    {"word": "operational", "partOfSpeech": "adj", "meaningVi": "thuộc quá trình vận hành"},
                    {"word": "operable", "partOfSpeech": "adj", "meaningVi": "có thể vận hành"}
                ],
                "synonyms": ["run", "function"],
                "antonyms": [],
                "toeicNotes": ["operate round the clock: vận hành suốt 24/24"],
                "needsReview": False
            },
            {
                "id": "processing",
                "word": "processing",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈprəʊsesɪŋ/", "us": "/ˈprɑːsesɪŋ/"},
                "frequency": 2,
                "meaningVi": "sự chế biến, sự gia công, xử lý",
                "exampleEn": "Food processing requires a clean environment.",
                "exampleVi": "Việc chế biến thực phẩm đòi hỏi môi trường phải thật vệ sinh.",
                "derivatives": [
                    {"word": "process", "partOfSpeech": "v", "meaningVi": "xử lý, tiến triển"},
                    {"word": "process", "partOfSpeech": "n", "meaningVi": "quy trình, quá trình"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["phân biệt processing (sự chế biến/xử lý) và process (quy trình chế biến)"],
                "needsReview": False
            },
            {
                "id": "capacity",
                "word": "capacity",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kəˈpæsəti/", "us": "/kəˈpæsəti/"},
                "frequency": 2,
                "meaningVi": "sức chứa, năng lực, tư cách",
                "exampleEn": "The warehouse's capacity will double after the construction.",
                "exampleVi": "Sức chứa của nhà kho sẽ tăng gấp đôi sau khi xây dựng.",
                "derivatives": [
                    {"word": "capacious", "partOfSpeech": "adj", "meaningVi": "rộng lớn, dung tích lớn"}
                ],
                "synonyms": ["volume", "role"],
                "antonyms": [],
                "toeicNotes": ["be filled to capacity: đầy ắp", "expand the capacity: mở rộng sức chứa", "storage capacity: dung lượng lưu trữ"],
                "needsReview": False
            },
            {
                "id": "assemble",
                "word": "assemble",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈsembl/", "us": "/əˈsembl/"},
                "frequency": 1,
                "meaningVi": "lắp ráp, triệu tập",
                "exampleEn": "Components are manufactured abroad and assembled domestically.",
                "exampleVi": "Các bộ phận được sản xuất ở nước ngoài và lắp ráp trong nước.",
                "derivatives": [
                    {"word": "assembly", "partOfSpeech": "n", "meaningVi": "sự lắp ráp, bộ phận lắp ráp"}
                ],
                "synonyms": ["build", "gather"],
                "antonyms": ["disassemble"],
                "toeicNotes": ["assembly line: dây chuyền lắp ráp", "assembly plant: nhà máy lắp ráp"],
                "needsReview": False
            },
            {
                "id": "utilize",
                "word": "utilize",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈjuːtəlaɪz/", "us": "/ˈjuːtəlaɪz/"},
                "frequency": 1,
                "meaningVi": "dùng, sử dụng, tận dụng, khai thác",
                "exampleEn": "The technicians utilized computer technology to improve processes.",
                "exampleVi": "Các kỹ thuật viên đã áp dụng công nghệ tin học để cải thiện quy trình sản xuất.",
                "derivatives": [
                    {"word": "utilization", "partOfSpeech": "n", "meaningVi": "sự sử dụng, sự tận dụng"}
                ],
                "synonyms": ["use", "employ", "harness"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "place",
                "word": "place",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/pleɪs/", "us": "/pleɪs/"},
                "frequency": 3,
                "meaningVi": "đặt, để, sắp xếp; đặt (hàng)",
                "exampleEn": "The factory supervisor has placed production operations on standby.",
                "exampleVi": "Người giám sát nhà máy đã sắp xếp bộ phận sản xuất ở trạng thái sẵn sàng hoạt động.",
                "derivatives": [
                    {"word": "placement", "partOfSpeech": "n", "meaningVi": "sự sắp xếp, sự đặt vào"}
                ],
                "synonyms": ["put", "leave", "set"],
                "antonyms": [],
                "toeicNotes": ["place A on standby: đặt A ở trạng thái sẵn sàng", "place an order: đặt hàng"],
                "needsReview": False
            },
            {
                "id": "fill",
                "word": "fill",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/fɪl/", "us": "/fɪl/"},
                "frequency": 3,
                "meaningVi": "lấp đầy, đổ đầy; đáp ứng (đơn hàng/vị trí)",
                "exampleEn": "It will take a week to fill the hotel's order for bed sheets.",
                "exampleVi": "Sẽ mất một tuần để đáp ứng đủ đơn hàng ga trải giường của khách sạn.",
                "derivatives": [],
                "synonyms": ["satisfy", "fulfill"],
                "antonyms": ["empty"],
                "toeicNotes": ["fill A with B: lấp đầy A bằng B", "fill an order: đáp ứng đơn đặt hàng", "fill the position: bổ nhiệm vị trí"],
                "needsReview": False
            },
            {
                "id": "manufacturing",
                "word": "manufacturing",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˌmænjuˈfæktʃərɪŋ/", "us": "/ˌmænjuˈfæktʃərɪŋ/"},
                "frequency": 1,
                "meaningVi": "thuộc sản xuất, chế tạo",
                "exampleEn": "The manufacturing process in the automotive industry has changed with computer advances.",
                "exampleVi": "Quy trình sản xuất trong ngành công nghiệp ô tô đã thay đổi nhờ những tiến bộ về tin học.",
                "derivatives": [
                    {"word": "manufacture", "partOfSpeech": "v", "meaningVi": "sản xuất, chế tạo"},
                    {"word": "manufacturer", "partOfSpeech": "n", "meaningVi": "nhà sản xuất"}
                ],
                "synonyms": ["production"],
                "antonyms": [],
                "toeicNotes": ["manufacturing process: quy trình sản xuất"],
                "needsReview": False
            },
            {
                "id": "renovate",
                "word": "renovate",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ˈrenəveɪt/", "us": "/ˈrenəveɪt/"},
                "frequency": 3,
                "meaningVi": "nâng cấp, cải tạo (nhà cửa, nội thất)",
                "exampleEn": "The packaging area was renovated to use the space more effectively.",
                "exampleVi": "Khu vực đóng gói đã được cải tạo để tận dụng không gian hiệu quả hơn.",
                "derivatives": [
                    {"word": "renovation", "partOfSpeech": "n", "meaningVi": "sự cải tạo, nâng cấp"}
                ],
                "synonyms": ["remodel", "refurbish"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "decision",
                "word": "decision",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈsɪʒn/", "us": "/dɪˈsɪʒn/"},
                "frequency": 3,
                "meaningVi": "quyết định",
                "exampleEn": "The CEO's decision was to release the computer in February.",
                "exampleVi": "Quyết định của giám đốc điều hành là sẽ ra mắt máy tính đó vào tháng Hai.",
                "derivatives": [
                    {"word": "decide", "partOfSpeech": "v", "meaningVi": "quyết định"},
                    {"word": "decisive", "partOfSpeech": "adj", "meaningVi": "dứt khoát, quả quyết"}
                ],
                "synonyms": ["choice", "resolution"],
                "antonyms": [],
                "toeicNotes": ["make a decision about: đưa ra quyết định về"],
                "needsReview": False
            },
            {
                "id": "material",
                "word": "material",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/məˈtɪəriəl/", "us": "/məˈtɪəriəl/"},
                "frequency": 3,
                "meaningVi": "chất liệu, tài liệu, nguyên liệu",
                "exampleEn": "The designers selected the material because of its durability.",
                "exampleVi": "Các nhà thiết kế đã lựa chọn chất liệu này vì độ bền của nó.",
                "derivatives": [],
                "synonyms": ["substance"],
                "antonyms": [],
                "toeicNotes": ["phân biệt material (nguyên liệu đồ vật) và ingredient (nguyên liệu món ăn)"],
                "needsReview": False
            },
            {
                "id": "success",
                "word": "success",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/səkˈses/", "us": "/səkˈses/"},
                "frequency": 3,
                "meaningVi": "sự thành công, thắng lợi",
                "exampleEn": "The company owes its success to strict quality control.",
                "exampleVi": "Công ty có được thành công nhờ việc kiểm soát chất lượng nghiêm ngặt.",
                "derivatives": [
                    {"word": "succeed", "partOfSpeech": "v", "meaningVi": "thành công"},
                    {"word": "successful", "partOfSpeech": "adj", "meaningVi": "thành công"},
                    {"word": "successfully", "partOfSpeech": "adv", "meaningVi": "trôi chảy, thành công"}
                ],
                "synonyms": ["triumph", "achievement"],
                "antonyms": ["failure"],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "attribute",
                "word": "attribute",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/əˈtrɪbjuːt/", "us": "/əˈtrɪbjuːt/"},
                "frequency": 3,
                "meaningVi": "quy cho, gán cho",
                "exampleEn": "Management has attributed last year's gains to increased development.",
                "exampleVi": "Ban quản lý cho rằng những thành tựu đạt được năm ngoái là do sự phát triển tăng trưởng.",
                "derivatives": [
                    {"word": "attribution", "partOfSpeech": "n", "meaningVi": "sự quy vào, sự gán cho"}
                ],
                "synonyms": ["ascribe", "credit"],
                "antonyms": [],
                "toeicNotes": ["attribute A to B: quy A là do B", "A is attributed to B: A được cho là nguyên nhân do B"],
                "needsReview": False
            },
            {
                "id": "efficiency",
                "word": "efficiency",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ɪˈfɪʃnsi/", "us": "/ɪˈfɪʃnsi/"},
                "frequency": 3,
                "meaningVi": "hiệu quả, năng lực, năng suất",
                "exampleEn": "The consultant suggested measures to improve energy efficiency.",
                "exampleVi": "Cố vấn đã đề xuất các giải pháp để nâng cao hiệu quả sử dụng năng lượng.",
                "derivatives": [
                    {"word": "efficient", "partOfSpeech": "adj", "meaningVi": "có hiệu quả"},
                    {"word": "efficiently", "partOfSpeech": "adv", "meaningVi": "có hiệu quả"}
                ],
                "synonyms": ["effectiveness", "productivity"],
                "antonyms": ["inefficiency"],
                "toeicNotes": ["energy efficiency: hiệu quả sử dụng năng lượng", "office efficiency: hiệu quả văn phòng"],
                "needsReview": False
            },
            {
                "id": "limit",
                "word": "limit",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈlɪmɪt/", "us": "/ˈlɪmɪt/"},
                "frequency": 3,
                "meaningVi": "giới hạn, ranh giới",
                "exampleEn": "There is a limit to the amount of merchandise the factory can make in a day.",
                "exampleVi": "Có một giới hạn về lượng hàng hóa mà nhà máy có thể sản xuất trong một ngày.",
                "derivatives": [
                    {"word": "limitation", "partOfSpeech": "n", "meaningVi": "sự giới hạn"},
                    {"word": "limited", "partOfSpeech": "adj", "meaningVi": "bị hạn chế"}
                ],
                "synonyms": ["bound", "boundary", "cap"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "tailored",
                "word": "tailored",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈteɪləd/", "us": "/ˈteɪlərd/"},
                "frequency": 1,
                "meaningVi": "được tùy chỉnh, điều chỉnh (theo nhu cầu)",
                "exampleEn": "This equipment can be tailored to the company's production needs.",
                "exampleVi": "Thiết bị này có thể được điều chỉnh theo nhu cầu sản xuất của công ty.",
                "derivatives": [
                    {"word": "tailor", "partOfSpeech": "v", "meaningVi": "may, điều chỉnh, tùy biến"}
                ],
                "synonyms": ["customized", "adapted"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "component",
                "word": "component",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/kəmˈpəʊnənt/", "us": "/kəmˈpəʊnənt/"},
                "frequency": 2,
                "meaningVi": "thành phần, bộ phận, linh kiện",
                "exampleEn": "The store returned the defective components to the manufacturer.",
                "exampleVi": "Cửa hàng đã trả lại những bộ phận bị lỗi cho nhà sản xuất.",
                "derivatives": [],
                "synonyms": ["part", "piece", "element"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "capable",
                "word": "capable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈkeɪpəbl/", "us": "/ˈkeɪpəbl/"},
                "frequency": 2,
                "meaningVi": "có khả năng, có năng lực",
                "exampleEn": "Ferrum Corporation is capable of processing all kinds of metals.",
                "exampleVi": "Tập đoàn Ferrum có khả năng gia công mọi loại kim loại.",
                "derivatives": [
                    {"word": "capability", "partOfSpeech": "n", "meaningVi": "khả năng, năng lực"},
                    {"word": "capably", "partOfSpeech": "adv", "meaningVi": "thành thạo"}
                ],
                "synonyms": ["able", "competent"],
                "antonyms": ["incapable"],
                "toeicNotes": ["be capable of + V-ing: có khả năng làm gì (khác với be able to + V)"],
                "needsReview": False
            },
            {
                "id": "economize",
                "word": "economize",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/ɪˈkɒnəmaɪz/", "us": "/ɪˈkɑːnəmaɪz/"},
                "frequency": 2,
                "meaningVi": "tiết kiệm",
                "exampleEn": "Hybrid cars are becoming popular because they economize on fuel.",
                "exampleVi": "Dòng xe hơi chạy bằng xăng và điện ngày càng được ưa chuộng vì chúng tiết kiệm nhiên liệu.",
                "derivatives": [
                    {"word": "economy", "partOfSpeech": "n", "meaningVi": "nền kinh tế"},
                    {"word": "economical", "partOfSpeech": "adj", "meaningVi": "tiết kiệm"}
                ],
                "synonyms": ["save", "cut back"],
                "antonyms": ["waste", "squander"],
                "toeicNotes": ["economize on: tiết kiệm về (nhiên liệu, chi phí)"],
                "needsReview": False
            },
            {
                "id": "flexible",
                "word": "flexible",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈfleksəbl/", "us": "/ˈfleksəbl/"},
                "frequency": 2,
                "meaningVi": "mềm, dẻo; dễ thuyết phục; linh hoạt",
                "exampleEn": "Management is more flexible about granting vacations when business is slow.",
                "exampleVi": "Ban quản lý linh hoạt hơn trong việc cho nhân viên nghỉ phép khi hoạt động kinh doanh chậm lại.",
                "derivatives": [
                    {"word": "flexibility", "partOfSpeech": "n", "meaningVi": "tính linh hoạt"}
                ],
                "synonyms": ["adaptable", "pliable"],
                "antonyms": ["rigid", "stiff"],
                "toeicNotes": ["flexible schedule: lịch trình linh hoạt"],
                "needsReview": False
            },
            {
                "id": "comparable",
                "word": "comparable",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈkɒmpərəbl/", "us": "/ˈkɑːmpərəbl/"},
                "frequency": 2,
                "meaningVi": "có thể so sánh",
                "exampleEn": "The car's quality standards are comparable to the industry average.",
                "exampleVi": "Tiêu chuẩn chất lượng của loại xe hơi đó có thể so sánh với mặt bằng của ngành.",
                "derivatives": [
                    {"word": "compare", "partOfSpeech": "v", "meaningVi": "so sánh"},
                    {"word": "comparison", "partOfSpeech": "n", "meaningVi": "sự so sánh"}
                ],
                "synonyms": ["similar", "equivalent"],
                "antonyms": ["incomparable"],
                "toeicNotes": ["be comparable to: được so sánh với / tương đương với"],
                "needsReview": False
            },
            {
                "id": "produce",
                "word": "produce",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/prəˈdjuːs/", "us": "/prəˈduːs/"},
                "frequency": 2,
                "meaningVi": "sản xuất, chế tạo",
                "exampleEn": "The new machinery produces 1,000 units per hour.",
                "exampleVi": "Chiếc máy mới sản xuất được 1.000 sản phẩm mỗi giờ.",
                "derivatives": [
                    {"word": "product", "partOfSpeech": "n", "meaningVi": "sản phẩm"},
                    {"word": "production", "partOfSpeech": "n", "meaningVi": "sự sản xuất"},
                    {"word": "productivity", "partOfSpeech": "n", "meaningVi": "năng suất"}
                ],
                "synonyms": ["turn out", "manufacture"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "respectively",
                "word": "respectively",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/rɪˈspektɪvli/", "us": "/rɪˈspektɪvli/"},
                "frequency": 2,
                "meaningVi": "riêng từng cái, tương ứng",
                "exampleEn": "The camera and tablet computer cost $225 and $350 respectively.",
                "exampleVi": "Máy ảnh và máy tính bảng có giá lần lượt là 225 đô-la và 350 đô-la.",
                "derivatives": [
                    {"word": "respective", "partOfSpeech": "adj", "meaningVi": "tương ứng"}
                ],
                "synonyms": ["correspondingly"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "device",
                "word": "device",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/dɪˈvaɪs/", "us": "/dɪˈvaɪs/"},
                "frequency": 2,
                "meaningVi": "máy móc, thiết bị",
                "exampleEn": "The new device was tested for possible defects.",
                "exampleVi": "Thiết bị mới đã được kiểm tra để xem có còn lỗi nào không.",
                "derivatives": [
                    {"word": "devise", "partOfSpeech": "v", "meaningVi": "nghĩ ra, sáng chế"}
                ],
                "synonyms": ["gadget", "appliance", "instrument"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "trim",
                "word": "trim",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/trɪm/", "us": "/trɪm/"},
                "frequency": 1,
                "meaningVi": "cắt, tỉa, loại bỏ; cắt giảm",
                "exampleEn": "The team trimmed nearly 20 percent off of current production costs.",
                "exampleVi": "Nhóm đã cắt giảm gần 20% chi phí sản xuất hiện tại.",
                "derivatives": [],
                "synonyms": ["cut", "reduce", "crop"],
                "antonyms": [],
                "toeicNotes": ["trim off: cắt giảm (chi phí, thời gian)"],
                "needsReview": False
            },
            {
                "id": "launch",
                "word": "launch",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/lɔːntʃ/", "us": "/lɔːntʃ/"},
                "frequency": 1,
                "meaningVi": "ra mắt (sản phẩm mới)",
                "exampleEn": "Computer programmers fix technical malfunctions before launching any software.",
                "exampleVi": "Lập trình viên máy tính phải khắc phục các lỗi kỹ thuật trước khi ra mắt bất cứ phần mềm nào.",
                "derivatives": [
                    {"word": "launch", "partOfSpeech": "n", "meaningVi": "buổi giới thiệu / ra mắt"}
                ],
                "synonyms": ["introduce", "release"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "separately",
                "word": "separately",
                "partOfSpeech": "adv",
                "pronunciation": {"uk": "/ˈseprətli/", "us": "/ˈseprətli/"},
                "frequency": 1,
                "meaningVi": "tách biệt, riêng rẽ, khác nhau",
                "exampleEn": "The cushioning pads are made separately as each shoe is slightly different.",
                "exampleVi": "Các tấm lót giày được thiết kế riêng vì mỗi chiếc giày sẽ khác nhau một chút.",
                "derivatives": [
                    {"word": "separate", "partOfSpeech": "adj", "meaningVi": "riêng lẻ"},
                    {"word": "separation", "partOfSpeech": "n", "meaningVi": "sự chia cắt"}
                ],
                "synonyms": ["individually"],
                "antonyms": ["together", "jointly"],
                "toeicNotes": ["be made separately: được làm riêng", "be ordered separately: được đặt hàng riêng"],
                "needsReview": False
            },
            {
                "id": "expiration",
                "word": "expiration",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˌekspəˈreɪʃn/", "us": "/ˌekspəˈreɪʃn/"},
                "frequency": 1,
                "meaningVi": "sự hết hạn",
                "exampleEn": "The expiration date is printed on the top of the milk carton.",
                "exampleVi": "Hạn sử dụng được in trên nắp hộp sữa.",
                "derivatives": [
                    {"word": "expire", "partOfSpeech": "v", "meaningVi": "hết hạn"}
                ],
                "synonyms": [],
                "antonyms": [],
                "toeicNotes": ["expiration date: hạn sử dụng"],
                "needsReview": False
            },
            {
                "id": "maneuver",
                "word": "maneuver",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/məˈnuːvər/", "us": "/məˈnuːvər/"},
                "frequency": 1,
                "meaningVi": "diễn tập, điều động, điều khiển",
                "exampleEn": "Assembly line workers maneuvered the machinery into place.",
                "exampleVi": "Các công nhân ở dây chuyền lắp ráp đã điều khiển máy móc vào đúng vị trí.",
                "derivatives": [
                    {"word": "maneuver", "partOfSpeech": "n", "meaningVi": "sự điều động, diễn tập"}
                ],
                "synonyms": ["move", "navigate", "steer"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "coming",
                "word": "coming",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈkʌmɪŋ/", "us": "/ˈkʌmɪŋ/"},
                "frequency": 1,
                "meaningVi": "sắp tới",
                "exampleEn": "Factory output will double in the coming year.",
                "exampleVi": "Sản lượng của nhà máy sẽ tăng gấp đôi trong năm tới.",
                "derivatives": [
                    {"word": "come", "partOfSpeech": "v", "meaningVi": "đến"}
                ],
                "synonyms": ["upcoming", "approaching"],
                "antonyms": [],
                "toeicNotes": [],
                "needsReview": False
            },
            {
                "id": "damaged",
                "word": "damaged",
                "partOfSpeech": "adj",
                "pronunciation": {"uk": "/ˈdæmɪdʒd/", "us": "/ˈdæmɪdʒd/"},
                "frequency": 1,
                "meaningVi": "bị phá hủy, bị hư hại, hỏng",
                "exampleEn": "The conveyor belts were damaged from excessive use.",
                "exampleVi": "Các băng chuyền đã hỏng vì bị sử dụng quá nhiều.",
                "derivatives": [
                    {"word": "damage", "partOfSpeech": "n", "meaningVi": "sự thiệt hại"},
                    {"word": "damage", "partOfSpeech": "v", "meaningVi": "làm hư hại"}
                ],
                "synonyms": ["broken", "impaired"],
                "antonyms": ["intact"],
                "toeicNotes": ["phân biệt damaged (sự vật hư hại), impaired (khiếm khuyết con người), injured (chấn thương người)"],
                "needsReview": False
            },
            {
                "id": "prevent",
                "word": "prevent",
                "partOfSpeech": "v",
                "pronunciation": {"uk": "/prɪˈvent/", "us": "/prɪˈvent/"},
                "frequency": 1,
                "meaningVi": "ngăn chặn, ngăn ngừa",
                "exampleEn": "Employees are expected to observe safety guidelines to prevent accidents.",
                "exampleVi": "Nhân viên được yêu cầu phải tuân thủ các chỉ dẫn an toàn để phòng tránh tai nạn.",
                "derivatives": [
                    {"word": "prevention", "partOfSpeech": "n", "meaningVi": "sự ngăn ngừa"},
                    {"word": "preventive", "partOfSpeech": "adj", "meaningVi": "nhằm phòng ngừa"}
                ],
                "synonyms": ["avoid", "stop", "hinder"],
                "antonyms": ["allow", "permit"],
                "toeicNotes": ["prevent A from -ing: phòng tránh A khỏi việc gì"],
                "needsReview": False
            },
            {
                "id": "power",
                "word": "power",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈpaʊər/", "us": "/ˈpaʊər/"},
                "frequency": 1,
                "meaningVi": "sức mạnh, năng lượng, điện",
                "exampleEn": "The plant was closed for half a business day due to a power outage.",
                "exampleVi": "Nhà máy bị đóng cửa nửa ngày làm việc vì mất điện.",
                "derivatives": [
                    {"word": "powerful", "partOfSpeech": "adj", "meaningVi": "mạnh mẽ"},
                    {"word": "empower", "partOfSpeech": "v", "meaningVi": "trao quyền"}
                ],
                "synonyms": ["electricity", "energy"],
                "antonyms": [],
                "toeicNotes": ["power outage / failure: sự mất điện", "power plant: nhà máy điện", "power supply: nguồn cung cấp điện"],
                "needsReview": False
            },
            {
                "id": "chemical",
                "word": "chemical",
                "partOfSpeech": "n",
                "pronunciation": {"uk": "/ˈkemɪkl/", "us": "/ˈkemɪkl/"},
                "frequency": 1,
                "meaningVi": "chất hóa học",
                "exampleEn": "Protective gear is needed when working with dangerous chemicals.",
                "exampleVi": "Đồ bảo hộ rất cần thiết khi làm việc với những hóa chất nguy hiểm.",
                "derivatives": [
                    {"word": "chemist", "partOfSpeech": "n", "meaningVi": "nhà hóa học"},
                    {"word": "chemistry", "partOfSpeech": "n", "meaningVi": "môn hóa học"}
                ],
                "synonyms": ["substance"],
                "antonyms": [],
                "toeicNotes": ["phân biệt chemical (chất hóa học) và chemist (nhà hóa học)"],
                "needsReview": False
            }
        ]

        quiz_questions = [
            {
                "q": "The production plant will be fully ___d by next year.",
                "a": "automate",
                "options": ["automate", "renovate", "economize", "operate"]
            },
            {
                "q": "The quality control team checks if all items meet product ___s.",
                "a": "specification",
                "options": ["specification", "precaution", "decision", "material"]
            },
            {
                "q": "Machinery must be well-maintained to operate ___.",
                "a": "properly",
                "options": ["properly", "separately", "respectively", "capable"]
            },
            {
                "q": "After the accident, the company introduced stricter safety ___s.",
                "a": "precaution",
                "options": ["precaution", "component", "device", "efficiency"]
            },
            {
                "q": "The warehouse's ___ will double after the construction.",
                "a": "capacity",
                "options": ["capacity", "material", "power", "decision"]
            },
            {
                "q": "Components are manufactured abroad and ___d domestically.",
                "a": "assemble",
                "options": ["assemble", "utilize", "renovate", "maneuver"]
            },
            {
                "q": "The packaging area was ___d to use the space more effectively.",
                "a": "renovate",
                "options": ["renovate", "produce", "prevent", "trim"]
            },
            {
                "q": "Ferrum Corporation is ___ of processing all kinds of metals.",
                "a": "capable",
                "options": ["capable", "flexible", "comparable", "tailored"]
            },
            {
                "q": "Hybrid cars are becoming popular because they ___ on fuel.",
                "a": "economize",
                "options": ["economize", "attribute", "maneuver", "launch"]
            },
            {
                "q": "Employees are expected to observe safety guidelines to ___ accidents.",
                "a": "prevent",
                "options": ["prevent", "fill", "place", "trim"]
            }
        ]

            
    # Format story dynamically
    story_json = {}
    story_data = STORIES_DB.get(day_num)
    if story_data:
        formatted_words = []
        placeholders = {}
        
        default_meanings = {
            "inform": "thông báo", "résumé": "sơ yếu lý lịch", "opening": "vị trí trống", 
            "applicant": "ứng viên", "requirement": "yêu cầu", "meet": "đáp ứng", 
            "qualified": "đủ năng lực", "candidate": "ứng viên", "confidence": "sự tự tin", 
            "professional": "chuyên nghiệp", "submit": "nộp", "policy": "chính sách", 
            "comply": "tuân thủ", "regulation": "quy định", "exception": "ngoại lệ", 
            "adhere": "tuân thủ", "severely": "nặng nề", "permission": "sự cho phép", 
            "access": "tiếp cận", "procedure": "thủ tục", "department": "phòng ban", 
            "colleague": "đồng nghiệp", "assist": "hỗ trợ", "delegate": "giao phó", 
            "coordinate": "phối hợp", "supervisor": "người giám sát", "remind": "nhắc nhở", 
            "instruction": "hướng dẫn", "assignment": "nhiệm vụ", "schedule": "lịch trình", 
            "meeting": "cuộc họp", "agenda": "chương trình nghị sự", "conduct": "tiến hành", 
            "discuss": "thảo luận", "review": "xem xét", "report": "báo cáo", 
            "decision": "quyết định", "executive": "điều hành", "deadline": "hạn chót", 
            "file": "hồ sơ", "document": "tài liệu", "cabinet": "tủ hồ sơ", 
            "folder": "thư mục", "organize": "sắp xếp", "retrieve": "tìm lại", 
            "archive": "lưu trữ", "sensitive": "nhạy cảm", "confidential": "mật", 
            "update": "cập nhật", "relax": "thư giãn", "activity": "hoạt động", 
            "community": "cộng đồng", "participate": "tham gia", "organize": "tổ chức", 
            "gather": "tụ họp", "entertainment": "giải trí", "hobby": "sở thích", 
            "outdoor": "ngoài trời", "enjoy": "tận hưởng", "market": "thị trường", 
            "campaign": "chiến dịch", "advertisement": "quảng cáo", "target": "nhắm tới", 
            "customer": "khách hàng", "strategy": "chiến lược", "promotion": "khuyến mãi", 
            "attract": "thu hút", "brand": "thương hiệu", "budget": "ngân sách", 
            "survey": "khảo sát", "feedback": "phản hồi", "response": "phản hồi", 
            "analyze": "phân tích", "consumer": "người tiêu dùng", "preference": "sự ưu tiên", 
            "satisfaction": "sự hài lòng", "result": "kết quả", "improve": "cải thiện", 
            "economy": "kinh tế", "growth": "tăng trưởng", "inflation": "lạm phát", 
            "industry": "ngành công nghiệp", "recover": "phục hồi", "revenue": "doanh thu", 
            "profit": "lợi nhuận", "demand": "nhu cầu", "passenger": "hành khách", 
            "cost": "chi phí", "store": "cửa hàng", "purchase": "mua", 
            "price": "giá cả", "discount": "giảm giá", "receipt": "hóa đơn", 
            "refund": "hoàn tiền", "quality": "chất lượng", "warranty": "bảo hành", 
            "choice": "sự lựa chọn", "design": "thiết kế", "develop": "phát triển", 
            "product": "sản phẩm", "feature": "đặc điểm", "innovative": "sáng tạo", 
            "test": "thử nghiệm", "service": "dịch vụ", "produce": "sản xuất", 
            "factory": "nhà máy", "assembly": "lắp ráp", "component": "linh kiện", 
            "check": "kiểm tra", "standard": "tiêu chuẩn", "efficiency": "hiệu suất", 
            "worker": "công nhân", "machine": "máy móc", "output": "sản lượng", 
            "complaint": "khiếu nại", "resolve": "giải quyết", "polite": "lịch sự", 
            "assistance": "trợ giúp", "request": "yêu cầu", "satisfy": "làm hài lòng", 
            "help": "giúp đỡ", "experience": "trải nghiệm", "airport": "sân bay", 
            "flight": "chuyến bay", "ticket": "vé", "passport": "hộ chiếu", 
            "boarding": "lên máy bay", "luggage": "hành lý", "delay": "trì hoãn", 
            "gate": "cổng", "destination": "điểm đến", "contract": "hợp đồng", 
            "agreement": "thỏa thuận", "sign": "ký kết", "negotiate": "thương lượng", 
            "terms": "điều khoản", "clause": "điều khoản", "partner": "đối tác", 
            "approve": "phê duyệt", "conditions": "điều kiện", "period": "giai đoạn", 
            "pay": "thanh toán", "transaction": "giao dịch", "card": "thẻ", 
            "currency": "tiền tệ", "fee": "lệ phí", "charge": "tính phí", 
            "bill": "hóa đơn", "account": "tài khoản", "ship": "vận chuyển", 
            "cargo": "khoang hàng", "freight": "cước vận chuyển", "delivery": "giao hàng", 
            "transport": "vận chuyển", "warehouse": "nhà kho", "package": "đóng gói", 
            "tracking": "theo dõi", "logistics": "hậu cần", "hotel": "khách sạn", 
            "room": "phòng", "stay": "ở lại", "reservation": "sự đặt chỗ", 
            "restaurant": "nhà hàng", "menu": "thực đơn", "food": "món ăn"
        }
        
        for idx, exp_w in enumerate(story_data["words"]):
            # Find fuzzy match in words_data
            matched_w = None
            for w_entry in words_data:
                if to_ascii(exp_w) in to_ascii(w_entry["word"]):
                    matched_w = w_entry
                    break
            
            # If not found, search with sequence matcher
            if not matched_w:
                for w_entry in words_data:
                    if difflib.SequenceMatcher(None, to_ascii(exp_w), to_ascii(w_entry["word"])).ratio() > 0.7:
                        matched_w = w_entry
                        break
                        
            # Extract word and meaning
            if matched_w:
                w_disp = matched_w["word"]
                meaning_disp = matched_w["meaningVi"].split(',')[0].split(';')[0].strip()
            else:
                w_disp = exp_w
                meaning_disp = default_meanings.get(exp_w, "nghĩa")
                
            # Format placeholder
            placeholders[f"w{idx}"] = f"**{w_disp}**"
            formatted_words.append({
                "word": w_disp,
                "meaningVi": meaning_disp
            })
            
        formatted_content = story_data["template"].format(**placeholders)
        
        story_json = {
            "title": story_data["title"],
            "content": formatted_content,
            "words": formatted_words
        }
            
    day_json = {
        "id": f"unit-{day_num:02d}",
        "day": day_num,
        "title": info["title"],
        "topic": info["topic"],
        "sourcePages": [1 + (day_num - 1) * 16, day_num * 16],
        "words": words_data,
        "story": story_json,
        "quiz": [
            {
                "type": "fill-in-the-blank",
                "instruction": "Chọn từ thích hợp điền vào chỗ trống:",
                "questions": quiz_questions
            }
        ]
    }
    
    output_path = os.path.join(output_dir, f"unit-{day_num:02d}.json")
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(day_json, out_f, ensure_ascii=False, indent=2)
        
    print(f"Saved {output_path} with {len(words_data)} words and {len(quiz_questions)} quiz questions.")
