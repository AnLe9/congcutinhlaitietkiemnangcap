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

st.title("💰 SMART SAVINGS CALCULATOR")
st.caption("Công cụ tính toán và phân tích tiền gửi tiết kiệm")

# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================================================
# THANH BÊN - THÔNG TIN KHOẢN GỬI
# =========================================================

with st.sidebar:

    st.header("⚙️ Thông tin khoản gửi")

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=100000,
        value=100000000,
        step=1000000
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=30.0,
        value=5.0,
        step=0.1
    )

    hinh_thuc_lai = st.selectbox(
        "Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    hinh_thuc_nhan = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Lãnh lãi theo tháng",
            "Lãnh lãi theo quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

    tinh_toan = st.button(
        "🧮 TÍNH TOÁN",
        use_container_width=True
    )


# =========================================================
# TÍNH TOÁN
# =========================================================

# Luôn tính để app hiển thị ngay
# Không cần bắt buộc bấm nút

lai_nam = lai_suat / 100
lai_thang = lai_nam / 12

# ---------------------------------------------------------
# LÃI ĐƠN
# ---------------------------------------------------------

tong_lai_don = tien_gui * lai_nam * (ky_han / 12)
tong_tien_don = tien_gui + tong_lai_don

# ---------------------------------------------------------
# LÃI KÉP
# ---------------------------------------------------------

tong_tien_kep = tien_gui * (1 + lai_thang) ** ky_han
tong_lai_kep = tong_tien_kep - tien_gui

# =========================================================
# TÍNH THEO HÌNH THỨC NGƯỜI DÙNG CHỌN
# =========================================================

if hinh_thuc_lai == "Lãi đơn":

    tong_lai = tong_lai_don
    tong_tien = tong_tien_don

    # Lãi nhận định kỳ
    if hinh_thuc_nhan == "Lãnh lãi theo tháng":
        lai_dinh_ky = tien_gui * lai_thang

    elif hinh_thuc_nhan == "Lãnh lãi theo quý":
        lai_dinh_ky = tien_gui * lai_thang * 3

    else:
        lai_dinh_ky = tong_lai

else:

    tong_lai = tong_lai_kep
    tong_tien = tong_tien_kep

    # Lãi định kỳ nếu xét theo quá trình sinh lãi
    if hinh_thuc_nhan == "Lãnh lãi theo tháng":

        lai_dinh_ky = tien_gui * lai_thang

    elif hinh_thuc_nhan == "Lãnh lãi theo quý":

        tien_sau_3_thang = tien_gui * (1 + lai_thang) ** 3
        lai_dinh_ky = tien_sau_3_thang - tien_gui

    else:

        lai_dinh_ky = tong_lai


# =========================================================
# TIÊU ĐỀ KẾT QUẢ
# =========================================================

st.header("📊 Kết quả tính toán")

# =========================================================
# 3 Ô KẾT QUẢ
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💵 Tiền lãi định kỳ",
        format_money(lai_dinh_ky)
    )

with col2:
    st.metric(
        "📈 Tổng tiền lãi",
        format_money(tong_lai)
    )

with col3:
    st.metric(
        "💰 Tổng tiền nhận được",
        format_money(tong_tien)
    )


# =========================================================
# THÔNG TIN KHOẢN GỬI
# =========================================================

st.divider()

st.header("📋 Thông tin khoản gửi")

info1, info2, info3, info4 = st.columns(4)

with info1:
    st.write("**Số tiền gốc**")
    st.write(format_money(tien_gui))

with info2:
    st.write("**Kỳ hạn**")
    st.write(f"{ky_han} tháng")

with info3:
    st.write("**Lãi suất**")
    st.write(f"{lai_suat:.2f}%/năm")

with info4:
    st.write("**Hình thức tính lãi**")
    st.write(hinh_thuc_lai)


# =========================================================
# BIỂU ĐỒ TĂNG TRƯỞNG
# =========================================================

st.divider()

st.header("📈 Biểu đồ tăng trưởng khoản tiền")

