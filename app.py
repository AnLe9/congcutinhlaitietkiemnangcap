import streamlit as st
import pandas as pd


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

/* Tiêu đề chính */
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: #999999;
    font-size: 16px;
    margin-bottom: 30px;
}


/* 3 ô kết quả */
[data-testid="stMetric"] {
    background-color: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.35);
    border-radius: 14px;
    padding: 20px 18px;
    min-height: 125px;
}


/* Tên của chỉ tiêu */
[data-testid="stMetricLabel"] {
    font-size: 16px !important;
}


/* Số tiền */
[data-testid="stMetricValue"] {
    font-size: 25px !important;
    font-weight: 700 !important;
}


/* Khoảng cách */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG
# =========================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


def dinh_dang_trieu(so_tien):
    return f"{so_tien / 1_000_000:,.1f} triệu"


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
# SIDEBAR - NHẬP THÔNG TIN
# =========================================================

st.sidebar.header("⚙️ Thông tin khoản gửi")


tien_gui = st.sidebar.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)


ky_han = st.sidebar.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)


lai_suat = st.sidebar.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1
)


hinh_thuc_lai = st.sidebar.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)


hinh_thuc_nhan_lai = st.sidebar.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)


tinh_lai = st.sidebar.button(
    "🧮 TÍNH TOÁN",
    use_container_width=True
)


# =========================================================
# KHI CHƯA BẤM TÍNH
# =========================================================

if not tinh_lai:

    st.info(
        "👈 Nhập thông tin khoản gửi ở thanh bên "
        "và nhấn **TÍNH TOÁN** để xem kết quả."
    )

    st.stop()


# =========================================================
# KIỂM TRA DỮ LIỆU
# =========================================================

if tien_gui <= 0:

    st.error("⚠️ Số tiền gửi phải lớn hơn 0.")
    st.stop()


# =========================================================
# THÔNG SỐ TÍNH TOÁN
# =========================================================

lai_nam = lai_suat / 100
so_nam = ky_han / 12


# Xác định số lần ghép lãi trong năm

if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

    tan_suat = 12

elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

    tan_suat = 4

else:

    tan_suat = 1


# =========================================================
# TÍNH LÃI ĐƠN
# =========================================================

lai_don = tien_gui * lai_nam * so_nam

tong_tien_don = tien_gui + lai_don


# =========================================================
# TÍNH LÃI KÉP
# =========================================================

so_ky = ky_han / (12 / tan_suat)

tong_tien_kep = tien_gui * (
    1 + lai_nam / tan_suat
) ** so_ky

lai_kep = tong_tien_kep - tien_gui


# =========================================================
# CHỌN KẾT QUẢ THEO HÌNH THỨC TÍNH LÃI
# =========================================================

if hinh_thuc_lai == "Lãi đơn":

    tong_tien = tong_tien_don
    tong_tien_lai = lai_don

else:

    tong_tien = tong_tien_kep
    tong_tien_lai = lai_kep


# =========================================================
# TÍNH TIỀN LÃI ĐỊNH KỲ
# =========================================================

if hinh_thuc_lai == "Lãi đơn":

    if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

        lai_dinh_ky = tien_gui * lai_nam / 12

    elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

        lai_dinh_ky = tien_gui * lai_nam / 4

    else:

        lai_dinh_ky = tong_tien_lai

else:

    if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

        lai_dinh_ky = tien_gui * lai_nam / 12

    elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

        lai_dinh_ky = (
            tien_gui
            * (
                (1 + lai_nam / 4) ** 1 - 1
            )
        )

    else:

        lai_dinh_ky = tong_tien_lai


# =========================================================
# KẾT QUẢ TÍNH TOÁN
# =========================================================

st.subheader("📊 Kết quả tính toán")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        label="💵 Tiền lãi kỳ đầu",
        value=dinh_dang_tien(lai_dinh_ky)
    )


with col2:

    st.metric(
        label="📈 Tổng tiền lãi",
        value=dinh_dang_tien(tong_tien_lai)
    )


with col3:

    st.metric(
        label="💰 Tổng tiền nhận được",
        value=dinh_dang_tien(tong_tien)
    )


# =========================================================
# THÔNG TIN KHOẢN GỬI
# =========================================================

st.divider()

st.subheader("📋 Thông tin khoản gửi")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.write("**Số tiền gốc**")
    st.write(dinh_dang_tien(tien_gui))


with col2:

    st.write("**Kỳ hạn**")
    st.write(f"{ky_han} tháng")


with col3:

    st.write("**Lãi suất**")
    st.write(f"{lai_suat:.2f}%/năm")


with col4:

    st.write("**Hình thức**")
    st.write(hinh_thuc_lai)


# =========================================================
# BIỂU ĐỒ
# =========================================================

st.divider()

st.subheader("📈 Khoản tiền tăng theo thời gian")

st.caption(
    "Biểu đồ thể hiện tổng số tiền gồm gốc và lãi "
    "tại các mốc thời gian trong kỳ hạn."
)


# Chọn tối đa 7 mốc để biểu đồ không bị rối

