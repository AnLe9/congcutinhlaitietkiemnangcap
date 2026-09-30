import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Smart Savings Calculator",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# CSS - GIAO DIỆN
# =========================================================

st.markdown("""
<style>

    /* Nền tổng thể */
    .stApp {
        background: #101820;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #18242b;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #b8c5ca;
        font-size: 16px;
        margin-bottom: 35px;
    }

    /* Card kết quả */
    .result-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 18px;
        padding: 24px 20px;
        min-height: 145px;
        transition: 0.25s ease;
    }

    .result-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255,255,255,0.45);
        background: rgba(255,255,255,0.07);
    }

    .result-title {
        color: #c7d0d4;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .result-value {
        color: white;
        font-size: 26px;
        font-weight: 800;
    }

    .result-note {
        color: #9eabb0;
        font-size: 13px;
        margin-top: 8px;
    }

    /* Khung thông tin */
    .info-box {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 16px;
        padding: 20px;
        margin-top: 20px;
        margin-bottom: 25px;
    }

    .info-label {
        color: #9eabb0;
        font-size: 14px;
        margin-bottom: 7px;
    }

    .info-value {
        color: white;
        font-size: 18px;
        font-weight: 700;
    }

    /* Section */
    .section-title {
        font-size: 25px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Bảng */
    .table-container {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 16px;
        padding: 15px;
        margin-top: 10px;
    }

    /* Nút */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 48px;
        font-weight: 800;
        font-size: 16px;
        background: #ffffff;
        color: #101820;
        border: none;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        background: #e9eef0;
    }

    /* Ẩn menu mặc định */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def format_vnd(value):
    """Định dạng tiền Việt Nam."""
    return f"{value:,.0f} VNĐ"


def calculate_savings(principal, months, annual_rate, interest_type):
    """
    Tính tiền gửi.

    Lãi đơn:
        Mỗi tháng tính lãi trên tiền gốc ban đầu.

    Lãi kép:
        Tiền lãi được cộng vào vốn sau mỗi tháng.
    """

    monthly_rate = annual_rate / 12 / 100

    rows = []

    current_amount = principal
    total_interest = 0

    # Tháng 0
    rows.append({
        "Tháng": 0,
        "Tiền lãi nhận được": 0,
        "Tổng tiền nhận được": principal
    })

    for month in range(1, months + 1):

        if interest_type == "Lãi đơn":
            interest = principal * monthly_rate
            current_amount = principal + principal * monthly_rate * month

        else:
            new_amount = current_amount * (1 + monthly_rate)
            interest = new_amount - current_amount
            current_amount = new_amount

        total_interest += interest

        rows.append({
            "Tháng": month,
            "Tiền lãi nhận được": interest,
            "Tổng tiền nhận được": current_amount
        })

    return pd.DataFrame(rows), total_interest, current_amount


# =========================================================
# SIDEBAR - NHẬP DỮ LIỆU
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Thông tin khoản gửi")

    principal = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0,
        value=100_000_000,
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
        value=5.0,
        step=0.1,
        format="%.2f"
    )

    interest_type = st.selectbox(
        "Hình thức tính lãi",
        ["Lãi đơn", "Lãi kép"]
    )

    st.markdown("")

    calculate = st.button("🧮 TÍNH TOÁN")


# =========================================================
# TRANG CHÍNH
# =========================================================

st.markdown(
    '<div class="main-title">💰 SMART SAVINGS CALCULATOR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Công cụ tính toán và phân tích tiền gửi tiết kiệm</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHỈ HIỆN KẾT QUẢ SAU KHI BẤM TÍNH
# =========================================================

if calculate:

    df, total_interest, final_amount = calculate_savings(
        principal,
        months,
        annual_rate,
        interest_type
    )

    monthly_interest = (
        principal * annual_rate / 12 / 100
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
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">💵 Tiền lãi định kỳ</div>
            <div class="result-value">{format_vnd(monthly_interest)}</div>
            <div class="result-note">Tiền lãi mỗi tháng</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">📈 Tổng tiền lãi</div>
            <div class="result-value">{format_vnd(total_interest)}</div>
            <div class="result-note">Tổng lãi sau {months} tháng</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">💰 Tổng tiền nhận được</div>
            <div class="result-value">{format_vnd(final_amount)}</div>
            <div class="result-note">Bao gồm cả gốc và lãi</div>
        </div>
        """, unsafe_allow_html=True)


    # =====================================================
    # THÔNG TIN KHOẢN GỬI
    # =====================================================

    st.markdown(
        '<div class="section-title">📋 Thông tin khoản gửi</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="info-box">
        <div style="display:flex; justify-content:space-between; 
                    gap:30px; flex-wrap:wrap;">

            <div>
                <div class="info-label">Số tiền gốc</div>
                <div class="info-value">{format_vnd(principal)}</div>
            </div>

            <div>
                <div class="info-label">Kỳ hạn</div>
                <div class="info-value">{months} tháng</div>
            </div>

            <div>
                <div class="info-label">Lãi suất</div>
                <div class="info-value">{annual_rate:.2f}%/năm</div>
            </div>

            <div>
                <div class="info-label">Hình thức tính lãi</div>
                <div class="info-value">{interest_type}</div>
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)


    # =====================================================
    # BIỂU ĐỒ
    # =====================================================

    st.markdown(
        '<div class="section-title">📈 Biểu đồ tăng trưởng khoản tiền</div>',
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Tháng"],
            y=df["Tổng tiền nhận được"],
            mode="lines+markers",
            name="Tổng tiền",
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate=
                "Tháng %{x}<br>"
                "Tổng tiền: %{y:,.0f} VNĐ"
                "<extra></extra>"
        )
    )

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(
            title="Tháng",
            dtick=1,
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)"
        ),
        yaxis=dict(
            title="Tổng tiền (VNĐ)",
            tickformat=",.0f",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)"
        ),
        hovermode="x unified",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    # =====================================================
    # BẢNG DIỄN BIẾN KHOẢN TIỀN
    # =====================================================

    st.markdown(
        '<div class="section-title">📅 Bảng diễn biến khoản tiền</div>',
        unsafe_allow_html=True
    )

    table_df = df.copy()

    table_df["Tiền lãi nhận được"] = table_df[
        "Tiền lãi nhận được"
    ].apply(format_vnd)

    table_df["Tổng tiền nhận được"] = table_df[
        "Tổng tiền nhận được"
    ].apply(format_vnd)

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tháng": st.column_config.NumberColumn(
                "Tháng",
                format="%d"
            ),
            "Tiền lãi nhận được": st.column_config.TextColumn(
                "Tiền lãi nhận được"
            ),
            "Tổng tiền nhận được": st.column_config.TextColumn(
                "Tổng tiền nhận được"
            )
        }
    )


    # =====================================================
    # GIẢI THÍCH NGẮN
    # =====================================================

    st.markdown(
        '<div class="section-title">💡 Cách hiểu kết quả</div>',
        unsafe_allow_html=True
    )

    if interest_type == "Lãi đơn":

        st.info(
            "Lãi đơn: tiền lãi mỗi kỳ được tính dựa trên số tiền gốc ban đầu. "
            "Tiền lãi không được cộng vào vốn để tiếp tục sinh lãi."
        )

    else:

        st.info(
            "Lãi kép: tiền lãi được cộng vào số tiền đang có sau mỗi kỳ. "
            "Vì vậy, các kỳ sau có thể tạo ra nhiều tiền lãi hơn các kỳ trước."
        )


else:

    # =====================================================
    # MÀN HÌNH BAN ĐẦU
    # =====================================================

    st.markdown("""
    <div style="
        margin-top:60px;
        text-align:center;
        padding:50px 20px;
        border:1px solid rgba(255,255,255,0.12);
        border-radius:20px;
        background:rgba(255,255,255,0.03);
    ">
        <div style="font-size:50px;">💰</div>

        <div style="
            font-size:25px;
            font-weight:800;
            margin-top:15px;
        ">
            Nhập thông tin khoản gửi
        </div>

        <div style="
            color:#9eabb0;
            font-size:16px;
            margin-top:10px;
        ">
            Điền số tiền, kỳ hạn và lãi suất ở bên trái,
            sau đó bấm <b>TÍNH TOÁN</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)
