import pandas as pd
import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Phân Tích & Biểu Diễn Lãi Tiết Kiệm",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Biểu Diễn & Phân Tích Chi Tiết Tiền Lãi Tiết Kiệm")
st.write(
    "Ứng dụng tập trung trực quan hóa dòng tiền lãi, hiệu suất sinh lời và"
    " sự tăng trưởng của lãi."
)


# =========================
# HÀM HỖ TRỢ
# =========================
def dinh_dang_tien(so_tien):
  return f"{so_tien:,.0f} VNĐ"


# =========================
# SIDEBAR - NHẬP THÔNG TIN
# =========================
st.sidebar.header("📌 Thông tin khoản gửi")

tien_gui = st.sidebar.number_input(
    "Số tiền gửi gốc (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=10_000_000.0,
    format="%.0f",
)

ky_han = st.sidebar.number_input(
    "Kỳ hạn gửi (tháng)", min_value=1, value=12, step=1
)

lai_suat = st.sidebar.number_input(
    "Lãi suất (%/năm)", min_value=0.0, value=6.5, step=0.1
)

hinh_thuc_gui = st.sidebar.selectbox(
    "Hình thức tính lãi", ["Lãi đơn", "Lãi kép"]
)

if hinh_thuc_gui == "Lãi kép":
  hinh_thuc_nhan_lai = st.sidebar.selectbox(
      "Kỳ hạn nhập gốc (Tái đầu tư lãi)",
      ["Nhập gốc hàng tháng", "Nhập gốc hàng quý", "Nhập gốc cuối kỳ"],
  )
else:
  hinh_thuc_nhan_lai = st.sidebar.selectbox(
      "Hình thức nhận lãi",
      ["Lãnh lãi hàng tháng", "Lãnh lãi hàng quý", "Lãnh lãi cuối kỳ"],
  )

