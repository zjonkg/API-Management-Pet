from pydantic import BaseModel
from typing import List, Dict

class Item(BaseModel):
    id: int
    name: str
    description: str

class ItemBuy(BaseModel):
    id_item: int
    quantity: int
    price: int
    totalPrice: int

class BuyItems(BaseModel):
    id_user: int
    item: List[ItemBuy]
    totalPrice: int
