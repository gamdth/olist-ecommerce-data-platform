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
    print("BẮT ĐẦU QUY TRÌNH INGESTION ")

    print("1. Đang kết nối Kaggle và tải dữ liệu...")
    api = KaggleApi()
    api.authenticate()
    
   
    dataset_path = 'olistbr/brazilian-ecommerce' 
    api.dataset_download_files(dataset_path, path='./data_ingestion', unzip=True)
    print("-> Đã tải và giải nén thành công 9 file CSV.\n")

    print("2. Đang kết nối tới MotherDuck (Tầng Bronze)...")
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
    con = duckdb.connect(f"md:raw_db?motherduck_token={motherduck_token}")
    print("-> Kết nối thành công.\n")

    csv_file = "./data_ingestion/olist_orders_dataset.csv"
    table_name = "bronze_olist_orders"
    chunk_size = 10000 
    
    print(f"3. Bắt đầu đẩy file {csv_file} lên bảng {table_name} theo từng chunk ({chunk_size} dòng/chunk)...")
    
    chunk_count = 0
    for chunk_df in pd.read_csv(csv_file, chunksize=chunk_size):
        chunk_count += 1
        print(f"--> Đang xử lý chunk thứ {chunk_count} ({len(chunk_df)} dòng)...")
        
        if chunk_count == 1:
            con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM chunk_df")
        else:
            con.execute(f"INSERT INTO {table_name} SELECT * FROM chunk_df")
            
        print(f"    Đã đẩy xong chunk {chunk_count}.")
        
        time.sleep(2)
        
    print(f"\n HOÀN THÀNH TOÀN BỘ FILE: Đã đẩy {chunk_count} chunks lên MotherDuck!")

if __name__ == "__main__":
    main()