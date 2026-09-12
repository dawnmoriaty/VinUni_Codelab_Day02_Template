# 02 - Deep-Dive Report: Vinhomes Resident Issue Triage

**Owner:** Tran Quoc Vuong  
**Status:** Proposal for controlled prototype  
**Evidence status:** Metrics below are planning assumptions and must be baselined from anonymized tickets before production.

## 1. Current-State Workflow

```text
Cư dân gửi phản ánh
  -> [Handoff] Tổng đài/ứng dụng nhận yêu cầu
  -> Nhân viên đọc nội dung và ảnh (3-5 phút)
  -> Tra bảng tòa nhà/bộ phận (2-3 phút) [BOTTLENECK]
  -> Tạo phiếu thủ công (3-4 phút) [BOTTLENECK]
  -> [Handoff] Ban kỹ thuật/CSKH tiếp nhận
  -> Phản hồi trạng thái cho cư dân

Tổng thời gian giả định: 8-12 phút/yêu cầu.
```

## 2. Problem Statement - 6 Fields

| Field | Nội dung |
|---|---|
| **1. Actor / Operator** | Nhân viên tổng đài hoặc CSKH tiếp nhận phản ánh; ban quản lý và đội kỹ thuật xử lý sau đó. |
| **2. Current Workflow** | Nhân viên đọc nội dung tự do, xem ảnh nếu có, tra bảng tuyến xử lý theo tòa nhà/chủ đề, tạo phiếu và chuyển sang bộ phận liên quan. Các trường thường nhập gồm tòa nhà, loại sự cố, mức độ và mô tả. |
| **3. Bottleneck** | Phân biệt chủ đề/mức độ từ ngôn ngữ tự do và chọn đúng tuyến xử lý; nội dung thiếu tòa nhà hoặc có nhiều vấn đề dễ gây chuyển nhầm. |
| **4. Business Impact** | Với giả định 300 yêu cầu/ngày và 10 phút/yêu cầu, khoảng 50 giờ công/ngày dành cho nhập liệu và phân tuyến. Chuyển nhầm làm tăng thời gian phản hồi và số lần cư dân gọi lại. Cần xác minh các số này từ ticket log. |
| **5. Success Metric** | Prototype: ít nhất 90% yêu cầu có đủ trường bắt buộc trong 30 giây; macro-F1 phân loại tối thiểu 0.85 trên tập test được gắn nhãn; tỷ lệ chuyển nhầm dưới 5%; giảm thời gian nhập phiếu trung vị xuống dưới 2 phút. |
| **6. Operational Boundary** | AI chỉ phân loại, trích xuất thông tin và tạo draft phiếu. AI không được tự đóng ticket, cam kết thời gian sửa chữa, phán đoán trách nhiệm/phí, hay gửi phản hồi cuối cùng. Ticket khẩn, thiếu dữ liệu, liên quan an toàn hoặc confidence thấp phải chuyển người duyệt. |

## 3. Future-State Flow & AI Fit

**AI Fit:** LLM Feature được bao quanh bởi Rule/State Machine. Agentic loop không phù hợp vì việc tự gọi nhiều hệ thống và tự quyết định có thể tạo hành động ngoài phạm vi.

```text
Nhận yêu cầu
  -> Rule: kiểm tra spam, trường bắt buộc, dấu hiệu khẩn cấp
  -> [AI] LLM trích xuất JSON: building, category, priority, summary, confidence
  -> Rule: kiểm tra schema và mapping tuyến xử lý
  -> confidence >= 0.85 và không khẩn?
       | Có -> [HITL] nhân viên duyệt/chỉnh draft -> tạo ticket -> gửi trạng thái
       | Không -> [Fallback] xếp hàng thủ công, không tự route
  -> Lưu input/output/version để audit
```

### Structured output tối thiểu

```json
{
  "building": "Vinhomes Ocean Park - S2.05",
  "category": "elevator",
  "priority": "normal",
  "summary": "Thang máy dừng lâu ở tầng 8",
  "suggested_team": "building_maintenance",
  "confidence": 0.91,
  "needs_human_review": true
}
```

`needs_human_review` luôn là `true` trước khi tạo ticket chính thức; đây là chủ ý an toàn.

## 4. AI Safety and Fallback

- Dữ liệu gửi model phải loại bỏ tên, số điện thoại và thông tin định danh không cần thiết.
- Output không đúng JSON/schema, confidence thấp hơn 0.85, hoặc chứa tín hiệu nguy hiểm sẽ bị từ chối và chuyển hàng đợi thủ công.
- Nhân viên xem nội dung gốc cùng draft trước khi tạo ticket.
- Nếu model/API lỗi, giao diện giữ nguyên quy trình nhập thủ công.
- Log version prompt, model, timestamp, output và quyết định của nhân viên; không lưu secret/API key.

## 5. Readiness Evaluation

| Câu hỏi | Đánh giá | Bằng chứng cần bổ sung |
|---|---|---|
| Có dữ liệu mẫu sạch không? | **NOT YET** | Tối thiểu 500 ticket đã ẩn danh, có nhãn tuyến xử lý và chia train/test. |
| Rủi ro AI sai có kiểm soát không? | **GO có điều kiện** | Có schema validation, confidence threshold, HITL và fallback thủ công. |
| Stakeholder sẵn sàng thay đổi quy trình? | **NOT YET** | Cần pilot một tòa nhà và xác nhận SLA với ban quản lý. |

### Quyết định: NOT YET

Chưa nên triển khai production vì chưa có baseline và tập dữ liệu gắn nhãn. Có thể **GO cho prototype offline/pilot giới hạn** sau khi thu thập dữ liệu ẩn danh, đo macro-F1 và xác nhận mapping tuyến xử lý. Rule-based vẫn nên giữ cho các điều kiện cứng như ticket khẩn, schema, SLA và quyền gửi.
