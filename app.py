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
# CSS - GIAO DIỆN KHOA HỌC, GỌN GÀNG
# =========================================================

st.markdown("""
<style>

    /* =========================
       NỀN CHUNG
       ========================= */

    .stApp {
        background: #0f172a;
    }

    /* =========================
       TIÊU ĐỀ
       ========================= */

    .main-title {
        text-align: center;
        color: #f8fafc;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 15px;
        margin-bottom: 35px;
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: #111827;
    }

    section[data-testid="stSidebar"] h2 {
        color: #f8fafc;
    }

    /* =========================
       SECTION
       ========================= */

    .section-title {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 750;
        margin-top: 20px;
        margin-bottom: 16px;
    }

    /* =========================
       CARD THÔNG TIN
       ========================= */

    .info-card {
        background: #172033;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
        min-height: 105px;
        transition: all 0.2s ease;
    }

    .info-card:hover {
        border-color: #64748b;
        transform: translateY(-2px);
    }

    .info-label {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .info-value {
        color: #f8fafc;
        font-size: 22px;
        font-weight: 750;
    }

    /* =========================
       CARD KẾT QUẢ
       ========================= */

    .result-card {
        background: #172033;
        border: 1px solid #334155;
        border-radius: 15px;
        padding: 22px;
        min-height: 145px;
        transition: all 0.25s ease;
    }

    .result-card:hover {
        border-color: #94a3b8;
        transform: translateY(-2px);
    }

    .result-card-main {
        background: #18263d;
        border: 1px solid #7c8da8;
        box-shadow: 0 0 18px rgba(148, 163, 184, 0.10);
    }

    .result-title {
        color: #cbd5e1;
        font-size: 14px;
        font-weight: 650;
        margin-bottom: 12px;
    }

    .result-number {
        color: #f8fafc;
        font-size: 27px;
        font-weight: 800;
        line-height: 1.2;
    }

    .result-note {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 10px;
    }

    /* =========================
       PHÂN TÍCH
       ========================= */

    .analysis-box {
        background: #111c30;
        border-left: 4px solid #64748b;
        border-radius: 9px;
        padding: 18px 20px;
        color: #cbd5e1;
        line-height: 1.8;
        margin-top: 12px;
    }

    /* =========================
       THANH TĂNG TRƯỞNG
       ========================= */

    .progress-bg {
        width: 100%;
        height: 9px;
        background: #273449;
        border-radius: 20px;
        overflow: hidden;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .progress-fill {
        height: 100%;
        background: #94a3b8;
        border-radius: 20px;
        transition: width 0.5s ease;
    }

    .progress-text {
        color: #94a3b8;
        font-size: 13px;
    }

    /* =========================
       NÚT TÍNH
       ========================= */

    div.stButton > button {
        width: 100%;
        height: 46px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 750;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
    }

    /* =========================
       BẢNG
       ========================= */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* =========================
       ĐƯỜNG KẺ
       ========================= */

    hr {
        border-color: #334155;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================================================
# TIÊU ĐỀ ỨNG DỤNG
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
# SIDEBAR - NHẬP THÔNG TIN
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Thông tin khoản gửi")

    # -------------------------
    # SỐ TIỀN
    # -------------------------

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=0.0,
        step=1_000_000.0,
        format="%.0f"
    )

    # -------------------------
    # KỲ HẠN
    # -------------------------

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=0,
        max_value=120,
        value=0,
        step=1
    )

    # -------------------------
    # LÃI SUẤT
    # -------------------------

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
        format="%.2f"
    )

    # -------------------------
    # HÌNH THỨC TÍNH LÃI
    # -------------------------

    hinh_thuc_gui = st.selectbox(
        "Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    # -------------------------
    # CÁCH TÍNH LÃI
    # -------------------------

    cach_tinh_lai = st.selectbox(
        "Lãi được tính",
        [
            "Mỗi tháng",
            "Mỗi 3 tháng",
            "Cuối kỳ"
        ]
    )

    # Giải thích ngắn
    if hinh_thuc_gui == "Lãi đơn":
        st.caption(
            "Lãi đơn: tiền lãi luôn được tính trên số tiền gốc ban đầu."
        )
    else:
        st.caption(
            "Lãi kép: tiền lãi được cộng vào gốc để tiếp tục sinh lãi."
        )

    st.markdown("")

    tinh_toan = st.button(
        "🧮 TÍNH LÃI",
        use_container_width=True
    )


# =========================================================
# TRẠNG THÁI ỨNG DỤNG
# =========================================================

if "da_tinh" not in st.session_state:
    st.session_state.da_tinh = False


# =========================================================
# XỬ LÝ NÚT TÍNH
# =========================================================

if tinh_toan:

    if tien_gui <= 0:
        st.error("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.session_state.da_tinh = False

    elif ky_han <= 0:
        st.error("⚠️ Vui lòng nhập kỳ hạn lớn hơn 0.")
        st.session_state.da_tinh = False

    elif lai_suat <= 0:
        st.error("⚠️ Vui lòng nhập lãi suất lớn hơn 0.")
        st.session_state.da_tinh = False

    else:
        st.session_state.da_tinh = True


# =========================================================
# MÀN HÌNH BAN ĐẦU
# =========================================================

if not st.session_state.da_tinh:

    st.markdown("""
    <div class="info-card"
         style="text-align:center; padding:48px 25px; margin-top:20px;">

        <div style="font-size:42px; margin-bottom:14px;">
            📊
        </div>

        <div style="
            color:#f8fafc;
            font-size:22px;
            font-weight:750;
            margin-bottom:12px;
        ">
            Sẵn sàng tính khoản tiết kiệm
        </div>

        <div style="
            color:#94a3b8;
            font-size:15px;
            line-height:1.8;
        ">
            Nhập số tiền gửi, kỳ hạn và lãi suất ở bảng bên trái.
            <br>
            Sau đó nhấn <b>🧮 TÍNH LÃI</b> để xem kết quả.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.stop()


# =========================================================
# TÍNH TOÁN
# =========================================================

r = lai_suat / 100
so_nam = ky_han / 12


# =========================================================
# TÍNH TỔNG TIỀN
# =========================================================

if hinh_thuc_gui == "Lãi đơn":

    tong_tien_lai = tien_gui * r * so_nam
    tong_tien = tien_gui + tong_tien_lai

else:

    if cach_tinh_lai == "Mỗi tháng":

        tan_suat = 12

        tong_tien = tien_gui * (
            1 + r / tan_suat
        ) ** (
            tan_suat * so_nam
        )

    elif cach_tinh_lai == "Mỗi 3 tháng":

        tan_suat = 4

        tong_tien = tien_gui * (
            1 + r / tan_suat
        ) ** (
            tan_suat * so_nam
        )

    else:

        tong_tien = tien_gui * (1 + r) ** so_nam

    tong_tien_lai = tong_tien - tien_gui


# =========================================================
# TÍNH LÃI ĐỊNH KỲ
# =========================================================

if hinh_thuc_gui == "Lãi đơn":

    if cach_tinh_lai == "Mỗi tháng":
        lai_dinh_ky = tien_gui * r / 12

    elif cach_tinh_lai == "Mỗi 3 tháng":
        lai_dinh_ky = tien_gui * r / 4

    else:
        lai_dinh_ky = tong_tien_lai

else:

    if cach_tinh_lai == "Mỗi tháng":
        lai_dinh_ky = tien_gui * r / 12

    elif cach_tinh_lai == "Mỗi 3 tháng":
        lai_dinh_ky = tien_gui * r / 4

    else:
        lai_dinh_ky = tong_tien_lai


# =========================================================
# KẾT QUẢ
# =========================================================

st.markdown(
    '<div class="section-title">📊 Kết quả tính toán</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


# -------------------------
# CARD 1
# -------------------------

with col1:

    st.markdown(f"""
    <div class="result-card">

        <div class="result-title">
            💵 Tiền lãi định kỳ
        </div>

        <div class="result-number">
            {dinh_dang_tien(lai_dinh_ky)}
        </div>

        <div class="result-note">
            {cach_tinh_lai}
        </div>

    </div>
    """, unsafe_allow_html=True)


# -------------------------
# CARD 2
# -------------------------

with col2:

    st.markdown(f"""
    <div class="result-card">

        <div class="result-title">
            📈 Tổng tiền lãi
        </div>

        <div class="result-number">
            {dinh_dang_tien(tong_tien_lai)}
        </div>

        <div class="result-note">
            Sau {ky_han} tháng
        </div>

    </div>
    """, unsafe_allow_html=True)


# -------------------------
# CARD 3
# -------------------------

with col3:

    st.markdown(f"""
    <div class="result-card result-card-main">

        <div class="result-title">
            💰 Tổng gốc + lãi
        </div>

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

        <div class="info-label">
            Số tiền gốc
        </div>

        <div class="info-value">
            {dinh_dang_tien(tien_gui)}
        </div>

    </div>
    """, unsafe_allow_html=True)


with info2:

    st.markdown(f"""
    <div class="info-card">

        <div class="info-label">
            Kỳ hạn
        </div>

        <div class="info-value">
            {ky_han} tháng
        </div>

    </div>
    """, unsafe_allow_html=True)


with info3:

    st.markdown(f"""
    <div class="info-card">

        <div class="info-label">
            Lãi suất
        </div>

        <div class="info-value">
            {lai_suat:.2f}%/năm
        </div>

    </div>
    """, unsafe_allow_html=True)


with info4:

    st.markdown(f"""
    <div class="info-card">

        <div class="info-label">
            Hình thức
        </div>

        <div class="info-value">
            {hinh_thuc_gui}
        </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# MỨC TĂNG SO VỚI VỐN BAN ĐẦU
# =========================================================

st.markdown("")
st.markdown(
    '<div class="section-title">📌 Mức tăng so với vốn ban đầu</div>',
    unsafe_allow_html=True
)

ty_le_lai = (tong_tien_lai / tien_gui) * 100

# Giới hạn chiều dài thanh để giao diện không bị quá dài
phan_tram_thanh = min(ty_le_lai * 5, 100)

st.markdown(f"""
<div class="info-card">

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
    ">

        <div class="info-label" style="margin:0;">
            Tiền lãi tăng thêm
        </div>

        <div style="
            color:#f8fafc;
            font-size:20px;
            font-weight:750;
        ">
            +{ty_le_lai:.2f}%
        </div>

    </div>

    <div class="progress-bg">
        <div
            class="progress-fill"
            style="width:{phan_tram_thanh}%;">
        </div>
    </div>

    <div class="progress-text">
        {dinh_dang_tien(tong_tien_lai)}
        tiền lãi trên vốn ban đầu
        {dinh_dang_tien(tien_gui)}
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# PHÂN TÍCH NHANH
# =========================================================

lai_trung_binh_thang = tong_tien_lai / ky_han

st.markdown(
    '<div class="section-title">🔎 Phân tích nhanh</div>',
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="analysis-box">

    <b>• Tổng tiền lãi:</b>
    {dinh_dang_tien(tong_tien_lai)}.

    <br>

    <b>• Lãi bình quân mỗi tháng:</b>
    {dinh_dang_tien(lai_trung_binh_thang)}.

    <br>

    <b>• Tỷ lệ lãi trên vốn:</b>
    {ty_le_lai:.2f}%.

    <br>

    <b>• Cuối kỳ nhận được:</b>
    {dinh_dang_tien(tong_tien)}.

</div>
""", unsafe_allow_html=True)


# =========================================================
# BIỂU ĐỒ
# =========================================================

st.markdown(
    '<div class="section-title">📈 Lãi tích lũy theo thời gian</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# TẠO DỮ LIỆU BIỂU ĐỒ
# ---------------------------------------------------------

du_lieu_bieu_do = []

tien_hien_tai = tien_gui
lai_tich_luy = 0.0

for thang in range(0, ky_han + 1):

    # Tháng 0
    if thang == 0:

        du_lieu_bieu_do.append({
            "Tháng": 0,
            "Tiền lãi tích lũy": 0.0
        })

        continue

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

        if cach_tinh_lai == "Mỗi tháng":

            lai_phat_sinh = tien_hien_tai * r / 12

            tien_hien_tai += lai_phat_sinh

            lai_tich_luy = tien_hien_tai - tien_gui

        elif cach_tinh_lai == "Mỗi 3 tháng":

            if thang % 3 == 0:

                lai_phat_sinh = tien_hien_tai * r / 4

                tien_hien_tai += lai_phat_sinh

                lai_tich_luy = tien_hien_tai - tien_gui

        else:

            if thang == ky_han:

                tien_hien_tai = tong_tien
                lai_tich_luy = tong_tien_lai

    du_lieu_bieu_do.append({
        "Tháng": thang,
        "Tiền lãi tích lũy": lai_tich_luy
    })


bieu_do = pd.DataFrame(du_lieu_bieu_do)

bieu_do = bieu_do.set_index("Tháng")

# Đổi sang triệu VNĐ
bieu_do["Tiền lãi tích lũy (triệu VNĐ)"] = (
    bieu_do["Tiền lãi tích lũy"] / 1_000_000
)

bieu_do = bieu_do[["Tiền lãi tích lũy (triệu VNĐ)"]]


# ---------------------------------------------------------
# HIỂN THỊ BIỂU ĐỒ
# ---------------------------------------------------------

st.line_chart(
    bieu_do,
    height=400
)

st.caption(
    "Biểu đồ tập trung vào phần tiền lãi tăng thêm, "
    "giúp quan sát tốc độ tăng rõ hơn so với biểu đồ tổng số dư."
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

        if cach_tinh_lai == "Mỗi tháng":

            lai_phat_sinh = tien_hien_tai * r / 12

            tien_hien_tai += lai_phat_sinh

            lai_tich_luy = tien_hien_tai - tien_gui

        elif cach_tinh_lai == "Mỗi 3 tháng":

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
        "Lãi": dinh_dang_tien(lai_phat_sinh),
        "Tổng gốc và lãi": dinh_dang_tien(tien_hien_tai)
    })


bang_chi_tiet = pd.DataFrame(chi_tiet)


st.dataframe(
    bang_chi_tiet,
    use_container_width=True,
    hide_index=True,
    height=min(500, 70 + len(bang_chi_tiet) * 35)
)


# =========================================================
# GHI CHÚ CUỐI
# =========================================================

st.markdown("---")

st.caption(
    "Lưu ý: Kết quả là mô phỏng theo công thức toán học. "
    "Lãi suất và cách tính thực tế có thể khác tùy quy định của từng ngân hàng."
)
