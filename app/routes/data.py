from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from app.core.security import get_current_user
from app.core.database import db

# Collections
stores_collection = db["stores"]
vendors_collection = db["vendors"]
products_collection = db["products"]
inventory_collection = db["inventory"]

router = APIRouter(prefix="/api/data", tags=["Convenience Store Data"])

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    doc["id"] = str(doc.get("id") or doc.get("_id"))
    if "_id" in doc:
        del doc["_id"]
    return doc

@router.get("/stores", response_model=List[Dict[str, Any]])
async def get_stores(current_user: dict = Depends(get_current_user)):
    role = current_user.get("role", "").lower()
    
    if role == "store manager":
        store_id = current_user.get("storeId")
        if not store_id:
            return []
        stores_cursor = stores_collection.find({"id": store_id})
    elif role == "regional head":
        region = current_user.get("region")
        if not region:
            return []
        # Find stores in the regional head's city (case-insensitive)
        stores_cursor = stores_collection.find({"city": {"$regex": f"^{region}$", "$options": "i"}})
    else:
        # Retail Head / Super Admin get all stores
        stores_cursor = stores_collection.find()
        
    stores_list = await stores_cursor.to_list(length=100)
    return [serialize_doc(s) for s in stores_list]

@router.get("/products", response_model=List[Dict[str, Any]])
async def get_products(current_user: dict = Depends(get_current_user)):
    products_cursor = products_collection.find()
    products_list = await products_cursor.to_list(length=200)
    return [serialize_doc(p) for p in products_list]

@router.get("/vendors", response_model=List[Dict[str, Any]])
async def get_vendors(current_user: dict = Depends(get_current_user)):
    vendors_cursor = vendors_collection.find()
    vendors_list = await vendors_cursor.to_list(length=100)
    return [serialize_doc(v) for v in vendors_list]

@router.get("/inventory", response_model=List[Dict[str, Any]])
async def get_inventory(current_user: dict = Depends(get_current_user)):
    role = current_user.get("role", "").lower()
    
    if role == "store manager":
        store_id = current_user.get("storeId")
        if not store_id:
            return []
        inv_cursor = inventory_collection.find({"storeId": store_id})
    elif role == "regional head":
        region = current_user.get("region")
        if not region:
            return []
        # Find store IDs in this region
        stores_in_region = await stores_collection.find(
            {"city": {"$regex": f"^{region}$", "$options": "i"}}
        ).to_list(length=100)
        store_ids = [s["id"] for s in stores_in_region]
        
        if not store_ids:
            return []
        inv_cursor = inventory_collection.find({"storeId": {"$in": store_ids}})
    else:
        # Full inventory
        inv_cursor = inventory_collection.find()
        
    inv_list = await inv_cursor.to_list(length=2000)
    return [serialize_doc(item) for item in inv_list]
