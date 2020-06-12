from CoinGeckoAPI import CoinGeckoAPI
from datetime import datetime
import pandas as pd
from github import Github
import requests as re

def daily_update():
    df_tokens = pd.read_csv("https://raw.githubusercontent.com/zhongzhu-zhou/demo/master/data/index_coingecko.csv")
    tokenlist = list(df_tokens["Name"])
    c_api = CoinGeckoAPI()
    dt0 = datetime.utcnow()
    dt0 = dt0.replace(day=dt0.day - 1)
    dt = dt0.strftime("%d-%m-%Y")
    columns = ["token", "prices", "market_caps", "total_volumes"]
    resultlist = []
    for token in tokenlist:
        try:
            result = c_api.get_coin_history_by_id(token.lower(), dt)["market_data"]
            templist = [token.lower()]
            for key, values in result.items():
                for currency, value in values.items():
                    if currency == "usd":
                        templist.append(value)
            resultlist.append(templist)
        except KeyError:
            continue
    df_section = pd.DataFrame()
    for each in resultlist:
        df_section = df_section.append(pd.Series(each), ignore_index=True)
    df_section.columns = columns
    set_time = dt0.strftime('%Y-%m-%d')
    df_section["time"] = pd.to_datetime(set_time)
    df_section = df_section.reindex(columns=["time", "token", "market_caps", "prices", "total_volumes"])
    df_all = pd.read_csv("https://raw.githubusercontent.com/zhongzhu-zhou/demo/master/data/historical.csv",parse_dates=["time"])
    if df_all.loc[df_all["time"] == df_section["time"].head(1).values[0]].empty:
        df_section.to_csv("data/historical.csv", mode="a",
                          header=False)
        g = Github("zhongzhu-zhou", "zzz578643")
        repo = g.get_user("zhongzhu-zhou").get_repo("demo")
        url = "https://api.github.com/repos/zhongzhu-zhou/demo/branches/master"
        master = re.get(url).json()
        head_tree_sha = master['commit']['commit']['tree']['sha']
        url2 = "https://api.github.com/repos/zhongzhu-zhou/demo/git/trees/" + head_tree_sha
        page2 = re.get(url2)
        for each in page2.json()["tree"]:
            if each["path"] == "data":
                sha = each["sha"]
                break
        url3 = "https://api.github.com/repos/zhongzhu-zhou/demo/git/trees/" + sha
        page3 = re.get(url3)

        for each in page3.json()["tree"]:
            if each["path"] == "historical.csv":
                sha = each["sha"]
                break
        data = open("data/historical.csv", "rb").read()
        repo.update_file(path="data/historical.csv", message="daily commit", content=data, sha=sha)

if __name__ == "__main__":
    daily_update()