if ky_han <= 6:

    cac_moc = list(range(ky_han + 1))

else:

    cac_moc = [
        round(i * ky_han / 6)
        for i in range(7)
    ]

    cac_moc = sorted(list(set(cac_moc)))


tien_theo_moc = []


for thang in cac_moc:

    if hinh_thuc_lai == "Lãi đơn":

        gia_tri = tien_gui * (
            1 + lai_nam * thang / 12
        )

    else:

        so_ky_moc = thang / (12 / tan_suat)

        gia_tri = tien_gui * (
            1 + lai_nam / tan_suat
        ) ** so_ky_moc

    tien_theo_moc.append(gia_tri)


# Tạo DataFrame cho biểu đồ

du_lieu_bieu_do = pd.DataFrame({
    "Tháng": cac_moc,
    "Tổng tiền": tien_theo_moc
})


st.line_chart(
    du_lieu_bieu_do,
    x="Tháng",
    y="Tổng tiền"
)


# =========================================================
# CÁC MỐC CHÍNH
# =========================================================

st.write("**Các mốc chính:**")


cac_cot = st.columns(len(cac_moc))


for i in range(len(cac_moc)):

    with cac_cot[i]:

        st.metric(
            f"Tháng {cac_moc[i]}",
            dinh_dang_trieu(tien_theo_moc[i])
        )


# =========================================================
# SO SÁNH LÃI ĐƠN VÀ LÃI KÉP
# =========================================================

st.divider()

st.subheader("⚖️ So sánh lãi đơn và lãi kép")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "💵 Tổng lãi đơn",
        dinh_dang_tien(lai_don)
    )


with col2:

    st.metric(
        "📈 Tổng lãi kép",
        dinh_dang_tien(lai_kep)
    )


with col3:

    st.metric(
        "💰 Lãi kép tăng thêm",
        dinh_dang_tien(lai_kep - lai_don)
    )


st.info(
    "Lãi đơn chỉ tính lãi trên số tiền gốc ban đầu. "
    "Lãi kép cộng tiền lãi vào vốn để tiếp tục sinh lãi "
    "ở các kỳ tiếp theo."
)


# =========================================================
# BẢNG DIỄN BIẾN KHOẢN TIỀN
# =========================================================

st.divider()

st.subheader("📅 Diễn biến khoản tiền theo từng tháng")


st.caption(
    "Tiền gốc = số tiền ban đầu | "
    "Lãi phát sinh = phần lãi trong tháng | "
    "Tổng tiền = tiền gốc + tiền lãi"
)


bang_du_lieu = []


for thang in range(ky_han + 1):


    # -----------------------------------------
    # THÁNG 0
    # -----------------------------------------

    if thang == 0:

        tong_thang = tien_gui
        lai_thang = 0


    # -----------------------------------------
    # CÁC THÁNG SAU
    # -----------------------------------------

    else:

        if hinh_thuc_lai == "Lãi đơn":

            tong_thang = tien_gui * (
                1 + lai_nam * thang / 12
            )

            tong_thang_truoc = tien_gui * (
                1 + lai_nam * (thang - 1) / 12
            )

            lai_thang = (
                tong_thang
                - tong_thang_truoc
            )

        else:

            so_ky_hien_tai = (
                thang / (12 / tan_suat)
            )

            so_ky_truoc = (
                (thang - 1) / (12 / tan_suat)
            )

            tong_thang = tien_gui * (
                1 + lai_nam / tan_suat
            ) ** so_ky_hien_tai

            tong_thang_truoc = tien_gui * (
                1 + lai_nam / tan_suat
            ) ** so_ky_truoc

            lai_thang = (
                tong_thang
                - tong_thang_truoc
            )


    bang_du_lieu.append({

        "Tháng": thang,

        "Tiền gốc": dinh_dang_tien(
            tien_gui
        ),

        "Lãi phát sinh": dinh_dang_tien(
            lai_thang
        ),

        "Tổng tiền nhận được": dinh_dang_tien(
            tong_thang
        )

    })


# Tạo bảng

df = pd.DataFrame(bang_du_lieu)


st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# GIẢI THÍCH KẾT QUẢ
# =========================================================

st.divider()

st.subheader("💡 Giải thích")


if hinh_thuc_lai == "Lãi đơn":

    st.info(
        "Bạn đang sử dụng **lãi đơn**. "
        "Tiền lãi được tính dựa trên số tiền gốc ban đầu, "
        "vì vậy tiền lãi mỗi kỳ không tăng theo số vốn."
    )

else:

    st.success(
        "Bạn đang sử dụng **lãi kép**. "
        "Tiền lãi được cộng vào vốn để tiếp tục sinh lãi "
        "ở các kỳ tiếp theo."
    )


st.write(
    f"Với số tiền gửi **{dinh_dang_tien(tien_gui)}**, "
    f"kỳ hạn **{ky_han} tháng**, "
    f"lãi suất **{lai_suat:.2f}%/năm** và "
    f"hình thức **{hinh_thuc_lai}**, "
    f"tổng tiền cuối kỳ là "
    f"**{dinh_dang_tien(tong_tien)}**."
)
