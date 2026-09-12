# 03 - AI Interaction Log & Reflection

**Người thực hiện:** Tran Quoc Vuong  
**Use case:** Phân loại và điều hướng phản ánh cư dân Vinhomes

## 1. AI đã hỗ trợ gì?

Tôi dùng AI như một thought-partner ở giai đoạn brainstorm và stress-test. AI giúp mở rộng danh sách pain point qua bốn lens, gợi ý các trường cần có trong quick card, và đặt câu hỏi phản biện về metric, actor, bottleneck và operational boundary. Tôi giữ quyết định cuối cùng bằng cách đối chiếu với rubric của worksheet.

AI cũng giúp chuyển quy trình thành các bước rõ ràng: nhận phản ánh, kiểm tra dữ liệu, phân loại, định tuyến, duyệt bởi nhân viên và fallback. Phần này hữu ích để phát hiện handoff giữa tổng đài và ban quản lý.

## 2. AI có thể trả lời sai hoặc hallucinate ở đâu?

- AI có thể trình bày các con số như số ticket/ngày, thời gian xử lý hoặc tỷ lệ chuyển nhầm như sự thật dù chưa có log nội bộ.
- AI có thể gán nhãn quá tự tin cho phản ánh mơ hồ, ví dụ trộn lỗi thang máy với lỗi điện.
- AI có thể đề xuất để model tự gửi thông báo hoặc tự đóng ticket, vượt quá quyền hạn vận hành.
- AI có thể đưa thông tin định danh của cư dân vào prompt nếu không có quy tắc bảo vệ dữ liệu.

Vì vậy, các số liệu trong bài này được ghi rõ là giả định cần xác minh, không dùng làm bằng chứng production.

## 3. Tôi đã sửa prompt và đặt ranh giới thế nào?

Tôi yêu cầu output theo JSON schema cố định gồm `building`, `category`, `priority`, `summary`, `suggested_team`, `confidence` và `needs_human_review`. Tôi đặt ngưỡng confidence 0.85; dưới ngưỡng này phải chuyển xử lý thủ công. Tôi cũng yêu cầu luôn bật HITL trước khi tạo ticket và cấm model đóng ticket, cam kết SLA, phán đoán phí/trách nhiệm hoặc gửi phản hồi cuối cùng.

Các luật cứng được tách khỏi LLM: kiểm tra trường bắt buộc, nhận diện tín hiệu khẩn cấp, validate schema và mapping tuyến xử lý. Khi API lỗi, JSON không hợp lệ hoặc có dấu hiệu rủi ro, hệ thống dùng fallback thủ công.

## 4. Bài học cá nhân

AI giúp tôi nhìn thấy nhiều khả năng nhanh hơn, nhưng không thay thế việc kiểm tra bằng dữ liệu thực tế. Một câu trả lời trôi chảy không chứng minh metric là đúng. Cách làm đáng tin cậy hơn là coi AI là công cụ tạo giả thuyết, ghi rõ giả định, yêu cầu output có cấu trúc và luôn giữ quyền quyết định ở con người với các hành động có tác động đến cư dân.

## 5. Kế hoạch kiểm chứng tiếp theo

1. Xin một tập ticket đã ẩn danh và gắn nhãn bởi nhân viên.
2. Đo baseline thời gian xử lý và macro-F1 của bộ phân loại hiện tại.
3. Chạy test adversarial cho prompt injection, dữ liệu thiếu, ticket khẩn và output sai schema.
4. Pilot offline, review mẫu lỗi cùng ban quản lý trước khi cho phép tạo ticket bán tự động.
