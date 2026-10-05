import streamlit as st
import pandas as pd

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
# CSS - GIAO DIỆN GỌN GÀNG, HỌC THUẬT
# =========================================================

st.markdown("""
<style>

    /* Nền tổng thể */
    .stApp {
        background: #0f172a;
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 10px;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 15px;
        margin-bottom: 35px;
    }

    /* Tiêu đề section */
    .section-title {
        color: #f8fafc;
        font-size: 25px;
        font-weight: 750;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* Card */
    .info-card {
        background: #172033;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
    }

    .info-label {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 6px;
    }

    .info-value {
        color: #f8fafc;
        font-size: 23px;
        font-weight: 750;
    }

    /* Kết quả chính */
    .result-card {
        background: #172033;
        border: 1px solid #475569;
        border-radius: 15px;
        padding: 22px;
        min-height: 135px;
        transition: 0.2s ease;
    }

    .result-card:hover {
        border-color: #94a3b8;
        transform: translateY(-2px);
    }

    .result-title {
        color: #cbd5e1;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .result-number {
        color: #f8fafc;
        font-size: 27px;
        font-weight: 800;
    }

    .result-note {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 8px;
    }

    /* Phân tích */
    .analysis-box {
        background: #111c30;
        border-left: 4px solid #94a3b8;
        border-radius: 8px;
        padding: 17px 20px;
        color: #cbd5e1;
        line-height: 1.7;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    /* Nút */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 46px;
        font-weight: 700;
        font-size: 16px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
    }

    /* Divider */
    hr {
        border-color: #334155;
    }

    /* Bảng */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


def dinh_dang_trieu(so_tien):
    return f"{so_tien / 1_000_000:.2f} triệu VNĐ"


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">💰 SMART SAVINGS CALCULATOR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Công cụ tính toán và phân tích tiền gửi tiết kiệm'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR - NHẬP DỮ LIỆU
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Thông tin khoản gửi")

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=0.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=1,
        step=1
    )

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1
    )

    hinh_thuc_gui = st.selectbox(
        "Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    hinh_thuc_nhan_lai = st.selectbox(
        "Chu kỳ nhập lãi",
        [
            "Theo tháng",
            "Theo quý",
            "Cuối kỳ"
        ]
    )

    st.markdown("")

    tinh_toan = st.button(
        "🧮 TÍNH LÃI",
        use_container_width=True
    )


# =========================================================
# TRẠNG THÁI BAN ĐẦU
# =========================================================

if "da_tinh" not in st.session_state:
    st.session_state.da_tinh = False

if tinh_toan:

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.session_state.da_tinh = False

    elif lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.session_state.da_tinh = False

    else:
        st.session_state.da_tinh = True


# =========================================================
# MÀN HÌNH CHỜ - KHÔNG TỰ TÍNH
# =========================================================

if not st.session_state.da_tinh:

    st.markdown("""
    <div class="info-card" style="text-align:center; padding:45px 25px;">
        <div style="font-size:42px; margin-bottom:12px;">📊</div>
        <div style="
            color:#f8fafc;
            font-size:22px;
            font-weight:750;
            margin-bottom:10px;
        ">
            Sẵn sàng tính khoản tiết kiệm của bạn
        </div>
        <div style="
            color:#94a3b8;
            font-size:15px;
            line-height:1.7;
        ">
            Nhập số tiền, kỳ hạn và lãi suất ở bảng điều khiển bên trái,
            <br>
            sau đó nhấn <b>🧮 TÍNH LÃI</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# =========================================================
# TÍNH TOÁN
# =========================================================

r = lai_suat / 100
so_nam = ky_han / 12

# ---------------------------------------------------------
# LÃI ĐƠN
# ---------------------------------------------------------

if hinh_thuc_gui == "Lãi đơn":

    tong_tien_lai = tien_gui * r * so_nam
    tong_tien = tien_gui + tong_tien_lai

# ---------------------------------------------------------
# LÃI KÉP
# ---------------------------------------------------------

else:

    if hinh_thuc_nhan_lai == "Theo tháng":
        tan_suat = 12

        tong_tien = tien_gui * (
            1 + r / tan_suat
        ) ** (
            tan_suat * so_nam
        )

    elif hinh_thuc_nhan_lai == "Theo quý":
        tan_suat = 4

        tong_tien = tien_gui * (
            1 + r / tan_suat
        ) ** (
            tan_suat * so_nam
        )

    else:
        # Nhập lãi một lần cuối kỳ
        tong_tien = tien_gui * (1 + r) ** so_nam

    tong_tien_lai = tong_tien - tien_gui


# =========================================================
# LÃI ĐỊNH KỲ
# =========================================================

if hinh_thuc_gui == "Lãi đơn":

    if hinh_thuc_nhan_lai == "Theo tháng":
        lai_dinh_ky = tien_gui * r / 12

    elif hinh_thuc_nhan_lai == "Theo quý":
        lai_dinh_ky = tien_gui * r / 4

    else:
        lai_dinh_ky = tong_tien_lai

else:

    if hinh_thuc_nhan_lai == "Theo tháng":
        lai_dinh_ky = tien_gui * r / 12

    elif hinh_thuc_nhan_lai == "Theo quý":
        lai_dinh_ky = tien_gui * r / 4

    else:
        lai_dinh_ky = tong_tien_lai


# =========================================================
# KẾT QUẢ CHÍNH
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
        <div class="result-number">
            {dinh_dang_tien(lai_dinh_ky)}
        </div>
        <div class="result-note">
            Theo {hinh_thuc_nhan_lai.lower()}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">📈 Tổng tiền lãi</div>
        <div class="result-number">
            {dinh_dang_tien(tong_tien_lai)}
        </div>
        <div class="result-note">
            Sau {ky_han} tháng
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">💰 Tổng gốc + lãi</div>
        <div class="result-number">
            {dinh_dang_tien(tong_tien)}
        </div>
        <div class="result-note">
            Giá trị cuối kỳ
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# THÔNG TIN KHOẢN GỬI
# =========================================================

st.markdown("")
st.markdown(
    '<div class="section-title">📋 Thông tin khoản gửi</div>',
    unsafe_allow_html=True
)

info1, info2, info3, info4 = st.columns(4)

with info1:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">Số tiền gốc</div>
        <div class="info-value">{dinh_dang_tien(tien_gui)}</div>
    </div>
    """, unsafe_allow_html=True)

with info2:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">Kỳ hạn</div>
        <div class="info-value">{ky_han} tháng</div>
    </div>
    """, unsafe_allow_html=True)

