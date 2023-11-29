from enum import Enum
from typing import List, Dict
from dataclasses import dataclass

class Network(Enum):
    ETH = 'ETH'
    BTC = 'BTC'
    TRON = 'TRON'

@dataclass
class Exchange():
    name: str
    centralized: bool
    addresses: Dict[Network, str]

@dataclass
class Token():
    name: str
    addresses: Dict[Network, str]
    native: bool = False

    @classmethod
    def from_address(cls, network: Network, address: str):
        for raw_token in TOKENS:
            token: Token = raw_token
            if token_address := token.addresses[network]:
                if token_address.lower() == address.lower():
                    return token

@dataclass
class TokenPair:
    base: Token
    quote: Token

    def __repr__(self) -> str:
        return f"{self.base.value}/{self.quote.value}"

@dataclass
class ExchangeTokenPair:
    exchange: Exchange
    pair: TokenPair
    price: float = 1

    @property
    def invertedPrice(self):
        return 1 / self.price

    @property
    def name(self):
        return f"{self.exchange.value}_{self.pair}"

    def __repr__(self) -> str:
        return f"{self.exchange.value}_{self.pair}"

EXCHANGES: List[Exchange] = [
    Exchange('Uniswap', False, {}),
    Exchange('Binance', True, {})
]

TOKENS: List[Token] = [
    Token('USDT', {Network.ETH: '0xdAC17F958D2ee523a2206206994597C13D831ec7'}),
    Token('LINK', {Network.ETH: '0x514910771AF9Ca656af840dff83E8264EcF986CA'})
]

a = TOKENS[0]




