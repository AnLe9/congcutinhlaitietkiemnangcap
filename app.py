import streamlit as st
import pandas as pd
import io
import math

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

    /* Nền chính */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(77, 208, 225, 0.08), transparent 25%),
            radial-gradient(circle at 90% 20%, rgba(156, 39, 176, 0.08), transparent 25%),
            linear-gradient(135deg, #101522 0%, #111827 50%, #0b1120 100%);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #151c2d 0%, #101625 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {
        color: #f5f7ff !important;
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 4px;
        background: linear-gradient(90deg, #ffffff, #8be9fd, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        color: #aeb8cc;
        font-size: 16px;
        margin-bottom: 35px;
    }

    /* Card */
    .card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.18);
        backdrop-filter: blur(10px);
    }

    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }

    /* Kết quả */
    .result-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 18px;
        padding: 22px;
        min-height: 150px;
        transition: all 0.25s ease;
    }

    .result-card:hover {
        transform: translateY(-4px);
        border-color: rgba(139,233,253,0.65);
        box-shadow: 0 10px 35px rgba(139,233,253,0.08);
    }

    .result-label {
        color: #aeb8cc;
        font-size: 14px;
        margin-bottom: 12px;
    }

    .result-value {
        color: #ffffff;
        font-size: 26px;
        font-weight: 800;
    }

    .result-small {
        color: #8be9fd;
        font-size: 13px;
        margin-top: 8px;
    }

    /* Thông tin */
    .info-box {
        background: rgba(255,255,255,0.035);
        border-radius: 15px;
        padding: 18px;
        border: 1px solid rgba(255,255,255,0.10);
        height: 100%;
    }

    .info-label {
        color: #8995aa;
        font-size: 13px;
    }

    .info-value {
        color: white;
        font-size: 17px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Badge */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(139,233,253,0.12);
        border: 1px solid rgba(139,233,253,0.25);
        color: #8be9fd;
        font-size: 13px;
        font-weight: 600;
    }

    /* Hiệu ứng sparkle */
    .sparkle {
        position: fixed;
        width: 5px;
        height: 5px;
        background: white;
        border-radius: 50%;
        box-shadow:
            0 0 8px #fff,
            0 0 16px #8be9fd,
            0 0 24px #8be9fd;
        animation: sparkle 2.5s ease-in-out infinite;
        z-index: 9999;
        pointer-events: none;
    }

    @keyframes sparkle {
        0%, 100% {
            opacity: 0;
            transform: scale(0);
        }
        50% {
            opacity: 1;
            transform: scale(1.8);
        }
    }

    /* Bong bóng */
    .bubble {
        position: fixed;
        bottom: -30px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,0.4);
        background: rgba(139,233,253,0.12);
        animation: bubble 6s linear infinite;
        z-index: 9998;
        pointer-events: none;
    }

    @keyframes bubble {
        0% {
            transform: translateY(0) scale(0.7);
            opacity: 0;
        }
        15% {
            opacity: 0.7;
        }
        100% {
            transform: translateY(-100vh) scale(1.2);
            opacity: 0;
        }
    }

    /* Nút */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(139,233,253,0.3);
        font-weight: 700;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: #8be9fd;
        box-shadow: 0 6px 20px rgba(139,233,253,0.15);
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.10);
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG
# =========================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


def dinh_dang_so(so):
    return f"{so:,.0f}"


# =========================================================
# HIỆU ỨNG
# =========================================================

def hieu_ung():
    st.balloons()

    st.markdown("""
    <div class="sparkle" style="left:10%;top:20%;animation-delay:0s;"></div>
    <div class="sparkle" style="left:25%;top:35%;animation-delay:.5s;"></div>
    <div class="sparkle" style="left:45%;top:18%;animation-delay:1s;"></div>
    <div class="sparkle" style="left:65%;top:30%;animation-delay:.3s;"></div>
    <div class="sparkle" style="left:82%;top:18%;animation-delay:1.2s;"></div>
    <div class="sparkle" style="left:90%;top:45%;animation-delay:.7s;"></div>

    <div class="bubble" style="left:12%;animation-delay:.2s;"></div>
    <div class="bubble" style="left:28%;animation-delay:1.5s;"></div>
    <div class="bubble" style="left:48%;animation-delay:2.3s;"></div>
    <div class="bubble" style="left:68%;animation-delay:.8s;"></div>
    <div class="bubble" style="left:85%;animation-delay:3s;"></div>
    """, unsafe_allow_html=True)


# =========================================================
# TIÊU ĐỀ
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
        value=12,
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

    st.markdown("---")

    tinh_toan = st.button(
        "🧮 TÍNH LÃI",
        use_container_width=True
    )


