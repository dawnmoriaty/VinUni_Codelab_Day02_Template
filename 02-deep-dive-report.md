# Deep-Dive Report — Vin Smart Future (GSM / Xanh SM)

Bài toán: **Xanh SM — Xử lý sự cố hết pin thực địa cho tài xế**

---

## Phase 3.1 — Current-State Workflow Mapping

### Quy trình hiện tại (As-Is) — 100% thủ công

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │ 🔄  │ Bước 2       │     │ Bước 3       │     │ Bước 4       │ 🔄  │ Bước 5       │
│ Tài xế gọi   │ ──→ │ Dispatcher   │ ──→ │ Tra cứu trạm │ ──→ │ Soạn tin     │ ──→ │ Gọi xe cứu   │
│ tổng đài báo │     │ tra cứu vị   │     │ sạc VinFast  │     │ nhắn chỉ dẫn │     │ hộ nếu cần   │
│ hết pin      │     │ trí GPS xe   │     │ còn trụ trống│     │ gửi tài xế   │     │              │
│              │     │              │     │              │     │              │     │              │
│ Ai: Tài xế   │     │ Ai: Dispatch │     │ Ai: Dispatch │     │ Ai: Dispatch │     │ Ai: Dispatch │
│ ⏱ 1 phút     │     │ ⏱ 2 phút     │     │ 🔴 ⏱ 5 phút  │     │ 🔴 ⏱ 5 phút  │     │ ⏱ 2 phút     │
│ In: Điện thoại│     │ In: Biển số  │     │ In: Toạ độ   │     │ In: Raw data │     │ In: Quyết định│
│ Out: Log sự cố│     │ Out: Toạ độ  │     │ Out: Trạm sạc│     │ Out: SMS     │     │ Out: Lệnh    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
🔄 = Handoff (chuyển giao)     🔴 = Bottleneck
⏱ Tổng thời gian: 15 phút/lượt × ~80 sự cố/ngày = 20 giờ lãng phí/ngày
```

**Pain points hiện tại:**
- Bước 3–4 chiếm 10/15 phút (67%) — tra cứu tay + soạn tin tay
- Không có log lưu trữ → không thể phân tích incident sau này
- Không tính OLA/SLA → không biết vi phạm cam kết bao nhiêu lần
- Không tracking chi phí → không biết dispatch cứu hộ sai bao nhiêu lần

---

## Phase 3.2 — Problem Statement (6-field)

| Field | Nội dung |
|---|---|
| **1. Actor / Operator** | Điều phối viên (Dispatcher) — Trung tâm Điều vận Xanh SM Hà Nội. |
| **2. Current Workflow** | 5 bước thủ công, 15 phút/lượt. Tài xế gọi tổng đài → Dispatcher tra GPS → tra trạm sạc → soạn tin nhắn → gọi cứu hộ nếu cần. Hoàn toàn phụ thuộc vào kỹ năng và kinh nghiệm của từng Dispatcher. |
| **3. Bottleneck** | Bước 3 & 4 (10 phút): tra cứu thủ công trạm sạc phù hợp loại cổng (CCS2/GBT) + soạn tin nhắn hướng dẫn chi tiết bằng tiếng Việt. Dễ sai khi tải cao (giờ cao điểm ~20 sự cố/giờ). |
| **4. Business Impact** | ~80 sự cố/ngày tại HN → 20 giờ lao động lãng phí/ngày. Rò rỉ doanh thu ~15% do xe nằm chờ. ~5 lần/ngày dispatch cứu hộ sai → phí cứu hộ 500K/lần × 5 = 2.5M/ngày. |
| **5. Success Metric** | **SLA-01:** Thời gian phản hồi end-to-end ≤ 3 phút (95th percentile). **SLA-02:** Độ chính xác hướng dẫn ≥ 98%. **SLA-03:** Xe cứu hộ đến ≤ 20 phút khi pin < 5%. |
| **6. Operational Boundary** | **Always:** Tag `[DRAFT_ONLY]` trên mọi output AI, log mọi incident + decision. **Ask First (HITL):** Dispatcher phải approve trước khi gửi tin cho tài xế hoặc dispatch cứu hộ. **Never:** AI không đề xuất trạm > 5km khi pin < 5%; không tự gửi tin; không tiết lộ PII. |

---

## Phase 3.3 — Future-State Flow (To-Be) — 8 bước chi tiết

### AI Fit: **LLM Feature** (không phải Agent)

**Lý do:** An toàn giao thông là yếu tố cốt lõi. AI chỉ làm phần tính toán + soạn thảo (Service Task). Mọi quyết định gửi tin / dispatch cứu hộ phải qua người duyệt (User Task / HITL Gate). Nguyên tắc **Separation of Duties** từ Dawn-Brain: "The implementation worker MUST NOT approve its own gate."

### Luồng To-Be — BPMN Chi tiết

```text
═══════════════════════════════════════════════════════════════════════════════════════════
LANE: TÀI XẾ (Field Actor)
═══════════════════════════════════════════════════════════════════════════════════════════
                                                                                    ▼
 [START] ──→ ┌──────────────────┐                                    ┌──────────────────┐
             │ 👤 USER TASK 1    │                                    │ 👤 USER TASK 7    │
             │ Tài xế submit    │                                    │ Nhận kết quả     │
             │ Form sự cố       │                                    │ + Đánh giá ⭐     │
             │                  │                                    │ (1-5 sao)        │
             │ Fields:          │                                    └──────────────────┘
             │ • Họ tên tài xế  │
             │ • Biển số xe     │
             │ • Loại xe (VF5/8)│
             │ • Vị trí GPS     │
             │ • Mức pin %      │
             │ • Mô tả lỗi     │
             │ • Timestamp auto │
             └────────┬─────────┘
                      │ 📋 LOG: INCIDENT_CREATED
