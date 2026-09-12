[DRAFT_ONLY]

# Phase 1 — SCAN (Khám phá bài toán)

Dưới đây là danh sách 5 bài toán vận hành thực tế tại các công ty thành viên Vingroup, được phân loại theo các lăng kính (Lens) khác nhau:

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | **Xanh SM** | Lặp lại / Tốn thời gian | **Xử lý sự cố hết pin thực địa cho tài xế:** Tài xế xe điện báo hết pin giữa đường, tổng đài viên phải dò tìm trạm sạc gần nhất thủ công, tính toán khoảng cách và đưa ra quyết định gọi xe cứu hộ hay chỉ đường. Quá trình kéo dài gây ảnh hưởng trải nghiệm khách hàng và doanh thu. |
| 2 | **Xanh SM** | Pain từ người khác | **Phân loại lý do hủy chuyến:** Khách hàng hủy chuyến nhiều, tổng đài viên phải nghe lại hàng ngàn cuộc gọi/đọc ghi chú thủ công để tìm ra nguyên nhân gốc rễ (xe đến trễ, thái độ tài xế, app lỗi). |
| 3 | **VinFast** | AI có thể tốt hơn | **Chẩn đoán mã lỗi xe qua giọng nói/văn bản:** Khách hàng mô tả lỗi xe bằng ngôn ngữ tự nhiên (VD: "xe có tiếng kêu lạ ở gầm"), kỹ thuật viên mất thời gian tra cứu thủ công để chuyển thành mã lỗi kỹ thuật hệ thống. |
| 4 | **Vinhomes** | Lặp lại | **Điều phối khiếu nại cư dân:** Hàng trăm phản ánh cư dân (mất nước, hỏng thang máy, tiếng ồn) gửi qua app mỗi ngày, ban quản lý phải đọc từng tin và gán thủ công cho đúng bộ phận xử lý (kỹ thuật, an ninh, vệ sinh). |
| 5 | **Vinmec** | Tốn thời gian | **Soạn tóm tắt hồ sơ xuất viện (Discharge Summary):** Bác sĩ mất 15-20 phút thu thập dữ liệu từ bệnh án điện tử, kết quả xét nghiệm để viết tóm tắt xuất viện bằng ngôn ngữ dễ hiểu cho bệnh nhân. |

---

# Phase 2 — QUICK-ASSESS (Đánh giá nhanh)

Từ danh sách trên, 3 bài toán tiềm năng nhất được lựa chọn để phân tích bằng Quick Problem Card:

### QUICK PROBLEM CARD #1 (MAIN)
```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán (1 câu): Tối ưu hóa quy trình xử lý sự cố hết pin  │
│                   thực địa cho tài xế Xanh SM để giảm thời  │
│                   gian chờ đợi.                             │
│ Công ty thành viên: [x] Xanh SM                             │
│                                                             │
│ Ai đang đau (Actor)? Điều phối viên (Dispatcher) tổng đài & │
│                      Tài xế Xanh SM.                        │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Tài xế báo sự cố hết pin qua app/tổng đài              │
│   ──> 2. Dispatcher tra cứu toạ độ GPS của xe trên hệ thống │
│   ──> 3. Dispatcher dò tìm trạm sạc gần nhất, xem lượng pin │
│   ──> 4. Nhắn tin chỉ đường hoặc gọi xe cứu hộ pin          │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 & 4 (⏱ 5-8 phút/lượt)
│ AI có thể nhảy vào hỗ trợ ở bước nào? Phân tích tin nhắn báo│
│           sự cố, tự động đối chiếu GPS/pin để đưa ra đề xuất│
│           (Draft tin nhắn hoặc gọi xe cứu hộ).              │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│   Giảm thời gian phản hồi từ 5-8 phút ──> dưới 1 phút.      │
│   Giảm tỷ lệ xe cạn pin giữa đường (khi pin <5%) xuống 0%.  │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

### QUICK PROBLEM CARD #2
```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán (1 câu): Tự động hóa việc phân loại và trích xuất  │
│                   nguyên nhân khách hàng hủy chuyến.        │
│ Công ty thành viên: [x] Xanh SM                             │
│                                                             │
│ Ai đang đau (Actor)? Nhân viên phân tích chất lượng dịch vụ │
│                      (QA) và CSKH.                          │
│                                                             │
│ Workflow thủ công hiện tại (3 bước):                        │
│   1. Xuất dữ liệu cuốc xe bị hủy hằng ngày                  │
│   ──> 2. QA nghe lại ghi âm hoặc đọc ghi chú của tài xế/khách│
│   ──> 3. Gán tag lý do hủy (App lỗi, kẹt xe, tài xế thô lỗ) │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 3 (⏱ 3-5 phút/lượt)
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 3: Đọc text/ │
│           nghe audio và tự động gán nhãn, tổng hợp báo cáo. │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│   Tăng tỷ lệ xử lý cuốc hủy từ 10% (lấy mẫu) ──> 100% tự động.
│   Tiết kiệm 40 giờ làm việc của nhân sự QA mỗi tuần.        │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

