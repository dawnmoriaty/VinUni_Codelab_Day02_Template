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
6. **Giá trị dữ liệu dài hạn**: Dữ liệu sự cố chảy ngược về VinFast phục vụ điều tra lỗi xe, và chảy xuôi xây dựng quy trình chăm sóc khách hàng tự động.

---

## Phụ lục A — Dữ liệu Sự cố → Chảy ngược về VinFast (Defect Intelligence)

### Vấn đề

Hiện tại khi xử lý sự cố pin, dữ liệu chỉ dùng để dispatch → xong → quên. Thực tế, **mỗi incident là một data point quý giá** cho VinFast:
- Xe nào hết pin bất thường? (pin mới mà tụt nhanh → lỗi phần cứng?)
- Khu vực nào hay xảy ra sự cố? (hạ tầng trạm sạc thiếu?)
- Dòng xe nào gặp sự cố nhiều nhất? (VF5 vs VF8 — khác nhau thế nào?)
- Tài xế nào lặp lại sự cố? (hành vi lái không tối ưu hay xe lỗi?)

### Data Pipeline: Xanh SM → VinFast

```text
═══════════════════════════════════════════════════════════════════════════
LUỒNG DỮ LIỆU (Data Flow)
═══════════════════════════════════════════════════════════════════════════

  Xanh SM Dispatching System                    VinFast Engineering
  ─────────────────────────                     ────────────────────

  ┌──────────────┐                              ┌──────────────────┐
  │ incident_db  │──── Batch ETL ──────────────→│ Defect Analytics │
  │              │     (mỗi 24h)                │ Platform         │
  │ • 80 sự cố/ │                              │                  │
  │   ngày       │                              │ • Aggregate by   │
  │ • GPS trail  │                              │   model/VIN      │
  │ • SOC curve  │                              │ • Anomaly detect │
  │ • Error desc │                              │ • Trend analysis │
  └──────────────┘                              └────────┬─────────┘
                                                         │
                                                         ▼
                                                ┌──────────────────┐
                                                │ ⚙️ Script Task    │
                                                │ Defect Pattern   │
                                                │ Detection        │
                                                │                  │
                                                │ Rule:            │
                                                │ IF same VIN ≥ 3  │
                                                │ incidents in 30d │
                                                │ → FLAG for       │
                                                │ warranty check   │
                                                └────────┬─────────┘
                                                         │
                                          ┌──────────────┼──────────────┐
                                          ▼              ▼              ▼
                                   ┌────────────┐ ┌────────────┐ ┌────────────┐
                                   │ Alert:     │ │ Report:    │ │ Action:    │
                                   │ Recall     │ │ Monthly    │ │ Đặt thêm  │
                                   │ candidate  │ │ Defect     │ │ trạm sạc  │
                                   │ (xe lỗi    │ │ Trend by   │ │ tại khu   │
                                   │ hàng loạt) │ │ model/area │ │ vực nóng  │
                                   └────────────┘ └────────────┘ └────────────┘
```

### Dữ liệu gửi cho VinFast (Aggregated — không PII)

| Data point | Nguồn | VinFast dùng để |
|---|---|---|
| `vehicle_model` + `vin_hash` + `incident_count` | incident_db | Phát hiện xe lỗi: nếu VIN X có ≥ 3 sự cố/tháng → kiểm tra bảo hành |
| `soc_drain_curve` (SOC theo thời gian) | location_trail | Phát hiện pin chai/lỗi cell: so sánh với baseline drain rate per model |
| `incident_heatmap` (lat/lng aggregate) | location_trail | Quy hoạch trạm sạc: khu vực nào thiếu trạm → đề xuất mở rộng |
| `error_description_clusters` | incident form | NLP phân loại lỗi: "tiếng kêu lạ" / "pin tụt đột ngột" → mã lỗi kỹ thuật |
| `rescue_rate_by_model` | decision_log | Dòng xe nào cần cứu hộ nhiều nhất → cải thiện range estimation |
| `charging_port_mismatch_rate` | guardrail_log | Tỷ lệ tài xế đến sai loại trạm → cải thiện UI app VinFast |

### Business Rules cho Defect Detection

| Rule ID | Điều kiện | Action | Gửi cho |
|---|---|---|---|
| `BR-DEFECT-01` | Cùng VIN ≥ 3 sự cố pin / 30 ngày | Flag "WARRANTY_CHECK_REQUIRED" | VinFast Service Center |
| `BR-DEFECT-02` | ≥ 10 xe cùng model, cùng lỗi / 7 ngày | Flag "POTENTIAL_BATCH_DEFECT" | VinFast Quality Assurance |
| `BR-DEFECT-03` | SOC drain > 2× baseline rate for model | Flag "BATTERY_ANOMALY" | VinFast Battery Lab |
| `BR-DEFECT-04` | Khu vực có > 5 sự cố/ngày (bình thường 1) | Flag "INFRASTRUCTURE_GAP" | VinFast Charging Infra team |
| `BR-DEFECT-05` | Tài xế cùng 1 người ≥ 5 sự cố / 30 ngày | Flag "DRIVER_BEHAVIOR_REVIEW" | Xanh SM Training team |

