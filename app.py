import streamlit as st

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Smart Savings Calculator",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# CSS GIAO DIỆN
# =========================================================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f5f7fa;
        text-align: center;
    }

    .result-title {
        font-size: 16px;
        color: #666;
    }

    .result-value {
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


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
# SIDEBAR
# =========================================================
st.sidebar.header("⚙️ Thông tin khoản gửi")

tien_gui = st.sidebar.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
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

hinh_thuc_gui = st.sidebar.selectbox(
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
# TÍNH TOÁN
# =========================================================
if tinh_lai:

    if tien_gui <= 0:

        st.error("⚠️ Số tiền gửi phải lớn hơn 0.")

    else:

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

            if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

                tan_suat = 12

                tong_tien = tien_gui * (
                    1 + r / tan_suat
                ) ** (tan_suat * so_nam)

            elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

                tan_suat = 4

                tong_tien = tien_gui * (
                    1 + r / tan_suat
                ) ** (tan_suat * so_nam)

            else:

                tong_tien = tien_gui * (
                    1 + r
                ) ** so_nam

            tong_tien_lai = tong_tien - tien_gui


        # =================================================
        # LÃI ĐỊNH KỲ
        # =================================================
        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

            lai_dinh_ky = tien_gui * r / 12

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

            lai_dinh_ky = tien_gui * r / 4

        else:

            lai_dinh_ky = tong_tien_lai


        # =================================================
        # SO SÁNH LÃI ĐƠN - LÃI KÉP
        # =================================================
        lai_don_so_sanh = tien_gui * r * so_nam

        lai_kep_so_sanh = (
            tien_gui * (1 + r) ** so_nam
            - tien_gui
        )

        chenhlech = lai_kep_so_sanh - lai_don_so_sanh


        # =================================================
        # KẾT QUẢ
        # =================================================
        st.subheader("📊 Kết quả tính toán")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                f"""
                <div class="result-box">
                    <div class="result-title">
                        💵 Tiền lãi định kỳ
                    </div>
                    <div class="result-value">
                        {dinh_dang_tien(lai_dinh_ky)}
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
                        {dinh_dang_tien(tong_tien_lai)}
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
                        💰 Tổng gốc + lãi
                    </div>
                    <div class="result-value">
                        {dinh_dang_tien(tong_tien)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # THÔNG TIN KHOẢN GỬI
        # =================================================
        st.divider()

        st.subheader("📋 Thông tin khoản gửi")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write("**Số tiền gửi**")
            st.write(dinh_dang_tien(tien_gui))

        with col2:
            st.write("**Kỳ hạn**")
            st.write(f"{ky_han} tháng")

        with col3:
            st.write("**Lãi suất**")
            st.write(f"{lai_suat:.2f}%/năm")

        with col4:
            st.write("**Hình thức**")
            st.write(hinh_thuc_gui)


        # =================================================
        # BIỂU ĐỒ TĂNG TRƯỞNG
        # =================================================
        st.divider()

        st.subheader("📈 Biểu đồ tăng trưởng khoản tiền")

        thang_list = []
        tien_list = []

        for thang in range(ky_han + 1):

            nam = thang / 12

            if hinh_thuc_gui == "Lãi đơn":

                gia_tri = tien_gui * (1 + r * nam)

            else:

                if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

                    gia_tri = tien_gui * (
                        1 + r / 12
                    ) ** thang

                elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

                    so_quy = thang / 3

                    gia_tri = tien_gui * (
                        1 + r / 4
                    ) ** so_quy

                else:

                    gia_tri = tien_gui * (
                        1 + r
                    ) ** nam

            thang_list.append(thang)
            tien_list.append(gia_tri)


        # Streamlit tự tạo biểu đồ
        chart_data = {
            "Số tiền (VNĐ)": tien_list
        }

        st.line_chart(
            chart_data,
            x=thang_list,
            x_label="Thời gian (tháng)",
            y_label="Số tiền (VNĐ)"
        )


        # =================================================
        # SO SÁNH
        # =================================================
        st.divider()

        st.subheader("⚖️ So sánh lãi đơn và lãi kép")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Lãi đơn",
                dinh_dang_tien(lai_don_so_sanh)
            )

        with col2:

            st.metric(
                "Lãi kép",
                dinh_dang_tien(lai_kep_so_sanh)
            )

        with col3:

            st.metric(
                "Chênh lệch",
                dinh_dang_tien(chenhlech)
            )


        # =================================================
        # BẢNG DIỄN BIẾN
        # =================================================
        st.divider()

        st.subheader("📅 Bảng diễn biến khoản tiền")

        st.dataframe(
            {
                "Tháng": thang_list,
                "Số tiền (VNĐ)": [
                    dinh_dang_tien(x)
                    for x in tien_list
                ]
            },
            use_container_width=True,
            hide_index=True
        )


        # =================================================
        # NHẬN XÉT
        # =================================================
        st.divider()

        st.subheader("💡 Nhận xét")

        if hinh_thuc_gui == "Lãi đơn":

            st.info(
                "Lãi đơn được tính dựa trên số tiền gốc ban đầu. "
                "Tiền lãi không được cộng vào vốn để tiếp tục sinh lãi."
            )

        else:

            st.info(
                "Lãi kép cho phép tiền lãi được cộng vào vốn "
                "và tiếp tục sinh lãi trong các kỳ tiếp theo."
            )

        if chenhlech > 0:

            st.success(
                f"Với kỳ hạn {ky_han} tháng, "
                f"lãi kép cao hơn lãi đơn "
                f"{dinh_dang_tien(chenhlech)}."
            )

else:

    st.info(
        "👈 Nhập thông tin khoản gửi ở thanh bên "
        "và nhấn **TÍNH TOÁN** để xem kết quả."
    )