# =========================
# XỬ LÝ TÍNH TOÁN
# =========================
if st.sidebar.button("🧮 Phân Tích Tiền Lãi", use_container_width=True):
  if tien_gui <= 0:
    st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
  else:
    r = lai_suat / 100
    so_nam = ky_han / 12

    # 1. Tính toán Lãi đơn
    lai_don_tong_lai = tien_gui * r * so_nam
    lai_don_tong_tien = tien_gui + lai_don_tong_lai

    # 2. Tính toán Lãi kép
    if (
        hinh_thuc_nhan_lai == "Nhập gốc hàng tháng"
        or hinh_thuc_nhan_lai == "Lãnh lãi hàng tháng"
    ):
      n = 12
    elif (
        hinh_thuc_nhan_lai == "Nhập gốc hàng quý"
        or hinh_thuc_nhan_lai == "Lãnh lãi hàng quý"
    ):
      n = 4
    else:
      n = 1 / so_nam

    if hinh_thuc_gui == "Lãi kép" and hinh_thuc_nhan_lai != "Nhập gốc cuối kỳ":
      lai_kep_tong_tien = tien_gui * ((1 + r / n) ** (n * so_nam))
    else:
      lai_kep_tong_tien = tien_gui * ((1 + r) ** so_nam)

    lai_kep_tong_lai = lai_kep_tong_tien - tien_gui

    # Chọn số liệu hiển thị chính
    if hinh_thuc_gui == "Lãi đơn":
      tong_tien_lai = lai_don_tong_lai
      tong_tien = lai_don_tong_tien
    else:
      tong_tien_lai = lai_kep_tong_lai
      tong_tien = lai_kep_tong_tien

    hieu_suat_sinh_loi = (tong_tien_lai / tien_gui) * 100
    lai_trung_binh_thang = tong_tien_lai / ky_han

    st.success("✅ Phân tích tiền lãi thành công!")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
      st.metric("Tổng tiền lãi nhận được", dinh_dang_tien(tong_tien_lai))
    with c2:
      st.metric("Lãi trung bình / tháng", dinh_dang_tien(lai_trung_binh_thang))
    with c3:
      st.metric("Tỷ lệ sinh lời (ROI)", f"{hieu_suat_sinh_loi:.2f}%")
    with c4:
      st.metric("Tổng tiền nhận về (Gốc + Lãi)", dinh_dang_tien(tong_tien))

    st.divider()

    # DỮ LIỆU BẢNG LÃI THEO THÁNG
    lich_trinh = []
    goc_don = tien_gui
    goc_kep = tien_gui
    lai_thang_don = (tien_gui * r) / 12

    for m in range(1, ky_han + 1):
      lai_don_trong_thang = lai_thang_don
      lai_don_tich_luy = lai_don_trong_thang * m

      if hinh_thuc_nhan_lai == "Nhập gốc hàng tháng":
        lai_kep_trong_thang = goc_kep * (r / 12)
        goc_kep += lai_kep_trong_thang
        lai_kep_tich_luy = goc_kep - tien_gui
      elif hinh_thuc_nhan_lai == "Nhập gốc hàng quý":
        if m % 3 == 0:
          lai_kep_trong_thang = goc_kep * (r / 4)
          goc_kep += lai_kep_trong_thang
        else:
          lai_kep_trong_thang = 0
        lai_kep_tich_luy = goc_kep - tien_gui
      else:
        lai_kep_trong_thang = 0
        lai_kep_tich_luy = (
            tien_gui * ((1 + r) ** (m / 12)) - tien_gui
            if m == ky_han
            else 0
        )

      lich_trinh.append({
          "Tháng": m,
          "Lãi tích lũy (Lãi đơn)": lai_don_tich_luy,
          "Lãi tích lũy (Lãi kép)": lai_kep_tich_luy,
          "Lãi phát sinh tháng đó": (
              lai_kep_trong_thang
              if hinh_thuc_gui == "Lãi kép"
              else lai_don_trong_thang
          ),
      })

    df = pd.DataFrame(lich_trinh)

    tab1, tab2, tab3 = st.tabs([
        "📊 Biểu đồ tích lũy lãi",
        "📊 Cơ cấu Gốc vs Lãi",
        "📋 Bảng chi tiết tiền lãi từng tháng",
    ])

    with tab1:
      st.subheader("Sự tăng trưởng của TIỀN LÃI qua các tháng")
      if hinh_thuc_gui == "Lãi kép":
        st.line_chart(
            df.set_index("Tháng")[
                ["Lãi tích lũy (Lãi đơn)", "Lãi tích lũy (Lãi kép)"]
            ]
        )
        chenh_lech_lai = lai_kep_tong_lai - lai_don_tong_lai
        st.info(
            f"💡 **Chênh lệch:** Nhờ sức mạnh lãi kép, tiền lãi tăng thêm"
            f" **{dinh_dang_tien(chenh_lech_lai)}** so với lãi đơn!"
        )
      else:
        st.line_chart(df.set_index("Tháng")[["Lãi tích lũy (Lãi đơn)"]])

    with tab2:
      st.subheader("Cơ cấu Tổng số tiền nhận về")
      col_chart1, col_chart2 = st.columns([2, 1])

      with col_chart1:
        df_bar = pd.DataFrame(
            {"Số tiền (VNĐ)": [tien_gui, tong_tien_lai]},
            index=["Tiền Gốc Ban Đầu", "Tiền Lãi Sinh Ra"],
        )
        st.bar_chart(df_bar)

      with col_chart2:
        st.write("### Tóm tắt cơ cấu:")
        st.write(f"- **Tiền gốc:** {dinh_dang_tien(tien_gui)}")
        st.write(f"- **Tiền lãi:** {dinh_dang_tien(tong_tien_lai)}")
        st.write(
            f"- **Tỷ lệ lãi/gốc:** {tong_tien_lai / tien_gui * 100:.2f}%"
        )

    with tab3:
      st.subheader("Bảng thống kê tiền lãi phát sinh")
      df_display = df.copy()
      df_display["Lãi tích lũy (Lãi đơn)"] = df_display[
          "Lãi tích lũy (Lãi đơn)"
      ].apply(dinh_dang_tien)
      df_display["Lãi tích lũy (Lãi kép)"] = df_display[
          "Lãi tích lũy (Lãi kép)"
      ].apply(dinh_dang_tien)
      df_display["Lãi phát sinh tháng đó"] = df_display[
          "Lãi phát sinh tháng đó"
      ].apply(dinh_dang_tien)

      st.dataframe(df_display, use_container_width=True)
