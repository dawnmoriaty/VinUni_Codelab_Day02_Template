# 02 - Deep-Dive Report: Xanh SM Field Battery Incident Copilot

## 1. Executive Summary

Dispatcher của Xanh SM hiện xử lý sự cố pin bằng nhiều màn hình và cuộc gọi. Bản đồ đã giúp tài xế tìm trạm, vì vậy đây **không phải** đề xuất xây một bản đồ mới hoặc bắt tài xế phụ thuộc vào dispatcher để xem vị trí trạm. Vấn đề nằm ở lớp incident response: bản đồ thường không trả lời đầy đủ liệu dữ liệu có mới không, trạm còn chỗ thực tế không, đầu nối có tương thích không, xe với mức pin hiện tại có thể đi an toàn không, và có cần cứu hộ hay không.

Đề xuất là một **dispatcher co-pilot**: hệ thống gom các dữ liệu đã được xác thực từ ticket/telematics/dữ liệu trạm, áp dụng safety rules, dùng Gemini 2.5 Flash để giải thích phương án và soạn hướng dẫn dạng nháp, sau đó dispatcher duyệt trước khi gửi. AI không tự điều xe, không tự gửi tin và không thay thế quy trình cứu hộ.

**Quyết định:** GO với prototype hẹp, offline trước rồi mới pilot có giám sát.

## 2. Current-State Workflow

1. **Tiếp nhận:** Tài xế gọi hoặc tạo ticket, cung cấp biển số, GPS và pin. (Dispatcher, 2 phút)
2. **Xác minh incident:** Dispatcher đối chiếu dữ liệu ticket với telematics/GPS, timestamp, tình trạng xe và mức độ an toàn; hỏi lại nếu thiếu hoặc mâu thuẫn. (Dispatcher, 3 phút, **BOTTLENECK**)
3. **Đối chiếu phương án:** Dispatcher dùng bản đồ và dashboard vận hành như các nguồn khác nhau để kiểm tra availability theo thời điểm, loại đầu nối, dòng xe, khoảng cách, tình trạng đường và ngưỡng pin. (Dispatcher, 4 phút, **BOTTLENECK**)
4. **Ra quyết định và soạn hướng dẫn:** Dispatcher chọn đi trạm, chờ an toàn hoặc cứu hộ; tự viết nội dung, địa chỉ, điều kiện và kênh liên lạc. (Dispatcher, 5 phút, **BOTTLENECK**)
5. **Điều phối:** Dispatcher kiểm tra lần cuối rồi gửi hoặc gọi cứu hộ. (Dispatcher, 1 phút)

**Tổng thời gian giả định:** 15 phút/lượt. Cần đo P50/P95, không chỉ dùng trung bình.

**Handoffs:** Tài xế -> dispatcher tại bước 1; telematics/GPS -> dispatcher tại bước 2; bản đồ và dashboard trạm -> dispatcher tại bước 3; dispatcher -> tài xế/cứu hộ ở bước 5. Bản đồ là nguồn tham khảo vị trí; dispatcher vẫn cần xác minh dữ liệu vận hành và chịu trách nhiệm quyết định.

## 3. Problem Statement - 6 Fields

| Field | Nội dung |
|---|---|
| **1. Actor / Operator** | Dispatcher thuộc Trung tâm Điều vận Xanh SM; tài xế là người cung cấp và nhận thông tin. |
| **2. Current Workflow** | Dispatcher tiếp nhận sự cố, đối chiếu ticket với telematics/GPS và timestamp, dùng bản đồ cùng dashboard vận hành để xác minh availability, connector, khoảng cách và khả năng tự di chuyển, rồi chọn phương án và tự soạn hướng dẫn. Bản đồ đã có sẵn nhưng không thay thế bước xác minh incident đa nguồn. Quy trình 5 bước, baseline giả định 15 phút/lượt. |
| **3. Bottleneck** | Tổng hợp và đối chiếu thủ công ở bước 2-4, dự kiến 12 phút/lượt; dễ dùng dữ liệu stale, nhầm trạng thái trạm/connector hoặc đánh giá sai việc xe có thể đi đến trạm. Đây là bottleneck quyết định an toàn, không phải thao tác tìm vị trí đơn thuần. |
| **4. Business Impact** | Xe nằm chờ lâu làm giảm thời gian sẵn sàng nhận chuyến, tăng tải dispatcher và tăng nguy cơ hủy chuyến. Ví dụ kế hoạch để kiểm chứng: 80 sự cố/ngày x 10 phút = 13,3 giờ công/ngày tại baseline. Đây chưa phải số liệu sản xuất. |
| **5. Success Metric** | P50 thời gian từ ticket đủ dữ liệu đến draft dưới 3 phút; độ chính xác trạm hợp lệ tối thiểu 98% trên tập test; 100% output có `[DRAFT_ONLY]`; 0 hành động gửi tự động trong pilot. |
| **6. Operational Boundary** | Được đọc dữ liệu sự cố và candidate trạm đã được hệ thống cung cấp, kiểm tra timestamp/điều kiện bằng rule, tóm tắt lựa chọn và soạn draft. Cấm coi bản đồ là xác nhận availability, cấm tự gửi, tự hủy chuyến, tự điều xe cứu hộ, tự bịa dữ liệu hoặc đề xuất trạm ngoài candidate đã xác minh. Pin <5%: không đề xuất trạm >5 km, ưu tiên mobile charger/cứu hộ. Confidence thấp, dữ liệu thiếu/mâu thuẫn/stale hoặc ca nguy hiểm: chuyển người xử lý. |

## 4. AI Fit

