import decimal
import random
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(
    title="CryptoFi Frontend Coding Challenge",
)

USER_ORDERS = {"1": [], "2": []}


class UserIds(str, Enum):
    user_1: str = "1"
    user_2: str = "2"


class Tokens(str, Enum):
    BTC: str = "BTC"
    LTC: str = "LTC"
    BCH: str = "BCH"
    ETH: str = "ETH"


class Order(BaseModel):
    price: str
    quantity: str
    token: Tokens
    user_id: UserIds


def generate_random_decimal() -> str:
    x = decimal.Decimal(str(random.uniform(100, 1000)))
    return str(x)


class TokenPrice(BaseModel):
    token_name: Tokens
    token_price: str = Field(
        default_factory=generate_random_decimal, description="GMT based time of order"
    )


@app.get("/token-prices")
def token_prices() -> List[TokenPrice]:
    token_prices = []
    for token in Tokens.__members__.values():
        token_price = TokenPrice(token_name=token)
        token_prices.append(token_price)
    return token_prices


@app.post("/buy-order")
def post_buy_order(order: Order) -> Order:
    USER_ORDERS[order.user_id].append(order)
    return order


@app.get("/orders")
def get_orders(user_id: UserIds) -> List[Order]:
    return USER_ORDERS[user_id]