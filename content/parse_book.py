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
