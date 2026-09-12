"""
Refined High-Impact Infographic Diagram
- Prominent KPI Numbers at the top
- Clear Problem vs Adapter Solution
- 5-Lane BPMN Workflow WITH EXPLICIT FALLBACK (3 levels) & RETRY (2x + Circuit Breaker)
- Explicit Identification of NEW BOTTLENECK (Dispatcher HITL Queue under Surge Load)
- Key Architectural Improvement: FAST-TRACK AUTO-APPROVAL (65% low-risk cases auto-approved in 5s)
- Enterprise Technical Summary
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 2400, 1850
img = Image.new("RGB", (W, H), "#0B132B")  # Deep high-tech navy
draw = ImageDraw.Draw(img)

FONT_DIR = "/usr/share/fonts/liberation-sans-fonts"
f_hero = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 44)
f_sub = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Regular.ttf", 20)

f_kpi_title = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 16)
f_kpi_num = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 46)
f_kpi_badge = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 15)
f_kpi_sub = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Regular.ttf", 14)

f_panel_title = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 19)
f_panel_text = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Regular.ttf", 14)

f_lane_title = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 16)
f_node_title = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 15)
f_node_tag = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 12)
f_node_text = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Regular.ttf", 13)
f_edge = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 12)

# -------------------------------------------------------------
# 1. HEADER
# -------------------------------------------------------------
draw.text((W//2, 30), "XANH SM — ĐIỀU VẬN CỨU HỘ PIN THỜI GIAN THỰC", fill="#F8FAFC", font=f_hero, anchor="mt")
draw.text((W//2, 82), "Kiến trúc AI Agent làm Enterprise Semantic Adapter | Cơ chế Fallback đa tầng & Tối ưu hóa Điểm nghẽn HITL", fill="#94A3B8", font=f_sub, anchor="mt")

# -------------------------------------------------------------
# 2. TOP KPI BANNER (MASSIVE NUMBERS)
# -------------------------------------------------------------
kpis = [
    {
        "title": "THỜI GIAN XỬ LÝ (MTTR)",
        "num": "15 min  ->  2.8 min",
        "badge": "GIẢM 81.3%",
        "badge_bg": "#059669",
        "sub": "Từ 15 phút thủ công giảm còn dưới 3 phút",
        "border": "#10B981"
    },
    {
        "title": "LỆCH DỮ LIỆU CRM - ERP",
        "num": "14.5%  ->  0.05%",
        "badge": "TRIỆT TIÊU LỖI",
        "badge_bg": "#2563EB",
        "sub": "Chấm dứt sai lệch do nhập tay giữa 4 hệ thống",
        "border": "#3B82F6"
    },
    {
        "title": "TIẾT KIỆM CHI PHÍ FLEET",
        "num": "263 Triệu / tháng",
        "badge": "ROI 2,528%",
        "badge_bg": "#D97706",
        "sub": "Giảm 100% cuốc điều cứu hộ nhầm (5 cuốc/ngày)",
        "border": "#F59E0B"
    },
    {
        "title": "TỶ LỆ ĐẠT CHUẨN SLA",
        "num": "78%  ->  98.5%",
        "badge": "ĐẠT CHỈ TIÊU",
        "badge_bg": "#7C3AED",
        "sub": "Cam kết phản hồi <=3p & cứu hộ <=20p",
        "border": "#8B5CF6"
    }
]

card_w = 535
card_h = 145
card_y = 120
card_gap = 25
start_x = (W - (card_w * 4 + card_gap * 3)) // 2

for i, k in enumerate(kpis):
    cx = start_x + i * (card_w + card_gap)
    draw.rounded_rectangle([(cx, card_y), (cx + card_w, card_y + card_h)], radius=14, fill="#1C2541", outline=k["border"], width=2)
    draw.text((cx + 20, card_y + 16), k["title"], fill="#94A3B8", font=f_kpi_title)
    
    bw = draw.textlength(k["badge"], font=f_kpi_badge) + 18
    draw.rounded_rectangle([(cx + card_w - bw - 18, card_y + 14), (cx + card_w - 18, card_y + 38)], radius=6, fill=k["badge_bg"])
    draw.text((cx + card_w - bw//2 - 18, card_y + 26), k["badge"], fill="#FFFFFF", font=f_kpi_badge, anchor="mm")
    
    draw.text((cx + 20, card_y + 48), k["num"], fill="#F8FAFC", font=f_kpi_num)
    draw.text((cx + 20, card_y + 112), k["sub"], fill="#CBD5E1", font=f_kpi_sub)

# -------------------------------------------------------------
# 3. THREE OPERATIONAL PANELS: PROBLEM / ADAPTER / BOTTLENECK & IMPROVEMENT
# -------------------------------------------------------------
p_y = 285
p_h = 145
p_w = (W - 160) // 3

# Panel 1: Problem
bx1 = 60
draw.rounded_rectangle([(bx1, p_y), (bx1 + p_w, p_y + p_h)], radius=12, fill="#1C2541", outline="#EF4444", width=2)
draw.rounded_rectangle([(bx1, p_y), (bx1 + 10, p_y + p_h)], radius=4, fill="#EF4444")
draw.text((bx1 + 22, p_y + 14), "[!] VẤN ĐỀ CŨ: BỆNH HUMAN MIDDLEWARE", fill="#FCA5A5", font=f_panel_title)
items_p1 = [
    "* 4 Hệ thống phân mảnh: CRM | ERP SAP | IoT Telematics | CSMS.",
    "* Điều phối viên mở 4 màn hình, copy paste gõ tay mất 10-15 phút.",
    "* Lệch dữ liệu 14.5%; Trung bình 5 cuốc/ngày điều xe cứu hộ nhầm."
]
for j, item in enumerate(items_p1):
    draw.text((bx1 + 22, p_y + 45 + j * 28), item, fill="#E2E8F0", font=f_panel_text)

# Panel 2: Agent Adapter Solution
bx2 = bx1 + p_w + 20
draw.rounded_rectangle([(bx2, p_y), (bx2 + p_w, p_y + p_h)], radius=12, fill="#1C2541", outline="#10B981", width=2)
draw.rounded_rectangle([(bx2, p_y), (bx2 + 10, p_y + p_h)], radius=4, fill="#10B981")
draw.text((bx2 + 22, p_y + 14), "[+] GIẢI PHÁP: AI AGENT SEMANTIC ADAPTER", fill="#6EE7B7", font=f_panel_title)
items_p2 = [
    "* Ingress: Nhận text/voice tài xế + CAN-bus -> Chuẩn hóa Canonical Event.",
    "* Multi-Objective: Cân bằng Chi phí ERP vs SLA CRM vs An toàn Pin.",
    "* Egress (2 chiều): Ghi Work Order (ERP) + Voucher (CRM) + Lock slot."
]
for j, item in enumerate(items_p2):
    draw.text((bx2 + 22, p_y + 45 + j * 28), item, fill="#E2E8F0", font=f_panel_text)

# Panel 3: NEW BOTTLENECK & IMPROVEMENT (KEY REQUEST)
bx3 = bx2 + p_w + 20
draw.rounded_rectangle([(bx3, p_y), (bx3 + p_w, p_y + p_h)], radius=12, fill="#1C2541", outline="#F59E0B", width=2)
draw.rounded_rectangle([(bx3, p_y), (bx3 + 10, p_y + p_h)], radius=4, fill="#F59E0B")
draw.text((bx3 + 22, p_y + 14), "[*] ĐIỂM NGHẼN MỚI & CẢI TIẾN FAST-TRACK", fill="#FCD34D", font=f_panel_title)
items_p3 = [
    "* Điểm nghẽn mới: Hàng đợi HITL quá tải khi giờ cao điểm (Surge Load).",
    "* Cải tiến 1: Fast-Track Auto-Approve (Duyệt tự động 65% ca rủi ro thấp <5s).",
    "* Cải tiến 2: Fallback đa tầng (Rule-based, Timeout Escalate & Offline Queue)."
]
for j, item in enumerate(items_p3):
    draw.text((bx3 + 22, p_y + 45 + j * 28), item, fill="#E2E8F0", font=f_panel_text)

# -------------------------------------------------------------
# 4. BPMN 5 SWIMLANES WITH FALLBACK & RETRY
# -------------------------------------------------------------
lanes = [
    {"name": "LANE 1: TÀI XẾ (Field Actor)", "y": 450, "h": 165, "bg": "#121F3D", "bd": "#0284C7"},
    {"name": "LANE 2: HỆ THỐNG / SCRIPT TASKS (Validation & Deduplication)", "y": 630, "h": 165, "bg": "#1E243D", "bd": "#D97706"},
    {"name": "LANE 3: AI AGENT ADAPTER (Gemini 3.6 + Optimization Engine)", "y": 810, "h": 185, "bg": "#112E2E", "bd": "#059669"},
    {"name": "LANE 4: ĐIỀU PHỐI VIÊN / HITL GATE (Human-in-the-Loop Cockpit)", "y": 1010, "h": 185, "bg": "#22193E", "bd": "#7C3AED"},
    {"name": "LANE 5: ĐỒNG BỘ 2 CHIỀU ERP - CRM - CSMS & THỰC ĐỊA", "y": 1210, "h": 195, "bg": "#2A1828", "bd": "#E11D48"}
]

for lane in lanes:
    draw.rounded_rectangle([(60, lane["y"]), (W - 60, lane["y"] + lane["h"])], radius=12, fill=lane["bg"], outline=lane["bd"], width=2)
    tw = draw.textlength(lane["name"], font=f_lane_title) + 30
    draw.rounded_rectangle([(60, lane["y"]), (60 + tw, lane["y"] + 32)], radius=8, fill=lane["bd"])
    draw.text((75, lane["y"] + 16), lane["name"], fill="#FFFFFF", font=f_lane_title, anchor="lm")

def draw_node(x, y, w, h, title, lines, tag, tag_bg, bg="#1E293B", bd="#38BDF8"):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=10, fill=bg, outline=bd, width=2)
    tw = draw.textlength(tag, font=f_node_tag) + 16
    draw.rounded_rectangle([(x + w - tw - 8, y + 8), (x + w - 8, y + 25)], radius=4, fill=tag_bg)
    draw.text((x + w - tw // 2 - 8, y + 16), tag, fill="#FFFFFF", font=f_node_tag, anchor="mm")
    draw.text((x + 14, y + 16), title, fill="#FFFFFF", font=f_node_title, anchor="lm")
    for idx, l in enumerate(lines):
        draw.text((x + 14, y + 40 + idx * 20), l, fill="#CBD5E1", font=f_node_text)

def draw_arrow(x1, y1, x2, y2, label="", color="#94A3B8"):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    a = math.atan2(y2 - y1, x2 - x1)
    draw.polygon([(x2, y2),
                   (int(x2 - 12 * math.cos(a - 0.35)), int(y2 - 12 * math.sin(a - 0.35))),
                   (int(x2 - 12 * math.cos(a + 0.35)), int(y2 - 12 * math.sin(a + 0.35)))], fill=color)
    if label:
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        draw.text((mx, my - 12), label, fill=color, font=f_edge, anchor="mm")

# --- LANE 1: TÀI XẾ ---
draw_node(90, 492, 340, 105, "1. Tài xế Gửi Form",
          ["* Biển số, Mức pin (%), GPS", "* Mô tả ngắn sự cố", "* Client queue nếu mất sóng"],
          "User Task", "#0284C7", bg="#0369A1", bd="#38BDF8")

# Fallback Offline Queue notice on Lane 1
draw.rounded_rectangle([(460, 495), (750, 595)], radius=8, fill="#1E293B", outline="#F59E0B", width=1)
draw.text((475, 512), "[FB-3] MẤT SÓNG 4G / OFFLINE", fill="#FCD34D", font=f_node_tag)
draw.text((475, 535), "* Lưu client-side IndexedDB", fill="#CBD5E1", font=f_node_text)
draw.text((475, 555), "* Auto-retry khi có sóng lại", fill="#CBD5E1", font=f_node_text)
draw.text((475, 575), "* Fallback gửi tin SMS khẩn cấp", fill="#CBD5E1", font=f_node_text)

draw_node(1950, 492, 380, 105, "8. Nhận Kết Quả & Đánh Giá",
          ["* Nhận lộ trình trạm / xe cứu hộ", "* Đánh giá chất lượng 1-5 sao", "* Tự động bồi hoàn nếu trễ SLA"],
          "User Task", "#0284C7", bg="#0369A1", bd="#38BDF8")

# --- LANE 2: HỆ THỐNG / SCRIPT TASKS ---
draw_node(90, 672, 340, 105, "2. Validate Form Dữ Liệu",
          ["* Kiểm tra regex biển số & GPS VN", "* Pin hợp lệ trong ngưỡng 0-100%", "* Xe thuộc đội xe hoạt động GSM"],
          "Script Task", "#D97706", bg="#B45309", bd="#F59E0B")

draw_node(480, 672, 360, 105, "3. Chống Trùng (Idempotency)",
          ["* Redis Lock: SHA256(Biển số + Giờ)", "* Ngăn spam bấm gửi liên tục", "* Nuốt trùng -> Trả Incident cũ"],
          "Script Task", "#D97706", bg="#B45309", bd="#F59E0B")

# --- LANE 3: AI AGENT ADAPTER ---
draw_node(480, 852, 360, 125, "4. AI Pull IoT & Chuẩn Hóa",
          ["* Ingest CAN-bus telemetry thực tế", "* Cross-check mức pin & tọa độ", "* Bắt cờ DATA_CONFLICT nếu lệch"],
          "Service Task", "#059669", bg="#047857", bd="#10B981")

draw_node(890, 852, 400, 125, "5. Tính Toán Đa Phương Án",
          ["* Option A: Trạm VinFast gần (2km)", "* Option B: Trạm công suất cao (4km)", "* Option C: Điều xe sạc lưu động ERP"],
          "Gemini 3.6", "#059669", bg="#047857", bd="#10B981")

draw_node(1340, 852, 370, 125, "6. Enterprise Guardrail",
          ["* Giữ tag [DRAFT_ONLY] bắt buộc", "* Cấm trạm >5km khi pin <5%", "* Masking PII trước khi xử lý"],
          "Guardrail", "#059669", bg="#047857", bd="#10B981")

# Fallback AI Fail Box on Lane 3
draw.rounded_rectangle([(1740, 852), (2040, 977)], radius=8, fill="#1E293B", outline="#EF4444", width=2)
draw.text((1755, 868), "[FB-1] NẾU AI LỖI / TIMEOUT", fill="#FCA5A5", font=f_node_tag)
draw.text((1755, 892), "* Retry 2x (Fresh Context)", fill="#F8FAFC", font=f_node_text)
draw.text((1755, 915), "* Circuit Breaker kích hoạt", fill="#F8FAFC", font=f_node_text)
draw.text((1755, 938), "* Fallback: Rule-Based tĩnh", fill="#FCA5A5", font=f_node_text)
draw.text((1755, 958), "* Dispatch cứu hộ nếu pin <5%", fill="#CBD5E1", font=f_node_text)

# --- LANE 4: DISPATCHER HITL (WITH FAST-TRACK IMPROVEMENT) ---
draw_node(1340, 1050, 370, 125, "7. Bảng Điều Khiển Cockpit",
          ["* Hiển thị Form đề xuất từ AI", "* So sánh chi phí ERP & SLA CRM", "* Cảnh báo nếu dữ liệu xung đột"],
          "Cockpit", "#7C3AED", bg="#6D28D9", bd="#A855F7")

# Node: HITL Gate (THE BOTTLENECK)
draw_node(1760, 1050, 360, 125, "CHỐT CHẶN DUYỆT (HITL)",
          ["* [Duyệt A/B/C] -> Kích hoạt tự động", "* [Sửa đổi] -> Can thiệp thủ công", "* [Từ chối] -> Yêu cầu AI làm lại"],
          "Human Gate", "#7C3AED", bg="#6D28D9", bd="#A855F7")

# Fast-Track Bypass Improvement box on Lane 4
draw.rounded_rectangle([(890, 1050), (1290, 1175)], radius=10, fill="#064E3B", outline="#34D399", width=2)
draw.text((905, 1066), "[CẢI TIẾN ĐỘT PHÁ] FAST-TRACK AUTO-APPROVAL", fill="#6EE7B7", font=f_node_tag)
draw.text((905, 1090), "* Áp dụng ca rủi ro thấp (Pin >15%, trạm gần)", fill="#F8FAFC", font=f_node_text)
draw.text((905, 1112), "* AI Tự động duyệt trong 5 giây (Bypass HITL)", fill="#34D399", font=f_node_text)
draw.text((905, 1134), "* Giải phóng 65% tải cho Điều phối viên", fill="#F8FAFC", font=f_node_text)
draw.text((905, 1154), "* TRIỆT TIÊU ĐIỂM NGHẼN GIỜ CAO ĐIỂM", fill="#FCD34D", font=f_node_tag)

# Timeout Fallback Box on Lane 4
draw.rounded_rectangle([(2150, 1050), (2370, 1175)], radius=8, fill="#1E293B", outline="#F59E0B", width=1)
draw.text((2165, 1066), "[FB-2] TIMEOUT > 5P", fill="#FCD34D", font=f_node_tag)
draw.text((2165, 1092), "* Auto-escalate Trưởng ca", fill="#CBD5E1", font=f_node_text)
draw.text((2165, 1115), "* Tự động chuyển cuốc", fill="#CBD5E1", font=f_node_text)
draw.text((2165, 1138), "* Pin <5%: Auto-cứu hộ", fill="#FCA5A5", font=f_node_text)

# --- LANE 5: ĐỒNG BỘ 2 CHIỀU & THỰC ĐỊA ---
draw_node(1760, 1255, 360, 130, "8. Đồng Bộ 2 Chiều Hệ Thống",
          ["* [ERP SAP]: Sinh Work Order xe cứu hộ", "* [CRM]: Mở Ticket & Cấp Voucher SLA", "* [CSMS]: Khóa trước trụ sạc 15 phút"],
          "Saga Adapter", "#E11D48", bg="#BE123C", bd="#FB7185")

draw_node(1340, 1255, 370, 130, "9. Thực Địa Xử Lý Sự Cố",
          ["* Xe cứu hộ di động di chuyển tới nơi", "* Sạc cấp cứu hoặc dẫn xe tới trạm", "* Kỹ thuật viên chụp ảnh & nghiệm thu"],
          "Rescue Field", "#E11D48", bg="#BE123C", bd="#FB7185")

draw_node(890, 1255, 400, 130, "10. Lưu Trữ & Báo Cáo VinFast",
          ["* Ghi nhận 10 điểm Log kiểm toán", "* Gửi Defect Intelligence cho VinFast", "* Tính toán SLA & hạch toán chi phí"],
          "Data Lake", "#E11D48", bg="#BE123C", bd="#FB7185")

# --- ARROWS ---
# Step 1 -> 2
draw_arrow(260, 597, 260, 672, "H1: Form Data")
# Step 2 -> 3
draw_arrow(430, 724, 480, 724, "Valid")
# Step 3 -> 4
draw_arrow(660, 777, 660, 852, "H2: Canonical Event")
# Step 4 -> 5
draw_arrow(840, 914, 890, 914, "IoT Stream")
# Step 5 -> 6
draw_arrow(1290, 914, 1340, 914, "Draft Options")
# Step 6 -> 7
draw_arrow(1525, 977, 1525, 1050, "H5: Guarded Draft")
# Step 7 -> HITL
draw_arrow(1710, 1112, 1760, 1112, "Review")

# Step 6 -> Fallback 1 (shortened label, no collision)
draw_arrow(1710, 914, 1740, 914, "Lỗi / <85%", "#EF4444")

# Fast-Track connection from Step 5/6
draw_arrow(1090, 977, 1090, 1050, "Ca Rủi Ro Thấp (65%)", "#34D399")

# Fast-Track bypass cleanly routed via corridor between Lane 4 and Lane 5:
draw.line([(1090, 1175), (1090, 1220), (1940, 1220)], fill="#34D399", width=3)
draw_arrow(1940, 1220, 1940, 1255, "Auto-Approve 5s (Bypass)", "#34D399")

# HITL -> 8 (Egress)
draw_arrow(1940, 1175, 1940, 1220, "Approve -> Trigger Saga", "#10B981")

# HITL -> Timeout FB
draw_arrow(2120, 1112, 2150, 1112, ">5 min", "#F59E0B")
# 8 -> 9 (Field)
draw_arrow(1760, 1320, 1710, 1320, "Dispatch Command")
# 9 -> 10 (Audit)
draw_arrow(1340, 1320, 1290, 1320, "Completion Form")
# Return to Driver Rating on Lane 1
draw.line([(2120, 1320), (2360, 1320), (2360, 544), (2330, 544)], fill="#38BDF8", width=3)
draw.polygon([(2330, 544), (2342, 538), (2342, 550)], fill="#38BDF8")
draw.text((2350, 750), "H7: Push Notification & Danh gia 1-5*", fill="#38BDF8", font=f_edge, anchor="mm")

# -------------------------------------------------------------
# 5. BOTTOM ARCHITECTURE & GOVERNANCE FOOTER
# -------------------------------------------------------------
bot_y = 1430
bot_h = 390
draw.rounded_rectangle([(60, bot_y), (W - 60, bot_y + bot_h)], radius=12, fill="#1C2541", outline="#475569", width=2)

draw.text((90, bot_y + 22), "NGUYÊN TẮC KỸ THUẬT, FALLBACK & KIẾN TRÚC ENTERPRISE ADAPTER", fill="#F8FAFC", font=f_panel_title)

col_w = (W - 240) // 3

# Sub-block 1
bx1 = 90
draw.rounded_rectangle([(bx1, bot_y + 58), (bx1 + col_w, bot_y + bot_h - 22)], radius=8, fill="#0F172A")
draw.text((bx1 + 18, bot_y + 78), "1. Cơ Chế Fallback Đa Tầng & Retry", fill="#38BDF8", font=f_node_title)
items_tech1 = [
    "* Level 1 (Semantic Fallback): AI lỗi / confidence <85% ->",
    "  Chuyển Decision Tree rule-based tĩnh, không làm tắc luồng.",
    "* Level 2 (Human Fallback): Dispatcher bận >5p -> Auto-escalate",
    "  sang Trưởng ca; xe pin <5% tự động gọi cứu hộ khẩn cấp.",
    "* Level 3 (Infrastructure Fallback): ERP/IoT mất mạng ->",
    "  Lưu Kafka Offline Queue & gửi SMS trực tiếp tài xế.",
    "* Independent Retry: Tối đa 2 lần với Fresh Neutral Context,",
    "  kích hoạt Circuit Breaker nếu lỗi 3 lần liên tiếp."
]
for idx, it in enumerate(items_tech1):
    draw.text((bx1 + 18, bot_y + 110 + idx * 26), it, fill="#94A3B8", font=f_node_text)

# Sub-block 2
bx2 = bx1 + col_w + 30
draw.rounded_rectangle([(bx2, bot_y + 58), (bx2 + col_w, bot_y + bot_h - 22)], radius=8, fill="#0F172A")
draw.text((bx2 + 18, bot_y + 78), "2. Tối Ưu Điểm Nghẽn Mới (Fast-Track)", fill="#34D399", font=f_node_title)
items_tech2 = [
    "* Nhận diện Điểm nghẽn mới: Hàng đợi duyệt HITL của Dispatcher",
    "  sẽ bị quá tải khi trời mưa/giờ cao điểm (Surge Load 30 xe/h).",
    "* Giải pháp Fast-Track Bypass: Phân loại rủi ro (Risk Triage):",
    "  - Ca rủi ro thấp (Pin >15%, trạm gần) -> Auto-approve 5s.",
    "  - Ca rủi ro cao (Pin <5%, lỗi pin) -> Dispatcher duyệt kỹ.",
    "* Giải phóng 65% - 70% tải cho Điều phối viên.",
    "* Giữ vững cam kết SLA <=3 phút trong mọi kịch bản tải đột biến."
]
for idx, it in enumerate(items_tech2):
    draw.text((bx2 + 18, bot_y + 110 + idx * 26), it, fill="#94A3B8", font=f_node_text)

# Sub-block 3
bx3 = bx2 + col_w + 30
draw.rounded_rectangle([(bx3, bot_y + 58), (bx3 + col_w, bot_y + bot_h - 22)], radius=8, fill="#0F172A")
draw.text((bx3 + 18, bot_y + 78), "3. Nhất Quán Giao Dịch & Vòng Lặp VinFast", fill="#F472B6", font=f_node_title)
items_tech3 = [
    "* Saga Pattern: Điều phối phân tán giữa ERP SAP + CRM + CSMS,",
    "  tự động hoàn tác (Compensating) nếu ghi lỗi giữa chừng.",
    "* Idempotency Key: Khóa Redis SHA-256 chống tạo trùng cuốc xe.",
    "* Defect Intelligence: Bắt bệnh pin tụt bất thường -> Cảnh báo",
    "  bảo hành & gửi R&D VinFast phân tích lỗi Cell pin theo lô.",
    "* Heatmap sự cố thực địa làm căn cứ mở rộng trạm sạc mới."
]
for idx, it in enumerate(items_tech3):
    draw.text((bx3 + 18, bot_y + 110 + idx * 26), it, fill="#94A3B8", font=f_node_text)

# Save
out_path = "/mnt/win_d/VinUni/VinUni_Codelab_Day02_Template/04-workflow-diagram.png"
img.save(out_path, "PNG", dpi=(300, 300))
print(f"✅ Enhanced Infographic with Fallback & Bottleneck generated at: {out_path}")
