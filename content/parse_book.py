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