# =========================================================
# CHỈ TÍNH KHI NGƯỜI DÙNG BẤM NÚT
# =========================================================

if tinh_toan:

    if tien_gui <= 0:
        st.error("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif lai_suat < 0:
        st.error("⚠️ Lãi suất không được nhỏ hơn 0.")

    else:

        # -------------------------------------------------
        # THÔNG SỐ CHUNG
        # -------------------------------------------------

        r = lai_suat / 100
        so_nam = ky_han / 12

        # -------------------------------------------------
        # TÍNH TOÁN
        # -------------------------------------------------

        if hinh_thuc_gui == "Lãi đơn":

            tong_tien_lai = tien_gui * r * so_nam
            tong_tien = tien_gui + tong_tien_lai

        else:

            if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
                so_lan_nhap_lai = 12

            elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
                so_lan_nhap_lai = 4

            else:
                so_lan_nhap_lai = 1

            if hinh_thuc_nhan_lai == "Lãnh lãi cuối kỳ":

                tong_tien = tien_gui * (1 + r) ** so_nam

            else:

                tong_so_ky = so_lan_nhap_lai * so_nam

                tong_tien = tien_gui * (
                    1 + r / so_lan_nhap_lai
                ) ** tong_so_ky

            tong_tien_lai = tong_tien - tien_gui

        # -------------------------------------------------
        # LÃI ĐỊNH KỲ
        # -------------------------------------------------

        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
            lai_dinh_ky = tien_gui * r / 12

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
            lai_dinh_ky = tien_gui * r / 4

        else:
            lai_dinh_ky = tong_tien_lai

        # -------------------------------------------------
        # LÃI ĐƠN ĐỂ SO SÁNH
        # -------------------------------------------------

        lai_don_so_sanh = tien_gui * r * so_nam
        chenhlech_laikep = tong_tien_lai - lai_don_so_sanh

        # =================================================
        # HIỆU ỨNG
        # =================================================

        hieu_ung()

        st.success("✨ Đã tính toán xong!")

        # =================================================
        # KẾT QUẢ CHÍNH
        # =================================================

        st.markdown("## 📊 Kết quả tính toán")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">💵 Tiền lãi định kỳ</div>
                <div class="result-value">
                    {dinh_dang_tien(lai_dinh_ky)}
                </div>
                <div class="result-small">
                    {hinh_thuc_nhan_lai}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">📈 Tổng tiền lãi</div>
                <div class="result-value">
                    {dinh_dang_tien(tong_tien_lai)}
                </div>
                <div class="result-small">
                    Sau {ky_han} tháng
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">💰 Tổng gốc + lãi</div>
                <div class="result-value">
                    {dinh_dang_tien(tong_tien)}
                </div>
                <div class="result-small">
                    Số tiền cuối kỳ
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # =================================================
        # THÔNG TIN KHOẢN GỬI
        # =================================================

        st.markdown("## 📋 Thông tin khoản gửi")

        info1, info2, info3, info4 = st.columns(4)

        with info1:
            st.markdown(f"""
            <div class="info-box">
                <div class="info-label">Số tiền gốc</div>
                <div class="info-value">{dinh_dang_tien(tien_gui)}</div>
            </div>
            """, unsafe_allow_html=True)

        with info2:
            st.markdown(f"""
            <div class="info-box">
                <div class="info-label">Kỳ hạn</div>
                <div class="info-value">{ky_han} tháng</div>
            </div>
            """, unsafe_allow_html=True)

        with info3:
            st.markdown(f"""
            <div class="info-box">
                <div class="info-label">Lãi suất</div>
                <div class="info-value">{lai_suat:.2f}%/năm</div>
            </div>
            """, unsafe_allow_html=True)

        with info4:
            st.markdown(f"""
            <div class="info-box">
                <div class="info-label">Hình thức</div>
                <div class="info-value">{hinh_thuc_gui}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # =================================================
        # THANH TIẾN TRÌNH
        # =================================================

        st.markdown("### ⏳ Thời gian gửi")

        st.progress(
            min(ky_han / 60, 1.0),
            text=f"Kỳ hạn {ky_han} tháng"
        )

        # =================================================
        # BIỂU ĐỒ TĂNG TRƯỞNG
        # =================================================

        st.markdown("## 📈 Biểu đồ tăng trưởng khoản tiền")

        # Tạo dữ liệu từng tháng
        thang_list = [0]
        tien_list = [tien_gui]

        for thang in range(1, ky_han + 1):

            if hinh_thuc_gui == "Lãi đơn":

                tien_theo_thang = tien_gui * (
                    1 + r * thang / 12
                )

            else:

                if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

                    tien_theo_thang = tien_gui * (
                        1 + r / 12
                    ) ** thang

                elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

                    so_quy = thang / 3

                    tien_theo_thang = tien_gui * (
                        1 + r / 4
                    ) ** so_quy

                else:

                    tien_theo_thang = tien_gui * (
                        1 + r
                    ) ** (thang / 12)

            thang_list.append(thang)
            tien_list.append(tien_theo_thang)

        chart_data = pd.DataFrame({
            "Tháng": thang_list,
            "Tổng tiền": tien_list
        })

        st.line_chart(
            chart_data,
            x="Tháng",
            y="Tổng tiền",
            height=380
        )

        # =================================================
        # SO SÁNH LÃI ĐƠN - LÃI KÉP
        # =================================================

        st.markdown("## ⚖️ So sánh lãi đơn và lãi kép")

        comp1, comp2, comp3 = st.columns(3)

        with comp1:
            st.metric(
                "Lãi đơn",
                dinh_dang_tien(lai_don_so_sanh)
            )

        with comp2:
            st.metric(
                "Lãi kép",
                dinh_dang_tien(tong_tien_lai)
            )

        with comp3:
            st.metric(
                "Lãi kép tăng thêm",
                dinh_dang_tien(max(chenhlech_laikep, 0))
            )

        if hinh_thuc_gui == "Lãi kép" and chenhlech_laikep > 0:
            st.info(
                f"💡 Với khoản gửi này, lãi kép tạo thêm "
                f"{dinh_dang_tien(chenhlech_laikep)} "
                f"tiền lãi so với lãi đơn."
            )

        # =================================================
        # BẢNG CHI TIẾT
        # =================================================

        st.markdown("## 📑 Bảng chi tiết")

        chi_tiet = []

        for i in range(len(thang_list)):

            tong = tien_list[i]
            lai = tong - tien_gui

            chi_tiet.append({
                "Tháng": i,
                "Tiền lãi": lai,
                "Tổng gốc và lãi": tong
            })

        df = pd.DataFrame(chi_tiet)

        # Hiển thị đẹp hơn
        df_hien_thi = df.copy()

        df_hien_thi["Tiền lãi"] = df_hien_thi["Tiền lãi"].apply(
            dinh_dang_tien
        )

        df_hien_thi["Tổng gốc và lãi"] = df_hien_thi[
            "Tổng gốc và lãi"
        ].apply(dinh_dang_tien)

        st.dataframe(
            df_hien_thi,
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # TẢI BẢNG CHI TIẾT
        # =================================================

        csv_buffer = io.StringIO()
        df_hien_thi.to_csv(
            csv_buffer,
            index=False,
            encoding="utf-8-sig"
        )

        st.download_button(
            label="⬇️ Tải bảng chi tiết",
            data=csv_buffer.getvalue(),
            file_name="bang_chi_tiet_tien_gui.csv",
            mime="text/csv",
            use_container_width=True
        )

        # =================================================
        # TÓM TẮT CUỐI
        # =================================================

        st.markdown("## 🧾 Tóm tắt")

        st.markdown(f"""
        <div class="card">
            <span class="badge">KẾT QUẢ</span>

            <p style="color:#dbe4f5;font-size:16px;margin-top:15px;">
                Bạn gửi <b>{dinh_dang_tien(tien_gui)}</b>
                trong <b>{ky_han} tháng</b>,
                với lãi suất <b>{lai_suat:.2f}%/năm</b>.
            </p>

            <p style="color:#dbe4f5;font-size:16px;">
                Hình thức tính:
                <b>{hinh_thuc_gui}</b>
            </p>

            <p style="color:#dbe4f5;font-size:16px;">
                Tổng tiền lãi:
                <b>{dinh_dang_tien(tong_tien_lai)}</b>
            </p>

            <p style="color:#8be9fd;font-size:18px;font-weight:700;">
                💰 Tổng nhận được:
                {dinh_dang_tien(tong_tien)}
            </p>
        </div>
        """, unsafe_allow_html=True)

else:

    # =====================================================
    # MÀN HÌNH CHỜ - KHÔNG TỰ TÍNH
    # =====================================================

    st.markdown("""
    <div class="card" style="text-align:center;padding:55px 25px;">

        <div style="font-size:55px;">💰</div>

        <h2 style="color:white;">
            Sẵn sàng tính khoản tiết kiệm của bạn?
        </h2>

        <p style="color:#aeb8cc;font-size:16px;">
            Nhập số tiền, kỳ hạn và lãi suất ở bảng bên trái,
            sau đó bấm <b>🧮 TÍNH LÃI</b>.
        </p>

        <p style="color:#8be9fd;">
            ✨ Ứng dụng sẽ hiển thị kết quả, biểu đồ
            và bảng chi tiết theo từng tháng.
        </p>

    </div>
    """, unsafe_allow_html=True)