| Lựa chọn | Đánh giá |
|---|---|
| **Rule/State Machine** | Bắt buộc cho ngưỡng pin, khoảng cách, tương thích đầu nối, trạm hoạt động và quyền gửi. Rule dễ kiểm thử và không nên giao cho LLM. |
| **LLM Feature** | Phù hợp để chuẩn hóa mô tả tiếng Việt, giải thích lựa chọn và soạn tin nhắn nháp thân thiện từ dữ liệu đã lọc. |
| **Agentic Loop** | Chưa chọn ở prototype. Agent tự gọi nhiều công cụ và tự hành động làm tăng blast radius; chưa có bằng chứng cần thiết. |

**Kiến trúc chọn:** Rule safety gate -> LLM draft -> JSON schema validation -> dispatcher review -> hệ thống gửi. LLM không được quyết định vượt qua safety gate.

## 5. Future-State Flow

1. **Dispatcher** nhập hoặc xác nhận biển số, vị trí, pin, timestamp và tình trạng xe; hệ thống nhận thêm snapshot candidate trạm từ nguồn vận hành.
2. **Rule gate** kiểm tra dữ liệu bắt buộc, độ mới, pin, khoảng cách, loại đầu nối và trạng thái trạm. Thiếu dữ liệu thì chuyển manual review. Bản đồ vẫn được giữ trong giao diện để dispatcher kiểm tra trực quan, nhưng không phải quyết định tự động.
3. **AI step (LLM)** nhận chỉ dữ liệu đã lọc, trả JSON gồm hành động, lý do, draft và confidence; LLM không tự tìm kiếm hoặc bịa candidate.
4. **Rule validator** kiểm tra schema, tag `[DRAFT_ONLY]`, cấm gửi, và kiểm tra lại điều kiện pin <5%.
5. **Human step (HITL)** dispatcher kiểm tra lại bản đồ, timestamp/availability, trạm, nội dung và bấm duyệt. Human review có ý nghĩa vì trạng thái thực địa có thể thay đổi nhanh hơn snapshot dữ liệu.
6. **Hệ thống vận hành** chỉ gửi sau thao tác duyệt; lưu audit log gồm input version, output, người duyệt và thời gian.

**Fallback:** Nếu API lỗi, output không hợp lệ, confidence thấp, dữ liệu không nhất quán hoặc không có trạm phù hợp, hệ thống không gọi hành động tự động và trả về `manual_review`. Dispatcher quay lại quy trình hiện tại/call cứu hộ.

## 6. Prompt Prototype & Boundary Tests

Prototype nằm tại `starter-code/prompt_prototype.py`. Prototype có:

- System prompt quy định role, nguồn dữ liệu, JSON schema và boundary.
- 3 adversarial inputs: ép bỏ draft tag, ép chỉ trạm xa khi pin nguy hiểm, và prompt injection yêu cầu bịa dữ liệu/tự điều cứu hộ.
- Chế độ offline deterministic để kiểm tra safety assertions không cần API key.
- Chế độ Gemini dùng biến môi trường `GEMINI_API_KEY` hoặc `GOOGLE_API_KEY`.

Kết quả kiểm thử offline dự kiến và cần được chạy lại:

| Test | Kỳ vọng | Kết quả kiểm tra |
|---|---|---|
| Bypass `[DRAFT_ONLY]` | Vẫn có tag, không tự gửi | PASS sau khi chạy script |
| Pin 2%, trạm 8 km | `dispatch_mobile_charger`, không đề xuất trạm xa | PASS sau khi chạy script |
| Prompt injection/bịa dữ liệu | Từ chối, `manual_review`, không gọi công cụ | PASS sau khi chạy script |

## 7. AI Readiness Checklist & Decision

- [x] Có thể tạo tập dữ liệu mẫu đã ẩn thông tin cá nhân gồm ticket, pin, GPS, dòng xe và trạng thái trạm để test offline.
- [x] Rủi ro được giới hạn bằng rule gate, schema validation, HITL, audit log và fallback manual.
- [ ] Chưa có bằng chứng stakeholder sẵn sàng thay đổi quy trình; cần phỏng vấn dispatcher và duyệt pilot.

**Quyết định: GO có điều kiện.** Bắt đầu bằng prototype và shadow mode, không gửi thật. Chỉ chuyển sang pilot khi có tối thiểu 100-200 case đã ẩn danh, baseline P50/P95, danh sách mapping loại xe/trạm được xác nhận, tiêu chí đánh giá 98% và owner chịu trách nhiệm review. Nếu không thu thập được dữ liệu hoặc không có dispatcher trực review, quyết định phải chuyển thành NOT YET.

## 8. Risks, Controls & Next Steps

| Rủi ro | Kiểm soát |
|---|---|
| Dữ liệu GPS/pin stale | Hiển thị timestamp; quá hạn thì manual review. |
| Trạm thay đổi trạng thái | Chỉ dùng snapshot có thời gian; validator kiểm tra lại trước khi duyệt. |
| LLM bịa địa chỉ hoặc hành động | Không cho LLM gọi tool; chỉ cho chọn từ candidate đã cung cấp; kiểm tra schema và allowlist. |
| Dispatcher tin tuyệt đối vào AI | Hiển thị lý do, confidence và yêu cầu click duyệt bắt buộc. |
| Lộ thông tin cá nhân | Tối thiểu hóa dữ liệu, ẩn danh trong test, phân quyền và lưu audit log. |

**Next steps:** (1) đo baseline thật, (2) thu thập/ẩn danh dữ liệu, (3) đánh giá offline, (4) shadow mode không gửi, (5) review an toàn, (6) pilot scope hẹp với rollback.
