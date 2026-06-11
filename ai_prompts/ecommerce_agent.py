import duckdb
import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

def get_coo_ai_insights():
    """
    Hàm kết nối MotherDuck, lấy dữ liệu từ Data Marts và gọi Llama 3 phân tích
    """
    # Lấy API key từ file .env
    load_dotenv()
    md_token = os.getenv("MOTHERDUCK_TOKEN")
    groq_key = os.getenv("GROQ_API_KEY")

    if not md_token or not groq_key:
        return "❌ Lỗi: Thiếu MOTHERDUCK_TOKEN hoặc GROQ_API_KEY trong file .env!"

    try:
        # 1. KẾT NỐI VÀ TRÍCH XUẤT DỮ LIỆU TỪ MOTHERDUCK
        print("🔌 Đang kết nối vào kho dữ liệu olist_dw...")
        conn = duckdb.connect(f"md:olist_dw?motherduck_token={md_token}")
        
        # Lấy số liệu từ 2 bảng mart do Nhung chuẩn bị (Chỉ lấy top 15 dòng để tiết kiệm token AI)
        df_delivery = conn.execute("SELECT * FROM olist_dw.marts.delivery_performance_mart LIMIT 15").df()
        df_reviews = conn.execute("SELECT * FROM olist_dw.marts.bad_review_mart LIMIT 15").df()
        
        conn.close()
        
        # Chuyển bảng DataFrame thành dạng văn bản Markdown để AI Llama 3 dễ đọc
        delivery_context = df_delivery.to_markdown(index=False)
        review_context = df_reviews.to_markdown(index=False)

    except Exception as e:
        return f"❌ Lỗi khi đọc dữ liệu từ MotherDuck: {e}"

    # 2. XÂY DỰNG PROMPT & GỌI Llama 3 (Groq)
    print("🧠 Llama 3 đang đóng vai COO phân tích số liệu...")
    client = Groq(api_key=groq_key)
    
    # Định hình nhân cách và ép cấu trúc đầu ra cho AI
    system_prompt = """
    Bạn là Giám đốc Vận hành (COO) cấp cao với 15 năm kinh nghiệm của sàn TMĐT Olist tại Brazil.
    Văn phong của bạn: Quyết đoán, sắc sảo, đi thẳng vào vấn đề, luôn lập luận dựa trên số liệu (Data-driven), tuyệt đối không dùng sáo ngữ chung chung.
    
    QUY TẮC BẮT BUỘC:
    1. Trả lời bằng tiếng Việt, dùng định dạng Markdown chuyên nghiệp.
    2. TRÍCH DẪN SỐ LIỆU CỤ THỂ: Phải đưa các con số (% giao trễ, điểm số) từ báo cáo vào câu trả lời để chứng minh luận điểm.
    3. Cấu trúc bài phân tích phải gồm 3 phần:
       - 🚨 ĐIỂM NÓNG VẬN CHUYỂN: Bóc tách TOP các bang có tỷ lệ giao trễ nghiêm trọng nhất và đánh giá mức độ rủi ro.
       - 📉 TỔN THẤT TRẢI NGHIỆM: Liên kết trực tiếp giữa sự chậm trễ ở các bang trên với tỷ lệ đánh giá 1-2 sao. Trải nghiệm tồi tệ này gây thiệt hại thế nào đến lòng trung thành của khách hàng?
       - 💡 CHIẾN LƯỢC THỰC CHIẾN (Quan trọng nhất): Đề xuất 3 giải pháp vận hành đột phá, cụ thể và khả thi. Thay vì đưa ra lời khuyên chung chung như "tăng cường quản lý", hãy đề xuất các mô hình cụ thể. Ví dụ: Thiết lập mạng lưới O2O (Online-to-Offline) với các điểm lấy hàng tập trung (Click & Collect) tại các bang xa như AL, MA để cắt giảm chi phí Last-mile delivery; hoặc tái cấu trúc quy trình phân bổ đối tác vận chuyển theo SLA (Cam kết chất lượng dịch vụ).
    """

    user_prompt = f"""
    Báo cáo Hiệu suất Giao hàng theo khu vực:
    {delivery_context}

    Báo cáo nguyên nhân Đánh giá kém (1-2 sao):
    {review_context}
    
    Hãy thực hiện phân tích dựa trên dữ liệu trên.
    """

    try:
        # Gọi mô hình Llama 3 bản 70B cực kỳ thông minh
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3, # Mức sáng tạo thấp để AI tập trung phân tích số học chính xác
            max_tokens=1000
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ Lỗi khi gọi Groq API: {e}"

# Khối lệnh này để Leader chạy test độc lập file này
if __name__ == "__main__":
    result = get_coo_ai_insights()
    print("\n" + "="*60)
    print("📈 KẾT QUẢ PHÂN TÍCH TỪ AI (Dành cho Dashboard):")
    print("="*60 + "\n")
    print(result)