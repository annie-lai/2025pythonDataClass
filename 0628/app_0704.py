import streamlit as st
import yfinance as yf
import os
import pandas as pd

def download_data():
    #上下3個雙引號寫function的說明
    """
    1.下載yfinance股價數據資料：2330 台積電、2303 聯電、2454 聯發科、2317 鴻海
    2.在目前目錄下建立一個data的資料夾，如果已經有這個資料夾，就不建立
    3.下載的四檔股票必須儲存為4個csv檔，檔名為2330_{當天日期}.csv、2303_{當天日期}.csv
    、2454_{當天日期}.csv、2317_{當天日期}.csv
    4.檔案如果當天已經有下載，就不要再下載
    5.每次下載成功後，刪除舊日期的檔案，只保留最新的一份
    """    
    
    # 定義股票代碼列表
    tickers = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']

    # 獲取今天的日期字串，格式為 YYYY-MM-DD
    today_date = pd.Timestamp.today().strftime('%Y-%m-%d')

    # 檢查並建立data資料夾
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # 遍歷所有股票代碼
    for ticker in tickers:
        base_code = ticker.split('.')[0]
        # 規則 3: 建立包含今天日期的檔名
        filename = f"{base_code}_{today_date}.csv"
        filepath = os.path.join(data_dir, filename)

        # 規則 4: 如果當天檔案已存在，則跳過
        if os.path.exists(filepath):
            print(f"{filename} 當天檔案已存在，跳過下載。")
            continue

        try:
            # 下載數據
            print(f"下載股票數據： {ticker}...")
            data = yf.download(ticker, start='2024-01-01',
                               end=today_date,
                               auto_adjust=True,
                               progress=False)  # 關閉下載進度條，讓輸出更簡潔

            if data.empty:
                print(f"找不到 {ticker} 的數據或日期範圍內無資料，跳過。")
                continue

            data.to_csv(filepath)
            print(f"儲存 {ticker} 至 {filepath}")

            # 規則 5: 刪除舊檔案
            print(f"正在清理 {base_code} 的舊檔案...")
            for old_file in os.listdir(data_dir):
                if old_file.startswith(f"{base_code}_") and old_file != filename:
                    os.remove(os.path.join(data_dir, old_file))
                    print(f"已刪除舊檔案： {old_file}")
        except Exception as e:
            print(f"下載 {ticker} 時發生錯誤: {e}")
            

def combine_close_prices():
    """
    組合這四個csv檔成為一個DataFrame，要組合的只有欄位`Close`，也就是當天的收盤價
    - 檔案名稱`2330_xxxx1`欄位名稱為`台積電`
    - 檔案名稱`2303_xxxx1`欄位名稱為`聯電`
    - 檔案名稱`2454_xxxx1`欄位名稱為`聯發科`
    - 檔案名稱`2317_xxxx1`欄位名稱為`鴻海`
    ###Date要顯示今天日期   
    由於今日是例假日或國定假日，股市沒有開盤，所以沒有資料
    解決方法：只顯示csv檔內所有的資料，而不是使用日期 
    """
    data_dir = 'data'
    combined_df = pd.DataFrame()
    
    # 定義股票代碼和對應的中文名稱
    stock_map = {
        '2330': '台積電',
        '2303': '聯電',
        '2454': '聯發科',
        '2317': '鴻海'
    }

    # 遍歷資料夾中的所有檔案
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(data_dir, filename)
            base_code = filename.split('_')[0]
            
            if base_code in stock_map:
                try:
                    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
                    if 'Close' in df.columns:
                        # 確保 'Close' 欄位是數值型態，無法轉換的會變成 NaN
                        close_prices = pd.to_numeric(df['Close'], errors='coerce')
                        # 將處理過的收盤價加入 combined_df
                        combined_df[stock_map[base_code]] = close_prices
                    else:
                        print(f"檔案 {filename} 中找不到 'Close' 欄位。")
                except Exception as e:
                    print(f"讀取檔案 {filename} 時發生錯誤: {e}")
       
    if combined_df.empty:
        print("\n在 data 資料夾中找不到任何有效的股票數據。")
        return combined_df

    # 【關鍵修正】
    # 移除索引不是有效日期的行 (例如 'Ticker' 或 'Date' 字串)
    # pd.to_datetime 會將無法轉換的索引變成 NaT (Not a Time)
    # .notna() 會篩選出所有轉換成功的行，也就是有效的日期
    combined_df = combined_df[pd.to_datetime(combined_df.index, errors='coerce').notna()]

    # 將索引明確轉換為 DatetimeIndex，這是解決 TypeError 的關鍵
    combined_df.index = pd.to_datetime(combined_df.index)

    # 按照日期排序，確保資料是時間序列
    combined_df.sort_index(inplace=True)

    return combined_df


