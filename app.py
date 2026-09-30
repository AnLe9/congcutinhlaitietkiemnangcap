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
# CSS - GIAO DIỆN
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
    color: #888;
    margin-bottom: 30px;
}

/* Các ô kết quả */
.result-box {
    padding: 22px 10px;
    border-radius: 14px;
    background-color: #ffffff;
    border: 1px solid #dddddd;
    text-align: center;
    min-height: 125px;
}

.result-title {
    font-size: 16px;
    color: #555555;
    margin-bottom: 12px;
}

.result-value {
    font-size: 25px;
    font-weight: bold;
    color: #222222;
}


/* Tiêu đề phần */
.section-title {
    font-size: 25px;
    font-weight: bold;
}


/* Làm bảng dễ đọc */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
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
    value=100000000.0,
    step=1000000.0,
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

        lai_nam = lai_suat / 100
        so_nam = ky_han / 12


        # =================================================
        # XÁC ĐỊNH SỐ LẦN GHÉP LÃI
        # =================================================

        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
            tan_suat = 12

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
            tan_suat = 4

        else:
            tan_suat = 1


        # =================================================
        # LÃI ĐƠN
        # =================================================

        if hinh_thuc_gui == "Lãi đơn":

            tong_tien_lai = (
                tien_gui
                * lai_nam
                * so_nam
            )

            tong_tien = tien_gui + tong_tien_lai


        # =================================================
        # LÃI KÉP
        # =================================================

        else:

            tong_so_ky = ky_han / (12 / tan_suat)

            tong_tien = tien_gui * (
                1 + lai_nam / tan_suat
            ) ** tong_so_ky

            tong_tien_lai = tong_tien - tien_gui


        # =================================================
        # TÍNH LÃI KỲ ĐẦU
        # =================================================

        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

            lai_ky_dau = tien_gui * lai_nam / 12

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

            lai_ky_dau = tien_gui * lai_nam / 4

        else:

            lai_ky_dau = tong_tien_lai


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
                        💵 Tiền lãi kỳ đầu
                    </div>

                    <div class="result-value">
                        {dinh_dang_tien(lai_ky_dau)}
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
                        💰 Tổng tiền nhận được
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
            st.write(hinh_thuc_gui)


        # =================================================
        # BIỂU ĐỒ
        # =================================================

        st.divider()

        st.subheader("📈 Khoản tiền tăng theo thời gian")

        st.caption(
            "Biểu đồ thể hiện tổng số tiền (gốc + lãi) "
            "tại một số mốc thời gian trong kỳ hạn."
        )


        # Chỉ lấy tối đa 7 mốc để biểu đồ dễ nhìn
        so_moc = min(7, ky_han + 1)

        if ky_han <= 6:

            cac_moc = list(range(ky_han + 1))

        else:

            buoc = ky_han / (so_moc - 1)

            cac_moc = [
                round(i * buoc)
                for i in range(so_moc)
            ]

            cac_moc = sorted(list(set(cac_moc)))


        tien_theo_moc = []


        for thang in cac_moc:

            nam = thang / 12


            if hinh_thuc_gui == "Lãi đơn":

                gia_tri = tien_gui * (
                    1 + lai_nam * nam
                )


            else:

                so_ky = thang / (12 / tan_suat)

                gia_tri = tien_gui * (
                    1 + lai_nam / tan_suat
                ) ** so_ky


            tien_theo_moc.append(gia_tri)


        # Dữ liệu biểu đồ
        chart_data = {
            "Tháng": cac_moc,
            "Tổng tiền": tien_theo_moc
        }


        st.line_chart(
            chart_data,
            x="Tháng",
            y="Tổng tiền"
        )


        # Hiển thị các mốc dưới biểu đồ
        st.write("**Các mốc chính:**")

        cols = st.columns(len(cac_moc))

        for i in range(len(cac_moc)):

            with cols[i]:

                st.metric(
                    f"Tháng {cac_moc[i]}",
                    dinh_dang_trieu(tien_theo_moc[i])
                )


        # =================================================
        # SO SÁNH LÃI ĐƠN VÀ LÃI KÉP
        # =================================================

        st.divider()

        st.subheader("⚖️ So sánh lãi đơn và lãi kép")

        # Lãi đơn
        lai_don = (
            tien_gui
            * lai_nam
            * so_nam
        )


        # Lãi kép
        tong_tien_kep = tien_gui * (
            1 + lai_nam / tan_suat
        ) ** (
            ky_han / (12 / tan_suat)
        )

        lai_kep = tong_tien_kep - tien_gui

        chenhlech = lai_kep - lai_don


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "💵 Lãi đơn",
                dinh_dang_tien(lai_don)
            )


        with col2:

            st.metric(
                "📈 Lãi kép",
                dinh_dang_tien(lai_kep)
            )


        with col3:

            st.metric(
                "💰 Lãi kép tăng thêm",
                dinh_dang_tien(chenhlech)
            )


        st.info(
            "Lãi đơn chỉ tính lãi trên số tiền gốc ban đầu. "
            "Lãi kép cộng tiền lãi vào vốn để tiếp tục sinh lãi "
            "ở các kỳ tiếp theo."
        )


        # =================================================
        # BẢNG DIỄN BIẾN
        # =================================================

        st.divider()

        st.subheader("📅 Diễn biến khoản tiền theo từng tháng")

        st.caption(
            "Gốc = số tiền ban đầu | "
            "Lãi phát sinh = tiền lãi trong tháng | "
            "Tổng tiền = gốc + lãi"
        )


        bang_thang = []
        bang_goc = []
        bang_lai = []
        bang_tong = []


        tien_truoc = tien_gui


        for thang in range(0, ky_han + 1):


            if thang == 0:

                tong_thang = tien_gui
                lai_thang = 0


            else:

                nam = thang / 12


                if hinh_thuc_gui == "Lãi đơn":

                    tong_thang = tien_gui * (
                        1 + lai_nam * nam
                    )


                    tong_thang_truoc = tien_gui * (
                        1 + lai_nam * ((thang - 1) / 12)
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


            bang_thang.append(thang)

            bang_goc.append(
                dinh_dang_tien(tien_gui)
            )

            bang_lai.append(
                dinh_dang_tien(lai_thang)
            )

            bang_tong.append(
                dinh_dang_tien(tong_thang)
            )


        bang_du_lieu = {

            "Tháng": bang_thang,

            "Tiền gốc": bang_goc,

            "Lãi phát sinh": bang_lai,

            "Tổng tiền nhận được": bang_tong

        }


        st.dataframe(
            bang_du_lieu,
            use_container_width=True,
            hide_index=True
        )


        # =================================================
        # NHẬN XÉT
        # =================================================

        st.divider()

        st.subheader("💡 Giải thích kết quả")


        if hinh_thuc_gui == "Lãi đơn":

            st.info(
                "Bạn đang sử dụng lãi đơn. "
                "Tiền lãi được tính dựa trên số tiền gốc ban đầu "
                "nên tiền lãi mỗi kỳ không thay đổi."
            )

        else:

            st.success(
                "Bạn đang sử dụng lãi kép. "
                "Tiền lãi được cộng vào số tiền vốn để tiếp tục "
                "sinh lãi ở các kỳ tiếp theo."
            )


        st.write(
            f"💰 Với số tiền gửi **{dinh_dang_tien(tien_gui)}**, "
            f"kỳ hạn **{ky_han} tháng** và lãi suất "
            f"**{lai_suat:.2f}%/năm**, "
            f"tổng số tiền cuối kỳ dự kiến là "
            f"**{dinh_dang_tien(tong_tien)}**."
        )


else:

    st.info(
        "👈 Nhập thông tin khoản gửi ở thanh bên "
        "và nhấn **TÍNH TOÁN** để xem kết quả."
    )
