from CoinGeckoAPI import CoinGeckoAPI
from datetime import datetime
import pandas as pd
import time

# Generate the initial historical.csv file. Only need to be run once
if __name__ == "__main__":
    c_api = CoinGeckoAPI()
    dt = datetime.now()
    dt2 = dt.replace(year=dt.year - 3)
    ts = time.mktime(dt.timetuple())
    ts2 = time.mktime(dt2.timetuple())

    df_tokens = pd.read_excel("index_coingecko.xlsx")
    tokenlist = list(df_tokens["Name"])
    pd_all = pd.DataFrame()

    for token in tokenlist:
        df_result = pd.DataFrame()
        result = c_api.get_coin_market_chart_range_by_id(token.lower(), "usd", int(ts2), int(ts))
        for key, value in result.items():
            for each in value:
                newtime = datetime.utcfromtimestamp(each[0] * 0.001).strftime('%Y-%m-%d')
                df_result = df_result.append(pd.Series([token.lower(), key, newtime, each[1]]), ignore_index=True)
        df_result.columns = ["token", "type", "time", "value"]
        df_result = pd.pivot_table(df_result, values="value", columns="type", index=["time", "token"])
        df_result.reset_index(inplace=True)
        df_result.columns = ["time", "token", "market_caps", "prices", "total_volumes"]
        # print(df_result)
        pd_all = pd_all.append(df_result, ignore_index=True)
    pd_all.to_csv("coingecko\\historical.csv")

