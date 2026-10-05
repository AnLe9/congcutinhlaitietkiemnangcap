import streamlit as st
import pandas as pd


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)


# =========================================================
# GIAO DIỆN
# =========================================================

st.markdown("""
<style>

    /* Nền */
    .stApp {
        background: linear-gradient(
            135deg,
            #0b1120 0%,
            #111827 50%,
            #0b1220 100%
        );
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* Thẻ kết quả */
    .result-card {
        padding: 20px;
        min-height: 130px;
        border-radius: 15px;
        border: 1px solid rgba(148, 163, 184, 0.20);
        background: rgba(255, 255, 255, 0.04);
    }

    .result-title {
        color: #cbd5e1;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .result-value {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 750;
    }

    .result-note {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 7px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">💰 SMART SAVINGS CALCULATOR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Công cụ tính toán tiền gửi tiết kiệm'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================================================
# SIDEBAR - NHẬP THÔNG TIN
# =========================================================

with st.sidebar:

    st.header("⚙️ Thông tin khoản gửi")

    st.write("Nhập các thông tin bên dưới:")

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
            "Lãnh lãi theo tháng",
            "Lãnh lãi theo quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

    st.write("")

    tinh_lai = st.button(
        "🧮 TÍNH LÃI",
        use_container_width=True,
        type="primary"
    )

    xoa_du_lieu = st.button(
        "↺ Xóa dữ liệu",
        use_container_width=True
    )

    if xoa_du_lieu:
        st.rerun()


# =========================================================
# MÀN HÌNH BAN ĐẦU
# =========================================================

if not tinh_lai:

    st.write("")

    st.subheader("📊 Sẵn sàng tính khoản tiết kiệm")

    st.caption(
        "Nhập số tiền gửi, kỳ hạn và lãi suất ở bảng bên trái. "
        "Sau đó nhấn **🧮 TÍNH LÃI** để xem kết quả."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "**① Nhập thông tin**\n\n"
            "Điền số tiền gửi, kỳ hạn và lãi suất."
        )

    with col2:
        st.info(
            "**② Chọn cách tính**\n\n"
            "Chọn lãi đơn hoặc lãi kép."
        )

    with col3:
        st.info(
            "**③ Xem kết quả**\n\n"
            "Xem tiền lãi, tổng tiền và biểu đồ."
        )

    st.write("")
    st.caption(
        "Smart Savings Calculator · Công cụ hỗ trợ tính toán"
    )

    st.stop()


# =========================================================
# KIỂM TRA DỮ LIỆU
# =========================================================

if tien_gui <= 0:
    st.error("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0.")
    st.stop()

if ky_han <= 0:
    st.error("⚠️ Vui lòng nhập kỳ hạn lớn hơn 0 tháng.")
    st.stop()

if lai_suat <= 0:
    st.error("⚠️ Vui lòng nhập lãi suất lớn hơn 0.")
    st.stop()


# =========================================================
# CÁC THÔNG SỐ TÍNH TOÁN
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

    if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

        so_lan_nhap_lai = 12

        tong_tien = tien_gui * (
            1 + r / so_lan_nhap_lai
        ) ** (
            so_lan_nhap_lai * so_nam
        )

    elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

        so_lan_nhap_lai = 4

        tong_tien = tien_gui * (
            1 + r / so_lan_nhap_lai
        ) ** (
            so_lan_nhap_lai * so_nam
        )

    else:

        # Lãi kép cuối kỳ:
        # Mỗi kỳ hạn là một lần nhập lãi
        tong_tien = tien_gui * (1 + r) ** so_nam

    tong_tien_lai = tong_tien - tien_gui


# =========================================================
# TÍNH LÃI ĐỊNH KỲ
# =========================================================

if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

    if hinh_thuc_gui == "Lãi đơn":
        lai_dinh_ky = tien_gui * r / 12
        ghi_chu_lai = "Lãi mỗi tháng"
    else:
        lai_dinh_ky = None
        ghi_chu_lai = "Lãi được cộng vào vốn"

elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

    if hinh_thuc_gui == "Lãi đơn":
        lai_dinh_ky = tien_gui * r / 4
        ghi_chu_lai = "Lãi mỗi quý"
    else:
        lai_dinh_ky = None
        ghi_chu_lai = "Lãi được cộng vào vốn"

else:

    lai_dinh_ky = tong_tien_lai
    ghi_chu_lai = "Tổng lãi cuối kỳ"


# =========================================================
# KẾT QUẢ
# =========================================================

st.subheader("📊 Kết quả tính toán")

col1, col2, col3 = st.columns(3)


with col1:

    if lai_dinh_ky is not None:
        lai_text = dinh_dang_tien(lai_dinh_ky)
    else:
        lai_text = "Cộng vào vốn"

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-title">
                💵 Tiền lãi định kỳ
            </div>

            <div class="result-value">
                {lai_text}
            </div>

            <div class="result-note">
                {ghi_chu_lai}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-title">
                📈 Tổng tiền lãi
            </div>

            <div class="result-value">
                {dinh_dang_tien(tong_tien_lai)}
            </div>

            <div class="result-note">
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

            <div class="result-title">
                💰 Tổng gốc + lãi
            </div>

            <div class="result-value">
                {dinh_dang_tien(tong_tien)}
            </div>

            <div class="result-note">
                Số tiền nhận được
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# THÔNG TIN KHOẢN GỬI
# =========================================================

st.divider()

st.subheader("📋 Thông tin khoản gửi")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Số tiền gốc",
        dinh_dang_tien(tien_gui)
    )

with c2:
    st.metric(
        "Kỳ hạn",
        f"{ky_han} tháng"
    )

with c3:
    st.metric(
        "Lãi suất",
        f"{lai_suat:.2f}%/năm"
    )

with c4:
    st.metric(
        "Cách tính",
        hinh_thuc_gui
    )


# =========================================================
# TẠO DỮ LIỆU CHO BIỂU ĐỒ
# =========================================================

thang_list = []
lai_list = []
tong_list = []


for thang in range(0, ky_han + 1):

    thang_list.append(thang)

    if hinh_thuc_gui == "Lãi đơn":

        lai_tich_luy = tien_gui * r * (thang / 12)

    else:

        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

            lai_tich_luy = tien_gui * (
                (1 + r / 12) ** thang - 1
            )

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

            so_quy = thang / 3

            lai_tich_luy = tien_gui * (
                (1 + r / 4) ** so_quy - 1
            )

        else:

            lai_tich_luy = tien_gui * (
                (1 + r) ** (thang / 12) - 1
            )

    tong_thang = tien_gui + lai_tich_luy

    lai_list.append(lai_tich_luy)
    tong_list.append(tong_thang)


# =========================================================
# BIỂU ĐỒ
# =========================================================

st.divider()

st.subheader("📈 Tiền lãi tích lũy theo thời gian")

chart_data = pd.DataFrame(
    {
        "Tiền lãi": lai_list
    },
    index=thang_list
)

st.line_chart(
    chart_data,
    height=400,
    use_container_width=True
)

st.caption(
    "Biểu đồ thể hiện số tiền lãi tích lũy qua từng tháng."
)


# =========================================================
# BẢNG CHI TIẾT
# =========================================================

st.subheader("📑 Chi tiết khoản gửi theo tháng")

bang_chi_tiet = []

for i in range(len(thang_list)):

    bang_chi_tiet.append(
        {
            "Tháng": thang_list[i],
            "Lãi": dinh_dang_tien(lai_list[i]),
            "Tổng gốc và lãi": dinh_dang_tien(tong_list[i])
        }
    )


df_bang = pd.DataFrame(bang_chi_tiet)

st.dataframe(
    df_bang,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# TÓM TẮT
# =========================================================

st.divider()

st.subheader("📝 Tóm tắt")

st.info(
    f"""
Bạn gửi **{dinh_dang_tien(tien_gui)}** trong **{ky_han} tháng**,
với lãi suất **{lai_suat:.2f}%/năm**.

**Cách tính:** {hinh_thuc_gui}

**Cách nhận lãi:** {hinh_thuc_nhan_lai}

**Tổng tiền lãi:** {dinh_dang_tien(tong_tien_lai)}

**Tổng số tiền nhận được:** {dinh_dang_tien(tong_tien)}
"""
)


# =========================================================
# GIẢI THÍCH CÁCH TÍNH
# =========================================================

if hinh_thuc_gui == "Lãi đơn":

    st.caption(
        "💡 Lãi đơn: tiền lãi luôn được tính dựa trên số tiền gốc ban đầu."
    )

else:

    st.caption(
        "💡 Lãi kép: tiền lãi được cộng vào vốn để tiếp tục tạo ra tiền lãi "
        "ở những kỳ tiếp theo."
    )


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.caption(
    "Smart Savings Calculator · Công cụ hỗ trợ tính toán tiền gửi tiết kiệm"
)
