import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


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
# CSS - GIAO DIỆN
# =========================================================

st.markdown("""
<style>

    /* Nền tổng thể */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #172554 50%,
            #111827 100%
        );
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-top: 10px;
        margin-bottom: 5px;

        background: linear-gradient(
            90deg,
            #f8fafc,
            #bfdbfe,
            #f8fafc
        );

        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        animation: shine 7s linear infinite;
    }

    @keyframes shine {
        0% {
            background-position: 200% center;
        }
        100% {
            background-position: -200% center;
        }
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 16px;
        margin-bottom: 35px;
    }

    /* Các card */
    .info-card {
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 18px;
        backdrop-filter: blur(8px);
    }

    .result-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(148,163,184,0.25);
        border-radius: 16px;
        padding: 22px;
        min-height: 145px;
    }

    .result-title {
        color: #cbd5e1;
        font-size: 15px;
        margin-bottom: 12px;
    }

    .result-value {
        color: #f8fafc;
        font-size: 27px;
        font-weight: 800;
    }

    .small-note {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 8px;
    }

    /* Nút tính */
    div.stButton > button {
        border-radius: 10px;
        height: 48px;
        font-size: 16px;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Header section */
    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #f8fafc;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Đường trang trí học thuật */
    .academic-line {
        height: 1px;
        width: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(147,197,253,0.7),
            transparent
        );
        margin: 12px 0 28px 0;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG
# =========================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


def dinh_dang_trieu(so_tien):
    return f"{so_tien / 1_000_000:.2f} triệu"


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

st.markdown(
    '<div class="academic-line"></div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR - NHẬP THÔNG TIN
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
        min_value=0,
        value=0,
        step=1
    )

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        value=0.0,
        step=0.1,
        format="%.2f"
    )

    hinh_thuc_gui = st.selectbox(
        "Cách tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    hinh_thuc_nhan_lai = st.selectbox(
        "Cách nhận lãi",
        [
            "Nhận lãi hàng tháng",
            "Nhận lãi hàng quý",
            "Nhận lãi cuối kỳ"
        ]
    )

    st.markdown("<br>", unsafe_allow_html=True)

    tinh_lai = st.button(
        "🧮 TÍNH LÃI",
        use_container_width=True
    )

    xoa_ket_qua = st.button(
        "↺ Xóa kết quả",
        use_container_width=True
    )


# =========================================================
# XÓA KẾT QUẢ
# =========================================================

if xoa_ket_qua:
    st.session_state["da_tinh"] = False
    st.rerun()


# =========================================================
# TRẠNG THÁI BAN ĐẦU
# =========================================================

if "da_tinh" not in st.session_state:
    st.session_state["da_tinh"] = False


# =========================================================
# TÍNH TOÁN
# =========================================================

if tinh_lai:

    if tien_gui <= 0:
        st.error("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif ky_han <= 0:
        st.error("⚠️ Vui lòng nhập kỳ hạn lớn hơn 0 tháng.")

    elif lai_suat <= 0:
        st.error("⚠️ Vui lòng nhập lãi suất lớn hơn 0.")

    else:

        st.session_state["da_tinh"] = True

        r = lai_suat / 100
        so_nam = ky_han / 12

        # =================================================
        # LÃI ĐƠN
        # =================================================

        if hinh_thuc_gui == "Lãi đơn":

            tong_tien_lai = tien_gui * r * so_nam
            tong_tien = tien_gui + tong_tien_lai

        # =================================================
        # LÃI KÉP
        # =================================================

        else:

            if hinh_thuc_nhan_lai == "Nhận lãi hàng tháng":

                so_lan_nhap_lai = 12

            elif hinh_thuc_nhan_lai == "Nhận lãi hàng quý":

                so_lan_nhap_lai = 4

            else:

                so_lan_nhap_lai = 1

            if hinh_thuc_nhan_lai == "Nhận lãi cuối kỳ":

                tong_tien = tien_gui * (1 + r) ** so_nam

            else:

                tong_tien = tien_gui * (
                    1 + r / so_lan_nhap_lai
                ) ** (
                    so_lan_nhap_lai * so_nam
                )

            tong_tien_lai = tong_tien - tien_gui

        # =================================================
        # LÃI NHẬN ĐỊNH KỲ
        # =================================================

        if hinh_thuc_nhan_lai == "Nhận lãi hàng tháng":

            lai_dinh_ky = tien_gui * r / 12

        elif hinh_thuc_nhan_lai == "Nhận lãi hàng quý":

            lai_dinh_ky = tien_gui * r / 4

        else:

            lai_dinh_ky = tong_tien_lai


        # =================================================
        # LƯU KẾT QUẢ
        # =================================================

        st.session_state["tien_gui"] = tien_gui
        st.session_state["ky_han"] = ky_han
        st.session_state["lai_suat"] = lai_suat
        st.session_state["hinh_thuc_gui"] = hinh_thuc_gui
        st.session_state["hinh_thuc_nhan_lai"] = hinh_thuc_nhan_lai
        st.session_state["lai_dinh_ky"] = lai_dinh_ky
        st.session_state["tong_tien_lai"] = tong_tien_lai
        st.session_state["tong_tien"] = tong_tien


# =========================================================
# HIỂN THỊ KẾT QUẢ
# =========================================================

if st.session_state["da_tinh"]:

    tien_gui = st.session_state["tien_gui"]
    ky_han = st.session_state["ky_han"]
    lai_suat = st.session_state["lai_suat"]
    hinh_thuc_gui = st.session_state["hinh_thuc_gui"]
    hinh_thuc_nhan_lai = st.session_state["hinh_thuc_nhan_lai"]
    lai_dinh_ky = st.session_state["lai_dinh_ky"]
    tong_tien_lai = st.session_state["tong_tien_lai"]
    tong_tien = st.session_state["tong_tien"]


    # =====================================================
    # KẾT QUẢ CHÍNH
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Kết quả tính toán</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">💵 Tiền lãi định kỳ</div>
                <div class="result-value">
                    {dinh_dang_tien(lai_dinh_ky)}
                </div>
                <div class="small-note">
                    {hinh_thuc_nhan_lai}
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
                    {dinh_dang_tien(tong_tien_lai)}
                </div>
                <div class="small-note">
                    Phần tiền tăng thêm
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">💰 Tổng gốc + lãi</div>
                <div class="result-value">
                    {dinh_dang_tien(tong_tien)}
                </div>
                <div class="small-note">
                    Số tiền nhận được
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
        st.metric(
            "Số tiền gốc",
            dinh_dang_tien(tien_gui)
        )

    with info2:
        st.metric(
            "Kỳ hạn",
            f"{ky_han} tháng"
        )

    with info3:
        st.metric(
            "Lãi suất",
            f"{lai_suat:.2f}%/năm"
        )

    with info4:
        st.metric(
            "Cách tính",
            hinh_thuc_gui
        )


    # =====================================================
    # BIỂU ĐỒ TĂNG TRƯỞNG
    # =====================================================

    st.markdown(
        '<div class="section-title">📈 Biểu đồ tăng trưởng khoản tiền</div>',
        unsafe_allow_html=True
    )

    # Tạo dữ liệu theo từng tháng
    thang = list(range(0, ky_han + 1))
    gia_tri = []

    for m in thang:

        thoi_gian_nam = m / 12

        if hinh_thuc_gui == "Lãi đơn":

            gia_tri_thang = tien_gui * (
                1 + (lai_suat / 100) * thoi_gian_nam
            )

        else:

            if hinh_thuc_nhan_lai == "Nhận lãi hàng tháng":

                gia_tri_thang = tien_gui * (
                    1 + (lai_suat / 100) / 12
                ) ** m

            elif hinh_thuc_nhan_lai == "Nhận lãi hàng quý":

                so_quy = m / 3

                gia_tri_thang = tien_gui * (
                    1 + (lai_suat / 100) / 4
                ) ** so_quy

            else:

                gia_tri_thang = tien_gui * (
                    1 + lai_suat / 100
                ) ** thoi_gian_nam

        gia_tri.append(gia_tri_thang)


    df_chart = pd.DataFrame({
        "Tháng": thang,
        "Tổng tiền": gia_tri
    })

    # =====================================================
    # BIỂU ĐỒ - ZOOM VÙNG TĂNG TRƯỞNG
    # =====================================================

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        df_chart["Tháng"],
        df_chart["Tổng tiền"],
        linewidth=3,
        marker="o",
        markersize=5
    )

    ax.set_xlabel("Tháng")
    ax.set_ylabel("Tổng tiền (VNĐ)")

    ax.set_title(
        "Sự thay đổi của khoản tiền theo thời gian"
    )

    ax.grid(
        True,
        alpha=0.2
    )

    # Zoom trục Y để nhìn rõ mức tăng
    gia_tri_min = min(gia_tri)
    gia_tri_max = max(gia_tri)

    khoang = gia_tri_max - gia_tri_min

    if khoang == 0:
        khoang = tien_gui * 0.01

    ax.set_ylim(
        gia_tri_min - khoang * 0.15,
        gia_tri_max + khoang * 0.15
    )

    fig.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


    # =====================================================
    # BẢNG CHI TIẾT THEO THÁNG
    # =====================================================

    st.markdown(
        '<div class="section-title">📑 Bảng chi tiết theo tháng</div>',
        unsafe_allow_html=True
    )

    bang_chi_tiet = []

    for i in range(len(thang)):

        tong_tien_thang = gia_tri[i]

        lai_thang = tong_tien_thang - tien_gui

        bang_chi_tiet.append({
            "Tháng": f"Tháng {thang[i]}",
            "Lãi": dinh_dang_tien(lai_thang),
            "Tổng gốc và lãi": dinh_dang_tien(tong_tien_thang)
        })

    df_bang = pd.DataFrame(bang_chi_tiet)

    st.dataframe(
        df_bang,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # TÓM TẮT
    # =====================================================

    st.markdown(
        '<div class="section-title">📝 Tóm tắt</div>',
        unsafe_allow_html=True
    )

    phan_tram_tang = (
        tong_tien_lai / tien_gui * 100
    )

    st.info(
        f"""
        Bạn gửi **{dinh_dang_tien(tien_gui)}**
        trong **{ky_han} tháng**, với lãi suất
        **{lai_suat:.2f}%/năm**.

        Hình thức tính lãi: **{hinh_thuc_gui}**.

        Tổng tiền lãi nhận được là
        **{dinh_dang_tien(tong_tien_lai)}**,
        tương đương mức tăng **{phan_tram_tang:.2f}%**
        so với số tiền gốc.

        Tổng số tiền cuối kỳ là
        **{dinh_dang_tien(tong_tien)}**.
        """
    )


# =========================================================
# MÀN HÌNH BAN ĐẦU
# =========================================================

else:

    st.markdown(
        """
        <div class="info-card">

        <h2 style="color:#f8fafc;">
        👋 Sẵn sàng tính khoản tiết kiệm của bạn?
        </h2>

        <p style="color:#cbd5e1;font-size:16px;">
        Nhập <b>số tiền gửi</b>, <b>kỳ hạn</b> và
        <b>lãi suất</b> ở bảng bên trái,
        sau đó chọn cách tính và bấm
        <b>🧮 TÍNH LÃI</b>.
        </p>

        <p style="color:#94a3b8;font-size:14px;">
        Ứng dụng sẽ cung cấp kết quả tổng tiền lãi,
        tổng số tiền nhận được, biểu đồ tăng trưởng
        và bảng chi tiết theo từng tháng.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