═══════════════════════╪═══════════════════════════════════════════════════════════════════
LANE: HỆ THỐNG (Script Tasks — Business Rules)
═══════════════════════╪═══════════════════════════════════════════════════════════════════
                      ▼
             ┌──────────────────┐     ┌──────────────────┐
             │ ⚙️ SCRIPT TASK 1  │     │ ⚙️ SCRIPT TASK 2  │
             │ Validate form    │ ──→ │ Dedup check      │
             │                  │     │ (idempotency)    │
             │ BR-FORM-01~04:  │     │                  │
             │ • Biển số regex  │     │ fingerprint =    │
             │ • Pin 0-100%    │     │ sha256(biển số   │
             │ • GPS hợp lệ    │     │ + ngày + giờ)    │
             │ • Xe thuộc fleet │     │                  │
             └────────┬─────────┘     └────────┬─────────┘
                      │ ❌ Fail → trả lại form         │ 🔁 Trùng → trả incident_id cũ
                      │                                │
═══════════════════════╪════════════════════════════════╪═══════════════════════════════════
LANE: AI ENGINE (Service Tasks — Gemini 2.5 Flash)
═══════════════════════╪════════════════════════════════╪═══════════════════════════════════
                      ▼                                ▼
             ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
             │ 🔌 SERVICE TASK 1 │     │ ⚙️ SCRIPT TASK 3  │     │ 🔌 SERVICE TASK 2 │
             │ AI xác định vị trí│ ──→│ Apply Business   │ ──→│ AI tính toán &   │
             │                  │     │ Rules (DMN)      │     │ đưa NHIỀU OPTIONS│
             │ • Pull GPS (IoT) │     │                  │     │                  │
             │ • Cross-validate │     │ IF pin<5%:       │     │ Option A: Trạm X │
             │   form vs IoT   │     │  → RESCUE        │     │   dist: 2km      │
             │ • Xác định quận  │     │ IF pin 5-15%:    │     │   cost: 0 VND    │
             │   / đường phố   │     │  → NEAREST       │     │   wait: 5 min    │
             │                  │     │ IF pin>15%:      │     │ Option B: Trạm Y │
             │ 📋 LOG: GPS_PULL │     │  → OPTIMAL       │     │   dist: 4km      │
             │ ⏱ OLA: ≤10s     │     │ Check port match │     │   cost: 0 VND    │
             │ ↩️ Fail: manual  │     │                  │     │   wait: 0 min    │
             └──────────────────┘     │ 📋 LOG: RULE_HIT │     │ Option C: Cứu hộ │
                                      └──────────────────┘     │   cost: 500K VND │
                                                               │   eta: 15 min    │
                                                               │                  │
                                                               │ 📋 LOG: AI_DRAFT │
                                                               │ ⏱ OLA: ≤15s     │
                                                               │ ↩️ Fail: template│
                                                               └────────┬─────────┘
                                                                        │
             ┌──────────────────┐                                       │
             │ ⚙️ SCRIPT TASK 4  │◄──────────────────────────────────────┘
             │ Guardrail Check  │
             │                  │
             │ GR-01: [DRAFT]?  │
             │ GR-02: PII scan  │
             │ GR-03: Pin<5%    │
             │   + trạm>5km?   │
             │ GR-04: Port OK?  │
             │                  │
             │ 📋 LOG: GUARD    │
             └────────┬─────────┘
                      │ ❌ Fail → template mẫu + alert