---

## Phụ lục B — OLA/SLA → Continuous Improvement (Cải tiến liên tục)

### Vòng lặp cải tiến

```text
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   │  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌────────┐│
   │  │ MEASURE │ ──→ │ ANALYZE │ ──→ │ IMPROVE │ ──→ │ CONTROL││
   │  │         │     │         │     │         │     │        ││
   │  │ Thu thập│     │ Tìm root│     │ Sửa quy│     │ Monitor││
   │  │ SLA/OLA │     │ cause   │     │ trình   │     │ new    ││
   │  │ metrics │     │ breach  │     │ + rules │     │ target ││
   │  └─────────┘     └─────────┘     └─────────┘     └───┬────┘│
   │                                                       │     │
   │  ◄────────────────────────────────────────────────────┘     │
   └──────────────────────────────────────────────────────────────┘
```

### Ví dụ cải tiến theo thời gian

| Giai đoạn | SLA Target | OLA-04 (Dispatcher review) | Cải tiến | Kết quả |
|---|---|---|---|---|
| **Tháng 1** (MVP) | ≤ 5 phút | ≤ 5 phút | Baseline — đo lường | 87% compliance |
| **Tháng 2** | ≤ 5 phút | ≤ 5 phút | Cải thiện AI draft quality → ít reject | 93% compliance |
| **Tháng 3** | ≤ **3 phút** | ≤ **3 phút** | Thắt chặt target, thêm auto-suggest option | 91% compliance |
| **Tháng 6** | ≤ 3 phút | ≤ **2 phút** | AI confidence score → skip review nếu > 95% | 96% compliance |
| **Tháng 12** | ≤ **2 phút** | ≤ **1 phút** | Dispatcher chỉ review edge cases | 98% compliance |

### OLA/SLA → Tăng khả năng xử lý sự cố

| OLA/SLA metric | Insight khai thác | Hành động cải tiến |
|---|---|---|
| OLA-01 breach rate (IoT) | IoT API chậm vào giờ cao điểm | Scale IoT gateway, thêm caching layer |
| OLA-03 breach rate (AI) | AI chậm khi prompt phức tạp | Tối ưu SYSTEM_PROMPT, giảm token, pre-compute |
| OLA-04 breach rate (Dispatcher) | Dispatcher quá tải lúc 8-9h sáng | Thêm Dispatcher cho ca sáng, load balancing |
| SLA-01 p95 > p50 × 3 | Phân phối lệch → có outlier | Tìm và fix bottleneck specific cases |
| SLA-02 drop < 98% | AI recommend sai nhiều hơn | Review + update business rules, retrain |
| Complaint rate tăng | Tài xế không hài lòng | Root cause analysis → fix prompt/process |

---

## Phụ lục C — Quy trình Chăm sóc Khách hàng (Customer Care Workflow)

### Tầm nhìn: Từ reactive → proactive

Dữ liệu SLA/OLA + lịch sử sự cố tạo nền tảng xây dựng quy trình chăm sóc khách hàng **chủ động**:

```text
GIAI ĐOẠN 1 (Hiện tại)          GIAI ĐOẠN 2 (6 tháng)          GIAI ĐOẠN 3 (12 tháng)
────────────────────            ────────────────────            ────────────────────
Reactive:                       Proactive:                      Predictive:
Tài xế gặp sự cố               Cảnh báo TRƯỚC khi              AI dự đoán sự cố
→ gọi tổng đài                  hết pin                         TRƯỚC KHI xảy ra
→ chờ xử lý                     → push "Pin còn 15%,            → tự đề xuất lộ trình
                                 trạm gần nhất 2km"              sạc tối ưu mỗi ngày
```

### Giai đoạn 2 — Proactive Alert (Dùng data từ hệ thống hiện tại)

