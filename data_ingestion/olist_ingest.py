import os
import time
import pandas as pd
import duckdb
from dotenv import load_dotenv

load_dotenv()
os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')

from kaggle.api.kaggle_api_extended import KaggleApi

def main():
    print("BẮT ĐẦU QUY TRÌNH INGESTION")

    print("1. Đang kết nối Kaggle và tải dữ liệu...")
    api = KaggleApi()
    api.authenticate()
    
    dataset_path = 'olistbr/brazilian-ecommerce' 
    output_dir = './data_ingestion'
    api.dataset_download_files(dataset_path, path=output_dir, unzip=True)
    print("-> Đã tải và giải nén thành công các file CSV.\n")

    print("2. Đang kết nối tới MotherDuck (Tầng Bronze)...")
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
    con = duckdb.connect(f"md:raw_db?motherduck_token={motherduck_token}")
    print("-> Kết nối thành công.\n")

    csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
    print(f"Tìm thấy {len(csv_files)} file CSV cần xử lý.")
    print("-" * 50)

    chunk_size = 10000 

    for filename in csv_files:
        csv_file_path = os.path.join(output_dir, filename)
 
        clean_name = filename.replace('_dataset.csv', '').replace('.csv', '')
        table_name = f"bronze_{clean_name}"
        
        print(f"\n[*] ĐANG XỬ LÝ FILE: {filename} -> BẢNG: {table_name}")
        
        chunk_count = 0
        for chunk_df in pd.read_csv(csv_file_path, chunksize=chunk_size):
            chunk_count += 1
            print(f"  --> Đang xử lý chunk thứ {chunk_count} ({len(chunk_df)} dòng)...")
            
            if chunk_count == 1:
                con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM chunk_df")
            else:
                con.execute(f"INSERT INTO {table_name} SELECT * FROM chunk_df")
                
            time.sleep(1) 
            
        print(f"-> HOÀN THÀNH FILE {filename}: Đã đẩy xong {chunk_count} chunks.")
        print("-" * 30)
        
    print("\n=== HOÀN THÀNH TOÀN BỘ 9 FILE LÊN MOTHERDUCK! ===")

if __name__ == "__main__":
    main()