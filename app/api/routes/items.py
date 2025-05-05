from fastapi import APIRouter, HTTPException
import supabase
from app.models.items import *
from app.core.database import supabase

router = APIRouter()

@router.get("/")
async def get_items():
    response = supabase.table("items").select("*").execute()
    
    return response.data

@router.get("/{id}")
async def get_item(id: int):
    response = supabase.table("items").select("*").eq("id", id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return response.data[0]

@router.post("/{id_user}/{id_item}/{quantity}")
async def create_item(id_user: int, id_item: int, quantity: int):
    response_user = supabase.table("users").select("id, balance").eq("id", id_user).execute()
    response_item = supabase.table("items").select("id, name, price").eq("id", id_item).execute()

    if response_item.data["price"] * quantity > response_user.data["balance"]:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    else:
        new_balance = response_user.data["balance"] - (response_item.data["price"] * quantity)
        supabase.table("users").update({"balance": new_balance}).eq("id", id_user).execute()
        return {"message": "Item created successfully"}
    
@router.put("/eat/{id_user}/{id_item}")
async def eat(id_user: int, id_item: int):
    user_response = supabase.table("user_items").select("*").eq("id_user", id_user).eq("id_item", id_item).execute()

    if user_response.data[0]["quantity"] > 0:
        less_quatity = user_response.data[0]["quantity"] - 1

    supabase.table("user_items").update({"quantity": less_quatity}).eq("id_item", id_item).execute()
    return {"message": "Item eaten successfully"}

@router.put("/buy")
async def buy_item(item: BuyItems):
    response_user = supabase.table("users").select("id, balance").eq("id", item.user).execute()

    if item["totalPrice"] > response_user.data[0]["balance"]:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    else:
        new_balance = response_user.data[0]["balance"] - item["totalPrice"]
        supabase.table("users").update({"balance": new_balance}).eq("id", item.user).execute()
        return {"message": "Item bought successfully"}