# --- Streamlit 頁面設定 ---
st.set_page_config(page_title="台股儀表板", layout="wide")

st.title("📈 台股收盤價儀表板")
st.caption("資料來源: Yahoo Finance")

# --- 快取資料載入函式 ---
# @st.cache_data 會快取函式的回傳值。當函式被同樣的參數呼叫時，
# Streamlit 會直接回傳快取的結果，而不是重新執行函式，可以大幅提升效能。
@st.cache_data
def load_data():
    """
    從 yf_stock 模組載入並組合股價資料。
    這個函式會被快取，只有在需要時才重新從檔案讀取。
    """
    df = combine_close_prices()
    return df

# --- 主介面 ---

# 建立兩個欄位佈局，左邊窄右邊寬
col1, col2 = st.columns([1, 3])

with col1:
    st.header("控制面板")
    # 按鈕：觸發資料下載
    if st.button("更新/下載最新股價資料"):
        with st.spinner("正在執行資料下載與清理，請稍候..."):
            download_data()
            # 清除快取，以便下次能讀取到最新的資料
            st.cache_data.clear()
        st.success("資料更新完成！")

    # 載入資料
    combined_df = load_data()

    # --- UI elements are only shown if data is available ---
    if not combined_df.empty:
        # 多選框：讓使用者選擇要顯示的股票
        st.header("圖表選項")
        all_stocks = combined_df.columns.tolist()
        selected_stocks = st.multiselect(
            "選擇要繪製的股票：",
            options=all_stocks,
            default=all_stocks  # 預設全選
        )

        # 日期範圍選擇器
        st.header("日期範圍")
        min_date = combined_df.index.min()
        max_date = combined_df.index.max()

        start_date = st.date_input(
            "開始日期",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )
        end_date = st.date_input(
            "結束日期",
            value=max_date,
            min_value=start_date,
            max_value=max_date
        )

        if start_date > end_date:
            st.error("錯誤：開始日期不能晚於結束日期。")
            st.stop()

    else:
        st.warning("找不到任何資料，請先點擊按鈕下載。")
        # Set placeholders so the rest of the code doesn't break
        selected_stocks = []
        start_date, end_date = None, None

with col2:
    st.header("資料預覽與圖表")
    # Check if we have everything needed to display
    if not combined_df.empty and selected_stocks and start_date:
        # Filter data based on user selections
        mask = (combined_df.index >= pd.to_datetime(start_date)) & (combined_df.index <= pd.to_datetime(end_date))
        filtered_df = combined_df.loc[mask]
        
        display_df = filtered_df[selected_stocks]

        # 顯示資料表格，並將數字格式化到小數點後兩位
        st.subheader(f"收盤價資料 ({start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')})")
        st.dataframe(display_df.style.format("{:.2f}"))

        # 繪製圖表，並設定固定高度
        st.subheader("股價走勢圖")
        st.line_chart(display_df, height=400)
    else:
        # Provide context-aware messages
        if combined_df.empty:
            st.info("資料載入後，將在此處顯示預覽與圖表。")
        elif not selected_stocks:
            st.info("請在左側選擇至少一檔股票以顯示圖表。")
