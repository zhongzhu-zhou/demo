import json
import requests
import pprint
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime



class CoinGeckoAPI:
    __API_URL_BASE = 'https://api.coingecko.com/api/v3/'

    def __init__(self, api_base_url=__API_URL_BASE):
        self.api_base_url = api_base_url
        self.request_timeout = 120

        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))


# private method that allows other public mathods to get content from CoinGecko
    def __request(self, url):
        # print(url)
        try:
            response = self.session.get(url, timeout=self.request_timeout)
            response.raise_for_status()
            content = json.loads(response.content.decode('utf-8'))
            return content
        except Exception as e:
            # check if json (with error message) is returned
            try:
                content = json.loads(response.content.decode('utf-8'))
                raise ValueError(content)
            # if no json
            except json.decoder.JSONDecodeError:
                pass
            # except UnboundLocalError as e:
            #    pass
            raise
            

#Private methods passing parameters to url endpoints
    def __api_url_params(self, api_url, params):
        if params:
            api_url += '?'
            for key, value in params.items():
                api_url += "{0}={1}&".format(key, value)
            api_url = api_url[:-1]
        return api_url



#Get historical data (name, price, market, stats) at a given date for a coin
    def get_coin_history_by_id(self, id, date, **kwargs):


        kwargs['date'] = date

        api_url = '{0}coins/{1}/history'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)

        return self.__request(api_url)


#Get all coins' latest info
    def get_coin_list(self):
        api_url = self.api_base_url+"coins/list"
        return self.__request(api_url)


#Get historical market data include price, market cap, and 24h volume within a range of timestamp (granularity auto)
    def get_coin_market_chart_range_by_id(self, id, vs_currency, from_timestamp, to_timestamp):

        api_url = '{0}coins/{1}/market_chart/range?vs_currency={2}&from={3}&to={4}'.format(self.api_base_url, id,
                                                                                           vs_currency, from_timestamp,
                                                                                           to_timestamp)

        return self.__request(api_url)


#Get a specific token's current data, including its latest price, market_caps, and price change.
    def get_coin_current_data(self,id):
        api_url = self.api_base_url+"coins/"+id
        return self.__request(api_url)


#Get a specific token's current data, including its latest price, market_caps, and price change. All values will be in the currency specified.
    def get_coin_market_data(self,currency,ids):
        api_url = self.api_base_url + "coins/markets?"+"vs_currency="+currency+"&ids="
        api_url += "%2C".join(ids)
        api_url += "&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24"
        return self.__request(api_url)













