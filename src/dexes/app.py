from providers.providers import GeckoProvider
from utilities import Network, TOKENS

# infura_api_key = '989a33ef7f114f45b58346df500b9917'
# infura_base_api = f'https://mainnet.infura.io/v3/{api_key}'


gecko_provider = GeckoProvider()
gecko_provider.get_simple_token_price(Network.ETH, TOKENS[1])




