import streamlit as st
import math

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Smart Savings Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS - GIAO DIỆN + HIỆU ỨNG
# =========================================================

st.markdown("""
<style>

/* ===== NỀN ===== */

.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(255,255,255,0.05), transparent 22%),
        radial-gradient(circle at 85% 10%, rgba(255,255,255,0.04), transparent 20%),
        linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0b0f19 100%);
    color: white;
}

/* ===== BỎ KHOẢNG TRỐNG TRÊN ===== */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ===== TIÊU ĐỀ ===== */

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 1px;
    margin-top: 5px;
    margin-bottom: 5px;
    color: white;
    text-shadow:
        0 0 8px rgba(255,255,255,0.35),
        0 0 25px rgba(255,255,255,0.10);
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    font-size: 16px;
    margin-bottom: 35px;
}

/* ===== HIỆU ỨNG LẤP LÁNH ===== */

.sparkle {
    position: fixed;
    width: 5px;
    height: 5px;
    background: white;
    border-radius: 50%;
    opacity: 0.65;
    box-shadow: 0 0 12px white;
    animation: sparkle 3s infinite ease-in-out;
    z-index: 0;
}

.sparkle1 {
    top: 18%;
    left: 10%;
    animation-delay: 0s;
}

.sparkle2 {
    top: 32%;
    left: 82%;
    animation-delay: 1s;
}

.sparkle3 {
    top: 72%;
    left: 18%;
    animation-delay: 2s;
}

.sparkle4 {
    top: 82%;
    left: 90%;
    animation-delay: 1.5s;
}

@keyframes sparkle {
    0%, 100% {
        opacity: 0.15;
        transform: scale(0.6);
    }
    50% {
        opacity: 0.9;
        transform: scale(1.5);
    }
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #151b29 0%, #0d111b 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.sidebar-title {
    font-size: 21px;
    font-weight: 800;
    margin-bottom: 25px;
}

/* ===== INPUT ===== */

div[data-baseweb="input"] {
    background: rgba(255,255,255,0.07);
    border-radius: 10px;
}

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.07);
    border-radius: 10px;
}

/* ===== NÚT TÍNH ===== */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.35);
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.12),
        rgba(255,255,255,0.04)
    );
    color: white;
    font-weight: 800;
    padding: 13px;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 0 15px rgba(255,255,255,0.15),
        0 8px 25px rgba(0,0,0,0.25);
    border-color: rgba(255,255,255,0.7);
}

/* ===== SECTION ===== */

.section-title {
    font-size: 27px;
    font-weight: 850;
    margin-top: 30px;
    margin-bottom: 18px;
}

/* ===== RESULT CARD ===== */

.result-card {
    min-height: 155px;
    padding: 24px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.25);
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.09),
            rgba(255,255,255,0.025)
        );
    box-shadow:
        0 10px 35px rgba(0,0,0,0.20),
        inset 0 1px 0 rgba(255,255,255,0.08);
    animation: cardAppear 0.65s ease both;
    transition: all 0.3s ease;
}

.result-card:hover {
    transform: translateY(-5px);
    box-shadow:
        0 15px 40px rgba(0,0,0,0.3),
        0 0 25px rgba(255,255,255,0.07);
}

.result-title {
    color: #cbd5e1;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 15px;
}

.result-value {
    color: white;
    font-size: 27px;
    font-weight: 900;
    letter-spacing: 0.5px;
}

.result-note {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 12px;
}

@keyframes cardAppear {
    from {
        opacity: 0;
        transform: translateY(18px) scale(0.97);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* ===== INFO BOX ===== */

.info-box {
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 18px;
    padding: 22px;
    background: rgba(255,255,255,0.035);
    margin-top: 25px;
}

/* ===== TABLE ===== */

.detail-table {
    width: 100%;
    border-collapse: collapse;
    overflow: hidden;
    border-radius: 15px;
    background: rgba(255,255,255,0.035);
}

.detail-table th {
    text-align: left;
    padding: 15px;
    background: rgba(255,255,255,0.08);
    color: #e2e8f0;
    font-size: 14px;
}

.detail-table td {
    padding: 13px 15px;
    border-top: 1px solid rgba(255,255,255,0.08);
    color: #cbd5e1;
}

.detail-table tr:hover {
    background: rgba(255,255,255,0.05);
}

/* ===== EMPTY STATE ===== */

.empty-box {
    text-align: center;
    padding: 60px 20px;
    border: 1px dashed rgba(255,255,255,0.18);
    border-radius: 20px;
    color: #94a3b8;
    background: rgba(255,255,255,0.025);
}

.empty-icon {
    font-size: 48px;
    margin-bottom: 10px;
}

/* ===== FOOTER ===== */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 50px;
}

</style>

<div class="sparkle sparkle1"></div>
<div class="sparkle sparkle2"></div>
<div class="sparkle sparkle3"></div>
<div class="sparkle sparkle4"></div>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">💰 SMART SAVINGS CALCULATOR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Công cụ tính toán và phân tích tiền gửi tiết kiệm</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR - THÔNG TIN ĐẦU VÀO
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚙️ Thông tin khoản gửi</div>',
        unsafe_allow_html=True
    )

    principal = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0,
        value=0,
        step=1_000_000,
        format="%d"
    )

    months = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

    annual_rate = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.01,
        format="%.2f"
    )

    interest_type = st.selectbox(
        "Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    payout_type = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Lãnh lãi cuối kỳ",
            "Lãnh lãi theo tháng"
        ]
    )

    st.write("")

    calculate = st.button("🧮 TÍNH TOÁN")


# =========================================================
# CHƯA TÍNH
# =========================================================

if not calculate:

    st.markdown("""
    <div class="empty-box">
        <div class="empty-icon">💰</div>
        <h3>Nhập thông tin khoản tiết kiệm</h3>
        <p>
            Điền số tiền, kỳ hạn và lãi suất ở bảng bên trái,
            sau đó nhấn <b>🧮 TÍNH TOÁN</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">Smart Savings Calculator • Công cụ mô phỏng tiền gửi</div>',
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# KIỂM TRA DỮ LIỆU
# =========================================================

if principal <= 0:

    st.error("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0 VNĐ.")
    st.stop()

if annual_rate < 0:

    st.error("⚠️ Lãi suất không được nhỏ hơn 0%.")
    st.stop()


# =========================================================
# TÍNH TOÁN
# =========================================================

monthly_rate = annual_rate / 100 / 12

balances = []
interests = []

balance = float(principal)

# ---------------------------------------------------------
# LÃI ĐƠN
# ---------------------------------------------------------

if interest_type == "Lãi đơn":

    monthly_interest = principal * monthly_rate

    for month in range(1, months + 1):

        interest = monthly_interest

        balance = principal + monthly_interest * month

        interests.append(interest)
        balances.append(balance)


# ---------------------------------------------------------
# LÃI KÉP
# ---------------------------------------------------------

else:

    if payout_type == "Lãnh lãi theo tháng":

        # Lãi được trả ra mỗi tháng nên không nhập vào vốn
        monthly_interest = principal * monthly_rate

        for month in range(1, months + 1):

            interest = monthly_interest

            balance = principal + monthly_interest * month

            interests.append(interest)
            balances.append(balance)

    else:

        # Lãi nhập vào vốn mỗi tháng
        for month in range(1, months + 1):

            old_balance = balance

            interest = old_balance * monthly_rate

            balance = old_balance + interest

            interests.append(interest)
            balances.append(balance)


# =========================================================
# KẾT QUẢ
# =========================================================

total_received = balances[-1]
total_interest = total_received - principal

periodic_interest = interests[0] if interests else 0


# =========================================================
# HIỆU ỨNG
# =========================================================

st.balloons()


# =========================================================
# KẾT QUẢ TÍNH TOÁN
# =========================================================

st.markdown(
    '<div class="section-title">📊 Kết quả tính toán</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">💵 Tiền lãi định kỳ</div>
        <div class="result-value">{format_money(periodic_interest)}</div>
        <div class="result-note">Khoản lãi phát sinh mỗi tháng</div>
    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">📈 Tổng tiền lãi</div>
        <div class="result-value">{format_money(total_interest)}</div>
        <div class="result-note">Tổng lãi sau {months} tháng</div>
    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">💰 Tổng tiền nhận được</div>
        <div class="result-value">{format_money(total_received)}</div>
        <div class="result-note">Gốc + toàn bộ tiền lãi</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# THÔNG TIN KHOẢN GỬI
# =========================================================

st.markdown(
    '<div class="section-title">📋 Thông tin khoản gửi</div>',
    unsafe_allow_html=True
)

info1, info2, info3, info4 = st.columns(4)

with info1:
    st.markdown(f"""
    **Số tiền gốc**

    {format_money(principal)}
    """)

with info2:
    st.markdown(f"""
    **Kỳ hạn**

    {months} tháng
    """)

with info3:
    st.markdown(f"""
    **Lãi suất**

    {annual_rate:.2f}%/năm
    """)

with info4:
    st.markdown(f"""
    **Hình thức**

    {interest_type}
    """)


# =========================================================
# BIỂU ĐỒ TĂNG TRƯỞNG
# =========================================================

st.markdown(
    '<div class="section-title">📈 Biểu đồ tăng trưởng khoản tiền</div>',
    unsafe_allow_html=True
)

# Dùng Streamlit native chart → KHÔNG CẦN PLOTLY
chart_data = {
    "Tháng": list(range(0, months + 1)),
    "Số tiền": [principal] + balances
}

st.line_chart(
    chart_data,
    x="Tháng",
    y="Số tiền",
    height=350
)


# =========================================================
# BẢNG CHI TIẾT
# =========================================================

st.markdown(
    '<div class="section-title">📑 Bảng chi tiết</div>',
    unsafe_allow_html=True
)

table_html = """
<table class="detail-table">
<tr>
    <th>Tháng</th>
    <th>Lãi</th>
    <th>Tổng gốc + lãi</th>
</tr>
"""

for i in range(months):

    table_html += f"""
    <tr>
        <td>Tháng {i + 1}</td>
        <td>{format_money(interests[i])}</td>
        <td>{format_money(balances[i])}</td>
    </tr>
    """

table_html += "</table>"

st.markdown(table_html, unsafe_allow_html=True)


# =========================================================
# GHI CHÚ
# =========================================================

st.markdown(f"""
<div class="info-box">

### 💡 Giải thích nhanh

- **Lãi đơn:** tiền lãi chỉ được tính trên số tiền gốc ban đầu.
- **Lãi kép:** tiền lãi được cộng vào vốn để tiếp tục sinh lãi ở các tháng sau.
- **Lãnh lãi theo tháng:** tiền lãi được nhận ra mỗi tháng nên không cộng vào vốn.
- **Lãnh lãi cuối kỳ:** tiền được nhận vào cuối kỳ hạn.

**Sau {months} tháng:**

💵 Tiền gốc: **{format_money(principal)}**

📈 Tiền lãi: **{format_money(total_interest)}**

💰 Tổng nhận: **{format_money(total_received)}**

</div>
""", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">✨ Smart Savings Calculator • Tính toán đơn giản, trực quan, dễ hiểu</div>',
    unsafe_allow_html=True
)
