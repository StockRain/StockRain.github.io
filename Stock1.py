import pandas as pd; import numpy as np
import tushare,talib
from datetime import datetime, timedelta
import json

pastNdays = 100     # 根据过去多少天判断
basics = tushare.get_stock_basics()

def analyse(code):
    result = {"code":code, "name":basics.name[code]}
    # clean 
    df = tushare.get_hist_data(code).sort_values(by='date')
    df.reset_index(inplace=True)
    startDate = datetime.today() - timedelta(days=pastNdays)
    df = df[ df['date'] > str(startDate) ]
    df.index = pd.to_datetime(df.date)

    # basics
    volume = df.volume.values
    close = df.close.values

    # indicators
    ## Bollinger Bands
    #upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)
    upper, middle, lower = talib.BBANDS(close, 20, 2, 2)
    chanceToRise = (middle[-1]-close[-1])/(upper[-1]-lower[-1])*100
    result["BollingerBands"] = upper[-1], middle[-1], lower[-1], close[-1], chanceToRise
    ## RSI
    result["RSI"] = talib.RSI(close)[-1]
    ## MACD
    result["MACD"] = talib.MACD(close)[0][-1]
    ## Custom VOL
    result["CustomVOL"] = volume[-1]/np.mean(volume)
    #print(result)
    return result

cnt = 1; n = 0; allData = []
for i in basics.index:
    try: allData.append(analyse(i))
    except: pass
    #analyse(i)
    n+=1
    if n%100==0:
        print(n,'/',basics.index.size)
        #now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        with open('data.json', 'w') as f:
            f.write("const data = ")
            json.dump(allData, f)





