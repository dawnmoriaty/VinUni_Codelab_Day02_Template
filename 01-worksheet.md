# Lab 02 — Worksheet: AI Product Scoping (Vin Smart Future)

---

## 🏛️ 1. Bối cảnh thực tế: Vin Smart Future (Vingroup)

**Vingroup** — Tập đoàn tư nhân lớn nhất Việt Nam — vừa sáp nhập toàn bộ các phòng ban công nghệ thuộc các công ty thành viên thành một đơn vị công nghệ thống nhất mang tên **Vin Smart Future**. 

Nhiệm vụ của **Vin Smart Future** là xây dựng các giải pháp AI, số hóa, và tự động hóa cốt lõi để nâng cao hiệu suất vận hành và trải nghiệm khách hàng xuyên suốt các công ty thành viên:
* 🚗 **VinFast:** Hệ thống xe điện thông minh (EV), trợ lý AI ảo trong xe, dự đoán bảo trì pin, và quản lý chuỗi cung ứng sản xuất.
* 🚕 **Xanh SM (GSM):** Vận hành đội xe taxi/xe máy điện thông minh, điều vận thông minh (Smart Dispatching), tối ưu hóa lộ trình di chuyển.
* 🏢 **Vinhomes:** Quản lý đô thị thông minh (Smart Cities), trợ lý cư dân thông minh, tối ưu hóa mức tiêu thụ năng lượng.
* 🏥 **Vinmec:** Y tế thông minh, chẩn đoán hình ảnh bằng AI, tối ưu hóa quản lý hồ sơ bệnh án.
* 🎢 **Vinpearl / VinWonders:** Trải nghiệm du lịch số hóa, quản lý phòng và luồng khách thông minh tại các khu vui chơi.

Trong buổi Lab hôm nay, nhóm của bạn sẽ đóng vai trò là **AI Product Engineer** tại **Vin Smart Future**, tiến hành tìm kiếm, scoping, phân tích độ khả thi, thiết lập ranh giới vận hành, và xây dựng một **bản mẫu kỹ thuật (prompt prototype)** cho một bài toán cụ thể thuộc một trong những mảng kinh doanh trên.

---

## 📊 2. Cơ cấu tính điểm bài lab

### 👥 Điểm nhóm (60 điểm)

| Gate | Điểm | Deliverable | Tiêu chí chấm |
|---|---:|---|---|
| **G1. Workflow Mapping** | 20 | Problem Deep-Dive | Vẽ chi tiết quy trình hiện tại: các bước, handoff, thời gian, bottleneck |
| **G2. Problem Statement** | 20 | Problem Deep-Dive | Problem Statement 6-field bám sát thực tế, metric có số và ranh giới rõ ràng |
| **G3. AI Fit & Future Flow** | 10 | Problem Deep-Dive | So sánh Rule vs LLM vs Agent, future flow có bước AI, ranh giới và Fallback |
| **G4. Decision Quality** | 10 | Problem Deep-Dive | Quyết định Go/Not Yet/No-Go trung thực và có chứng cứ rõ ràng |

### 👤 Điểm cá nhân (40 điểm)

| Gate | Điểm | Deliverable | Tiêu chí chấm |
|---|---:|---|---|
| **I1. Scan & Cards** | 15 | Quick Cards | Liệt kê 5 problems sử dụng 3 lenses, hoàn thiện 3 quick cards chất lượng |
| **I2. Prototyping** | 10 | 02-lab/ | Chạy thử nghiệm programmatic prompt prototype thành công |
| **I3. AI Log & Reflection** | 15 | 03-ai-log.md | Phản ánh trung thực về việc dùng AI làm thought-partner (giúp gì, sai gì, sửa gì) |

---

# 🚀 Phase 0 — worked Example: Xanh SM Intelligent Dispatcher (15 min)

*Giảng viên walk-through ví dụ thực tế từ Vin Smart Future để bạn hiểu rõ cách scoping một bài toán AI.*
Đọc chi tiết worked example tại file [02-deliverable-example.md](02-deliverable-example.md).

---

# 🔍 Phase 1 — SCAN (Cá nhân, 20 min)

Hãy sử dụng **4 Lenses** dưới đây để quét qua hoạt động vận hành của các công ty thành viên Vingroup. Ghi lại **ít nhất 5 bài toán/bottleneck** thực tế.

