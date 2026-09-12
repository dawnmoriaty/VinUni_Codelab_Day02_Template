# 01 - Problem Scan & Quick Cards

**Người thực hiện:** Tran Quoc Vuong  
**Bối cảnh:** Các số liệu trong tài liệu này là giả định dùng cho prototype scoping; cần xác minh bằng log vận hành trước khi triển khai.

## Phase 1 - SCAN

| # | Công ty | Lens | Bài toán thực tế cần xác minh |
|---|---|---|---|
| 1 | Vinhomes | Lặp lại | Phân loại phản ánh cư dân (mất nước, hỏng đèn, thang máy) và chuyển đúng ban quản lý/tòa nhà. |
| 2 | Xanh SM | Tốn thời gian | Điều phối viên đọc tin nhắn sự cố của tài xế, lấy vị trí và tạo phiếu hỗ trợ thủ công. |
| 3 | VinFast | Lặp lại | Đối chiếu dữ liệu phiên sạc từ nhiều đối tác với hóa đơn và log nội bộ. |
| 4 | Vinmec | Tốn thời gian | Bác sĩ soạn bản nháp tóm tắt xuất viện từ bệnh án, xét nghiệm và ghi chú. |
| 5 | Vinpearl | AI-upgrade | Gom và phân loại review khách sạn theo mức độ khẩn cấp, bộ phận xử lý và chủ đề. |
| 6 | Vinhomes | Pain từ stakeholder | Cư dân không biết trạng thái xử lý yêu cầu nên gọi lại nhiều lần cho ban quản lý. |

## Phase 2 - QUICK-ASSESS

### Card #1 - Phân loại phản ánh cư dân Vinhomes

- **Bài toán:** Phản ánh tự do trên ứng dụng phải được phân loại và chuyển đúng bộ phận.
- **Công ty:** Vinhomes
- **Actor bị ảnh hưởng:** Nhân viên trực tổng đài, ban quản lý tòa nhà và cư dân.
- **Quy trình hiện tại:**
  1. Cư dân gửi nội dung và ảnh qua ứng dụng.
  2. Nhân viên đọc, đoán chủ đề và mức độ khẩn cấp.
  3. Nhân viên tra bảng phân tuyến theo tòa nhà.
  4. Nhân viên tạo phiếu và chuyển cho bộ phận xử lý.
  5. Cư dân chờ cập nhật trạng thái.
- **Nút cổ chai:** Đọc và phân tuyến thủ công, 8-12 phút/yêu cầu; nội dung mơ hồ dễ bị chuyển nhầm.
- **AI hỗ trợ:** Trích xuất tòa nhà, chủ đề, mức độ khẩn cấp và tạo bản nháp phiếu.
- **Metric giả định:** 90% yêu cầu được phân loại trong 30 giây; giảm thời gian nhập phiếu từ 10 xuống dưới 2 phút; tỷ lệ chuyển nhầm dưới 5%.
- **Kiến trúc:** Rule cho SLA/keyword bắt buộc + LLM Feature cho phân loại và tóm tắt + HITL.

### Card #2 - Triage sự cố xe Xanh SM

- **Bài toán:** Tin nhắn sự cố của tài xế bị xử lý thủ công và thiếu thông tin.
- **Công ty:** Xanh SM
- **Actor bị ảnh hưởng:** Điều phối viên và tài xế.
- **Quy trình:** Nhận tin -> đọc nội dung -> gọi lại lấy thông tin -> tạo phiếu -> chuyển cứu hộ.
- **Nút cổ chai:** Gọi lại và nhập phiếu, 10-15 phút/lượt.
- **AI hỗ trợ:** Trích xuất loại sự cố, vị trí và mức độ ưu tiên; không tự điều xe cứu hộ.
- **Metric giả định:** 85% phiếu đủ trường dữ liệu trong 60 giây; 0 lệnh cứu hộ tự động.
- **Kiến trúc:** LLM Feature + Rule kiểm tra trường bắt buộc + HITL.

### Card #3 - Tóm tắt review Vinpearl

- **Bài toán:** Quản lý phải đọc nhiều review để tìm vấn đề ảnh hưởng trải nghiệm khách.
- **Công ty:** Vinpearl
- **Actor bị ảnh hưởng:** Guest Relations và quản lý khách sạn.
- **Quy trình:** Thu thập review -> đọc -> gắn nhãn -> gom chủ đề -> báo cáo tuần.
- **Nút cổ chai:** Đọc và gom chủ đề, 2-3 giờ/ngày/cơ sở.
- **AI hỗ trợ:** Tóm tắt, gắn nhãn cảm xúc/chủ đề và trích dẫn review nguồn.
- **Metric giả định:** Giảm thời gian tổng hợp 50%; 100% kết quả có liên kết đến review gốc.
- **Kiến trúc:** LLM Feature; không tự phản hồi khách.

## Lựa chọn

Chọn **Card #1 - Phân loại phản ánh cư dân Vinhomes** để deep-dive vì dữ liệu đầu vào dạng ngôn ngữ tự nhiên, giá trị đo được và rủi ro có thể kiểm soát bằng luật định tuyến, HITL và fallback thủ công. Đây là giả thuyết sản phẩm, không phải số liệu đã được Vinhomes xác nhận.