═══════════════════════╪═══════════════════════════════════════════════════════════════════
LANE: NHÂN VIÊN HỖ TRỢ (Dispatcher — User Tasks / HITL)
═══════════════════════╪═══════════════════════════════════════════════════════════════════
                      ▼
             ┌──────────────────┐                        ┌──────────────────┐
             │ 👤 USER TASK 2    │                        │ 👤 USER TASK 3    │
             │ Dispatcher nhận  │                        │ Dispatcher chọn  │
             │ FORM kết quả AI  │ ─────────────────────→ │ option + approve │
             │                  │                        │                  │
             │ Hiển thị:        │                        │ [✅ Approve A]   │
             │ • Thông tin xe   │                        │ [✅ Approve B]   │
             │ • Bản đồ vị trí  │                        │ [✅ Approve C]   │
             │ • Pin real-time  │                        │ [✏️ Edit & Send] │
             │ • Các options    │                        │ [❌ Reject]      │
             │ • Chi phí so sánh│                        │                  │
             │ • Cảnh báo (nếu) │                        │ 📋 LOG: DECISION │
             │                  │                        │ ⏱ OLA: ≤5 min   │
             │ ⏱ OLA: ≤5 min   │                        │ ⏱ Timeout →     │
             └──────────────────┘                        │   auto-escalate  │
                                                         └────────┬─────────┘
                                                                  │
                                               ┌─────────────────┬┴────────────────┐
                                               │                 │                  │
                                          [Approve]         [Reject lần 1]    [Reject ≥2]
                                               │                 │                  │
                                               ▼                 ▼                  ▼
                                                          AI re-generate     👤 USER TASK 4
                                                          (fresh context)    Dispatcher viết
                                                                             tin nhắn tay
═══════════════════════════════════════════════════════════════════════════════════════════
LANE: ĐIỀU PHỐI & XỬ LÝ THỰC ĐỊA
═══════════════════════════════════════════════════════════════════════════════════════════
                                               │
                                               ▼
             ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
             │ 🔌 SERVICE TASK 3 │     │ 🔌 SERVICE TASK 4 │     │ 👤 USER TASK 5    │
             │ Gửi tin nhắn    │ ──→ │ Dispatch cứu hộ  │ ──→ │ Nhân viên thực   │
             │ cho tài xế      │     │ (nếu option C)   │     │ địa xử lý sự cố │
             │                  │     │                  │     │                  │
             │ Channel: Push   │     │ Assign xe cứu hộ │     │ • Đến vị trí xe  │
             │ Fallback: SMS   │     │ gần nhất (GPS)   │     │ • Sạc pin / kéo  │
             │                  │     │                  │     │ • Xác nhận hoàn  │
             │ 📋 LOG: SENT    │     │ 📋 LOG: DISPATCH │     │   thành          │
             │ ⏱ OLA: ≤30s    │     │ ⏱ SLA: ≤20 min  │     │                  │
             │ ↩️ Fail 3x →   │     │                  │     │ 📋 LOG: RESOLVED │
             │   gọi ĐT       │     └──────────────────┘     └────────┬─────────┘
             └──────────────────┘                                      │
                                                                       │
