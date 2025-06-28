import streamlit as st
import yf_stock  # 匯入我們的主程式
import pandas as pd

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
    df = yf_stock.combine_close_prices()
    return df

# --- 主介面 ---

# 建立兩個欄位佈局，左邊窄右邊寬
col1, col2 = st.columns([1, 3])

with col1:
    st.header("控制面板")
    # 按鈕：觸發資料下載
    if st.button("更新/下載最新股價資料"):
        with st.spinner("正在執行資料下載與清理，請稍候..."):
            yf_stock.download_data()
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
