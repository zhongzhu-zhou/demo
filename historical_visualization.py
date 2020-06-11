import pandas as pd
import matplotlib.pyplot as plt
import io
pd.set_option("display.width",1000)
pd.set_option("display.max_column",10000)



def displayvisulization(industry,metrics):
    df_tokens = pd.read_csv("data/index_coingecko.csv")
    df_tokens = df_tokens.rename(columns={"Name": "token"})
    df_tokens["token"] = df_tokens["token"].str.lower()
    df1 = df_tokens[["token", "Index"]]
    df2 = pd.read_csv("data/historical.csv", thousands=",")
    df2["time"] = pd.to_datetime(df2["time"])
    df3 = df2.merge(df1, on="token")
    df3 = df3[df3["Index"] == industry]
    df3[metrics] = pd.to_numeric(df3[metrics], errors="coerce")
    fig, ax1 = plt.subplots(1, 1)
    # fig.set_size_inches(300,500)
    dftemp = df3.groupby("time").agg({metrics: "mean"})
    ax1.set_title(industry)
    ax1.plot(dftemp)
    ax1.set_xlabel("Time")
    ax1.set_ylabel(industry + " " + metrics)
    fig.autofmt_xdate()

    # plt.show()
    filename = "download/historical-"+industry+"-"+metrics+".png"
    plt.savefig(filename, dpi = 300)

if __name__ == "__main__":
    displayvisulization("Sustainability Index","market_caps")


