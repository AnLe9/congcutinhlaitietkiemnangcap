import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================

st.set_page_config(
    page_title="Smart Savings Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background: #0e1117;
}

/* Tiêu đề */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #aab2c0;
    font-size: 16px;
    margin-bottom: 35px;
}

/* Card kết quả */
.result-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 18px;
    padding: 24px;
    min-height: 155px;
    transition: all 0.25s ease;
}

.result-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255,255,255,0.55);
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.result-title {
    font-size: 16px;
    color: #cbd1dc;
    margin-bottom: 18px;
}

.result-value {
    font-size: 28px;
    font-weight: 800;
    color: white;
}

/* Thông tin */
.info-box {
    background: rgba(255,255,255,0.035);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    padding: 20px;
    height: 100%;
}

.info-label {
    color: #9da6b5;
    font-size: 14px;
    margin-bottom: 8px;
}

.info-value {
    color: white;
    font-size: 19px;
    font-weight: 700;
}

/* Nút */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 48px;
    font-weight: 700;
    font-size: 16px;
}

/* Bảng */
.dataframe {
    border-radius: 12px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================

def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("## ⚙️ Thông tin khoản gửi")

    amount_text = st.text_input(
        "Số tiền gửi (VNĐ)",
        placeholder="Ví dụ: 100000000"
    )

    months_text = st.text_input(
        "Kỳ hạn (tháng)",
        placeholder="Ví dụ: 12"
    )

    rate_text = st.text_input(
        "Lãi suất (%/năm)",
        placeholder="Ví dụ: 5"
    )

    interest_type = st.selectbox(
        "Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    receive_type = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Lĩnh lãi cuối kỳ",
            "Lĩnh lãi theo tháng"
        ]
    )

    calculate = st.button(
        "🧮 TÍNH TOÁN",
        use_container_width=True
    )


# =========================
# TIÊU ĐỀ
# =========================

st.markdown(
    '<div class="main-title">💰 SMART SAVINGS CALCULATOR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Công cụ tính toán và phân tích tiền gửi tiết kiệm</div>',
    unsafe_allow_html=True
)


# =========================
# TRẠNG THÁI BAN ĐẦU
# =========================

if "calculated" not in st.session_state:
    st.session_state.calculated = False


# =========================
# XỬ LÝ TÍNH TOÁN
# =========================

if calculate:

    try:
        amount = float(
            amount_text.replace(",", "").replace(".", "")
        )

        months = int(months_text)

        rate = float(
            rate_text.replace(",", ".")
        )

        if amount <= 0:
            st.error("Số tiền gửi phải lớn hơn 0.")

        elif months <= 0:
            st.error("Kỳ hạn phải lớn hơn 0 tháng.")

        elif rate < 0:
            st.error("Lãi suất không được âm.")

        else:
            st.session_state.calculated = True
            st.session_state.amount = amount
            st.session_state.months = months
            st.session_state.rate = rate
            st.session_state.interest_type = interest_type
            st.session_state.receive_type = receive_type

    except ValueError:
        st.error(
            "Vui lòng nhập số hợp lệ. Ví dụ: 100000000 ; 12 ; 5"
        )


# =========================
# HIỂN THỊ KẾT QUẢ
# =========================

if st.session_state.calculated:

    amount = st.session_state.amount
    months = st.session_state.months
    rate = st.session_state.rate
    interest_type = st.session_state.interest_type
    receive_type = st.session_state.receive_type

    monthly_rate = rate / 100 / 12

    # -------------------------
    # TÍNH TOÁN
    # -------------------------

    data = []

    for month in range(months + 1):

        if interest_type == "Lãi đơn":

            total = amount * (
                1 + (rate / 100) * month / 12
            )

        else:

            total = amount * (
                (1 + monthly_rate) ** month
            )

        interest = total - amount

        data.append({
            "Tháng": month,
            "Lãi": interest,
            "Tổng gốc + lãi": total
        })

    df = pd.DataFrame(data)

    final_total = df.iloc[-1]["Tổng gốc + lãi"]
    total_interest = df.iloc[-1]["Lãi"]

    periodic_interest = (
        total_interest / months
        if months > 0
        else 0
    )

    # =========================
    # KẾT QUẢ TỔNG QUÁT
    # =========================

    st.markdown("## 📊 Kết quả tính toán")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">💵 Tiền lãi định kỳ</div>
                <div class="result-value">
                    {format_money(periodic_interest)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">📈 Tổng tiền lãi</div>
                <div class="result-value">
                    {format_money(total_interest)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">💰 Tổng tiền nhận được</div>
                <div class="result-value">
                    {format_money(final_total)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # THÔNG TIN KHOẢN GỬI
    # =========================

    st.markdown("## 📋 Thông tin khoản gửi")

    info1, info2, info3, info4 = st.columns(4)

    with info1:
        st.markdown(
            f"""
            <div class="info-box">
                <div class="info-label">Số tiền gốc</div>
                <div class="info-value">
                    {format_money(amount)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with info2:
        st.markdown(
            f"""
            <div class="info-box">
                <div class="info-label">Kỳ hạn</div>
                <div class="info-value">
                    {months} tháng
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with info3:
        st.markdown(
            f"""
            <div class="info-box">
                <div class="info-label">Lãi suất</div>
                <div class="info-value">
                    {rate:.2f}%/năm
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with info4:
        st.markdown(
            f"""
            <div class="info-box">
                <div class="info-label">Hình thức tính lãi</div>
                <div class="info-value">
                    {interest_type}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # BIỂU ĐỒ
    # =========================

    st.markdown("## 📈 Biểu đồ tăng trưởng khoản tiền")

    chart_df = df.set_index("Tháng")[
        ["Tổng gốc + lãi"]
    ]

    st.line_chart(
        chart_df,
        use_container_width=True,
        height=400
    )

    # =========================
    # BẢNG CHI TIẾT
    # =========================

    st.markdown("## 📑 Bảng chi tiết")

    st.caption(
        "Theo dõi số tiền lãi và tổng số tiền nhận được qua từng tháng."
    )

    display_df = df.copy()

    display_df["Lãi"] = display_df["Lãi"].apply(
        lambda x: f"{x:,.0f} VNĐ"
    )

    display_df["Tổng gốc + lãi"] = display_df[
        "Tổng gốc + lãi"
    ].apply(
        lambda x: f"{x:,.0f} VNĐ"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # GHI CHÚ
    # =========================

    st.info(
        "💡 Lãi đơn chỉ tính lãi trên số tiền gốc ban đầu. "
        "Lãi kép cộng tiền lãi vào vốn để tiếp tục sinh lãi "
        "ở các tháng tiếp theo."
    )

else:

    # =========================
    # MÀN HÌNH KHI CHƯA NHẬP
    # =========================

    st.markdown(
        """
        <div style="
            margin-top:60px;
            padding:50px;
            text-align:center;
            border:1px solid rgba(255,255,255,0.12);
            border-radius:20px;
            background:rgba(255,255,255,0.025);
        ">
            <div style="font-size:55px;">💰</div>
            <h2>Chưa có dữ liệu tính toán</h2>
            <p style="color:#9da6b5;">
                Nhập số tiền, kỳ hạn và lãi suất ở bên trái,
                sau đó bấm <b>🧮 TÍNH TOÁN</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
