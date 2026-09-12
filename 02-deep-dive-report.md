# Deep-Dive Report — Vin Smart Future (GSM / Xanh SM Use Case)

Bài toán: **Xanh SM — Xử lý sự cố hết pin thực địa cho tài xế**

---

## Section 1: Phase 3.1 — Current-State Workflow Mapping

Quy trình xử lý sự cố hết pin thực địa hiện tại:

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │ 🔄  │ Bước 2       │ 🔄  │ Bước 3       │ 🔄  │ Bước 4       │ 🔄  │ Bước 5       │
│ Tài xế gọi   │ ──→ │ Điều phối    │ ──→ │ Tra cứu trạm │ ──→ │ Soạn tin     │ ──→ │ Gọi xe cứu   │
│ tổng đài báo │     │ viên tra cứu │     │ sạc VinFast  │     │ nhắn chỉ dẫn │     │ hộ nếu cần   │
│ hết pin      │     │ vị trí GPS xe│     │ còn trụ trống│     │ gửi tài xế   │     │              │
│ ⏱ 1 phút     │     │ ⏱ 2 phút     │     │ 🔴 ⏱ 5 phút  │     │ 🔴 ⏱ 5 phút  │     │ ⏱ 2 phút     │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

**Chú thích:**
* 🔴 **Bottleneck:** Bước 3 & Bước 4 chiếm nhiều thời gian nhất (tổng 10 phút).
* 🔄 **Handoff:** Chuyển giao thông tin thủ công giữa các bước.
* **Tổng thời gian xử lý thủ công (Total):** 15 phút/lượt.

---

## Section 2: Phase 3.2 — Problem Statement (6-field)

| Field | Nội dung |
|---|---|
| **1. Actor** | Điều phối viên Xanh SM (Dispatcher). |
| **2. Current Workflow** | 5 bước thủ công, tốn 15 phút/lượt (Từ việc tiếp nhận cuộc gọi, tra cứu GPS, tra cứu trạm sạc, soạn tin nhắn, cho đến việc gọi xe cứu hộ nếu cần thiết). |
| **3. Bottleneck** | Bước 3 & 4 (Tra cứu trạm sạc và soạn tin nhắn hướng dẫn) mất tổng cộng 10 phút. Quá trình tra cứu thủ công và soạn thảo tin nhắn rất dễ xảy ra lỗi và tốn thời gian. |
| **4. Business Impact** | Mỗi ngày có khoảng ~80 sự cố/ngày tại Hà Nội, gây lãng phí 20 giờ làm việc/ngày, đồng thời làm rò rỉ doanh thu ~15% do xe phải dừng hoạt động lâu. |
| **5. Success Metric** | Rút ngắn thời gian xử lý từ 15 min xuống dưới 3 min. Tỉ lệ chính xác đạt 98%. |
| **6. Operational Boundary** | **Luôn luôn (Always):** Tất cả kết quả của AI phải bắt đầu bằng tag `[DRAFT_ONLY]`.<br>**Hỏi trước (Ask First / HITL):** AI không được trực tiếp gửi tin nhắn cho tài xế mà không có sự phê duyệt của điều phối viên.<br>**Không bao giờ (Never):** Nếu pin < 5%, tuyệt đối không đề xuất trạm sạc cách > 5km, mà phải điều phối xe sạc di động. |

---

## Section 3: Phase 3.3 — Future-State Flow & AI Fit

* **AI Fit:** Phù hợp với **LLM Feature** (không phải Agent).
* **Lý do không chọn Agent:** Trong môi trường vận hành thời gian thực (real-time) liên quan đến phương tiện giao thông, an toàn là yếu tố cốt lõi. Việc giao toàn quyền quyết định cho một Autonomous Agent có thể dẫn đến rủi ro nghiêm trọng (ví dụ: điều hướng sai khiến xe cạn pin giữa đường, gây ách tắc giao thông). Do đó, cần áp dụng nguyên tắc **Separation of Duties**: AI đảm nhận phần trích xuất và soạn thảo tốn thời gian (LLM Feature), nhưng quyền quyết định và phê duyệt phải do con người kiểm soát (HITL).

**Future-State Flow:**

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Tài xế gọi   │ ──→ │ 🔵 AI tự động│ ──→ │ 🔵 AI soạn   │ ──→ │ 🟢 Điều phối │
│ tổng đài báo │     │ tra cứu GPS &│     │ nháp SMS chỉ │     │ viên kiểm tra│
│ hết pin      │     │ trạm sạc rảnh│     │ dẫn (Draft)  │     │ & gửi tài xế │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                                                                      ▼
                                                               ↩️ Fallback:
                                                               Nếu AI bị lỗi,
                                                               quy trình quay
                                                               về thủ công
                                                               (như cũ).
```

---

## Section 4: Phase 5 — EVALUATE

* **AI Readiness Checklist (3 items):**
    1. **Data Readiness (Sẵn sàng dữ liệu):** Có sẵn kết nối API lấy tọa độ GPS của xe theo thời gian thực và trạng thái các trụ sạc VinFast.
    2. **Process Readiness (Sẵn sàng quy trình):** Quy trình 5 bước hiện tại đã được chuẩn hóa rõ ràng, dễ dàng đưa AI vào tự động hóa Bước 2 & 3.
    3. **Value Readiness (Sẵn sàng giá trị):** Tác động kinh doanh rất lớn, tiết kiệm được 20 giờ lãng phí mỗi ngày và có khả năng giảm rò rỉ doanh thu 15%.

* **Decision:** **GO**

* **Justification (Biện luận):**
  Dự án hoàn toàn khả thi và nên được thực thi vì những lý do sau:
  - Bài toán hẹp, rõ ràng, có dữ liệu có sẵn.
  - Mang lại lợi ích ngay lập tức (giảm thời gian từ 15 phút xuống dưới 3 phút).
  - Các ranh giới an toàn đã được thiết lập chặt chẽ: AI chỉ đưa ra bản nháp (`[DRAFT_ONLY]`), ngăn chặn việc đề xuất trạm xa (>5km) khi pin yếu (<5%), và đảm bảo sự phê duyệt của con người thông qua bước HITL (Human-in-the-Loop) trong mọi thao tác xuất bản tin nhắn. Điều này giúp giảm thiểu tối đa rủi ro trong khi vẫn tối ưu hóa được phần lớn thời gian tra cứu và soạn thảo thủ công.