### 4 Lenses tìm bài toán AI cho Vingroup:
1. **Lặp lại (Repetitive):** Tác vụ lặp đi lặp lại nhiều lần hằng ngày. (Ví dụ: So khớp hóa đơn sạc điện tại VinFast, route lại chuyến taxi tại Xanh SM).
2. **Tốn thời gian (Time-consuming):** Tác vụ ngốn thời gian xử lý thủ công của nhân viên. (Ví dụ: Soạn thảo phản hồi đánh giá 1-star của cư dân Vinhomes).
3. **AI có thể tốt hơn (AI-upgrade):** Dịch vụ khách hàng hiện tại còn chậm hoặc phản hồi rập khuôn. (Ví dụ: Chatbot CSKH Vinpearl hỗ trợ đặt vé vui chơi).
4. **Pain từ người khác (Stakeholder Pain):** Bottleneck khiến khách hàng hoặc nhân viên thực địa phàn nàn. (Ví dụ: Tài xế Xanh SM phàn nàn về việc hệ thống gợi ý điểm đón khách không chính xác).

> [!TIP]
> **🤖 AI Prompts — Partner brainstorm:**
> Hãy sử dụng prompt sau để brainstorm các bài toán thực tế nếu bạn chưa có ý tưởng:
> *"Tôi là AI Engineer tại Vin Smart Future (Vingroup). Tôi đang tìm kiếm các pain point vận hành cụ thể có thể tối ưu bằng AI cho mảng [Chọn một: VinFast / Xanh SM / Vinhomes / Vinmec]. Hãy gợi ý cho tôi 5 quy trình nghiệp vụ thủ công, tốn nhiều thời gian và gây rò rỉ hiệu suất kèm con số thống kê ước tính về tổn thất."*

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
```
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

```
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
> [!TIP]
> **🤖 AI Prompts — Stress-Test thẻ bài toán:**
> Hãy dán nội dung thẻ bài toán của bạn vào LLM để nhận phản biện:
> *"Đây là một thẻ bài toán vận hành tôi đề xuất cho Vin Smart Future: [Dán nội dung]. Hãy đóng vai trò là một CFO và Trưởng phòng Vận hành cực kỳ khắt khe, chỉ ra cho tôi 3 điểm yếu về logic, metric, và giải thích vì sao rule-based code thông thường có thể giải quyết bài toán này tốt hơn là dùng AI."*

---

# 🏗️ Phase 3 — DEEP-DIVE (Nhóm, 85 min)

## 3.1. Current-State Workflow Mapping (25 min)
**Vẽ quy trình hiện tại lên bảng/giấy A3.** Sử dụng các ký hiệu:
* 🔴 **Bottleneck:** Bước gây tắc nghẽn, tốn thời gian, hoặc sai sót nhiều nhất.
* 🔄 **Handoff:** Điểm chuyển giao thông tin giữa người và hệ thống, hoặc giữa các bộ phận.
* Ghi rõ thời gian vận hành trung bình: **Tổng cộng = ____ phút/lượt**.

## 3.2. Problem Statement (6-field) & Metrics (15 min)
Điền đầy đủ 6 trường thông tin của bài toán:

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Ai đang thực hiện tác vụ hằng ngày? |
| **2. Current Workflow** | Mô tả tóm tắt quy trình thủ công hiện tại và công cụ sử dụng. |
| **3. Bottleneck** | Bước nào chậm, lỗi, hoặc cần xử lý ngôn ngữ tự động nhiều nhất? |
| **4. Business Impact** | Tổn thất thực tế đo bằng thời gian, chi phí, hoặc SLA của Vingroup. |
| **5. Success Metric** | AI giải quyết được thì đạt ngưỡng số mấy? (Ví dụ: *"85% vé được phân loại dưới 10s"*). |
| **6. Operational Boundary** | AI được phép làm gì, TUYỆT ĐỐI không được làm gì, điểm nào cần duyệt? |

## 3.3. Future-State Flow & AI Fit (25 min)
* **Xác định mức AI Fit (AI-Fit Matrix):** Giải pháp thuộc nhóm nào? [ ] Rule / State-Machine [ ] LLM Feature [ ] Agentic Loop.
* **Vẽ Future-State Flow:** Đánh dấu rõ:
  * 🔵 **AI Step:** Tác vụ LLM xử lý.
  * 🟢 **Human Step (HITL):** Bước con người phê duyệt/review (Human-in-the-loop).
  * ↩️ **Fallback:** Kế hoạch dự phòng khi LLM trả về kết quả lỗi hoặc không tự tin.
