import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sổ tiết kiệm", page_icon="🪙", layout="wide")

# ---------- GIAO DIỆN ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }
.hero { padding: 1.4rem 1.6rem; border-radius: 18px; color: #fff;
  background: linear-gradient(120deg, #0f766e, #134e4a 60%, #1e293b); margin-bottom: 1rem; }
.hero h1 { margin: 0; font-size: 1.9rem; font-weight: 800; }
.hero p { margin: .3rem 0 0; opacity: .85; }
div[data-testid="stMetric"] { background: rgba(15,118,110,.08); border: 1px solid rgba(15,118,110,.25);
  border-radius: 14px; padding: .8rem 1rem; }
.best { padding: .7rem 1rem; border-left: 4px solid #0f766e; background: rgba(15,118,110,.08);
  border-radius: 8px; margin: .5rem 0; }
</style>
<div class="hero"><h1>🪙 Sổ tiết kiệm</h1>
<p>Tính lãi, so sánh kịch bản, lập kế hoạch gửi góp và đặt mục tiêu tài chính.</p></div>
""",
    unsafe_allow_html=True,
)

# ---------- HÀM DÙNG CHUNG ----------
# (chu kỳ tháng, nhập lãi vào gốc?) ; chu kỳ None = theo kỳ hạn
CHE_DO = {
    "Lĩnh lãi cuối kỳ": (None, False),
    "Lĩnh lãi hàng tháng": (1, False),
    "Lĩnh lãi hàng quý": (3, False),
    "Nhập lãi vào gốc hàng tháng": (1, True),
    "Nhập lãi vào gốc hàng quý": (3, True),
}


def tien(x):
    return f"{x:,.0f} đ"


def doc_tien(x):
    if x >= 1e9:
        return f"≈ {x / 1e9:,.2f} tỷ"
    if x >= 1e6:
        return f"≈ {x / 1e6:,.1f} triệu"
    return f"≈ {x:,.0f} đồng"


def mo_phong(goc, lai_suat, thang, che_do):
    """Mô phỏng từng tháng. Trả về DataFrame."""
    r = lai_suat / 100 / 12
    chu_ky, nhap_goc = CHE_DO[che_do]
    chu_ky = chu_ky or thang
    base, cho, da_nhan, rows = goc, 0.0, 0.0, []
    for t in range(1, thang + 1):
        lai = base * r
        cho += lai
        if t % chu_ky == 0 or t == thang:
            if nhap_goc:
                base += cho
            else:
                da_nhan += cho
            cho = 0.0
        rows.append({
            "Tháng": t,
            "Lãi phát sinh": lai,
            "Lãi tích lũy": base - goc + da_nhan + cho,
            "Tổng tài sản": base + da_nhan + cho,
        })
    return pd.DataFrame(rows)


def loi_suat_nam(tong, goc, thang):
    return (tong / goc) ** (12 / thang) - 1 if goc > 0 and thang > 0 else 0


def bieu_do_cot(df, goc_col, lai_col, goc_ten="Vốn gốc", lai_ten="Tiền lãi"):
    d = pd.DataFrame({"Tháng": df["Tháng"], goc_ten: df[goc_col], lai_ten: df[lai_col]})
    d = d.melt("Tháng", var_name="Loại", value_name="Số tiền")
    return (
        alt.Chart(d)
        .mark_area(opacity=0.85)
        .encode(
            x=alt.X("Tháng:Q"),
            y=alt.Y("Số tiền:Q", stack=True, title=None),
            color=alt.Color("Loại:N", scale=alt.Scale(range=["#94a3b8", "#0f766e"]),
                            legend=alt.Legend(orient="top", title=None)),
            tooltip=["Tháng", "Loại", alt.Tooltip("Số tiền:Q", format=",.0f")],
        )
        .properties(height=320)
    )


CFG = {
    "Lãi phát sinh": st.column_config.NumberColumn(format="%.0f"),
    "Lãi tích lũy": st.column_config.NumberColumn(format="%.0f"),
    "Tổng tài sản": st.column_config.NumberColumn(format="%.0f"),
}

# ---------- THANH BÊN ----------
with st.sidebar:
    st.header("⚙️ Cài đặt chung")
    lam_phat = st.slider("Lạm phát dự kiến (%/năm)", 0.0, 15.0, 3.5, 0.1,
                         help="Dùng để tính lãi suất thực và sức mua của tiền.")
    st.caption("Lãi suất tính theo năm, chia đều 12 tháng. "
               "Thực tế ngân hàng có thể tính theo số ngày (365), nên kết quả mang tính tham khảo.")

tab1, tab2, tab3, tab4 = st.tabs(
    ["💰 Tính lãi", "⚖️ So sánh", "📅 Gửi góp hàng tháng", "🎯 Mục tiêu"]
)

# =====================================================
# TAB 1 - TÍNH LÃI
# =====================================================
with tab1:
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        goc = st.number_input("Số tiền gửi (VNĐ)", 1_000_000.0, value=100_000_000.0,
                              step=1_000_000.0, format="%.0f", key="t1_goc")
        st.caption(doc_tien(goc))
        thang = st.slider("Kỳ hạn (tháng)", 1, 120, 12, key="t1_thang")
        ls = st.number_input("Lãi suất (%/năm)", 0.0, 30.0, 5.5, 0.1, format="%.2f", key="t1_ls")
        che_do = st.selectbox("Hình thức nhận lãi", list(CHE_DO), key="t1_cd")

    df = mo_phong(goc, ls, thang, che_do)
    tong = df["Tổng tài sản"].iloc[-1]
    lai_tong = tong - goc
    chu_ky, nhap_goc = CHE_DO[che_do]
    ls_nam = loi_suat_nam(tong, goc, thang)
    ls_thuc = (1 + ls_nam) / (1 + lam_phat / 100) - 1
    gia_tri_thuc = tong / (1 + lam_phat / 100) ** (thang / 12)

    with c2:
        m1, m2, m3 = st.columns(3)
        if nhap_goc:
            m1.metric("Lãi nhập gốc", "Tự động")
        else:
            ck = chu_ky or thang
            m1.metric(f"Lãi nhận mỗi {'kỳ' if ck == thang else ('tháng' if ck == 1 else 'quý')}",
                      tien(goc * ls / 100 / 12 * ck))
        m2.metric("Tổng tiền lãi", tien(lai_tong))
        m3.metric("Tổng gốc + lãi", tien(tong))

        m4, m5, m6 = st.columns(3)
        m4.metric("Lợi suất hiệu dụng/năm", f"{ls_nam * 100:.2f}%")
        m5.metric("Lãi suất thực (sau lạm phát)", f"{ls_thuc * 100:.2f}%",
                  delta="Mất giá" if ls_thuc < 0 else "Có lời", delta_color="normal" if ls_thuc >= 0 else "inverse")
        m6.metric("Sức mua cuối kỳ (giá hôm nay)", tien(gia_tri_thuc))

        if ls_thuc < 0:
            st.warning(f"Với lạm phát {lam_phat:.1f}%/năm, tiền của bạn đang **mất giá thực tế**. "
                       "Hãy cân nhắc kênh có lãi suất cao hơn hoặc kỳ hạn dài hơn.")
        else:
            st.success(f"Sau lạm phát, bạn vẫn có lời khoảng **{ls_thuc * 100:.2f}%/năm**.")

    st.altair_chart(bieu_do_cot(df.assign(Gốc=goc), "Gốc", "Lãi tích lũy"),
                    use_container_width=True)

    with st.expander("📑 Bảng chi tiết từng tháng"):
        st.dataframe(df, column_config=CFG, hide_index=True, use_container_width=True)
    st.download_button("⬇️ Tải bảng chi tiết (CSV)", df.to_csv(index=False).encode("utf-8-sig"),
                       "chi_tiet_lai_tiet_kiem.csv", "text/csv")

# =====================================================
# TAB 2 - SO SÁNH
# =====================================================
with tab2:
    st.write("So sánh tối đa 3 gói tiết kiệm với cùng số tiền gửi.")
    goc2 = st.number_input("Số tiền gửi (VNĐ)", 1_000_000.0, value=100_000_000.0,
                           step=1_000_000.0, format="%.0f", key="t2_goc")
    mac_dinh = [("Gói A", 5.0, 6), ("Gói B", 5.8, 12), ("Gói C", 6.2, 24)]
    cols = st.columns(3)
    kich_ban = []
    for i, col in enumerate(cols):
        with col:
            ten = st.text_input("Tên", mac_dinh[i][0], key=f"t2_ten{i}")
            l = st.number_input("Lãi suất (%/năm)", 0.0, 30.0, mac_dinh[i][1], 0.1, key=f"t2_ls{i}")
            k = st.number_input("Kỳ hạn (tháng)", 1, 120, mac_dinh[i][2], key=f"t2_k{i}")
            cd = st.selectbox("Nhận lãi", list(CHE_DO), index=0, key=f"t2_cd{i}")
            kich_ban.append((ten, l, k, cd))

    rows = []
    for ten, l, k, cd in kich_ban:
        d = mo_phong(goc2, l, k, cd)
        t = d["Tổng tài sản"].iloc[-1]
        rows.append({"Gói": ten, "Kỳ hạn (tháng)": k, "Tổng lãi": t - goc2, "Tổng nhận": t,
                     "Lợi suất hiệu dụng/năm (%)": loi_suat_nam(t, goc2, k) * 100})
    kq = pd.DataFrame(rows)
    tot = kq.loc[kq["Lợi suất hiệu dụng/năm (%)"].idxmax()]
    st.markdown(f"<div class='best'>🏆 <b>{tot['Gói']}</b> có lợi suất hiệu dụng cao nhất: "
                f"<b>{tot['Lợi suất hiệu dụng/năm (%)']:.2f}%/năm</b>. "
                "Lưu ý: kỳ hạn dài hơn cho nhiều tiền lãi hơn nhưng khóa tiền lâu hơn.</div>",
                unsafe_allow_html=True)
    st.dataframe(kq, hide_index=True, use_container_width=True, column_config={
        "Tổng lãi": st.column_config.NumberColumn(format="%.0f"),
        "Tổng nhận": st.column_config.NumberColumn(format="%.0f"),
        "Lợi suất hiệu dụng/năm (%)": st.column_config.NumberColumn(format="%.2f"),
    })
    st.altair_chart(
        alt.Chart(kq).mark_bar(color="#0f766e", cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(x=alt.X("Gói:N", sort=None, title=None),
                y=alt.Y("Lợi suất hiệu dụng/năm (%):Q", title="% / năm"),
                tooltip=list(kq.columns)).properties(height=260),
        use_container_width=True)

# =====================================================
# TAB 3 - GỬI GÓP HÀNG THÁNG
# =====================================================
with tab3:
    a, b = st.columns([1, 2], gap="large")
    with a:
        von_dau = st.number_input("Vốn ban đầu (VNĐ)", 0.0, value=0.0, step=1_000_000.0,
                                  format="%.0f", key="t3_dau")
        gop = st.number_input("Gửi thêm mỗi tháng (VNĐ)", 0.0, value=5_000_000.0,
                              step=500_000.0, format="%.0f", key="t3_gop")
        st.caption(doc_tien(gop) + " / tháng")
        n3 = st.slider("Thời gian (tháng)", 1, 360, 60, key="t3_n")
        ls3 = st.number_input("Lãi suất (%/năm)", 0.0, 30.0, 6.0, 0.1, key="t3_ls")
        tang = st.number_input("Mỗi năm tăng tiền gửi thêm (%)", 0.0, 50.0, 0.0, 1.0,
                               help="Ví dụ lương tăng 10%/năm thì bạn gửi nhiều hơn 10%/năm.")

    so_du, da_gop, rows = von_dau, von_dau, []
    for t in range(1, n3 + 1):
        g = gop * (1 + tang / 100) ** ((t - 1) // 12)
        so_du = (so_du + g) * (1 + ls3 / 100 / 12)  # gửi đầu tháng, lãi nhập gốc hàng tháng
        da_gop += g
        rows.append({"Tháng": t, "Tổng đã gửi": da_gop, "Tiền lãi": so_du - da_gop, "Tổng tài sản": so_du})
    d3 = pd.DataFrame(rows)
    with b:
        x1, x2, x3 = st.columns(3)
        x1.metric("Tổng đã gửi", tien(da_gop))
        x2.metric("Tiền lãi", tien(so_du - da_gop))
        x3.metric("Tổng tài sản", tien(so_du))
        st.caption(f"Sức mua thực (giá hôm nay, lạm phát {lam_phat:.1f}%): "
                   f"**{tien(so_du / (1 + lam_phat / 100) ** (n3 / 12))}**")
        st.altair_chart(bieu_do_cot(d3, "Tổng đã gửi", "Tiền lãi", "Tiền bạn gửi", "Tiền lãi sinh ra"),
                        use_container_width=True)
    with st.expander("📑 Bảng chi tiết"):
        st.dataframe(d3, hide_index=True, use_container_width=True, column_config={
            c: st.column_config.NumberColumn(format="%.0f") for c in d3.columns[1:]})

# =====================================================
# TAB 4 - MỤC TIÊU
# =====================================================
with tab4:
    p, q = st.columns([1, 2], gap="large")
    with p:
        muc_tieu = st.number_input("Số tiền muốn có (VNĐ)", 1_000_000.0, value=500_000_000.0,
                                   step=10_000_000.0, format="%.0f", key="t4_mt")
        st.caption(doc_tien(muc_tieu))
        co_san = st.number_input("Số tiền đã có (VNĐ)", 0.0, value=50_000_000.0,
                                 step=1_000_000.0, format="%.0f", key="t4_cs")
        n4 = st.slider("Thời hạn (tháng)", 1, 360, 60, key="t4_n")
        ls4 = st.number_input("Lãi suất kỳ vọng (%/năm)", 0.0, 30.0, 6.0, 0.1, key="t4_ls")

    def can_gop(rate_nam):
        i = rate_nam / 100 / 12
        if i == 0:
            return max(muc_tieu - co_san, 0) / n4
        f = (1 + i) ** n4
        return max((muc_tieu - co_san * f) * i / ((f - 1) * (1 + i)), 0)

    with q:
        m = can_gop(ls4)
        if co_san * (1 + ls4 / 100 / 12) ** n4 >= muc_tieu:
            st.success("🎉 Chỉ cần giữ số tiền đang có, bạn đã đạt mục tiêu trong thời hạn này.")
        else:
            st.metric("Cần gửi mỗi tháng", tien(m))
            st.caption(f"Tổng bạn bỏ ra: {tien(co_san + m * n4)} · Lãi sinh ra: "
                       f"{tien(muc_tieu - co_san - m * n4)}")
        st.write("**Nếu lãi suất thay đổi thì sao?**")
        bang = pd.DataFrame({
            "Lãi suất (%/năm)": [max(ls4 - 2, 0), ls4, ls4 + 2],
            "Cần gửi mỗi tháng": [can_gop(max(ls4 - 2, 0)), can_gop(ls4), can_gop(ls4 + 2)],
        })
        st.dataframe(bang, hide_index=True, use_container_width=True, column_config={
            "Lãi suất (%/năm)": st.column_config.NumberColumn(format="%.1f"),
            "Cần gửi mỗi tháng": st.column_config.NumberColumn(format="%.0f")})
        st.info(f"Mục tiêu {tien(muc_tieu)} sau {n4} tháng, tính theo giá hôm nay tương đương "
                f"khoảng **{tien(muc_tieu / (1 + lam_phat / 100) ** (n4 / 12))}** (do lạm phát).")
