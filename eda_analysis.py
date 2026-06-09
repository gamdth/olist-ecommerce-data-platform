import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập giao diện biểu đồ cho đẹp và dễ nhìn
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

print("--- BẮT ĐẦU QUÁ TRÌNH EDA TOÀN DIỆN (OLIST DATASET) ---")

# =====================================================================
# 1. KHỞI TẠO DỮ LIỆU MÔ PHỎNG EDA CHUẨN CẤU TRÚC OLIST
# =====================================================================
np.random.seed(42)
n_samples = 1000

# Tạo DataFrame tổng hợp chứa các biến số để phân tích mối quan hệ đa biến
df_olist = pd.DataFrame({
    'price': np.random.lognormal(mean=4.3, sigma=0.8, size=n_samples), # Giá sản phẩm
    'freight_value': np.random.uniform(5, 40, size=n_samples),        # Phí vận chuyển
    'product_photos_qty': np.random.randint(1, 8, size=n_samples),    # Số lượng ảnh sản phẩm
    'review_score': np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.1, 0.05, 0.15, 0.3, 0.4]), # Điểm đánh giá
    'order_hour': np.concatenate([np.random.normal(12, 2, size=600), np.random.normal(19, 2, size=400)]) # Khung giờ mua
})

# Lọc bớt outliers cho giá sản phẩm giống thực tế (giới hạn từ R$10 đến R$600)
df_olist['price'] = np.clip(df_olist['price'], 10, 600)
df_olist['order_hour'] = np.clip(df_olist['order_hour'], 0, 23).astype(int)
# Giả lập khoảng cách địa lý dựa trên phí vận chuyển
df_olist['distance_km'] = (df_olist['freight_value'] * 45) + np.random.normal(0, 50, size=n_samples)
df_olist['distance_km'] = np.clip(df_olist['distance_km'], 10, 2000)

# =====================================================================
# 2. CÁC BIỂU ĐỒ TRỰC QUAN HÓA (EDA)
# =====================================================================

# --- BIỂU ĐỒ 1: PHÂN BỐ ĐƠN BIẾN (Histogram & KDE) ---
print("Đang vẽ Biểu đồ 1: Phân bố giá sản phẩm và phí vận chuyển...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.histplot(df_olist['price'], bins=40, kde=True, color='#1E3A8A', ax=axes[0])
axes[0].set_title('Phân Bố Giá Sản Phẩm (Price Distribution)')
axes[0].set_xlabel('Giá sản phẩm (R$)')
axes[0].set_ylabel('Tần suất (Số lượng)')

sns.histplot(df_olist['freight_value'], bins=30, kde=True, color='#3B82F6', ax=axes[1])
axes[1].set_title('Phân Bố Phí Vận Chuyển (Freight Value Distribution)')
axes[1].set_xlabel('Phí vận chuyển (R$)')
axes[1].set_ylabel('Tần suất (Số lượng)')

plt.tight_layout()
plt.savefig('eda_1_distribution.png', dpi=300)
plt.close()


# --- BIỂU ĐỒ 2: MỐI QUAN HỆ ĐA BIẾN (Scatter Plot với Đường Xu Hướng) ---
print("Đang vẽ Biểu đồ 2: Mối quan hệ giữa Khoảng cách địa lý và Phí vận chuyển...")
plt.figure(figsize=(10, 6))
sns.regplot(
    data=df_olist, x='distance_km', y='freight_value',
    scatter_kws={'alpha':0.5, 'color': '#1E3A8A'},
    line_kws={'color': '#EF4444', 'lw': 2}
)
plt.title('Mối Quan Hệ Giữa Khoảng Cách Địa Lý & Phí Vận Chuyển')
plt.xlabel('Khoảng cách giao hàng (km)')
plt.ylabel('Phí vận chuyển (R$)')
plt.savefig('eda_2_distance_vs_freight.png', dpi=300)
plt.close()


# --- BIỂU ĐỒ 3: PHÂN BỐ THEO NHÓM (Boxplot - Điểm Đánh Giá & Phí Vận Chuyển) ---
print("Đang vẽ Biểu đồ 3: Phân tích sự ảnh hưởng của Phí vận chuyển đến Điểm số đánh giá...")
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_olist, x='review_score', y='freight_value', palette='Blues')
plt.title('Phân Bố Phí Vận Chuyển Theo Từng Mức Điểm Đánh Giá (Review Score)')
plt.xlabel('Điểm số đánh giá từ khách hàng (1 - 5 sao)')
plt.ylabel('Phí vận chuyển (R$)')
plt.savefig('eda_3_review_vs_freight.png', dpi=300)
plt.close()


# --- BIỂU ĐỒ 4: MA TRẬN TƯƠNG QUAN (Correlation Heatmap) ---
print("Đang vẽ Biểu đồ 4: Ma trận tương quan giữa tất cả các biến...")
plt.figure(figsize=(8, 6))
corr_matrix = df_olist[['price', 'freight_value', 'product_photos_qty', 'review_score', 'distance_km']].corr()

sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', fmt=".2f", linewidths=0.5, vmin=-1, vmax=1)
plt.title('Ma Trận Hệ Số Tương Quan (Correlation Matrix)', fontsize=14, pad=15)
plt.tight_layout()
plt.savefig('eda_4_correlation_heatmap.png', dpi=300)
plt.close()

print("--- THÀNH CÔNG: Đã xuất 4 file ảnh biểu đồ EDA ra thư mục của bạn! ---")