with info3:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">Lãi suất</div>
        <div class="info-value">{lai_suat:.2f}%/năm</div>
    </div>
    """, unsafe_allow_html=True)

with info4:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">Phương pháp</div>
        <div class="info-value">{hinh_thuc_gui}</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# PHÂN TÍCH NHANH
# =========================================================

ty_le_lai = (tong_tien_lai / tien_gui * 100) if tien_gui > 0 else 0
lai_trung_binh_thang = tong_tien_lai / ky_han

st.markdown(
    '<div class="section-title">🔎 Phân tích nhanh</div>',
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="analysis-box">

<b>• Tỷ lệ tiền lãi:</b>
{ty_le_lai:.2f}% so với số tiền gốc ban đầu.

<br>

<b>• Lãi bình quân mỗi tháng:</b>
{dinh_dang_tien(lai_trung_binh_thang)}.

<br>

<b>• Giá trị cuối kỳ:</b>
{dinh_dang_tien(tong_tien)}.

<br>

<b>• Hình thức tính:</b>
{hinh_thuc_gui} — {hinh_thuc_nhan_lai.lower()}.

</div>
""", unsafe_allow_html=True)


# =========================================================
# BIỂU ĐỒ LÃI TÍCH LŨY
# =========================================================

st.markdown(
    '<div class="section-title">📈 Lãi tích lũy theo thời gian</div>',
    unsafe_allow_html=True
)

# Tạo dữ liệu theo từng tháng
thang_data = []
tien_hien_tai = tien_gui
lai_tich_luy = 0.0

