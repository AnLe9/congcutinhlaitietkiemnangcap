import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")
st.caption("Công cụ tính toán lãi suất đơn giản, trực quan và dễ sử dụng.")

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================
# BỐ CỤC CHÍNH
# =========================
cot_trai, cot_phai = st.columns([1, 2], gap="large")


# =========================================================
# CỘT TRÁI - NHẬP THÔNG TIN
# =========================================================
with cot_trai:

    st.subheader("📌 Thông tin khoản gửi")

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=0.0,
        step=1_000_000.0,
        format="%.0f",
        help="Nhập số tiền bạn muốn gửi tiết kiệm."
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=0,
        value=0,
        step=1,
        help="Nhập số tháng gửi tiền."
    )

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        value=0.0,
        step=0.1,
        format="%.2f",
        help="Nhập lãi suất ngân hàng tính theo năm."
    )

    hinh_thuc_gui = st.selectbox(
        "Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    hinh_thuc_nhan_lai = st.selectbox(
        "Hình thức nhận lãi",
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


# =========================================================
# CỘT PHẢI - KẾT QUẢ
# =========================================================
with cot_phai:

    if not tinh_lai:

        st.subheader("📊 Kết quả tính toán")

        st.info(
            "Nhập thông tin khoản gửi ở bên trái, "
            "sau đó nhấn **🧮 TÍNH LÃI** để xem kết quả."
        )

        st.write("")
        st.write("### 📋 Các bước sử dụng")

        st.write("1. Nhập số tiền gửi.")
        st.write("2. Nhập kỳ hạn và lãi suất.")
        st.write("3. Chọn hình thức tính lãi.")
        st.write("4. Chọn hình thức nhận lãi.")
        st.write("5. Nhấn **TÍNH LÃI**.")

    else:

        # =========================
        # KIỂM TRA DỮ LIỆU
        # =========================
        if tien_gui <= 0:
            st.error("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0.")

        elif ky_han <= 0:
            st.error("⚠️ Vui lòng nhập kỳ hạn lớn hơn 0.")

        elif lai_suat < 0:
            st.error("⚠️ Lãi suất không được nhỏ hơn 0.")

        else:

            # =========================
            # THÔNG SỐ TÍNH
            # =========================
            r = lai_suat / 100
            so_nam = ky_han / 12

            # =========================
            # TÍNH LÃI ĐƠN
            # =========================
            if hinh_thuc_gui == "Lãi đơn":

                tong_tien_lai = tien_gui * r * so_nam
                tong_tien = tien_gui + tong_tien_lai

                if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
                    lai_dinh_ky = tien_gui * r / 12

                elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
                    lai_dinh_ky = tien_gui * r / 4

                else:
                    lai_dinh_ky = tong_tien_lai

            # =========================
            # TÍNH LÃI KÉP
            # =========================
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

                    # Lãi kép theo kỳ hạn
                    tong_tien = tien_gui * (1 + r) ** so_nam

                tong_tien_lai = tong_tien - tien_gui

                # Với lãi kép, tiền lãi mỗi kỳ tăng dần
                # nên không dùng một con số cố định
                # cho "lãi định kỳ".
                lai_dinh_ky = None

            # =================================================
            # THÔNG BÁO
            # =================================================
            st.success("✅ Tính toán thành công!")

            st.subheader("📊 Kết quả tính toán")

            # =================================================
            # 3 Ô KẾT QUẢ - DÙNG STREAMLIT THUẦN
            # =================================================
            col1, col2, col3 = st.columns(3)

            with col1:

                if lai_dinh_ky is not None:

                    st.metric(
                        "💵 Tiền lãi định kỳ",
                        dinh_dang_tien(lai_dinh_ky)
                    )

                else:

                    st.metric(
                        "💵 Tiền lãi định kỳ",
                        "Tăng dần"
                    )

            with col2:

                st.metric(
                    "📈 Tổng tiền lãi",
                    dinh_dang_tien(tong_tien_lai)
                )

            with col3:

                st.metric(
                    "💰 Tổng gốc + lãi",
                    dinh_dang_tien(tong_tien)
                )

            st.divider()

            # =================================================
            # THÔNG TIN KHOẢN GỬI
            # =================================================
            st.subheader("📋 Thông tin khoản gửi")

            thong_tin1, thong_tin2 = st.columns(2)

            with thong_tin1:

                st.write(
                    f"**Số tiền gửi:** "
                    f"{dinh_dang_tien(tien_gui)}"
                )

                st.write(
                    f"**Kỳ hạn:** "
                    f"{ky_han} tháng"
                )

                st.write(
                    f"**Lãi suất:** "
                    f"{lai_suat:.2f}%/năm"
                )

            with thong_tin2:

                st.write(
                    f"**Hình thức tính:** "
                    f"{hinh_thuc_gui}"
                )

                st.write(
                    f"**Hình thức nhận lãi:** "
                    f"{hinh_thuc_nhan_lai}"
                )

            st.divider()

            # =================================================
            # BẢNG CHI TIẾT
            # =================================================
            st.subheader("📑 Bảng chi tiết theo thời gian")

            danh_sach_thang = []
            tien_hien_tai = tien_gui
            tong_lai_tich_luy = 0

            for thang in range(1, ky_han + 1):

                # -------------------------
                # LÃI ĐƠN
                # -------------------------
                if hinh_thuc_gui == "Lãi đơn":

                    lai_thang = tien_gui * r / 12

                    tong_lai_tich_luy += lai_thang

                    tong_goc_lai = (
                        tien_gui + tong_lai_tich_luy
                    )

                # -------------------------
                # LÃI KÉP
                # -------------------------
                else:

                    if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

                        lai_thang = tien_hien_tai * r / 12

                        tien_hien_tai += lai_thang

                        tong_lai_tich_luy = (
                            tien_hien_tai - tien_gui
                        )

                        tong_goc_lai = tien_hien_tai

                    elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

                        # Trong thời gian chưa đến kỳ nhập lãi,
                        # giá trị được giữ nguyên.
                        if thang % 3 == 0:

                            lai_quy = tien_hien_tai * r / 4

                            tien_hien_tai += lai_quy

                        tong_lai_tich_luy = (
                            tien_hien_tai - tien_gui
                        )

                        tong_goc_lai = tien_hien_tai

                        lai_thang = (
                            tong_lai_tich_luy
                            - (
                                danh_sach_thang[-1]["Tổng gốc và lãi"]
                                - tien_gui
                            )
                            if danh_sach_thang
                            else tong_lai_tich_luy
                        )

                    else:

                        # Lãi kép cuối kỳ
                        # Phân bổ giá trị theo thời gian
                        tong_goc_lai = tien_gui * (
                            1 + r
                        ) ** (thang / 12)

                        tong_lai_tich_luy = (
                            tong_goc_lai - tien_gui
                        )

                        if danh_sach_thang:

                            lai_thang = (
                                tong_goc_lai
                                - danh_sach_thang[-1]["Tổng gốc và lãi"]
                            )

                        else:

                            lai_thang = (
                                tong_goc_lai - tien_gui
                            )

                danh_sach_thang.append(
                    {
                        "Tháng": thang,
                        "Lãi": round(lai_thang),
                        "Tổng gốc và lãi": round(tong_goc_lai)
                    }
                )

            df = pd.DataFrame(danh_sach_thang)

            # Định dạng tiền
            df["Lãi"] = df["Lãi"].apply(
                lambda x: f"{x:,.0f} VNĐ"
            )

            df["Tổng gốc và lãi"] = df[
                "Tổng gốc và lãi"
            ].apply(
                lambda x: f"{x:,.0f} VNĐ"
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # =================================================
            # BIỂU ĐỒ
            # =================================================
            st.subheader("📈 Biểu đồ tăng trưởng")

            # Tạo dữ liệu riêng để biểu đồ dễ nhìn
            df_chart = pd.DataFrame(danh_sach_thang)

            df_chart["Tiền lãi tích lũy"] = (
                df_chart["Tổng gốc và lãi"] - tien_gui
            )

            df_chart = df_chart.set_index("Tháng")

            st.line_chart(
                df_chart["Tiền lãi tích lũy"],
                height=350
            )

            st.caption(
                "Biểu đồ thể hiện số tiền lãi tích lũy "
                "qua từng tháng."
            )

            # =================================================
            # TÓM TẮT
            # =================================================
            st.divider()

            st.subheader("📝 Tóm tắt")

            st.write(
                f"Với số tiền gửi **{dinh_dang_tien(tien_gui)}**, "
                f"kỳ hạn **{ky_han} tháng** và lãi suất "
                f"**{lai_suat:.2f}%/năm**, "
                f"bạn nhận được tổng tiền lãi là "
                f"**{dinh_dang_tien(tong_tien_lai)}**."
            )

            st.write(
                f"💰 Tổng số tiền cuối kỳ: "
                f"**{dinh_dang_tien(tong_tien)}**."
            )
