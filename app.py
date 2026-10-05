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
# CSS - GIAO DIỆN GỌN, KHOA HỌC, TINH TẾ
# =========================================================

st.markdown("""
<style>

    /* Nền tổng thể */
    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(100, 120, 180, 0.12),
                transparent 38%
            ),
            linear-gradient(
                135deg,
                #0b1120 0%,
                #111827 50%,
                #0b1220 100%
            );
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #f8fafc;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 35px;
    }

    /* Thanh trang trí nhỏ dưới tiêu đề */
    .title-line {
        width: 90px;
        height: 3px;
        margin: 0 auto 25px auto;
        border-radius: 10px;
        background: linear-gradient(
            90deg,
            transparent,
            #94a3b8,
            transparent
        );
    }

    /* Card */
    .info-card {
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        background: rgba(255, 255, 255, 0.035);
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.12);
    }

    /* Kết quả */
    .result-card {
        padding: 22px;
        min-height: 135px;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.22);
        background: rgba(255, 255, 255, 0.045);
        transition: all 0.25s ease;
    }

    .result-card:hover {
        border-color: rgba(203, 213, 225, 0.45);
        transform: translateY(-2px);
    }

    .result-title {
        color: #cbd5e1;
        font-size: 15px;
        margin-bottom: 10px;
    }

    .result-value {
        color: #f8fafc;
        font-size: 25px;
        font-weight: 750;
    }

    .result-note {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 8px;
    }

    /* Box chào mừng */
    .welcome-box {
        padding: 34px;
        margin-top: 20px;
        margin-bottom: 25px;
        text-align: center;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.045),
                rgba(255,255,255,0.018)
            );
    }

    .welcome-icon {
        font-size: 38px;
        margin-bottom: 12px;
        opacity: 0.9;
    }

    .welcome-title {
        color: #f8fafc;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .welcome-text {
        color: #94a3b8;
        font-size: 15px;
        line-height: 1.8;
    }

    /* Section title */
    .section-title {
        color: #f8fafc;
        font-size: 25px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Thông tin */
    .detail-label {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .detail-value {
        color: #f8fafc;
        font-size: 17px;
        font-weight: 650;
    }

    /* Ghi chú */
    .note-box {
        padding: 16px 20px;
        border-left: 3px solid #64748b;
        background: rgba(255,255,255,0.035);
        border-radius: 8px;
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.7;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid rgba(148,163,184,0.12);
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
    'Công cụ tính toán và phân tích tiền gửi tiết kiệm'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="title-line"></div>',
    unsafe_allow_html=True
)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


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
        format="%.0f",
        help="Nhập số tiền bạn muốn gửi."
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=0,
        value=0,
        step=1,
        help="Nhập số tháng bạn muốn gửi tiền."
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
        "Cách tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        help="Lãi kép sẽ cộng tiền lãi vào vốn để tiếp tục sinh lãi."
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
# TRẠNG THÁI BAN ĐẦU
# =========================================================

if not tinh_lai:

    st.markdown("""
    <div class="welcome-box">

        <div class="welcome-icon">📊</div>

        <div class="welcome-title">
            Sẵn sàng tính khoản tiết kiệm
        </div>

        <div class="welcome-text">
            Nhập số tiền gửi, kỳ hạn và lãi suất ở bảng bên trái.
            <br>
            Sau đó nhấn <b>🧮 TÍNH LÃI</b> để xem kết quả.
        </div>

    </div>
    """, unsafe_allow_html=True)

    # Hướng dẫn ngắn
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <b>① Nhập thông tin</b><br>
            <span style="color:#94a3b8;font-size:14px;">
            Điền số tiền, kỳ hạn và lãi suất.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <b>② Chọn cách tính</b><br>
            <span style="color:#94a3b8;font-size:14px;">
            Chọn lãi đơn hoặc lãi kép.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <b>③ Xem kết quả</b><br>
            <span style="color:#94a3b8;font-size:14px;">
            Xem tiền lãi và bảng theo từng tháng.
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Smart Savings Calculator · Công cụ hỗ trợ tính toán
    </div>
    """, unsafe_allow_html=True)

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

if lai_suat < 0:
    st.error("⚠️ Lãi suất không được nhỏ hơn 0.")
    st.stop()


# =========================================================
# TÍNH TOÁN
# =========================================================

r = lai_suat / 100
so_nam = ky_han / 12


# =========================================================
# LÃI ĐƠN
# =========================================================

if hinh_thuc_gui == "Lãi đơn":

    tong_tien_lai = tien_gui * r * so_nam
    tong_tien = tien_gui + tong_tien_lai


# =========================================================
# LÃI KÉP
# =========================================================

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

        # Với cuối kỳ, tính lãi theo kỳ hạn
        tong_tien = tien_gui * (1 + r * so_nam)

    tong_tien_lai = tong_tien - tien_gui


# =========================================================
# LÃI ĐỊNH KỲ
# =========================================================

if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

    if hinh_thuc_gui == "Lãi đơn":
        lai_dinh_ky = tien_gui * r / 12
    else:
        lai_dinh_ky = None

elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

    if hinh_thuc_gui == "Lãi đơn":
        lai_dinh_ky = tien_gui * r / 4
    else:
        lai_dinh_ky = None

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

    if lai_dinh_ky is not None:
        lai_text = dinh_dang_tien(lai_dinh_ky)
        note = "Số tiền lãi mỗi kỳ"
    else:
        lai_text = "Tùy theo số dư"
        note = "Lãi được cộng dồn vào vốn"

    st.markdown(f"""
    <div class="result-card">

        <div class="result-title">
            💵 Tiền lãi định kỳ
        </div>

        <div class="result-value">
            {lai_text}
        </div>

        <div class="result-note">
            {note}
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown(f"""
    <div class="result-card">

        <div class="result-title">
            📈 Tổng tiền lãi
        </div>

        <div class="result-value">
            {dinh_dang_tien(tong_tien_lai)}
        </div>

        <div class="result-note">
            Tiền lãi sau {ky_han} tháng
        </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown(f"""
    <div class="result-card">

        <div class="result-title">
            💰 Tổng gốc + lãi
        </div>

        <div class="result-value">
            {dinh_dang_tien(tong_tien)}
        </div>

        <div class="result-note">
            Số tiền nhận được cuối kỳ
        </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# THÔNG TIN KHOẢN GỬI
# =========================================================

st.markdown(
    '<div class="section-title">📋 Thông tin khoản gửi</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="detail-label">Số tiền gốc</div>
        <div class="detail-value">{dinh_dang_tien(tien_gui)}</div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="detail-label">Kỳ hạn</div>
        <div class="detail-value">{ky_han} tháng</div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="detail-label">Lãi suất</div>
        <div class="detail-value">{lai_suat:.2f}%/năm</div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="detail-label">Cách tính</div>
        <div class="detail-value">{hinh_thuc_gui}</div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BIỂU ĐỒ LÃI TÍCH LŨY
# =========================================================

st.markdown(
    '<div class="section-title">📈 Lãi tích lũy theo thời gian</div>',
    unsafe_allow_html=True
)

# Tạo dữ liệu từng tháng
du_lieu = []

for thang in range(0, ky_han + 1):

    if hinh_thuc_gui == "Lãi đơn":

        tien_lai = tien_gui * r * (thang / 12)

    else:

        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

            tien_lai = tien_gui * (
                (1 + r / 12) ** thang - 1
            )

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

            so_quy = thang / 3

            tien_lai = tien_gui * (
                (1 + r / 4) ** so_quy - 1
            )

        else:

            tien_lai = tien_gui * r * (thang / 12)

    du_lieu.append({
        "Tháng": thang,
        "Tiền lãi tích lũy": tien_lai
    })


df = pd.DataFrame(du_lieu)

df_chart = df.set_index("Tháng")

st.line_chart(
    df_chart,
    height=420,
    use_container_width=True
)

st.markdown("""
<div class="note-box">
    <b>💡 Cách đọc biểu đồ:</b>
    Đường càng dốc lên nhanh thì tiền lãi tích lũy càng tăng nhanh.
    Với lãi kép, tốc độ tăng sẽ rõ hơn khi thời gian gửi dài hơn.
</div>
""", unsafe_allow_html=True)


# =========================================================
# BẢNG CHI TIẾT THEO TỪNG THÁNG
# =========================================================

st.markdown(
    '<div class="section-title">📑 Bảng chi tiết theo từng tháng</div>',
    unsafe_allow_html=True
)

bang_chi_tiet = []

for thang in range(0, ky_han + 1):

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

            lai_tich_luy = tien_gui * r * (thang / 12)

    tong_goc_lai = tien_gui + lai_tich_luy

    bang_chi_tiet.append({
        "Tháng": thang,
        "Lãi": dinh_dang_tien(lai_tich_luy),
        "Tổng gốc + lãi": dinh_dang_tien(tong_goc_lai)
    })


df_bang = pd.DataFrame(bang_chi_tiet)

st.dataframe(
    df_bang,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# TÓM TẮT
# =========================================================

st.markdown(
    '<div class="section-title">📝 Tóm tắt khoản gửi</div>',
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="info-card">

    <div style="
        color:#cbd5e1;
        font-size:16px;
        line-height:2;
    ">

        Bạn gửi
        <b style="color:#f8fafc;">
            {dinh_dang_tien(tien_gui)}
        </b>

        trong

        <b style="color:#f8fafc;">
            {ky_han} tháng
        </b>

        với lãi suất

        <b style="color:#f8fafc;">
            {lai_suat:.2f}%/năm
        </b>.

        <br>

        Cách tính:
        <b style="color:#f8fafc;">
            {hinh_thuc_gui}
        </b>

        ·

        {hinh_thuc_nhan_lai}.

        <br>

        Tổng tiền lãi:

        <b style="color:#f8fafc;">
            {dinh_dang_tien(tong_tien_lai)}
        </b>

        <br>

        Tổng số tiền nhận được:

        <b style="color:#f8fafc;">
            {dinh_dang_tien(tong_tien)}
        </b>

    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# GIẢI THÍCH NGẮN
# =========================================================

if hinh_thuc_gui == "Lãi đơn":

    st.markdown("""
    <div class="note-box" style="margin-top:20px;">
        <b>ℹ️ Lãi đơn:</b>
        Tiền lãi được tính dựa trên số tiền gốc ban đầu.
        Phần lãi không được cộng vào vốn để tiếp tục sinh lãi.
    </div>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div class="note-box" style="margin-top:20px;">
        <b>ℹ️ Lãi kép:</b>
        Tiền lãi được cộng vào vốn,
        sau đó tiếp tục sinh ra tiền lãi ở các kỳ tiếp theo.
        Vì vậy, gửi càng lâu thì sự chênh lệch với lãi đơn càng rõ.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    Smart Savings Calculator · Công cụ hỗ trợ tính toán tiền gửi tiết kiệm
</div>
""", unsafe_allow_html=True)
