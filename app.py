import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')
st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます     
""")

st.sidebar.write("""
## 表示日数選択        
""")

days = st.sidebar.slider('日数',1,50,20)

st.write(f"""
### 過去 **{days}日間** のGAFA株価                 
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()  #二次元の表形式のデータで、列名はColumns、行名はindex
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])   #yf.Tickerにはその会社の株価情報が詰まっている
        hist = tkr.history(period = f'{days}d')    #何日間のデータを取ってくるか決める
        hist.index = hist.index.strftime('%d %B %Y')  #index(カラム番号的な)を変更する。'%d %B %Y'は25 March 2022と表示できる
        hist = hist[['Close']]  #カラムはClose項目のみ抽出
        hist.columns = [company]  #カラムの値(hist.columns)をCloseからappleに変更
        hist = hist.T  #行と列を逆にする
        hist.index.name = 'Name'   
        df = pd.concat([df, hist])
    return df

st.sidebar.write("""
## 株価の範囲指定
""")

ymin, ymax = st.sidebar.slider(
    '範囲を指定してください。',
    0.0, 3500.0, (0.0, 3500.0)
 )

tickers = {
    'apple': 'AAPL',
    'facebook': 'FB',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
    'amazon': 'AMZN',
    'ibm': 'IBM'     
}

df = get_data(days, tickers)
companies = st.multiselect(
    '会社名を選択してください',
    list(df.index),
    ['google', 'amazon', 'facebook', 'apple']
)

if not companies:
    st.error('少なくとも一社は選んでください')
else:
    data = df.loc[companies]
    st.write('### 株価 (USB)',data.sort_index())
    data = data.T.reset_index() 
    data = pd.melt(data, id_vars=['Date']).rename(
        columns = {'value': 'Stock Prices(USD)'}        
    ) 
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x = "Date:T",
            y = alt.Y("Stock Prices(USD):Q", stack = None, scale = alt.Scale(domain=[ymin,ymax])),
            color = 'Name:N'
        )        
    )
    st.altair_chart(chart, use_container_width=True) 
    
        