Bài toàn 2
Khách hàng đưa xe vào Service Center
              │
              ▼
① Service Advisor tiếp nhận
              │
              🔄 Handoff
              ▼
② Kỹ thuật viên đọc DTC + triệu chứng
              │
              ▼
③ Tra Service Manual / Knowledge Base
              │
              🔴 BOTTLENECK
              ▼
④ Đối chiếu lịch sử sửa chữa + dữ liệu xe
              │
              ▼
⑤ Khoanh vùng Root Cause
              │
              🔄 Handoff
              ▼
⑥ Kiểm tra / thay thử linh kiện
              │
              ▼
⑦ Test lại → đóng Repair Order

| Field                       | Nội dung                                                                                                                                                                                               |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Actor / Operator**     | **Technician / Service Advisor** tại VinFast Service Center                                                                                                                                            |
| **2. Current Workflow**     | Tiếp nhận xe → đọc DTC/symptom → tra Service Manual → tìm repair history → phân tích root cause → diagnostic test → sửa chữa → test lại                                                                |
| **3. Bottleneck**           | Tra cứu và tổng hợp knowledge ở bước ③–⑤. Thông tin nằm ở nhiều nguồn và technician phải tự xác định mối liên hệ giữa DTC, symptom, lịch sử sửa chữa và linh kiện.                                     |
| **4. Business Impact**      | Tăng thời gian diagnosis, tăng vehicle downtime, tăng khả năng thay nhầm linh kiện và repeat repair; đồng thời chiếm thời gian của technician có kinh nghiệm.                                          |
| **5. Success Metric**       | **Mean Time To Diagnose: 40 → ≤15 phút**; **First-Time Fix Rate: +10%**; **Repeat Repair Rate: -15%**                                                                                                  |
| **6. Operational Boundary** | AI **chỉ đề xuất** root cause, diagnostic sequence và relevant service documents. **Không tự quyết định thay linh kiện hoặc đóng repair order.** Technician phải xác nhận trước mọi thao tác sửa chữa. |

                  VIN / DTC / Symptom
                         │
                         ▼
                ┌──────────────────┐
                │ 🔵 AI: Context   │
                │ retrieval        │
                └────────┬─────────┘
                         │
              ┌──────────▼──────────┐
              │ 🔵 AI Diagnostic     │
              │ Copilot              │
              │                      │
              │ • Root causes       │
              │ • Evidence          │
              │ • Diagnostic steps  │
              │ • Relevant manuals  │
              └──────────┬──────────┘
                         │
                         ▼
                Confidence ≥ threshold?
                    /             \
                  YES              NO
                   │                │
                   ▼                ▼
             🟢 Technician       ↩️ Fallback
                Review             │
                   │               ▼
                   │          Manual search /
                   │          Senior technician
                   │
                   ▼
            🟢 Technician
              thực hiện test
                   │
                   ▼
             Result / Evidence
                   │
                   ▼
             🔵 AI cập nhật
             hypothesis
                   │
                   ▼
             🟢 Technician
               xác nhận
                   │
                   ▼
             Repair / Close


Vai trò từng lớp
🔵 AI Step

AI làm những việc mà LLM/RAG có lợi thế:

Đọc và hiểu symptom tự nhiên.
Retrieve đúng đoạn Service Manual.
Tổng hợp repair history.
Xếp hạng các root cause.
Giải thích “vì sao AI nghĩ nguyên nhân này có khả năng cao”.
Sinh diagnostic sequence.
🟢 Human-in-the-loop

Technician vẫn quyết định:

AI đề xuất → Technician kiểm chứng → Technician thực hiện.

Đặc biệt không để AI tự:

quyết định thay battery;
thay HV component;
disable safety system;
đóng warranty;
kết luận xe đã an toàn.
↩️ Fallback

Nếu:

Confidence thấp
OR
Không tìm được evidence
OR
Dữ liệu mâu thuẫn

→ không đoán.

Chuyển sang:

Manual Knowledge Base
        ↓
Senior Technician
        ↓
