import yfinance as yf
import pandas as pd
from datetime import datetime
import time
from tqdm import tqdm
from stock_data_us_all import stock_list  # 導入股票列表


def download_stock_data(stock_list, start_date, end_date, output_file):
    """
    下載股票數據並保存到CSV文件

    參數:
    stock_list (list): 股票代碼列表
    start_date (str): 起始日期 (YYYY-MM-DD)
    end_date (str): 結束日期 (YYYY-MM-DD)
    output_file (str): 輸出文件名
    """

    # 創建一個空的 DataFrame 來存儲所有數據
    all_data = pd.DataFrame()

    # 使用 tqdm 顯示進度條
    for symbol in tqdm(stock_list, desc="下載股票數據"):
        try:
            # 下載數據
            stock = yf.Ticker(symbol)
            df = stock.history(start=start_date, end=end_date)

            # 如果數據不為空
            if not df.empty:
                # 重設索引，將日期變成一個列
                df = df.reset_index()

                # 添加股票代碼列
                df['Symbol'] = symbol

                # 重新排列列的順序
                df = df[['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

                # 將數據增加到主 DataFrame
                all_data = pd.concat([all_data, df], ignore_index=True)

            # 暫停一下，避免發送太多請求
            time.sleep(0.5)

        except Exception as e:
            print(f"下載 {symbol} 時發生錯誤: {str(e)}")
            continue

    # 保存數據到CSV文件
    if not all_data.empty:
        all_data.to_csv(output_file, index=False)
        print(f"\n數據已保存到 {output_file}")
        return all_data
    else:
        print("沒有數據被下載")
        return None


# 使用示例
if __name__ == "__main__":
    # 可以直接指定日期
    start_date = "2024-02-01"  # 指定起始日期
    end_date = "2024-02-09"  # 指定結束日期

    # 下載數據
    data = download_stock_data(
        stock_list=stock_list,
        start_date=start_date,
        end_date=end_date,
        output_file='stock_data.csv'
    )