# Tạo dữ liệu từng tháng

thang_list = list(range(0, ky_han + 1))
tien_list = []

for thang in thang_list:

    if hinh_thuc_lai == "Lãi đơn":

        tien = tien_gui * (1 + lai_thang * thang)

    else:

        tien = tien_gui * (1 + lai_thang) ** thang

    tien_list.append(tien)


df_chart = pd.DataFrame({
    "Tháng": thang_list,
    "Số tiền nhận được (VNĐ)": tien_list
})

# Đặt tháng làm index để Streamlit vẽ biểu đồ
df_chart = df_chart.set_index("Tháng")

st.line_chart(
    df_chart,
    y="Số tiền nhận được (VNĐ)",
    use_container_width=True
)


# =========================================================
# CÁC MỐC CHÍNH
# =========================================================

st.subheader("📌 Các mốc chính")

# Chỉ hiện tối đa 7 mốc
if ky_han <= 6:

    moc_thang = thang_list

else:

    moc_thang = [
        0,
        ky_han // 6,
        ky_han // 3,
        ky_han // 2,
        (ky_han * 2) // 3,
        (ky_han * 5) // 6,
        ky_han
    ]

# Loại số trùng
moc_thang = sorted(list(set(moc_thang)))

cols = st.columns(len(moc_thang))

for i, thang in enumerate(moc_thang):

    if hinh_thuc_lai == "Lãi đơn":

        gia_tri = tien_gui * (1 + lai_thang * thang)

    else:

        gia_tri = tien_gui * (1 + lai_thang) ** thang

    with cols[i]:
        st.metric(
            f"Tháng {thang}",
            format_money(gia_tri)
        )


# =========================================================
# SO SÁNH LÃI ĐƠN VÀ LÃI KÉP
# =========================================================

st.divider()

st.header("⚖️ So sánh lãi đơn và lãi kép")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🟨 Tổng lãi đơn",
        format_money(tong_lai_don)
    )

with col2:

    st.metric(
        "📈 Tổng lãi kép",
        format_money(tong_lai_kep)
    )

with col3:

    chenh_lech = tong_lai_kep - tong_lai_don

    st.metric(
        "💰 Lãi kép tăng thêm",
        format_money(chenh_lech)
    )


# =========================================================
# GIẢI THÍCH
# =========================================================

st.info(
    "💡 Lãi đơn: tiền lãi chỉ được tính trên số tiền gốc ban đầu. "
    "Lãi kép: tiền lãi được cộng vào vốn để tiếp tục sinh lãi ở các kỳ tiếp theo."
)


# =========================================================
# BẢNG DIỄN BIẾN KHOẢN TIỀN
# =========================================================

st.divider()

st.header("📅 Bảng diễn biến khoản tiền")

bang = []

for thang in thang_list:

    if hinh_thuc_lai == "Lãi đơn":

        so_tien = tien_gui * (1 + lai_thang * thang)

    else:

        so_tien = tien_gui * (1 + lai_thang) ** thang

    tien_lai = so_tien - tien_gui

    bang.append({
        "Tháng": thang,
        "Tiền gốc ban đầu": format_money(tien_gui),
        "Tiền lãi tích lũy": format_money(tien_lai),
        "Tổng tiền nhận được": format_money(so_tien)
    })


df_bang = pd.DataFrame(bang)

st.dataframe(
    df_bang,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# KẾT LUẬN
# =========================================================

st.divider()

st.subheader("📝 Tóm tắt")

st.write(
    f"""
    - **Số tiền gốc:** {format_money(tien_gui)}
    - **Kỳ hạn:** {ky_han} tháng
    - **Lãi suất:** {lai_suat:.2f}%/năm
    - **Hình thức tính lãi:** {hinh_thuc_lai}
    - **Hình thức nhận lãi:** {hinh_thuc_nhan}
    - **Tổng tiền lãi:** {format_money(tong_lai)}
    - **Tổng tiền nhận được:** {format_money(tong_tien)}
    """
)