for thang in range(0, ky_han + 1):

    # Tháng 0
    if thang == 0:

        thang_data.append({
            "Tháng": 0,
            "Lãi tích lũy": 0.0
        })

        continue

    # -------------------------
    # LÃI ĐƠN
    # -------------------------

    if hinh_thuc_gui == "Lãi đơn":

        lai_thang = tien_gui * r / 12

        lai_tich_luy += lai_thang

        tien_hien_tai = tien_gui + lai_tich_luy

    # -------------------------
    # LÃI KÉP
    # -------------------------

    else:

        # Theo tháng
        if hinh_thuc_nhan_lai == "Theo tháng":

            lai_thang = tien_hien_tai * r / 12

            tien_hien_tai += lai_thang
            lai_tich_luy = tien_hien_tai - tien_gui

        # Theo quý
        elif hinh_thuc_nhan_lai == "Theo quý":

            if thang % 3 == 0:

                lai_quy = tien_hien_tai * r / 4

                tien_hien_tai += lai_quy

                lai_tich_luy = tien_hien_tai - tien_gui

        # Cuối kỳ
        else:

            if thang == ky_han:

                tien_hien_tai = tong_tien
                lai_tich_luy = tong_tien_lai

    thang_data.append({
        "Tháng": thang,
        "Lãi tích lũy": lai_tich_luy
    })


chart_df = pd.DataFrame(thang_data)

chart_df = chart_df.set_index("Tháng")

# Đổi sang triệu để biểu đồ dễ nhìn hơn
chart_df["Lãi tích lũy (triệu VNĐ)"] = (
    chart_df["Lãi tích lũy"] / 1_000_000
)

chart_df = chart_df[["Lãi tích lũy (triệu VNĐ)"]]

st.line_chart(
    chart_df,
    height=380
)

st.caption(
    "Biểu đồ thể hiện mức lãi tích lũy qua từng tháng. "
    "Trục dọc được quy đổi sang triệu VNĐ để dễ quan sát biến động."
)


# =========================================================
# BẢNG CHI TIẾT
# =========================================================

st.markdown(
    '<div class="section-title">📑 Bảng chi tiết theo tháng</div>',
    unsafe_allow_html=True
)

chi_tiet = []

tien_hien_tai = tien_gui
lai_tich_luy = 0.0

for thang in range(1, ky_han + 1):

    tien_truoc = tien_hien_tai

    # -------------------------
    # LÃI ĐƠN
    # -------------------------

    if hinh_thuc_gui == "Lãi đơn":

        lai_phat_sinh = tien_gui * r / 12

        lai_tich_luy += lai_phat_sinh

        tien_hien_tai = tien_gui + lai_tich_luy

    # -------------------------
    # LÃI KÉP
    # -------------------------

    else:

        if hinh_thuc_nhan_lai == "Theo tháng":

            lai_phat_sinh = tien_hien_tai * r / 12

            tien_hien_tai += lai_phat_sinh

            lai_tich_luy = tien_hien_tai - tien_gui

        elif hinh_thuc_nhan_lai == "Theo quý":

            if thang % 3 == 0:

                lai_phat_sinh = tien_hien_tai * r / 4

                tien_hien_tai += lai_phat_sinh

                lai_tich_luy = tien_hien_tai - tien_gui

            else:

                lai_phat_sinh = 0

        else:

            if thang == ky_han:

                lai_phat_sinh = tong_tien_lai

                tien_hien_tai = tong_tien

                lai_tich_luy = tong_tien_lai

            else:

                lai_phat_sinh = 0

    chi_tiet.append({
        "Tháng": thang,
        "Lãi phát sinh": dinh_dang_tien(lai_phat_sinh),
        "Tổng gốc và lãi": dinh_dang_tien(tien_hien_tai)
    })


bang_chi_tiet = pd.DataFrame(chi_tiet)

st.dataframe(
    bang_chi_tiet,
    use_container_width=True,
    hide_index=True,
    height=min(450, 65 + len(bang_chi_tiet) * 35)
)


# =========================================================
# GHI CHÚ
# =========================================================

st.markdown("---")

st.caption(
    "Lưu ý: Đây là công cụ mô phỏng theo công thức toán học. "
    "Lãi suất và cách nhập lãi thực tế của ngân hàng có thể có quy định riêng."
)
