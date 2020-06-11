from CoinGeckoAPI import CoinGeckoAPI
import pandas as pd
def mean_of_list(list):
    list = [0 if x is None else x for x in list]
    return round(float(sum(list))/float(len(list)),3)


def get_current_data():
    df0 = pd.read_csv("data/index_coingecko.csv")
    set1 = set(df0["Index"])
    final_data = {}
    for industry in set1:
        df1 = df0[df0["Index"] == industry]
        tokenlist = list(df1["Name"].str.lower())
        marketcap_list = []
        currentprice_list = []
        high24_list = []
        low24_list = []
        totalvolume_list = []
        marketcapchangepercentage24h_list = []
        c_api = CoinGeckoAPI()
        data = c_api.get_coin_market_data("usd", tokenlist)
        for each in data:
            marketcap_list.append(each["market_cap"])
            currentprice_list.append(each["current_price"])
            high24_list.append(each["high_24h"])
            low24_list.append(each["low_24h"])
            totalvolume_list.append(each["total_volume"])
            marketcapchangepercentage24h_list.append(each["market_cap_change_percentage_24h"])
        sub_final_data = {"market_cap": mean_of_list(marketcap_list),
                          "current_price": mean_of_list(currentprice_list),
                      "high_24h": mean_of_list(high24_list),
                      "low_24h": mean_of_list(low24_list),
                      "total_volume": sum(totalvolume_list),
                      "market_cap_change_percentage_24h": mean_of_list(marketcapchangepercentage24h_list)
                      }
        final_data[industry] = sub_final_data
    return final_data



    #     elements_list = ["current_price", "total_volume", "high_24h", "low_24h", "price_change_24h"]
    #     data_list = []
    #     for each in elements_list:
    #         data_list.
    #
    #     all_list.append(data_list)
    #     print(token)
    # print(all_list)


if __name__ == "__main__":
    print(get_current_data())