```text
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ ⏱️ Timer Event    │     │ ⚙️ Script Task    │     │ 🔌 Service Task   │
│ Mỗi 5 phút      │ ──→ │ Scan toàn bộ     │ ──→ │ AI generate      │
│ check fleet      │     │ fleet Xanh SM    │     │ proactive alert  │
│                  │     │                  │     │                  │
│                  │     │ Rule:            │     │ "[DRAFT_ONLY]    │
│                  │     │ IF soc ≤ 15%     │     │  Anh/chị ơi,    │
│                  │     │ AND no charging  │     │  pin xe còn 12%, │
│                  │     │ AND driving      │     │  trạm VinFast    │
│                  │     │ → TRIGGER ALERT  │     │  Cầu Giấy cách  │
│                  │     │                  │     │  1.5km. Ghé sạc  │
│                  │     │ IF soc ≤ 8%      │     │  nhé!"           │
│                  │     │ AND no alert sent│     │                  │
│                  │     │ → URGENT ALERT   │     │ 👤 Dispatcher    │
│                  │     │                  │     │ approve → send   │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Giai đoạn 3 — Predictive Maintenance (Dùng data tích lũy 12 tháng)

| Data tích lũy | AI Model | Output | Giá trị |
|---|---|---|---|
| SOC drain curves × 1000 xe × 12 tháng | Battery degradation model | Dự đoán xe nào cần thay pin trong 30 ngày | Giảm sự cố đột ngột 50% |
| Incident heatmap × 12 tháng | Demand forecasting | Dự đoán khu vực nào nhiều sự cố theo giờ/ngày/mùa | Pre-deploy rescue vehicle |
| Driver behavior × rating × incidents | Driver risk scoring | Xếp hạng tài xế: cần đào tạo hay khen thưởng | Giảm sự cố do hành vi 30% |
| OLA/SLA trends × 12 tháng | Capacity planning | Cần bao nhiêu Dispatcher mỗi ca, mỗi mùa | Tối ưu nhân sự ±20% |

### Customer Care Touchpoints (Điểm chạm chăm sóc)

| Thời điểm | Touchpoint | Kênh | Nội dung | Tự động? |
|---|---|---|---|---|
| **Trước sự cố** | Proactive alert | Push notification | "Pin còn X%, trạm gần nhất Y km" | ✅ Auto (HITL optional) |
| **Trong sự cố** | Real-time update | App + SMS | "Đang xử lý, ETA cứu hộ: 12 phút" | ✅ Auto |
| **Sau sự cố (1h)** | Satisfaction survey | In-app popup | "Đánh giá trải nghiệm 1-5 ⭐" | ✅ Auto |
| **Sau sự cố (24h)** | Follow-up | Push notification | "Xe đã OK chưa ạ? Cần hỗ trợ thêm?" | ✅ Auto |
| **Nếu SLA breach** | Compensation | SMS + voucher | "Xin lỗi vì chậm trễ. Tặng voucher 30K" | ⚠️ Need Supervisor approve |
| **Nếu ≥ 3 sự cố/tháng** | VIP care call | Điện thoại | "Chúng tôi nhận thấy xe gặp sự cố nhiều, mời kiểm tra miễn phí" | 👤 Manual |

---

## Phụ lục D — Edge Cases bổ sung (Gợi ý thêm)

### Các case thực tế production sẽ gặp

| # | Edge Case | Khi nào xảy ra | Giải pháp BPMN |
|---|---|---|---|
| **E1** | Tài xế mất mạng giữa chừng | Submit form → mất 3G/4G → form treo | Client-side queue + retry khi có mạng lại |
| **E2** | Pin tụt nhanh bất thường | Pin 20% → 2 phút sau pin 3% (không bình thường) | Script Task: detect anomaly → flag `BR-DEFECT-03` + priority CRITICAL |
| **E3** | Nhiều tài xế cùng khu vực hết pin | 5 xe cùng quận Cầu Giấy hết pin trong 30 phút | Demand surge detection → batch dispatch 1 xe cứu hộ cho cả 5 |
| **E4** | Trạm sạc full sau khi AI recommend | AI nói "Trạm X còn 2 slot" → tài xế đến → hết slot | Real-time slot reservation: khi Dispatcher approve → lock slot 15 phút |
| **E5** | Tài xế trên cao tốc | Không thể quay đầu, trạm sạc ở chiều ngược lại | Direction-aware routing: chỉ gợi ý trạm CÙNG CHIỀU + exit gần nhất |
| **E6** | Sự cố ngoài giờ (2h sáng) | Ít Dispatcher trực ca đêm | Auto-priority: nâng mọi incident lên HIGH, reduce OLA-04 → 2 phút |
| **E7** | Tài xế báo sai thông tin | Nói pin 50% (thực tế 5%) | Cross-validate form vs IoT (Script Task 1): nếu delta > 10% → ưu tiên IoT + flag |
| **E8** | AI hallucinate trạm sạc không tồn tại | Gemini bịa ra "Trạm VinFast Bờ Hồ" (không có) | Guardrail: cross-check output station names vs station_db → block nếu không match |
| **E9** | Dispatcher approve nhầm option sai | Pin 3% mà approve option "Trạm 7km" | Double-check Script Task: sau approve, re-validate lần cuối trước khi gửi |
| **E10** | Xe đã được cứu nhưng hệ thống chưa close | Nhân viên quên submit completion form | Timer Event: nếu status IN_PROGRESS > 60 phút → alert + auto-ask nhân viên |
