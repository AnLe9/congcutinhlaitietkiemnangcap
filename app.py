import streamlit as st
import pandas as pd
import math

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Smart Savings Calculator",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

    /* Nền tổng thể */
    .stApp {
        background-color: #0e1117;
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 16px;
        opacity: 0.75;
        margin-bottom: 35px;
    }

    /* Khung kết quả */
    .result-box {
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 14px;
        padding: 22px;
        min-height: 135px;
        background: transparent;
    }

    .result-title {
        font-size: 16px;
        opacity: 0.8;
        margin-bottom: 15px;
    }

    .result-value {
        font-size: 28px;
        font-weight: 700;
    }

    /* Khung thông tin */
    .info-box {
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 12px;
        padding: 18px;
        background: transparent;
    }

    /* Tiêu đề section */
    .section-title {
        font-size: 28px;
        font-weight: 750;
        margin-top: 20px;
        margin-bottom: 18px;
    }

    /* Note */
    .note-box {
        border-radius: 10px;
        padding: 14px 18px;
        background-color: rgba(80,160,220,0.15);
        border: 1px solid rgba(80,160,220,0.3);
        margin-top: 15px;
        margin-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================================================
# HÀM TÍNH LÃI
# =========================================================

def calculate_savings(principal, months, annual_rate, interest_type):

    monthly_rate = annual_rate / 100 / 12

    data = []

    # Tháng 0
    data.append({
        "Tháng": 0,
        "Tổng tiền nhận được (gốc + lãi)": principal
    })

    current = principal

    for month in range(1, months + 1):

        if interest_type == "Lãi đơn":
            current = principal * (
                1 + annual_rate / 100 * month / 12
            )

        else:
            current = principal * (
                1 + monthly_rate
            ) ** month

        data.append({
            "Tháng": month,
            "Tổng tiền nhận được (gốc + lãi)": current
        })

    df = pd.DataFrame(data)

    total_received = current
    total_interest = total_received - principal

    # Lãi của kỳ đầu tiên
    first_period_interest = principal * monthly_rate

    # Lãi đơn
    simple_interest = principal * annual_rate / 100 * months / 12

    # Lãi kép
    compound_total = principal * (
        1 + monthly_rate
    ) ** months

    compound_interest = compound_total - principal

    extra_compound = compound_interest - simple_interest

    return (
        df,
        first_period_interest,
        total_interest,
        total_received,
        simple_interest,
        compound_interest,
        extra_compound
    )


# =========================================================
# SIDEBAR - NHẬP THÔNG TIN
# =========================================================

with st.sidebar:

    st.header("⚙️ Thông tin khoản gửi")

    st.markdown("**Số tiền gửi (VNĐ)**")
    principal = st.number_input(
        "Số tiền gửi",
        min_value=0,
        value=0,
        step=1000000,
        format="%d",
        label_visibility="collapsed"
    )

    st.markdown("**Kỳ hạn (tháng)**")
    months = st.number_input(
        "Kỳ hạn",
        min_value=1,
        max_value=120,
        value=12,
        step=1,
        label_visibility="collapsed"
    )

    st.markdown("**Lãi suất (%/năm)**")
    annual_rate = st.number_input(
        "Lãi suất",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        format="%.2f",
        label_visibility="collapsed"
    )

    st.markdown("**Hình thức tính lãi**")
    interest_type = st.selectbox(
        "Hình thức tính lãi",
        ["Lãi đơn", "Lãi kép"],
        label_visibility="collapsed"
    )

    st.markdown("**Hình thức nhận lãi**")
    receive_type = st.selectbox(
        "Hình thức nhận lãi",
        ["Lãnh lãi theo tháng", "Lãnh lãi cuối kỳ"],
        label_visibility="collapsed"
    )

    calculate_button = st.button(
        "🧮 TÍNH TOÁN",
        use_container_width=True
    )


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
# CHỈ TÍNH KHI NGƯỜI DÙNG NHẤN TÍNH TOÁN
# =========================================================

if calculate_button:

    if principal <= 0:
        st.warning("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    # Tính toán
    (
        df,
        first_period_interest,
        total_interest,
        total_received,
        simple_interest,
        compound_interest,
        extra_compound
    ) = calculate_savings(
        principal,
        months,
        annual_rate,
        interest_type
    )

    # =====================================================
    # KẾT QUẢ
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Kết quả tính toán</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">💵 Tiền lãi định kỳ</div>
                <div class="result-value">
                    {format_money(first_period_interest)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="result-box">
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
            <div class="result-box">
                <div class="result-title">💰 Tổng tiền nhận được</div>
                <div class="result-value">
                    {format_money(total_received)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # THÔNG TIN KHOẢN GỬI
    # =====================================================

    st.markdown(
        '<div class="section-title">📋 Thông tin khoản gửi</div>',
        unsafe_allow_html=True
    )

    info1, info2, info3, info4 = st.columns(4)

    with info1:
        st.markdown("**Số tiền gốc**")
        st.write(format_money(principal))

    with info2:
        st.markdown("**Kỳ hạn**")
        st.write(f"{months} tháng")

    with info3:
        st.markdown("**Lãi suất**")
        st.write(f"{annual_rate:.2f}%/năm")

    with info4:
        st.markdown("**Hình thức tính lãi**")
        st.write(interest_type)

    st.divider()

    # =====================================================
    # BIỂU ĐỒ
    # =====================================================

    st.markdown(
        '<div class="section-title">📈 Biểu đồ tăng trưởng khoản tiền</div>',
        unsafe_allow_html=True
    )

    chart_df = df.set_index("Tháng")

    st.line_chart(
        chart_df,
        use_container_width=True
    )

    # =====================================================
    # CÁC MỐC CHÍNH
    # =====================================================

    st.markdown(
        '<div class="section-title">📌 Các mốc chính</div>',
        unsafe_allow_html=True
    )

    # Chọn các mốc: 0, 2, 4, 6, 8, 10, kỳ hạn
    milestone_months = [0]

    for m in range(2, months + 1, 2):
        if m not in milestone_months:
            milestone_months.append(m)

    if months not in milestone_months:
        milestone_months.append(months)

    milestone_months = sorted(
        set(milestone_months)
    )

    milestone_df = df[
        df["Tháng"].isin(milestone_months)
    ].copy()

    milestone_df["Tổng tiền nhận được (gốc + lãi)"] = (
        milestone_df[
            "Tổng tiền nhận được (gốc + lãi)"
        ].apply(format_money)
    )

    # Dùng dataframe thay vì HTML card
    # để không còn lỗi <div class=...>
    st.dataframe(
        milestone_df,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # SO SÁNH LÃI ĐƠN VÀ LÃI KÉP
    # =====================================================

    st.markdown(
        '<div class="section-title">⚖️ So sánh lãi đơn và lãi kép</div>',
        unsafe_allow_html=True
    )

    compare1, compare2, compare3 = st.columns(3)

    with compare1:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">🟨 Tổng lãi đơn</div>
                <div class="result-value">
                    {format_money(simple_interest)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with compare2:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">📈 Tổng lãi kép</div>
                <div class="result-value">
                    {format_money(compound_interest)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with compare3:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">💰 Lãi kép tăng thêm</div>
                <div class="result-value">
                    {format_money(extra_compound)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # GIẢI THÍCH
    # =====================================================

    st.markdown(
        f"""
        <div class="note-box">
            <b>Lãi đơn:</b> tiền lãi chỉ được tính trên số tiền gốc ban đầu.
            <br><br>
            <b>Lãi kép:</b> tiền lãi được cộng vào vốn để tiếp tục sinh lãi
            ở các kỳ tiếp theo.
            <br><br>
            Với khoản gửi hiện tại, nếu tính theo cùng kỳ hạn và lãi suất,
            lãi kép cao hơn lãi đơn
            <b>{format_money(extra_compound)}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # BẢNG DIỄN BIẾN KHOẢN TIỀN
    # =====================================================

    st.markdown(
        '<div class="section-title">📅 Bảng diễn biến khoản tiền</div>',
        unsafe_allow_html=True
    )

    display_df = df.copy()

    display_df[
        "Tổng tiền nhận được (gốc + lãi)"
    ] = display_df[
        "Tổng tiền nhận được (gốc + lãi)"
    ].apply(format_money)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:

    # =====================================================
    # TRẠNG THÁI BAN ĐẦU
    # =====================================================

    st.info(
        "👈 Nhập số tiền gửi ở bên trái rồi nhấn **TÍNH TOÁN** "
        "để xem kết quả."
    )
