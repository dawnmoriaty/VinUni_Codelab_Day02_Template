"""
Refined High-Impact Infographic Diagram
- NO emoji or unsupported unicode glyphs (so NO empty boxes)
- LARGE BOLD METRICS banner on top
- Visually clear Problem vs Agent Adapter contrast
- 5-Lane BPMN Workflow with spacious layout and clean arrows
- Technical Architecture Summary at the bottom
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 2400, 1750
img = Image.new("RGB", (W, H), "#0B132B")  # Deep high-tech navy blue
draw = ImageDraw.Draw(img)

FONT_DIR = "/usr/share/fonts/liberation-sans-fonts"
f_hero = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 44)
f_sub = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Regular.ttf", 20)

f_kpi_title = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 16)
f_kpi_num = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 48)
f_kpi_badge = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 15)
f_kpi_sub = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Regular.ttf", 14)

f_panel_title = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 20)
f_panel_text = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Regular.ttf", 15)

f_lane_title = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 16)
f_node_title = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 16)
f_node_tag = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 12)
f_node_text = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Regular.ttf", 14)
f_edge = ImageFont.truetype(f"{FONT_DIR}/LiberationSans-Bold.ttf", 13)

# -------------------------------------------------------------
# 1. HEADER
# -------------------------------------------------------------
draw.text((W//2, 35), "XANH SM — ĐIỀU VẬN CỨU HỘ PIN THỜI GIAN THỰC", fill="#F8FAFC", font=f_hero, anchor="mt")
draw.text((W//2, 88), "Kiến trúc AI Agent đóng vai trò Enterprise Semantic Adapter kết nối CRM - ERP SAP - IoT VinFast - CSMS Grid", fill="#94A3B8", font=f_sub, anchor="mt")

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
card_h = 150
card_y = 130
card_gap = 25
start_x = (W - (card_w * 4 + card_gap * 3)) // 2

for i, k in enumerate(kpis):
    cx = start_x + i * (card_w + card_gap)
    draw.rounded_rectangle([(cx, card_y), (cx + card_w, card_y + card_h)], radius=14, fill="#1C2541", outline=k["border"], width=2)
    
    # Title
    draw.text((cx + 20, card_y + 16), k["title"], fill="#94A3B8", font=f_kpi_title)
    
    # Badge
    bw = draw.textlength(k["badge"], font=f_kpi_badge) + 18
    draw.rounded_rectangle([(cx + card_w - bw - 18, card_y + 14), (cx + card_w - 18, card_y + 38)], radius=6, fill=k["badge_bg"])
    draw.text((cx + card_w - bw//2 - 18, card_y + 26), k["badge"], fill="#FFFFFF", font=f_kpi_badge, anchor="mm")
    
    # Big Number
    draw.text((cx + 20, card_y + 50), k["num"], fill="#F8FAFC", font=f_kpi_num)
    
    # Subtext
    draw.text((cx + 20, card_y + 115), k["sub"], fill="#CBD5E1", font=f_kpi_sub)

# -------------------------------------------------------------
# 3. PROBLEM VS SOLUTION CONTRAST
# -------------------------------------------------------------
p_y = 305
p_h = 130
p_w = (W - 140) // 2

# Left: Problem
draw.rounded_rectangle([(60, p_y), (60 + p_w, p_y + p_h)], radius=12, fill="#1C2541", outline="#EF4444", width=2)
draw.rounded_rectangle([(60, p_y), (72, p_y + p_h)], radius=4, fill="#EF4444")
draw.text((85, p_y + 15), "[!] BÀI TOÁN & VẤN ĐỀ CŨ: BỆNH 'HUMAN MIDDLEWARE'", fill="#FCA5A5", font=f_panel_title)
p_items_old = [
    "* 4 Hệ thống phân mảnh: CRM (Tài xế/SLA) | ERP (Chi phí xe cứu hộ) | IoT (GPS/Pin) | CSMS (Trụ sạc).",
    "* Điều phối viên phải mở 4 màn hình, copy paste, đối soát thủ công mất 10 - 15 phút/lượt.",
    "* Lệch dữ liệu (Data Mismatch) 14.5%; Trung bình 5 cuốc/ngày điều xe cứu hộ nhầm gây lãng phí lớn."
]
for j, item in enumerate(p_items_old):
    draw.text((85, p_y + 44 + j * 26), item, fill="#E2E8F0", font=f_panel_text)

# Right: Solution
draw.rounded_rectangle([(60 + p_w + 20, p_y), (60 + 2 * p_w + 20, p_y + p_h)], radius=12, fill="#1C2541", outline="#10B981", width=2)
draw.rounded_rectangle([(60 + p_w + 20, p_y), (60 + p_w + 32, p_y + p_h)], radius=4, fill="#10B981")
draw.text((85 + p_w + 20, p_y + 15), "[+] GIẢI PHÁP: AI AGENT ĐÓNG VAI TRÒ ENTERPRISE ADAPTER", fill="#6EE7B7", font=f_panel_title)
p_items_new = [
    "* Ingress Adapter: Ingest lời khai text/voice tài xế + stream Telemetry CAN-bus -> Chuẩn hóa Canonical Event.",
    "* Multi-Objective Solver: Cân đối tối ưu 3 bên: Chi phí cứu hộ (ERP) vs Cam kết SLA (CRM) vs An toàn (IoT).",
    "* Egress Adapter (2 chiều): Tự động ghi Work Order (ERP) + Voucher đền bù (CRM) + Giữ slot trạm (CSMS)."
]
for j, item in enumerate(p_items_new):
    draw.text((85 + p_w + 20, p_y + 44 + j * 26), item, fill="#E2E8F0", font=f_panel_text)

# -------------------------------------------------------------
# 4. BPMN 5 SWIMLANES
# -------------------------------------------------------------
lanes = [
    {"name": "LANE 1: TÀI XẾ (Field Actor)", "y": 455, "h": 160, "bg": "#121F3D", "bd": "#0284C7"},
    {"name": "LANE 2: HỆ THỐNG / SCRIPT TASKS (Validation & Deduplication)", "y": 630, "h": 160, "bg": "#1E243D", "bd": "#D97706"},
    {"name": "LANE 3: AI AGENT ADAPTER (Gemini 3.6 + Optimization Engine)", "y": 805, "h": 175, "bg": "#112E2E", "bd": "#059669"},
    {"name": "LANE 4: ĐIỀU PHỐI VIÊN / HITL GATE (Human-in-the-Loop Cockpit)", "y": 995, "h": 170, "bg": "#22193E", "bd": "#7C3AED"},
    {"name": "LANE 5: ĐỒNG BỘ 2 CHIỀU ERP - CRM - CSMS & THỰC ĐỊA", "y": 1180, "h": 185, "bg": "#2A1828", "bd": "#E11D48"}
]

for lane in lanes:
    draw.rounded_rectangle([(60, lane["y"]), (W - 60, lane["y"] + lane["h"])], radius=12, fill=lane["bg"], outline=lane["bd"], width=2)
    # Header tag for lane
    tw = draw.textlength(lane["name"], font=f_lane_title) + 30
    draw.rounded_rectangle([(60, lane["y"]), (60 + tw, lane["y"] + 32)], radius=8, fill=lane["bd"])
    draw.text((75, lane["y"] + 16), lane["name"], fill="#FFFFFF", font=f_lane_title, anchor="lm")

def draw_node(x, y, w, h, bg, bd, title, lines, tag, tag_bg):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=10, fill=bg, outline=bd, width=2)
    # Tag
    tw = draw.textlength(tag, font=f_node_tag) + 16
    draw.rounded_rectangle([(x + w - tw - 8, y + 8), (x + w - 8, y + 25)], radius=4, fill=tag_bg)
    draw.text((x + w - tw // 2 - 8, y + 16), tag, fill="#FFFFFF", font=f_node_tag, anchor="mm")
    # Title
    draw.text((x + 14, y + 16), title, fill="#FFFFFF", font=f_node_title, anchor="lm")
    # Lines
    for idx, l in enumerate(lines):
        draw.text((x + 14, y + 42 + idx * 21), l, fill="#CBD5E1", font=f_node_text)

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
draw_node(90, 498, 350, 102, "#0369A1", "#38BDF8", "1. Tài xế Gửi Form Sự Cố",
          ["* Biển số xe & Mức pin (%)", "* Tọa độ GPS tự động", "* Mô tả chi tiết sự cố"],
          "User Task", "#0284C7")

draw_node(1950, 498, 380, 102, "#0369A1", "#38BDF8", "8. Nhận Kết Quả & Đánh Giá",
          ["* Nhận SMS/Push chỉ dẫn lộ trình", "* Đánh giá chất lượng phục vụ 1-5 sao", "* SLA tính toán minh bạch"],
          "User Task", "#0284C7")

# --- LANE 2: HỆ THỐNG / SCRIPT TASKS ---
draw_node(90, 672, 350, 102, "#B45309", "#F59E0B", "2. Validate Form Dữ Liệu",
          ["* Kiểm tra định dạng biển số", "* Xác thực pin (ngưỡng 0 - 100%)", "* Đối soát xe thuộc fleet Xanh SM"],
          "Script Task", "#D97706")

draw_node(480, 672, 380, 102, "#B45309", "#F59E0B", "3. Chống Trùng Lặp (Idempotency)",
          ["* Redis Lock: SHA256(Biển số + Giờ)", "* Ngăn tài xế bấm gửi spam nhiều lần", "* Nuốt trùng -> Trả lại Ticket cũ"],
          "Script Task", "#D97706")

# --- LANE 3: AI AGENT ADAPTER ---
draw_node(480, 848, 380, 115, "#047857", "#10B981", "4. AI Pull IoT & Chuẩn Hóa",
          ["* Kéo Telemetry qua MQTT / gRPC", "* Đọc SOC pin thực tế & Cell Temp", "* Khắc phục độ lệch GPS"],
          "Service Task", "#059669")

draw_node(900, 848, 430, 115, "#047857", "#10B981", "5. Tính Toán Đa Phương Án",
          ["* Option A: Trạm sạc VinFast gần nhất (2km)", "* Option B: Trạm công suất cao (4km)", "* Option C: Điều xe sạc lưu động (ERP)"],
          "Gemini 3.6", "#059669")

draw_node(1370, 848, 390, 115, "#047857", "#10B981", "6. Enterprise Guardrail",
          ["* Bắt buộc giữ tag [DRAFT_ONLY]", "* Cấm đề xuất trạm >5km khi pin <5%", "* Masking PII (Số điện thoại / CCCD)"],
          "Guardrail", "#059669")

# --- LANE 4: DISPATCHER HITL ---
draw_node(1370, 1040, 390, 110, "#6D28D9", "#A855F7", "7. Bảng Điều Khiển Dispatcher",
          ["* Hiển thị Form đề xuất từ AI", "* So sánh chi phí ERP & cam kết SLA", "* Cảnh báo nếu dữ liệu bị xung đột"],
          "Cockpit", "#7C3AED")

draw_node(1800, 1040, 420, 110, "#6D28D9", "#A855F7", "CHỐT CHẶN AN TOÀN (HITL GATE)",
          ["* [Duyệt A/B/C] -> Kích hoạt lệnh tự động", "* [Sửa đổi] -> Can thiệp thủ công", "* [Từ chối] -> Yêu cầu AI tạo lại"],
          "Human Gate", "#7C3AED")

# --- LANE 5: ĐỒNG BỘ 2 CHIỀU & THỰC ĐỊA ---
draw_node(1800, 1225, 420, 125, "#BE123C", "#FB7185", "8. Đồng Bộ 2 Chiều Hệ Thống",
          ["* [ERP SAP]: Tạo Work Order điều xe cứu hộ", "* [CRM]: Tạo Ticket & Cấp Voucher SLA", "* [CSMS]: Khóa trước trụ sạc 15 phút"],
          "Saga Adapter", "#E11D48")

draw_node(1350, 1225, 410, 125, "#BE123C", "#FB7185", "9. Thực Địa Xử Lý Sự Cố",
          ["* Xe cứu hộ di động di chuyển tới hiện trường", "* Sạc khẩn cấp hoặc hỗ trợ dẫn xe tới trạm", "* Kỹ thuật viên chụp ảnh & nghiệm thu"],
          "Rescue Field", "#E11D48")

draw_node(900, 1225, 410, 125, "#BE123C", "#FB7185", "10. Lưu Trữ & Báo Cáo VinFast",
          ["* Ghi nhận 10 điểm Log kiểm toán", "* Gửi Defect Intelligence cho VinFast", "* Tính toán chỉ số SLA & hạch toán chi phí"],
          "Data Lake", "#E11D48")

# --- ARROWS ---
# Step 1 -> 2
draw_arrow(265, 600, 265, 672, "H1: Form Data")
# Step 2 -> 3
draw_arrow(440, 723, 480, 723, "Valid")
# Step 3 -> 4
draw_arrow(670, 774, 670, 848, "H2: Canonical Event")
# Step 4 -> 5
draw_arrow(860, 905, 900, 905, "IoT Stream")
# Step 5 -> 6
draw_arrow(1330, 905, 1370, 905, "Draft Options")
# Step 6 -> 7
draw_arrow(1565, 963, 1565, 1040, "H5: Guarded Draft")
# Step 7 -> HITL
draw_arrow(1760, 1095, 1800, 1095, "Review")
# HITL -> 8 (Egress)
draw_arrow(2010, 1150, 2010, 1225, "Approve -> Trigger Saga", "#10B981")
# 8 -> 9 (Field)
draw_arrow(1800, 1287, 1760, 1287, "Dispatch Command")
# 9 -> 10 (Audit)
draw_arrow(1350, 1287, 1310, 1287, "Completion Form")
# 10 / 8 -> Return to Driver Rating (Step 8 on Lane 1) via clean right margin
draw.line([(2220, 1287), (2360, 1287), (2360, 549), (2330, 549)], fill="#38BDF8", width=3)
draw.polygon([(2330, 549), (2342, 543), (2342, 555)], fill="#38BDF8")
draw.text((2350, 900), "H7: Push Notification & Danh gia 1-5*", fill="#38BDF8", font=f_edge, anchor="mm")

# -------------------------------------------------------------
# 5. BOTTOM ARCHITECTURE FOOTER
# -------------------------------------------------------------
bot_y = 1390
bot_h = 320
draw.rounded_rectangle([(60, bot_y), (W - 60, bot_y + bot_h)], radius=12, fill="#1C2541", outline="#475569", width=2)

draw.text((90, bot_y + 22), "NGUYÊN TẮC KỸ THUẬT & KIẾN TRÚC ENTERPRISE ADAPTER", fill="#F8FAFC", font=f_panel_title)

col_w = (W - 240) // 3
# Sub-block 1
bx1 = 90
draw.rounded_rectangle([(bx1, bot_y + 60), (bx1 + col_w, bot_y + bot_h - 22)], radius=8, fill="#0F172A")
draw.text((bx1 + 18, bot_y + 80), "1. Chuyển Đổi Giao Thức Đa Tầng", fill="#38BDF8", font=f_node_title)
items_tech1 = [
    "* Ingest: MQTT / gRPC (IoT) & HTTPS REST (Driver App)",
    "* Egress: SAP OData / RFC (ERP) & REST API (CRM)",
    "* Chuẩn hóa toàn bộ Payload sang format CloudEvents",
    "* Đảm bảo tính mở rộng khi kết nối thêm hệ thống"
]
for idx, it in enumerate(items_tech1):
    draw.text((bx1 + 18, bot_y + 115 + idx * 30), it, fill="#94A3B8", font=f_node_text)

# Sub-block 2
bx2 = bx1 + col_w + 30
draw.rounded_rectangle([(bx2, bot_y + 60), (bx2 + col_w, bot_y + bot_h - 22)], radius=8, fill="#0F172A")
draw.text((bx2 + 18, bot_y + 80), "2. Nhất Quán Giao Dịch (Saga Pattern)", fill="#34D399", font=f_node_title)
items_tech2 = [
    "* Điều phối chuỗi phân tán: ERP + CRM + CSMS Grid",
    "* Giao dịch bù trừ (Compensating): Tự động hoàn tác",
    "  nếu một trong các bước ghi dữ liệu bị gián đoạn",
    "* Idempotency key tránh tạo trùng đơn điều xe"
]
for idx, it in enumerate(items_tech2):
    draw.text((bx2 + 18, bot_y + 115 + idx * 30), it, fill="#94A3B8", font=f_node_text)

# Sub-block 3
bx3 = bx2 + col_w + 30
draw.rounded_rectangle([(bx3, bot_y + 60), (bx3 + col_w, bot_y + bot_h - 22)], radius=8, fill="#0F172A")
draw.text((bx3 + 18, bot_y + 80), "3. Phản Hồi Ngược VinFast (Defect Intelligence)", fill="#F472B6", font=f_node_title)
items_tech3 = [
    "* Bắt bệnh pin tụt nhanh bất thường -> Cảnh báo bảo hành",
    "* Cụm lỗi theo lô xe (Batch Defect) -> Gửi R&D VinFast",
    "* Heatmap sự cố thực địa -> Quy hoạch mở rộng trạm sạc",
    "* Xây dựng mô hình bảo trì dự đoán (Predictive)"
]
for idx, it in enumerate(items_tech3):
    draw.text((bx3 + 18, bot_y + 115 + idx * 30), it, fill="#94A3B8", font=f_node_text)

# Save
out_path = "/mnt/win_d/VinUni/VinUni_Codelab_Day02_Template/04-workflow-diagram.png"
img.save(out_path, "PNG", dpi=(300, 300))
print(f"Refined Infographic successfully generated at: {out_path}")
