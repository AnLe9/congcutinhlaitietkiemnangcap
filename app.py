import streamlit as st
import pandas as pd
import math

# =========================================================
# CẤU HÌNH
# =========================================================

st.set_page_config(
    page_title="Smart Savings Calculator",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# CSS - GIAO DIỆN + HIỆU ỨNG
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(80,140,255,0.08), transparent 30%),
        radial-gradient(circle at 85% 20%, rgba(120,80,255,0.07), transparent 30%),
        #0e1117;
}

/* ===== TIÊU ĐỀ ===== */

.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 850;
    margin-top: 15px;
    margin-bottom: 5px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #9ecbff,
        #ffffff,
        #b7a6ff,
        #ffffff
    );

    background-size: 300% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: titleGlow 6s linear infinite;
}

@keyframes titleGlow {
    0% {
        background-position: 0% center;
    }
    50% {
        background-position: 100% center;
    }
    100% {
        background-position: 0% center;
    }
}

.sub-title {
    text-align: center;
    font-size: 16px;
    opacity: 0.7;
    margin-bottom: 35px;
}

/* ===== SECTION ===== */

.section-title {
    font-size: 28px;
    font-weight: 750;
    margin-top: 22px;
    margin-bottom: 18px;
}

/* ===== CARD ===== */

.result-box {
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 16px;
    padding: 22px;
    min-height: 145px;

    background: rgba(255,255,255,0.025);

    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

.result-box:hover {
    transform: translateY(-5px);

    border-color: rgba(150,190,255,0.75);

    box-shadow:
        0 8px 30px rgba(80,130,255,0.15);
}

.result-title {
    font-size: 15px;
    opacity: 0.72;
    margin-bottom: 14px;
}

.result-value {
    font-size: 27px;
    font-weight: 750;
}

/* ===== INFO CARD ===== */

.info-card {
    border-left: 3px solid rgba(150,190,255,0.7);
    padding: 8px 15px;
    margin-bottom: 12px;
    background: rgba(255,255,255,0.025);
    border-radius: 5px;
}

/* ===== NOTE ===== */

.note-box {
    border-radius: 12px;
    padding: 16px 20px;
    background: rgba(70,140,230,0.10);
    border: 1px solid rgba(100,160,240,0.25);
    margin-top: 15px;
    margin-bottom: 20px;
}

/* ===== BIG NUMBER ===== */

.big-number {
    font-size: 34px;
    font-weight: 800;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.025);
}

/* ===== BUTTON ===== */

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(100,150,255,0.2);
}

/* ===== DIVIDER ===== */