═══════════════════════════════════════════════════════════════════════╪═════════════════
LANE: HOÀN TẤT & ĐÁNH GIÁ
═══════════════════════════════════════════════════════════════════════╪═════════════════
                                                                       ▼
             ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
             │ 👤 USER TASK 6    │     │ ⚙️ SCRIPT TASK 5  │     │ ⚙️ SCRIPT TASK 6  │
             │ Nhân viên submit │ ──→ │ Tính toán SLA    │ ──→ │ Lưu toàn bộ     │
             │ Form hoàn thành  │     │ + OLA metrics    │     │ vào Data Store   │ ──→ [END]
             │                  │     │                  │     │                  │
             │ Fields:          │     │ • response_time  │     │ • incident_record│
             │ • Kết quả xử lý │     │ • sla_breached?  │     │ • location_trail │
             │ • Ghi chú       │     │ • ola_violations │     │ • decision_log   │
             │ • Chi phí thực tế│     │ • cost_saved     │     │ • approval_log   │
             │ • Ảnh chụp      │     │ • ai_accuracy    │     │ • cost_record    │
             │ • Timestamp     │     │                  │     │ • sla_record     │
             └──────────────────┘     │ 📋 LOG: SLA_CALC│     │ • rating         │
                                      └──────────────────┘     └──────────────────┘
