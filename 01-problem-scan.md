# 01 - Problem Scan & Quick Problem Cards

**Vai trò:** AI Product Engineer, Vin Smart Future  
**Phạm vi khảo sát:** VinFast, Xanh SM, Vinhomes, Vinmec và Vinpearl  
**Lưu ý dữ liệu:** Các con số trong bản scoping này là giả định ban đầu để lập baseline. Cần xác minh bằng log vận hành, phỏng vấn stakeholder và đo thời gian thực tế trước khi triển khai.

## Phase 1 - SCAN

| # | Subsidiary | Lens | Bài toán / bottleneck | Giả định cần xác minh |
|---:|---|---|---|---|
| 1 | Xanh SM | Tốn thời gian | Khi tài xế báo xe sắp hết pin, bản đồ chỉ cho tài xế biết các trạm có thể có; dispatcher phải xử lý một incident có nhiều nguồn dữ liệu: xác minh pin/GPS mới nhất, tình trạng trạm theo thời điểm, loại đầu nối, khả năng xe đi đến trạm và phương án cứu hộ. Sau đó dispatcher soạn thông báo phù hợp. | 10-15 phút/sự cố; cần kiểm tra từ call log, dispatch log, dữ liệu trạm và timestamp. |
| 2 | Vinhomes | Lặp lại | Nhân viên phải đọc, phân loại và chuyển khiếu nại cư dân như mất nước, hỏng đèn, tiếng ồn đến đúng bộ phận. | Khối lượng ticket/ngày và tỷ lệ route sai cần lấy từ hệ thống Resident App. |
| 3 | VinFast | Lặp lại | Nhân viên tài chính đối chiếu bản ghi sạc từ đối tác với hóa đơn và phát hiện lệch số tiền, thời gian hoặc kWh. | Số lượng giao dịch/tuần và tỷ lệ lệch cần lấy từ ERP/log trạm. |
| 4 | Vinmec | Tốn thời gian | Bác sĩ tổng hợp bệnh án, xét nghiệm và ghi chú để soạn bản nháp tóm tắt xuất viện. | 20-30 phút/bệnh nhân là giả định; mọi nội dung phải được bác sĩ duyệt. |
| 5 | Vinpearl | Stakeholder Pain | Manager phải đọc review từ nhiều kênh để phát hiện phàn nàn khẩn cấp về vệ sinh, an toàn hoặc thái độ phục vụ. | Nguồn review, SLA phản hồi và tỷ lệ alert đúng cần được xác minh. |
| 6 | VinFast | AI-upgrade | Kỹ thuật viên tiếp nhận mô tả tiếng Việt không chuẩn về tiếng động/lỗi xe và tìm mã lỗi ban đầu bằng tay. | Cần kiểm tra bộ mã lỗi, dữ liệu nhãn và rủi ro an toàn trước khi thử nghiệm. |

## Phase 2 - QUICK-ASSESS

### Quick Problem Card #1 - Xanh SM: Sự cố pin thực địa

- **Bài toán:** Tài xế báo pin thấp hoặc hết pin giữa đường; dispatcher cần biến nhiều dữ liệu vận hành thành một phương án an toàn nhanh chóng. Đây **không phải** bài toán xây thêm bản đồ hay thay thế chức năng tìm trạm mà tài xế đã có.
- **Công ty:** Xanh SM (GSM)
- **Actor đang đau:** Tài xế cần biết nên tự đi sạc hay chờ cứu hộ; dispatcher phải chịu trách nhiệm xác minh và truyền đạt phương án trong lúc xử lý nhiều incident đồng thời.
- **Workflow thủ công hiện tại:**
-  1. Tài xế gọi/tạo ticket, cung cấp biển số, vị trí và phần trăm pin; các thông tin này có thể khác với dữ liệu telematics.
  2. Dispatcher xác minh timestamp GPS/pin, tình trạng xe, mức độ nguy hiểm và xem tài xế có đang chở khách hay dừng an toàn không.
  3. Dispatcher đối chiếu dữ liệu trạm theo thời điểm: trạm đang hoạt động, còn chỗ, đúng đầu nối, có thể tiếp nhận dòng xe và không quá xa so với pin hiện tại. Bản đồ của tài xế chỉ là nguồn tham khảo, không phải xác nhận availability theo thời gian thực.
  4. Dispatcher quyết định tuyến xử lý: đề xuất trạm hợp lệ, hướng dẫn chờ an toàn hoặc chuyển đội cứu hộ/mobile charger.
  5. Dispatcher tự kiểm tra và gửi thông báo qua kênh được phê duyệt.
