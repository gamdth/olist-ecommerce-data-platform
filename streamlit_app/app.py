import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# ==========================================
# 1. Cấu hình trang & Giao diện
# ==========================================
st.set_page_config(
    page_title="Olist E-commerce Data Platform",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stMetricValue"] { font-size: 30px; color: #1E3A8A; font-weight: 700; }
    [data-testid="stMetric"] {
        padding: 15px; background-color: #F8FAFC; 
        border-radius: 10px; border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Tạo dữ liệu mô phỏng (Mock Data cho Olist)
# ==========================================
# Dữ liệu Phương thức thanh toán (Biểu đồ tròn)
@st.cache_data
def get_payment_data():
    return pd.DataFrame({
        "Phương thức": ["Credit Card", "Boleto", "Voucher", "Debit Card"],
        "Giá trị (R$)": [12540000, 2860000, 950000, 480000]
    })

# Dữ liệu Top 10 danh mục doanh thu cao
@st.cache_data
def get_top_categories():
    return pd.DataFrame({
        "Hạng": range(1, 11),
        "Danh mục sản phẩm": [
            "Beleza_saude (Sức khỏe & Sắc đẹp)", "Relogios_presentes (Đồng hồ & Quà tặng)",
            "Cama_mesa_banho (Chăn ga gối đệm)", "Esporte_lazer (Thể thao & Giải trí)",
            "Informatica_acessorios (Phụ kiện máy tính)", "Moveis_decoracao (Nội thất)",
            "Utilidades_domesticas (Đồ gia dụng)", "Ferramentas_jardim (Dụng cụ làm vườn)",
            "Automotivo (Ô tô/Xe máy)", "Brinquedos (Đồ chơi)"
        ],
        "Doanh thu (R$)": [1250000, 1120000, 1050000, 980000, 910000, 840000, 720000, 650000, 590000, 520000],
        "Số đơn hàng": [10500, 8400, 11200, 7800, 6900, 7200, 6100, 4500, 3900, 4100]
    })

# Dữ liệu tọa độ vận chuyển tại Brazil (Bản đồ nhiệt)
@st.cache_data
def get_delivery_gps():
    # Giới hạn tọa độ chủ yếu quanh các bang lớn của Brazil: São Paulo, Rio de Janeiro, Minas Gerais
    df = pd.DataFrame({
        'lat': np.random.normal(-23.55, 2.5, size=1500),
        'lon': np.random.normal(-46.63, 2.5, size=1500)
    })
    return df

# ==========================================
# 3. Thiết kế thanh Sidebar
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#1E3A8A; margin-bottom: 5px;'>Olist Data Platform</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size: 14px; margin-top:0;'>Menu Điều Hướng Hệ Thống</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🔍 Chọn khu vực phân tích:")
    selected_tab = st.selectbox(
        "Khu vực chính:",
        ["📈 Tổng quan kinh doanh", "🚚 Quản lý vận chuyển", "⭐ Phân tích phản hồi"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    with st.expander("ℹ️ Thông tin dự án"):
        st.markdown("**Dự án:** Olist Platform\n\n**Năm:** 2026")

# ==========================================
# 4. Phân luồng hiển thị nội dung
# ==========================================
if selected_tab == "📈 Tổng quan kinh doanh":
    st.markdown("<h1 style='color:#1E3A8A;'>📈 Phân Tích Tổng Quan Kinh Doanh</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Số liệu KPIs nhanh
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng Doanh Thu", "R$ 16.83M", "+5.2%")
    col2.metric("Tổng Đơn Hàng", "99.4K đơn", "+12.8%")
    col3.metric("Giá Trị Đơn Trung Bình", "R$ 169.3", "+2.1%")
    col4.metric("Thời Gian Giao Khách", "12.5 ngày", "-1.4 ngày")
    
    st.markdown("---")
    
    # Chia bố cục 2 cột cho Biểu đồ tròn và Bảng Top 10
    left_col, right_col = st.columns([4, 6]) # Cột phải rộng hơn để hiện bảng dữ liệu
    
    with left_col:
        st.markdown("#### 💳 Tỷ Lệ Phương Thức Thanh Toán")
        df_pay = get_payment_data()
        # Biểu đồ tròn trực quan bằng Plotly
        fig_pie = px.pie(
            df_pay, values='Giá trị (R$)', names='Phương thức',
            color_discrete_sequence=px.colors.sequential.RdBu,
            hole=0.4 # Tạo biểu đồ Donut cho hiện đại
        )
        fig_pie.update_layout(margin=dict(t=20, b=20, l=0, r=0), height=350)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with right_col:
        st.markdown("#### 🏆 Top 10 Danh Mục Doanh Thu Cao Nhất")
        df_cat = get_top_categories()
        
        # Hiển thị bảng dữ liệu được format đẹp mắt
        st.dataframe(
            df_cat.set_index("Hạng"),
            column_config={
                "Doanh thu (R$)": st.column_config.NumberColumn(format="R$ %d"),
                "Số đơn hàng": st.column_config.NumberColumn(format="%d")
            },
            use_container_width=True,
            height=380
        )



elif selected_tab == "🚚 Quản lý vận chuyển":
    st.markdown("<h1 style='color:#1E3A8A;'>🚚 Quản Lý & Phân Tích Vận Chuyển</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("#### 🗺️ Bản Đồ Nhiệt Mật Độ Giao Hàng (Mô phỏng Brazil khu vực Đông Nam)")
    st.markdown("*Khu vực tập trung mật độ đơn hàng cao nhất tại các bang như SP, RJ, MG.*")
    
    # Lấy dữ liệu tọa độ địa lý
    df_gps = get_delivery_gps()
    
    # Hiển thị Bản đồ nhiệt (Map) tích hợp sẵn của Streamlit
    st.map(df_gps, zoom=4, use_container_width=True)

elif selected_tab == "⭐ Phân tích phản hồi":
    st.markdown("<h1 style='color:#1E3A8A;'>⭐ Đánh Giá & Phản Hồi Từ Khách Hàng</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("Khu vực tích hợp AI Prompts đang chờ cấu hình khóa API...")

