# 03 - AI Log & Reflection

## 1. Tôi đã dùng AI như thế nào?

Tôi dùng AI như một thought-partner trong ba việc: brainstorm các pain point thuộc nhiều công ty Vingroup, phản biện Quick Problem Cards, và kiểm tra operational boundary cho use case Xanh SM. Tôi không dùng câu trả lời của AI như bằng chứng vận hành; các con số trong bài đều được ghi là giả định cần xác minh.

## 2. Những phần AI hỗ trợ tốt

- AI giúp mở rộng danh sách bài toán theo bốn lens thay vì chỉ tập trung vào một công ty.
- AI gợi ý bổ sung actor, workflow, bottleneck và metric có baseline/mục tiêu.
- AI chỉ ra rằng ngưỡng pin, khoảng cách, tính tương thích trạm và quyền gửi phải là rule cứng, không để LLM tự suy đoán.
- Tôi nhận ra bản đồ đã giải quyết phần “trạm nằm ở đâu”. Vì vậy tôi chỉnh scope: AI không làm bản đồ thay tài xế, mà hỗ trợ incident response bằng cách đối chiếu snapshot availability, timestamp, connector, pin và phương án cứu hộ rồi tạo draft cho dispatcher.
- AI hỗ trợ tạo các prompt tấn công để kiểm tra khả năng bỏ qua `[DRAFT_ONLY]`, tự gửi tin và đề xuất trạm nguy hiểm.

## 3. Lỗi hoặc hallucination đã phát hiện

AI có xu hướng đưa ra số liệu trông rất cụ thể như số sự cố/ngày, tỷ lệ hủy chuyến hoặc số giờ tiết kiệm mà không có nguồn. Nếu đưa các số đó vào báo cáo như số liệu thật, kết luận GO sẽ thiếu cơ sở. AI cũng có thể tự điền địa chỉ, trạng thái trạm hoặc mã xe không có trong input.

## 4. Cách tôi sửa prompt và ranh giới

Tôi bổ sung các điều kiện:

1. Chỉ sử dụng dữ liệu được cung cấp; nếu thiếu phải trả `manual_review`, không được bịa.
2. Pin dưới 5% không được đề xuất trạm cách trên 5 km; phải ưu tiên `dispatch_mobile_charger`.
3. Mọi nội dung gửi tài xế chỉ là draft và bắt buộc bắt đầu bằng `[DRAFT_ONLY]`.
4. Không được tự gọi công cụ, tự gửi tin, tự điều xe hay tự hủy chuyến.
5. Output phải là JSON có schema cố định, confidence và lý do.

Tôi đồng thời tách safety gate bằng rule khỏi LLM. Như vậy prompt không phải lớp bảo vệ duy nhất.

## 5. Bài học và giới hạn

Kết quả tốt của một vài test không chứng minh hệ thống an toàn trong production. Cần test nhiều biến thể ngôn ngữ, dữ liệu thiếu, dữ liệu mâu thuẫn và trạng thái trạm thay đổi. Cần đo precision/recall hoặc tỷ lệ đề xuất hợp lệ, P50/P95 latency, tỷ lệ manual review và tỷ lệ lỗi nghiêm trọng. Con người vẫn chịu trách nhiệm cuối cùng trong pilot.

## 6. Tự đánh giá

AI hữu ích nhất khi được dùng để đặt câu hỏi phản biện và tạo test case, không phải để thay thế việc xác minh quy trình. Sau buổi lab, bước tiếp theo của tôi là phỏng vấn dispatcher, lấy log đã ẩn danh và đối chiếu từng giả định trong báo cáo với dữ liệu thực tế.