- **Bước tốn thời gian/lỗi nhất:** Bước 2-4, dự kiến 10 phút/lượt; lỗi thường không phải “không biết trạm ở đâu” mà là dùng dữ liệu cũ, nhầm trạng thái còn chỗ, nhầm đầu nối, đánh giá sai khả năng xe đi tới trạm hoặc gửi hướng dẫn thiếu thông tin.
- **AI hỗ trợ tại:** Chuẩn hóa mô tả sự cố, đối chiếu các trường dữ liệu đã xác minh, loại candidate không hợp lệ theo rule, giải thích vì sao chọn phương án và soạn tin nhắn nháp. AI không tự truy cập bản đồ cá nhân của tài xế và không thay thế quyết định của dispatcher.
- **Metric:** P50 thời gian từ ticket đủ thông tin đến draft giảm từ baseline 15 phút xuống dưới 3 phút; 100% output có `[DRAFT_ONLY]`; 0 khuyến nghị vượt boundary được chấp nhận.
- **Quick Architecture:** LLM Feature + Rule-based safety gate + Human-in-the-loop; không giao quyền tự gửi.

### Quick Problem Card #2 - Vinhomes: Route khiếu nại cư dân

- **Bài toán:** Khiếu nại tự do trên Resident App phải được chuyển đúng ban xử lý mà không làm mất SLA.
- **Công ty:** Vinhomes
- **Actor đang đau:** Nhân viên CSKH/ban quản lý tòa nhà và cư dân chờ phản hồi.
- **Workflow thủ công hiện tại:**
  1. CSKH đọc nội dung và kiểm tra tòa/căn hộ.
  2. CSKH gán loại vấn đề và mức độ ưu tiên.
  3. CSKH chuyển ticket cho điện/nước/an ninh/kỹ thuật.
  4. Bộ phận xử lý cập nhật trạng thái và draft phản hồi.
- **Bước tốn thời gian/lỗi nhất:** Bước 2-3, dự kiến 5 phút/ticket; lỗi route có thể làm trễ SLA.
- **AI hỗ trợ tại:** Phân loại có confidence, trích xuất tòa/căn hộ và đề xuất queue; con người duyệt ca nhạy cảm.
- **Metric:** 90% ticket được phân loại dưới 10 giây; macro-F1 tối thiểu 0,90 trên tập test; ticket confidence thấp phải vào hàng chờ review.
- **Quick Architecture:** Rule + LLM Feature; rule xử lý các từ khóa/SLA rõ, LLM xử lý ngôn ngữ tự do.

### Quick Problem Card #3 - Vinmec: Draft tóm tắt xuất viện

- **Bài toán:** Tạo bản nháp tóm tắt xuất viện từ hồ sơ lâm sàng để giảm thời gian nhập liệu của bác sĩ.
- **Công ty:** Vinmec
- **Actor đang đau:** Bác sĩ điều trị và bệnh nhân chờ hồ sơ dễ hiểu.
- **Workflow thủ công hiện tại:**
  1. Bác sĩ mở bệnh án điện tử, kết quả xét nghiệm và ghi chú.
  2. Bác sĩ chọn chẩn đoán, thuốc, diễn biến và hướng dẫn.
  3. Bác sĩ tự viết tóm tắt theo mẫu.
  4. Bác sĩ rà soát, ký và phát hành hồ sơ.
- **Bước tốn thời gian/lỗi nhất:** Bước 2-3, dự kiến 20 phút/bệnh nhân; nguy cơ bỏ sót hoặc diễn đạt sai thông tin.
- **AI hỗ trợ tại:** Trích xuất có dẫn nguồn và soạn draft, tuyệt đối không tự chẩn đoán/kê đơn/ký hồ sơ.
- **Metric:** Giảm thời gian soạn draft 20 xuống dưới 8 phút; 100% trường quan trọng có nguồn trích dẫn; 100% hồ sơ được bác sĩ ký duyệt.
- **Quick Architecture:** LLM Feature có retrieval giới hạn + Rule validation + Human-in-the-loop.

## Lựa chọn để Deep-Dive

Nhóm chọn **Quick Card #1 - Xanh SM xử lý sự cố pin thực địa** vì quy trình có đầu vào rõ, metric đo được, giá trị thời gian thực và có thể giới hạn AI ở việc đề xuất/draft. Hai card còn lại cần kiểm soát dữ liệu và rủi ro cao hơn; chúng có thể được xem xét sau khi có baseline và phê duyệt domain.