```

---

## Bảng Handoff — Ai chuyển cho ai, bằng gì

| # | From → To | BPMN Element | Artifact chuyển giao | Điều kiện | Nếu lỗi |
|---|---|---|---|---|---|
| **H1** | Tài xế → Hệ thống | 👤→⚙️ User→Script | `form_data.json` (tên, xe, GPS, pin, lỗi, timestamp) | Form submitted | Validation error → trả lại form |
| **H2** | Hệ thống → AI | ⚙️→🔌 Script→Service | `validated_incident` (incident_id, biển số) | Form valid + not duplicate | Duplicate → trả incident_id cũ |
| **H3** | AI → AI | 🔌→⚙️ Service→Script | `telemetry` (GPS, SOC, speed, port type) | IoT API OK | API fail 3x → Dispatcher nhập tay |
| **H4** | AI → AI | ⚙️→🔌 Script→Service | `decision` (action, rule_id, options[]) | Rules applied | — |
| **H5** | AI → Dispatcher | 🔌→👤 Service→User | `form_result` (draft, options, costs, map, alerts) | Guardrail passed | Guardrail blocked → template mẫu |
| **H6** | Dispatcher → Hệ thống | 👤→🔌 User→Service | `approved_option` (option_id, edits, dispatcher_id) | Click Approve | Reject → retry hoặc manual |
| **H7** | Hệ thống → Tài xế | 🔌→👤 Service→User | Push notification + SMS hướng dẫn | Delivery confirmed | Fail 3x → gọi ĐT trực tiếp |
| **H8** | Nhân viên thực địa → Hệ thống | 👤→⚙️ User→Script | `completion_form` (kết quả, chi phí, ảnh) | Sự cố resolved | — |

---

## OLA / SLA — Cam kết Mức Dịch vụ

### OLA (Operational Level Agreement) — Nội bộ giữa các Lane

| OLA ID | Từ → Đến | Bước | Cam kết | Breach Action |
|---|---|---|---|---|
| **OLA-01** | IoT → AI Engine | Service Task 1: Pull GPS | ≤ **10 giây** | Retry 3x → Dispatcher nhập tay |
| **OLA-02** | Station API → AI | Service Task 2: Query trạm | ≤ **5 giây** | Retry 3x → cached data (TTL 5 min) |
| **OLA-03** | AI Engine → Dispatcher | Service Task 2: Generate options | ≤ **15 giây** | Retry 1x → template tin mẫu |
| **OLA-04** | Dispatcher → Tài xế | User Task 2-3: Review + approve | ≤ **5 phút** | Timer → auto-escalate Supervisor |
| **OLA-05** | Hệ thống Gửi → Tài xế | Service Task 3: Send message | ≤ **30 giây** | Retry 3x → gọi ĐT trực tiếp |
| **OLA-06** | Nhân viên thực địa | User Task 5: Xử lý sự cố | ≤ **20 phút** | Alert Trưởng ca |

### SLA (Service Level Agreement) — Cam kết với Tài xế

| SLA ID | Cam kết | Cách đo | Target | Compensation nếu breach |
|---|---|---|---|---|
| **SLA-01** | Thời gian phản hồi tổng (end-to-end) | `first_response_at - created_at` | ≤ **3 phút** (p95) | Voucher 30K nếu > 15 phút |
| **SLA-02** | Độ chính xác hướng dẫn | `correct_results / total` | ≥ **98%** | Hoàn tiền chuyến nếu sai trạm |
| **SLA-03** | Xe cứu hộ đến nơi (khi pin < 5%) | `rescue_arrived_at - dispatched_at` | ≤ **20 phút** | Hoàn tiền chờ nếu > 30 phút |
| **SLA-04** | Tỷ lệ sự cố resolved | `resolved / total` per day | ≥ **99%** | Review quy trình nếu < 95% |

### Escalation Matrix khi SLA Breach

| Mức | Điều kiện | Auto-action | Ai nhận |
|---|---|---|---|
| **L1** | > 80% SLA (vd: 2.4 / 3 phút) | 🟡 Cảnh báo vàng trên dashboard | Dispatcher đang xử lý |
| **L2** | > 100% SLA (vd: 3.5 phút) | 🔴 Auto-assign Dispatcher backup | Supervisor |
| **L3** | > 200% SLA (vd: 6 phút) | 🚨 Alert + gọi trực tiếp tài xế | Trưởng ca |
| **L4** | > 300% SLA + pin < 5% | 🆘 Dispatch cứu hộ khẩn cấp | Operations Director |

---

## Chi phí AI — So sánh 3 Phương án

| Hạng mục | 🔴 Manual (As-Is) | 🟢 Hybrid AI+HITL (Đề xuất) | 🔵 Full Auto |
|---|---|---|---|
| Thời gian/incident | 15 phút | **3 phút** | 30 giây |
| Dispatcher FTE cần | 30 người/3 ca | **12 người/3 ca** | 2 người (monitor) |
| Lương Dispatcher/tháng | 450M VND | **180M VND** | 30M VND |
| AI API cost/tháng | 0 | **~2.4M VND** | ~2.4M VND |
| Sai sót/tháng | ~150 lần | **~30 lần** | ~60 lần |
| Rủi ro safety | Trung bình | **Thấp (HITL chặn)** | 🔴 Cao |
| Compliance | ✅ | **✅** | ❌ Vi phạm Separation of Duties |
| **Tổng cost/tháng** | **455M** | **~192M** | ~47M |
| **Net saving/tháng** | — | **~263M VND** | — (rủi ro quá cao) |

**ROI: ~263M saving / ~10.4M chi phí AI+infra = ROI 2,528% (payback < 2 tuần)**

---

## Data Model — Lưu trữ cho sau này

### Bảng dữ liệu cần lưu mỗi incident

| Entity | Fields chính | Mục đích |
|---|---|---|
| `incident` | incident_id, fingerprint, status, created_at, resolved_at, resolution_time_s, sla_breached | Tracking + SLA audit |
| `driver_info` | bien_so, driver_name, loai_xe, port_type, total_incidents | Lịch sử tài xế |
| `location_trail` | lat, lng, soc_percent, speed, captured_at, source (IoT/Manual) | GPS trail real-time |
| `decision_log` | rule_applied, action, options[], ai_model, tokens_used, ai_cost_usd, latency_ms | Tại sao AI quyết định thế |
| `approval_log` | dispatcher_id, decision (approve/edit/reject), edit_diff, review_time_s | **Ai xác nhận, lúc nào** |
| `cost_record` | ai_cost, sms_cost, dispatcher_labor, rescue_cost, total, saved_vs_manual | Chi phí so sánh |
| `rating` | driver_rating (1-5), comment, filed_at | Đánh giá chất lượng |
| `complaint` | type, description, resolution, resolved_by, compensation | Khiếu nại (nếu có) |

---

## Log Points — 10 điểm ghi log

| # | Bước | Event | Data | Actor |
|---|---|---|---|---|
| **L1** | User Task 1 | `INCIDENT_CREATED` | form_data, timestamp, incident_id | Tài xế |
| **L2** | Script Task 1 | `FORM_VALIDATED` / `FORM_REJECTED` | validation_result, errors[] | System |
| **L3** | Script Task 2 | `DEDUP_CHECK` | fingerprint, is_duplicate | System |
| **L4** | Service Task 1 | `GPS_TELEMETRY_PULLED` | lat, lng, soc, source | IoT API |
| **L5** | Script Task 3 | `RULE_APPLIED` | rule_id, action, options_count | Rules Engine |
| **L6** | Service Task 2 | `AI_OPTIONS_GENERATED` | model, tokens, cost, latency_ms | AI (Gemini) |
| **L7** | Script Task 4 | `GUARDRAIL_CHECK` | violations[], passed/blocked | System |
| **L8** | User Task 3 | `DISPATCHER_DECISION` | option_chosen, approve/reject, review_time | **Dispatcher (người)** |
| **L9** | Service Task 3 | `MESSAGE_DELIVERED` / `DELIVERY_FAILED` | channel, retry_count | System |
| **L10** | Script Task 5 | `SLA_CALCULATED` | response_time, sla_breached, cost_saved | System |

---

## Metrics hệ thống — Dashboard theo dõi

| Metric | Cách tính | Target | Alert |
|---|---|---|---|
| **Avg response time** | `AVG(resolved_at - created_at)` / 1h | ≤ 3 min | > 5 min |
| **SLA compliance** | `COUNT(sla_breached=false) / total` | ≥ 95% | < 90% |
| **AI accuracy** | `COUNT(no_complaint) / total` | ≥ 98% | < 95% |
| **Dispatcher utilization** | `SUM(review_time) / shift_time` | 40-70% | > 85% |
| **AI cost/incident** | `SUM(ai_cost) / COUNT(incidents)` | ≤ 4,000 VND | > 8,000 VND |
| **Complaint rate** | `COUNT(complaints) / COUNT(incidents)` / day | ≤ 2% | > 5% |
| **Rescue dispatch rate** | `COUNT(rescue) / total` | ~15% | > 30% |
| **Avg driver rating** | `AVG(rating)` / week | ≥ 4.2/5 | < 3.5/5 |
| **OLA violation rate** | `COUNT(ola_breach) / total` per OLA | ≤ 5% | > 10% |
| **Cost saved vs manual** | `SUM(saved_vs_manual)` / month | ≥ 200M VND | < 150M VND |

---

## Phase 5 — EVALUATE

### AI Readiness Checklist

1. [x] **Data sẵn sàng?** → Có API IoT (GPS, SOC), API trạm sạc VinFast, lịch sử 80 sự cố/ngày.
2. [x] **Rủi ro kiểm soát?** → HITL Gate bắt buộc, Guardrail Script Task chặn output vi phạm, Retry ≤ 2 lần → fallback manual, Escalation 4 mức.
3. [x] **Stakeholders sẵn sàng?** → Dispatcher team đã đào tạo quy trình mới, Trưởng ca ủng hộ giảm tải, Tài xế mong muốn phản hồi nhanh hơn.

### Quyết định: **GO** ✅

### Justification (Biện luận dựa trên bằng chứng)

Dự án đạt mức **GO** vì:

1. **Bài toán hẹp, metric rõ ràng**: 15 phút → 3 phút, 98% chính xác, SLA/OLA đã định nghĩa chi tiết.
2. **ROI cực cao**: Tiết kiệm ~263M VND/tháng, chi phí AI chỉ ~2.4M VND/tháng (ROI 2,528%).
3. **An toàn được đảm bảo**: 3-tier boundary (Always/Ask First/Never), Guardrail 4 rules, HITL Gate, Retry limit, Escalation 4 mức, Dawn-Brain Separation of Duties.
4. **Data pipeline sẵn sàng**: IoT API, Station API, lưu trữ 10 log points, audit trail đầy đủ (ai xác nhận gì, lúc nào).
5. **Chi phí thấp hơn mọi phương án**: Hybrid AI+HITL (192M) < Manual (455M), trong khi Full Auto (47M) bị loại vì rủi ro safety.
