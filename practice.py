#講座と一緒に書いた練習コード
import pandas as pd
#import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt

#appleのみの株価を可視化するコード
# aapl = yf.Ticker('AAPL')   #Tickerシンボル(企業ごとに決まっている文字列)を取ってくる
# days = 50  
# hist = aapl.history(period = f'{days}d')    #何日間のデータを取ってくるか決める
# hist.index = hist.index.strftime('%d %B %Y')  #index(カラム番号的な)を変更する。'%d %B %Y'は25 March 2022と表示できる
# hist = hist[['Close']]  #カラムはClose項目のみ抽出
# hist.columns = ['apple']  #カラムの値(hist.columns)をCloseからappleに変更
# hist = hist.T  #行と列を逆にする
# hist.index.name = 'Name'
# hist

#完成形コード(for文を使いまくる)
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
    
    #(altairの機能を確認するためにappleとfacebookの二社だけで考えてみる)
    companies = ['apple', 'facebook']
    data = df.loc[companies]
    data = data.sort_index()  #アルファベット順に並べる
    #グラフ化したいので、reset_indexによりNameを0 1 2 3として,Date,appleの株価,facebookの株価と言う並び順にしている
    data = data.T.reset_index() 
    
    #Name,Date,企業名,企業の株価という並び順にする。
    data = pd.melt(data, id_vars=['Date']).rename(
        columns = {'value': 'Stock Prices(USD)'}        
    )    
    data
    ymin,ymax = 200,300
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x = "Date:T",
            y = alt.Y("Stock Prices(USD):Q", stack = None, scale = alt.Scale(domain=[ymin,ymax])),
            color = 'Name:N'
        )        
    )
    chart



days = 20
tickers = {
    'apple': 'AAPL',
    'facebook': 'FB',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
    'amazon': 'AMZN'     
}


get_data(days, tickers)

