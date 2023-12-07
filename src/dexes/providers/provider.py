from typing import List
from utilities import Network, Token
import requests
class GeckoProvider:
    BASE_API = 'https://api.geckoterminal.com/api/v2'

    def get_simple_price_url(self, network: str, addresses: List[str]):
        return self.BASE_API + f"/simple/networks/{network}/token_price/{','.join(addresses)}"

    def get_simple_token_price(self, network: Network, token: Token):
        token_addresses = [token.addresses[network]]
        network_str = str(network.value).lower()
        simple_price_url = self.get_simple_price_url(network_str, token_addresses)
        raw_res = requests.get(simple_price_url)
        res = raw_res.json()
        prices = res['data']['attributes']['token_prices']
        for address, price in prices.items():
            token = Token.from_address(network, address)
            print(f'{token.name}: {price}')



        