hr {
    opacity: 0.2;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================================================
# HÀM TÍNH TOÁN
# =========================================================

def calculate_savings(principal, months, annual_rate, interest_type):

    monthly_rate = annual_rate / 100 / 12

    data = []

    # Tháng 0
    data.append({
        "Tháng": 0,
        "Tổng tiền nhận được (gốc + lãi)": principal
    })

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

    total_received = df.iloc[-1][
        "Tổng tiền nhận được (gốc + lãi)"
    ]

    total_interest = total_received - principal

    first_period_interest = principal * monthly_rate

    simple_interest = (
        principal
        * annual_rate
        / 100
        * months
        / 12
    )

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
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Thông tin khoản gửi")

    st.markdown("**Số tiền gửi (VNĐ)**")

    principal = st.number_input(
        "Số tiền gửi",
        min_value=0,
        value=0,
        step=1_000_000,
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

    st.write("")

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
    '<div class="sub-title">'
    'Công cụ tính toán và phân tích tiền gửi tiết kiệm'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHỈ HIỆN KẾT QUẢ SAU KHI NHẤN TÍNH
# =========================================================

if calculate_button:

    if principal <= 0:

        st.warning(
            "⚠️ Vui lòng nhập số tiền gửi lớn hơn 0."
        )

        st.stop()

    # =====================================================
    # TÍNH TOÁN
    # =====================================================

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

    # Hiệu ứng nhỏ
    st.toast(
        "✅ Đã tính toán thành công!",
        icon="💰"
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

                <div class="result-title">
                    💵 Tiền lãi định kỳ
                </div>

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

                <div class="result-title">
                    📈 Tổng tiền lãi
                </div>

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

                <div class="result-title">
                    💰 Tổng tiền nhận được
                </div>

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


    # =====================================================
    # BIỂU ĐỒ
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '📈 Biểu đồ tăng trưởng khoản tiền'
        '</div>',
        unsafe_allow_html=True
    )

    chart_df = df.set_index("Tháng")

    st.line_chart(
        chart_df,
        use_container_width=True,
        height=400
    )


    # =====================================================
    # TIẾN ĐỘ KỲ HẠN
    # =====================================================

    st.markdown(
        '<div class="section-title">⏳ Tiến độ kỳ hạn</div>',
        unsafe_allow_html=True
    )

    progress_value = 1.0

    st.progress(
        progress_value
    )

    st.caption(
        f"Khoản tiền đang được tính trong toàn bộ kỳ hạn "
        f"{months} tháng."
    )


    # =====================================================
    # TÓM TẮT HIỆU QUẢ
    # =====================================================

    st.markdown(
        '<div class="section-title">💡 Tóm tắt hiệu quả</div>',
        unsafe_allow_html=True
    )

    profit_rate = (
        total_interest / principal * 100
        if principal > 0
        else 0
    )

    gain_col1, gain_col2, gain_col3 = st.columns(3)

    with gain_col1:

        st.markdown(
            f"""
            <div class="result-box">

                <div class="result-title">
                    📌 Tỷ suất sinh lời
                </div>

                <div class="big-number">
                    {profit_rate:.2f}%
                </div>

                <small>
                    So với số tiền gốc ban đầu
                </small>

            </div>
            """,
            unsafe_allow_html=True
        )

    with gain_col2:

        st.markdown(
            f"""
            <div class="result-box">

                <div class="result-title">
                    💵 Tiền lãi tạo ra
                </div>

                <div class="big-number">
                    {format_money(total_interest)}
                </div>

                <small>
                    Phần tăng thêm ngoài tiền gốc
                </small>

            </div>
            """,
            unsafe_allow_html=True
        )

    with gain_col3:

        st.markdown(
            f"""
            <div class="result-box">

                <div class="result-title">
                    🏦 Tổng giá trị cuối kỳ
                </div>

                <div class="big-number">
                    {format_money(total_received)}
                </div>

                <small>
                    Gốc + toàn bộ tiền lãi
                </small>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # CÁC TAB PHÂN TÍCH
    # =====================================================

    st.markdown("")

    tab1, tab2 = st.tabs(
        ["⚖️ So sánh lãi đơn - lãi kép", "📅 Bảng chi tiết"]
    )


    # =====================================================
    # TAB 1 - SO SÁNH
    # =====================================================

    with tab1:

        st.markdown(
            '<div class="section-title">'
            '⚖️ So sánh lãi đơn và lãi kép'
            '</div>',
            unsafe_allow_html=True
        )

        compare1, compare2, compare3 = st.columns(3)

        with compare1:

            st.markdown(
                f"""
                <div class="result-box">

                    <div class="result-title">
                        🟨 Tổng lãi đơn
                    </div>

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

                    <div class="result-title">
                        📈 Tổng lãi kép
                    </div>

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

                    <div class="result-title">
                        💰 Lãi kép tăng thêm
                    </div>

                    <div class="result-value">
                        {format_money(extra_compound)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown("")

        comparison_df = pd.DataFrame({
            "Hình thức": [
                "Lãi đơn",
                "Lãi kép"
            ],
            "Tổng tiền lãi": [
                simple_interest,
                compound_interest
            ]
        })

        comparison_chart = comparison_df.set_index(
            "Hình thức"
        )

        st.bar_chart(
            comparison_chart,
            use_container_width=True,
            height=350
        )


        st.markdown(
            f"""
            <div class="note-box">

            <b>💡 Hiểu đơn giản:</b>

            <br><br>

            <b>Lãi đơn</b> chỉ tính lãi trên số tiền gốc ban đầu.

            <br><br>

            <b>Lãi kép</b> cộng tiền lãi vào vốn,
            sau đó tiếp tục tính lãi trên cả phần vốn mới.

            <br><br>

            Vì vậy, trong cùng kỳ hạn và cùng lãi suất,
            <b>lãi kép tạo ra thêm
            {format_money(extra_compound)}</b>
            tiền lãi so với lãi đơn.

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # TAB 2 - BẢNG CHI TIẾT
    # =====================================================

    with tab2:

        st.markdown(
            '<div class="section-title">'
            '📅 Diễn biến khoản tiền theo từng tháng'
            '</div>',
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


    # =====================================================
    # GHI CHÚ CUỐI
    # =====================================================

    st.divider()

    st.caption(
        "💰 Smart Savings Calculator • "
        "Kết quả được tính dựa trên số tiền, kỳ hạn và lãi suất bạn nhập."
    )


# =========================================================
# TRẠNG THÁI BAN ĐẦU
# =========================================================

else:

    st.markdown("")
    st.markdown("")

    st.info(
        "👈 Nhập số tiền gửi ở bên trái rồi nhấn "
        "**TÍNH TOÁN** để bắt đầu."
    )

    st.markdown("")

    empty1, empty2, empty3 = st.columns(3)

    with empty1:
        st.markdown(
            """
            ### 💰
            **Nhập khoản tiền**

            Điền số tiền bạn muốn gửi.
            """
        )

    with empty2:
        st.markdown(
            """
            ### 📈
            **Phân tích tăng trưởng**

            Xem khoản tiền thay đổi theo thời gian.
            """
        )

    with empty3:
        st.markdown(
            """
            ### ⚖️
            **So sánh lãi suất**

            Hiểu sự khác nhau giữa lãi đơn và lãi kép.
            """
        )