Engineering escalation
🎯 AI-Fit Matrix
Thành phần	Công nghệ	Lý do
Check VIN / DTC format	Rule	Deterministic
Warranty / safety constraint	Rule	Không nên để LLM tự quyết
Search Service Manual	RAG	Semantic retrieval
Symptom → root cause	LLM	Reasoning trên context
Diagnostic sequence	LLM + Rule	AI đề xuất, rule kiểm soát
Iterative diagnosis	Agentic Loop	Quan sát kết quả test → cập nhật hypothesis
Final repair decision	Human	Safety-critical

| Thành phần                   | Công nghệ        | Lý do                                       |
| ---------------------------- | ---------------- | ------------------------------------------- |
| Check VIN / DTC format       | **Rule**         | Deterministic                               |
| Warranty / safety constraint | **Rule**         | Không nên để LLM tự quyết                   |
| Search Service Manual        | **RAG**          | Semantic retrieval                          |
| Symptom → root cause         | **LLM**          | Reasoning trên context                      |
| Diagnostic sequence          | **LLM + Rule**   | AI đề xuất, rule kiểm soát                  |
| Iterative diagnosis          | **Agentic Loop** | Quan sát kết quả test → cập nhật hypothesis |
| Final repair decision        | **Human**        | Safety-critical                             |

                 ┌───────────────┐
                 │ Service App   │
                 └───────┬───────┘
                         │
              VIN / DTC / Symptom
                         │
                         ▼
                 ┌───────────────┐
                 │ Context Layer │
                 └───────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Repair History   Service KB    Vehicle Data
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                 ┌───────────────┐
                 │ LLM + RAG     │
                 │ Diagnostic AI │
                 └───────┬───────┘
                         ▼
                 Confidence Check
                         │
                         ▼
                  🟢 Technician
                         │
                         ▼
                  Repair System
***Giảm thời gian technician tìm kiếm và tổng hợp thông tin chẩn đoán bằng AI Diagnostic Copilot, từ đó giảm Mean Time To Diagnose và tăng First-Time Fix Rate, trong khi mọi quyết định sửa chữa vẫn thuộc về technician***
# 💻 Phase 4 — TECHNICAL PROMPT PROTOTYPE (Nhóm, 30 min)

Để đảm bảo kỹ sư của Vin Smart Future luôn giữ vững năng lực lập trình, nhóm của bạn sẽ tiến hành **lập trình bản mẫu prompt** trực tiếp trên **Gemini 2.5 Flash** bằng Python để stress-test hệ thống.

### Hướng dẫn thực hiện:
1. Mở file [starter-code/prompt_prototype.py](starter-code/prompt_prototype.py) bằng VS Code/Cursor.
2. Hoàn thiện các nội dung sau:
   * **System Prompt:** Viết chỉ thị cực kỳ nghiêm ngặt quy định vai trò, nhiệm vụ, định dạng output và **Operational Boundary (Ranh giới cấm)** của mô hình.
   * **Structured Output:** Định nghĩa định dạng JSON output rõ ràng.
   * **Adversarial Test Cases:** Viết ít nhất 3 prompts "tấn công" (Adversarial inputs) cố tình dụ AI vượt ranh giới hoặc đưa ra câu trả lời không được phép để kiểm tra xem ranh giới của bạn có thực sự vững chắc.
3. Chạy file python:
   ```bash
   python3 prompt_prototype.py
   ```
4. Kiểm tra xem các ranh giới an toàn có bị LLM phá vỡ hay không và ghi lại kết quả vào worksheet.

---

# 🏁 Phase 5 — EVALUATE (Nhóm, 20 min)

### AI Readiness Checklist:
1. [ ] Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test?
2. [ ] Rủi ro khi AI sai có nằm trong tầm kiểm soát (qua HITL hoặc Fallback)?
3. [ ] Stakeholders sẵn sàng thay đổi quy trình làm việc cũ?

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:
[ ] **GO (Bắt đầu xây dựng Prototype):** Bắt đầu phát triển với scope hẹp.
[ ] **NOT YET (Cần tích lũy thêm dữ liệu/xác lập baseline):** Trì hoãn để chuẩn bị thêm.
[ ] **NO-GO (Không khả thi / Rule-based tốt hơn):** Hủy bỏ dự án AI này.

**Justification (Lý giải quyết định dựa trên bằng chứng kỹ thuật và chi phí):**
> *Viết lý giải chi tiết tại đây*

---

# 📝 Phase 6 — REFLECTION (Cá nhân)
*Ghi nhận phản ánh của cá nhân bạn về việc phối hợp với AI trong buổi học hôm nay vào file `03-ai-log.md`.*
