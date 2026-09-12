# Nhật Ký Tương Tác AI — Lab 02: AI Product Scoping

## 1. Tổng quan
Trong quá trình thực hiện Lab 02 về AI Product Scoping cho bài toán của Xanh SM, mình đã sử dụng kết hợp nhiều công cụ AI như ChatGPT (GPT-4o) và Claude 3.5 Sonnet. Mục tiêu chính là dùng AI như một "thought-partner" (đối tác tư duy) để khám phá vấn đề, xây dựng các Quick Cards, và đặc biệt là drafting System Prompt cho tính năng xử lý sự cố hết pin thực địa của tài xế.

## 2. AI Giúp Được Gì (Điểm Mạnh)
- **Brainstorm bài toán Phase 1:** Khi mình bí ý tưởng về pain point của tài xế, AI đã gợi ý được rất nhiều tình huống thực tế mà mình chưa nghĩ tới. Nổi bật nhất là case tài xế nhận cuốc khách đi xa nhưng pin dưới 15% và xung quanh không có trạm sạc.
- **Stress-test Quick Cards Phase 2:** Đây là phần ấn tượng nhất. Khi mình yêu cầu AI đóng vai CFO của Xanh SM để phản biện giải pháp, nó đưa ra những câu hỏi rất sắc bén về chi phí vận hành xe sạc lưu động (mobile charger) so với doanh thu cứu hộ.
- **Viết System Prompt Phase 4:** AI xử lý cực kỳ tốt việc định dạng và tuân thủ các quy tắc ranh giới 3 lớp (Always/Ask First/Never). Nó giúp cấu trúc prompt rõ ràng và chèn chính xác quy tắc phản hồi (như luôn bắt đầu bằng `[DRAFT_ONLY]`).
- **Tìm và ước lượng số liệu:** Dù không có số liệu nội bộ của hãng, AI vẫn đưa ra được những con số ước tính về thời gian chờ và chi phí cơ hội khá hợp lý để làm baseline tính toán ROI.

## 3. AI Sai Ở Đâu (Hallucination & Limitations)
Dù hữu ích, nhưng AI cũng lộ rõ một số điểm yếu và lỗi sai (hallucination) trong quá trình mình làm bài:
- **Bịa số liệu cụ thể:** AI có xu hướng khẳng định chắc nịch những con số không thể kiểm chứng, ví dụ như "Xanh SM hiện có 500 xe tại khu vực ngoại thành Hà Nội". Mình đã phải cẩn thận gạch bỏ những thông tin này.
- **Đề xuất giải pháp quá phức tạp (Over-engineering):** Ban đầu, AI đề xuất một hệ thống Multi-Agent tự động điều phối xe sạc, tự động ngắt hệ thống điều hòa trên xe qua IoT. Điều này vượt quá phạm vi bài toán đơn giản là hỗ trợ ra quyết định (Decision Support) bằng LLM cho Dispatcher.
- **Không hiểu rõ ràng buộc thực tế hạ tầng:** AI đôi khi gợi ý điều hướng tài xế đến các trạm sạc công cộng nhưng lại quên mất ràng buộc là trạm sạc VinFast có thể đang quá tải hoặc lỗi hỏng cục bộ.

## 4. Cách Sửa Prompt & Đặt Ranh Giới
Để khắc phục các lỗi trên, mình đã phải tinh chỉnh prompt (Prompt Engineering) khá nhiều:
- **Thêm role-play và bối cảnh cụ thể:** Thay vì hỏi "đánh giá giải pháp này", mình đổi thành: *"Đóng vai CFO khắt khe của Xanh SM, hãy chỉ ra 3 điểm rủi ro lớn nhất về mặt chi phí của giải pháp xe sạc lưu động."*
- **Kiểm soát tính xác thực:** Mình thêm câu lệnh bắt buộc: *"Chỉ sử dụng số liệu ước tính mang tính logic. Ghi rõ 'đây là số liệu giả định' nếu không có nguồn chính thức."*
- **Giới hạn scope chặt chẽ:** Để tránh AI "đi quá xa", mình bổ sung vào prompt: *"Chỉ đề xuất tính năng LLM text-based hỗ trợ Dispatcher. KHÔNG đề xuất hệ thống Agent tự hành, không viết tính năng giao tiếp trực tiếp với tài xế nếu chưa có sự duyệt của Dispatcher."*

## 5. Bài Học Rút Ra
Sau Lab 02, bài học lớn nhất của mình là: AI thực sự là một "thought-partner" xuất sắc, giúp tăng tốc quá trình ideation và cấu trúc văn bản, nhưng nó **không thể thay thế domain expertise** (kiến thức ngành). Mọi con số, giải pháp mà AI đưa ra đều cần con người verify lại để đảm bảo tính khả thi thực tế. Cuối cùng, "garbage in, garbage out" — prompt càng cụ thể, đặt ranh giới càng rõ ràng (như 3-tier operational boundary), thì output của AI mới thực sự có giá trị sử dụng.
