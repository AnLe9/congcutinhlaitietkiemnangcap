import io
import pandas as pd
import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm & So Sánh Nâng Cấp",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Ứng dụng Tính Lãi Tiết Kiệm & Tối Ưu Đầu Tư")
st.write(
    "Hỗ trợ tính toán lãi đơn, lãi kép, so sánh hiệu quả và dự báo lạm phát."
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
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=10_000_000.0,
    format="%.0f",
)

ky_han = st.sidebar.number_input(
    "Kỳ hạn (tháng)", min_value=1, value=12, step=1
)

lai_suat = st.sidebar.number_input(
    "Lãi suất (%/năm)", min_value=0.0, value=6.0, step=0.1
)

hinh_thuc_gui = st.sidebar.selectbox(
    "Hình thức tính lãi", ["Lãi đơn", "Lãi kép"]
)

if hinh_thuc_gui == "Lãi kép":
  hinh_thuc_nhan_lai = st.sidebar.selectbox(
      "Kỳ hạn nhập gốc (tái đầu tư)",
      ["Nhập gốc hàng tháng", "Nhập gốc hàng quý", "Nhập gốc cuối kỳ"],
  )
else:
  hinh_thuc_nhan_lai = st.sidebar.selectbox(
      "Hình thức nhận lãi",
      ["Lãnh lãi hàng tháng", "Lãnh lãi hàng quý", "Lãnh lãi cuối kỳ"],
  )

st.sidebar.subheader("📉 Tùy chọn nâng cao")
lam_phat = st.sidebar.number_input(
    "Dự báo lạm phát hàng năm (%)", min_value=0.0, value=3.5, step=0.1
)

# =========================
# XỬ LÝ TÍNH TOÁN
# =========================
if st.sidebar.button("🧮 Tính Toán", use_container_width=True):
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

    # Chọn kết quả hiển thị chính theo lựa chọn của người dùng
    if hinh_thuc_gui == "Lãi đơn":
      tong_tien_lai = lai_don_tong_lai
      tong_tien = lai_don_tong_tien
    else:
      tong_tien_lai = lai_kep_tong_lai
      tong_tien = lai_kep_tong_tien

    # Tính tiền thực nhận sau lạm phát
    i = lam_phat / 100
    tong_tien_thuc_te = tong_tien / ((1 + i) ** so_nam)

    # Hiển thị Kết quả Tổng quan
    st.success("✅ Tính toán thành công!")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric("Tổng tiền lãi", dinh_dang_tien(tong_tien_lai))
    with col2:
      st.metric("Tổng gốc + lãi", dinh_dang_tien(tong_tien))
    with col3:
      st.metric(
          "Giá trị sau lạm phát",
          dinh_dang_tien(tong_tien_thuc_te),
          delta=f"-{dinh_dang_tien(tong_tien - tong_tien_thuc_te)}",
          delta_color="inverse",
      )
    with col4:
      st.metric(
          "Lợi nhuận chênh lệch Lãi kép",
          dinh_dang_tien(lai_kep_tong_tien - lai_don_tong_tien),
      )

    st.divider()

    # Tạo bảng dữ liệu tăng trưởng theo từng tháng
    lich_trinh = []
    goc_lai_don = tien_gui
    goc_lai_kep = tien_gui

    lai_thang_don = (tien_gui * r) / 12
    lai_thang_kep_rate = r / 12

    for m in range(1, ky_han + 1):
      # Lãi đơn
      lai_don_thang = lai_thang_don
      goc_lai_don += lai_don_thang

      # Lãi kép
      if hinh_thuc_gui == "Lãi kép":
        if hinh_thuc_nhan_lai == "Nhập gốc hàng tháng":
          lai_kep_thang = goc_lai_kep * lai_thang_kep_rate
          goc_lai_kep += lai_kep_thang
        elif hinh_thuc_nhan_lai == "Nhập gốc hàng quý" and m % 3 == 0:
          lai_kep_thang = goc_lai_kep * (r / 4)
          goc_lai_kep += lai_kep_thang
        else:
          lai_kep_thang = 0
      else:
        lai_kep_thang = 0

      lich_trinh.append({
          "Tháng": m,
          "Lãi đơn acumul": goc_lai_don,
          "Lãi kép acumul": goc_lai_kep if hinh_thuc_gui == "Lãi kép" else 0,
      })

    df = pd.DataFrame(lich_trinh)

    # TAB CHI TIẾT
    tab1, tab2 = st.tabs(
        ["📈 Biểu đồ & So sánh", "📋 Bảng lịch trình chi tiết"]
    )

    with tab1:
      st.write("### So sánh Tăng trưởng Tài sản qua Thời gian")
      if hinh_thuc_gui == "Lãi kép":
        st.line_chart(df.set_index("Tháng")[["Lãi đơn acumul", "Lãi kép acumul"]])
      else:
        st.line_chart(df.set_index("Tháng")[["Lãi đơn acumul"]])

      st.info(
          f"💡 **Mẹo:** Nếu gửi tiết kiệm theo dạng **Lãi kép**, bạn sẽ thu về"
          f" thêm **{dinh_dang_tien(lai_kep_tong_tien - lai_don_tong_tien)}**"
          " so với Lãi đơn."
      )

    with tab2:
      st.write("### Bảng Lịch trình Nhận Lãi")
      df_display = df.copy()
      df_display["Lãi đơn acumul"] = df_display["Lãi đơn acumul"].apply(
          dinh_dang_tien
      )
      if hinh_thuc_gui == "Lãi kép":
        df_display["Lãi kép acumul"] = df_display["Lãi kép acumul"].apply(
            dinh_dang_tien
        )
      else:
        df_display = df_display.drop(columns=["Lãi kép acumul"])

      st.dataframe(df_display, use_container_width=True)

      # Nút Tải dữ liệu CSV
      csv_data = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="📥 Tải Bảng Lịch Trình (CSV)",
          data=csv_data,
          file_name="lich_trinh_tiet_kiem.csv",
          mime="text/csv",
      )
