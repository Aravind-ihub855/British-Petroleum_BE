from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
import re
from app.core.security import get_current_user
from app.core.database import db

# Collections
stores_collection = db["stores"]
vendors_collection = db["vendors"]
products_collection = db["products"]
inventory_collection = db["inventory"]
purchase_orders_collection = db["purchase_orders"]
vendor_issues_collection = db["vendor_issues"]
recommendations_collection = db["recommendations"]

router = APIRouter(prefix="/api/data", tags=["Convenience Store Data"])

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    doc["id"] = str(doc.get("id") or doc.get("_id"))
    if "_id" in doc:
        del doc["_id"]
    return doc

def get_region_cities(region: str) -> List[str]:
    """
    Map a region name to all cities in that regional cluster.
    North Region: Chicago, Denver
    South Region: Houston, Los Angeles
    """
    r = region.lower().strip()
    if r == "north":
        return ["Chicago", "Denver"]
    if r == "south":
        return ["Houston", "Los Angeles"]
    # Fallback: treat it as a single city if unknown value stored
    return [region]

def city_filter(cities: List[str]) -> dict:
    """
    Build a case-insensitive MongoDB $or filter for a list of city names.
    Handles mixed-case values in the DB (e.g. 'chicago', 'Chicago', 'CHICAGO').
    """
    return {
        "$or": [
            {"city": {"$regex": f"^{re.escape(city)}$", "$options": "i"}}
            for city in cities
        ]
    }

@router.get("/stores", response_model=List[Dict[str, Any]])
async def get_stores(current_user: dict = Depends(get_current_user)):
    role = current_user.get("role", "").lower()

    if role == "store manager":
        store_id = current_user.get("storeId")
        if not store_id:
            return []
        stores_cursor = stores_collection.find({"id": store_id})

    elif role in ["vendor manager", "regional head"]:
        region = current_user.get("region")
        if not region:
            return []
        cities = get_region_cities(region)
        stores_cursor = stores_collection.find(city_filter(cities))

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
    role = current_user.get("role", "").lower()

    if role in ["vendor manager", "regional head"]:
        region = current_user.get("region")
        if not region:
            return []
        cities = get_region_cities(region)
        vendors_cursor = vendors_collection.find(city_filter(cities))
    else:
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

    elif role in ["vendor manager", "regional head"]:
        region = current_user.get("region")
        if not region:
            return []
        cities = get_region_cities(region)
        # Find store IDs in this region's cities (case-insensitive)
        stores_in_region = await stores_collection.find(
            city_filter(cities)
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

@router.get("/purchase-orders", response_model=List[Dict[str, Any]])
async def get_purchase_orders(current_user: dict = Depends(get_current_user)):
    role = current_user.get("role", "").lower()

    if role in ["vendor manager", "regional head"]:
        region = current_user.get("region")
        if not region:
            return []
        cities = get_region_cities(region)
        # Resolve store IDs for the region (case-insensitive)
        stores_in_region = await stores_collection.find(
            city_filter(cities)
        ).to_list(length=100)
        store_ids = [s["id"] for s in stores_in_region]

        if not store_ids:
            return []
        cursor = purchase_orders_collection.find({"storeId": {"$in": store_ids}})
    else:
        cursor = purchase_orders_collection.find()

    lst = await cursor.to_list(length=1000)
    return [serialize_doc(i) for i in lst]

@router.get("/vendor-issues", response_model=List[Dict[str, Any]])
async def get_vendor_issues(current_user: dict = Depends(get_current_user)):
    role = current_user.get("role", "").lower()

    if role in ["vendor manager", "regional head"]:
        region = current_user.get("region")
        if not region:
            return []
        cities = get_region_cities(region)
        # Resolve vendor IDs in these cities (case-insensitive)
        vendors_in_region = await vendors_collection.find(
            city_filter(cities)
        ).to_list(length=100)
        vendor_ids = [v["id"] for v in vendors_in_region]

        if not vendor_ids:
            return []
        cursor = vendor_issues_collection.find({"vendorId": {"$in": vendor_ids}})
    else:
        cursor = vendor_issues_collection.find()

    lst = await cursor.to_list(length=500)
    return [serialize_doc(i) for i in lst]

@router.get("/recommendations", response_model=List[Dict[str, Any]])
async def get_recommendations(current_user: dict = Depends(get_current_user)):
    cursor = recommendations_collection.find()
    lst = await cursor.to_list(length=100)
    return [serialize_doc(i) for i in lst]
