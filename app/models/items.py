from pydantic import BaseModel
from typing import List, Dict

class Item(BaseModel):
    id: int
    name: str
    description: str

class ItemBuy(BaseModel):
    name: str
    quantity: int
    price: int
    totalPrice: int

class BuyItems(BaseModel):
    user: int
    item: List[ItemBuy]
    totalPrice: int