### QUICK PROBLEM CARD #3
```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán (1 câu): Tự động phân loại và điều phối khiếu nại  │
│                   của cư dân đến đúng bộ phận xử lý.        │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau (Actor)? Ban quản lý tòa nhà & Lễ tân.          │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Cư dân gửi khiếu nại text/hình ảnh qua app Vinhomes    │
│   ──> 2. Lễ tân đọc nội dung, xác định mức độ nghiêm trọng  │
│   ──> 3. Lễ tân tạo ticket chuyển cho kỹ thuật/vệ sinh      │
│   ──> 4. Bộ phận liên quan xác nhận và đi xử lý             │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 3 (⏱ 3-5 phút/lượt)
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 3: Đọc text/ │
│           hình ảnh để phân loại và tự động tạo/gán ticket.  │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│   Thời gian phân phối ticket giảm từ 5 phút ──> dưới 10 giây.
│   Độ chính xác phân loại bộ phận đạt trên 90%.              │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

---

### Lựa chọn bài toán để Deep-Dive: Vì sao chọn Card #1?

Nhóm quyết định chọn **Card #1 (Xử lý sự cố sạc pin thực địa cho tài xế Xanh SM)** để tiến hành Deep-Dive vì các lý do sau:

1. **Tác động kinh doanh (Business Impact) rõ ràng và khẩn cấp:** Vấn đề hết pin giữa đường ảnh hưởng trực tiếp đến SLA (Service Level Agreement), doanh thu (cuốc xe bị gián đoạn) và trải nghiệm hành khách. Giảm thời gian giải quyết sự cố từ 5-8 phút xuống dưới 1 phút mang lại giá trị định lượng ngay lập tức.
2. **Operational Boundary chặt chẽ, dễ áp dụng HITL:** Bài toán này cần áp dụng nghiêm ngặt các quy tắc kinh doanh (như pin < 5% phải gọi xe cứu hộ, không chỉ đường xa quá 5km). Việc thiết lập một ranh giới (boundary) rõ ràng và luồng có sự phê duyệt của Dispatcher (Human-in-the-loop) là bài kiểm tra hoàn hảo cho năng lực kiểm soát rủi ro của AI.
3. **Lý do loại trừ Card #2 và #3:**
   * *Card #2 (Phân loại lý do hủy chuyến):* Mang tính chất báo cáo (reporting) nhiều hơn là can thiệp vận hành theo thời gian thực (real-time operation). Tuy tiết kiệm thời gian cho QA nhưng không giải quyết ngay vấn đề đau đớn tức thời trên đường phố.
   * *Card #3 (Phân loại khiếu nại Vinhomes):* Khá phổ biến và đã có nhiều hệ thống rule-based hoặc mô hình ML cổ điển làm tốt. Tuy có giá trị nhưng thiếu yếu tố rủi ro an toàn và điều kiện phức tạp (như vị trí GPS, mức pin, khoảng cách) để trình diễn sức mạnh lý luận của LLM như bài toán của Xanh SM.
