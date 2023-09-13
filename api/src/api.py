import random
from enum import Enum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List

app = FastAPI(
    title="CryptoFi Frontend Coding Challenge",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

class Balance(BaseModel):
    average_token_price: int = Field(default=0)
    quantity: int = Field(default=0)


USER_BALANCES = {
    "1": {"BTC": Balance(), "LTC": Balance(), "BCH": Balance(), "ETH": Balance()}, 
    "2": {"BTC": Balance(), "LTC": Balance(), "BCH": Balance(), "ETH": Balance()}
}


class UserIds(str, Enum):
    user_1: str = "1"
    user_2: str = "2"


class Tokens(str, Enum):
    BTC: str = "BTC"
    LTC: str = "LTC"
    BCH: str = "BCH"
    ETH: str = "ETH"


class Order(BaseModel):
    price: int = Field(ge=1)
    quantity: int = Field(ge=1)
    token: Tokens
    user_id: UserIds


def generate_random_int() -> int:
    return random.randint(10, 25000)


class TokenPrice(BaseModel):
    token_name: Tokens
    token_price: int = Field(
        default_factory=generate_random_int, description="GMT based time of order"
    )


@app.get("/token-prices")
def token_prices() -> List[TokenPrice]:
    token_prices = []
    for token in Tokens.__members__.values():
        token_price = TokenPrice(token_name=token)
        token_prices.append(token_price)
    return token_prices


@app.post("/buy-order")
def post_buy_order(order: Order) -> dict:
    current_balance: Balance = USER_BALANCES[order.user_id][order.token]
    current_quantity = current_balance.quantity
    current_average_token_price = current_balance.average_token_price
    updated_quantity = order.quantity + current_quantity
    
    total_cost_of_tokens = (current_average_token_price * current_quantity) + (order.price * order.quantity)
    updated_average_token_price = int(total_cost_of_tokens / updated_quantity)

    USER_BALANCES[order.user_id][order.token] = Balance(average_token_price=updated_average_token_price, quantity=updated_quantity)
    return {"message": "success"}


@app.get("/balance")
def get_balance(user_id: UserIds) -> Dict[str, Balance]:
    return USER_BALANCES[user_id]