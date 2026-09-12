### 📝 List bài toán của tôi:
| #     | Subsidiary   | Lens                                 | Mô tả ngắn bài toán                                                                                                                                                                                                                                      |
| ----- | ------------ | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | **VinFast**  | 🔁 Repetitive + ⏱️ Time-consuming    | **Xử lý hồ sơ bảo hành:** Nhân viên phải kiểm tra VIN, thời gian sử dụng, mileage, phụ tùng thay thế, hóa đơn và chính sách warranty để quyết định claim. AI có thể tự đọc hồ sơ, đối chiếu policy và phân loại **Approve / Review / Reject**.           |
| **2** | **VinFast**  | 🤖 AI-upgrade + Stakeholder Pain     | **Chẩn đoán lỗi xe tại Service Center:** Kỹ thuật viên phải tra DTC, service manual và lịch sử sửa chữa để tìm root cause. AI Diagnostic Copilot có thể đưa ra các nguyên nhân có xác suất cao và đề xuất sequence kiểm tra/phụ tùng.                    |
| **3** | **VinFast**  | 🔁 Repetitive                        | **Kiểm tra ngoại quan xe cuối dây chuyền:** Nhân viên phải kiểm tra scratch, dent, paint defect, gap/flush và lỗi lắp ráp. AI Computer Vision có thể kiểm tra 100% xe, phát hiện và phân loại defect tự động.                                            |
| **4** | **Xanh SM**  | ⏱️ Time-consuming + Stakeholder Pain | **Xử lý khiếu nại chuyến đi:** CSKH phải đọc nội dung chat/cuộc gọi, kiểm tra trip log, GPS, thời gian, giá cước rồi quyết định hướng xử lý. AI có thể tự phân loại complaint, truy xuất thông tin chuyến và đề xuất câu trả lời/compensation.           |
| **5** | **Vinhomes** | 🤖 AI-upgrade + Stakeholder Pain     | **Xử lý phản ánh của cư dân:** CSKH/BQL nhận rất nhiều phản ánh về thang máy, vệ sinh, parking, tiện ích, kỹ thuật... và phải chuyển ticket tới đúng bộ phận. AI có thể tự **phân loại → xác định mức độ ưu tiên → route tới đội xử lý → theo dõi SLA**. |


---

# 🃏 Phase 2 — QUICK-ASSESS (Cá nhân, 30 min)

Chọn **top 3 bài toán** từ danh sách trên và hoàn thiện **3 Quick Problem Cards** dưới đây (10 phút/card).

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #___                                     │
│                                                             │
│ Bài toán (1 câu): ________________________________________  │
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM  [ ] Vinhomes  │
│                     [ ] Vinmec   [ ] Khác (Ghi rõ)________  │
│                                                             │
│ Ai đang đau (Actor)? ______________________________________ │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                      │
│   1. ___ ──> 2. ___ ──> 3. ___ ──> 4. ___                   │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? ___ (⏱ ___ phút/lượt)      │
│ AI có thể nhảy vào hỗ trợ ở bước nào? _____________________ │
│                                                             │
│ Đo thành công bằng gì (Metric có số)? ______________________ │
│   VD: "Giảm thời gian soạn phản hồi từ 10 min ──> under 2 min"│
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [ ] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                      │
│                                                             │
│ Bài toán (1 câu): Kỹ thuật viên VinFast mất nhiều thời gian │
│ tra cứu và xác định root cause khi xe phát sinh lỗi.        │
│                                                             │
│ Công ty thành viên: [x] VinFast  [ ] Xanh SM  [ ] Vinhomes │
│                     [ ] Vinmec   [ ] Khác                   │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│ Kỹ thuật viên Service Center, Service Advisor, khách hàng.  │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                      │
│ 1. Đọc DTC/symptom                                          │
│    ──> 2. Tra service manual & lịch sử sửa chữa             │
│    ──> 3. Khoanh vùng nguyên nhân                           │
│    ──> 4. Test linh kiện                                    │
│    ──> 5. Chọn phương án sửa chữa/phụ tùng                  │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất?                            │
│ Tra cứu + khoanh vùng root cause (⏱ ~20–45 phút/lượt)*      │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                       │
│ Bước 2–3: tổng hợp DTC, VIN, repair history, manual và      │
│ đưa ra Top-N root causes + diagnostic sequence.             │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ - Giảm Mean Time To Diagnose: 30 min → <10 min              │
│ - Tăng First-Time Fix Rate: +10–15%                         │
│ - Giảm repeat repair: -15–20%                               │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [x] Agent│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                      │
│                                                             │
│ Bài toán (1 câu): Việc kiểm tra ngoại quan cuối dây chuyền  │
│ phụ thuộc nhiều vào con người, dễ bỏ sót defect nhỏ và      │
│ thiếu nhất quán giữa các inspector.                         │
│                                                             │
│ Công ty thành viên: [x] VinFast  [ ] Xanh SM  [ ] Vinhomes │
│                     [ ] Vinmec   [ ] Khác                   │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│ QC inspector, Quality Engineer, Production Manager, khách   │
│ hàng cuối.                                                  │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                      │
│ 1. Xe tới trạm QC                                           │
│    ──> 2. Inspector kiểm tra paint/body/interior            │
│    ──> 3. Ghi nhận defect                                   │
│    ──> 4. Phân loại severity                                │
│    ──> 5. Rework / release                                  │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất?                            │
│ Visual inspection + classification (⏱ ~3–8 phút/xe)*        │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                       │
│ Bước 2–4: Computer Vision tự detect scratch, dent, gap,      │
│ missing part, misalignment và phân loại severity.           │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ - Inspection coverage: sampling → 100%                      │
│ - Giảm inspection time: 5 min → <1 min/xe                   │
│ - Giảm defect escape: mục tiêu -30%                         │
│ - Recall >95% với nhóm defect trọng yếu                     │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] AI Vision      │
│                     [ ] Agent                               │
└─────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                      │
│                                                             │
│ Bài toán (1 câu): Nhân viên phải đọc và đối chiếu thủ công  │
│ nhiều thông tin để quyết định một warranty claim hợp lệ hay │
│ cần review thêm.                                            │
│                                                             │
│ Công ty thành viên: [x] VinFast  [ ] Xanh SM  [ ] Vinhomes │
│                     [ ] Vinmec   [ ] Khác                   │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│ Warranty reviewer, Service Advisor, Finance/Operations.     │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                      │
│ 1. Nhận claim                                               │
│    ──> 2. Đọc VIN/mileage/repair/parts                      │
│    ──> 3. Tra warranty policy                               │
│    ──> 4. Kiểm tra eligibility                              │
│    ──> 5. Approve / reject / escalate                       │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất?                            │
│ Đối chiếu claim với policy (⏱ ~15–30 phút/claim)*           │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                       │
│ Bước 2–4: Document AI + RAG trích xuất dữ liệu claim,       │
│ đối chiếu policy và đề xuất Approve / Review / Reject.      │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ - Processing time: 20 min → <5 min/claim                    │
│ - Auto-triage >70% claim đơn giản                           │
│ - Decision agreement với reviewer >95%                     │
│ - Giảm backlog >50%                                         │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [x] LLM  [x] Agent│
└─────────────────────────────────────────────────────────────┘
```