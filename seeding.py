import math
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.core.database import db

# Collections
stores_collection = db["stores"]
vendors_collection = db["vendors"]
products_collection = db["products"]
inventory_collection = db["inventory"]
purchase_orders_collection = db["purchase_orders"]
vendor_issues_collection = db["vendor_issues"]
recommendations_collection = db["recommendations"]

def get_seed_hash(s: str) -> int:
    hash_val = 0
    for char in s:
        hash_val = ord(char) + ((hash_val << 5) - hash_val)
        # Cast to 32-bit signed int
        hash_val = (hash_val + 2**31) % 2**32 - 2**31
    return abs(hash_val)

# 1. 25 Onboarded Vendors
vendors_data = [
  { "id": "VND-001", "name": "Castrol USA Lubricants", "contact": "John Davis", "email": "orders@castrol.us", "isExternal": True, "type": "Manufacturer", "region": "Midwest", "city": "Chicago", "onboardingDate": "12-Oct-2019", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-002", "name": "Coca-Cola Bottling Co.", "contact": "Sarah Miller", "email": "delivery@coca-cola.com", "isExternal": True, "type": "DSD", "region": "South", "city": "Houston", "onboardingDate": "05-Jan-2020", "managedBy": "Emma Stone", "contractStatus": "Active", "paymentTerms": "Net 15" },
  { "id": "VND-003", "name": "Frito-Lay North America", "contact": "Mike Johnson", "email": "snacks@fritolay.com", "isExternal": True, "type": "DSD", "region": "West", "city": "Los Angeles", "onboardingDate": "18-Feb-2020", "managedBy": "Marcus Vance", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-004", "name": "McLane Company Distribution", "contact": "Robert Lee", "email": "supply@mclane.com", "isExternal": True, "type": "Distributor", "region": "Midwest", "city": "Chicago", "onboardingDate": "22-Jul-2018", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 45" },
  { "id": "VND-005", "name": "Keurig Dr Pepper Group", "contact": "Emily Watson", "email": "beverages@kdp.com", "isExternal": True, "type": "DSD", "region": "South", "city": "Houston", "onboardingDate": "14-Mar-2020", "managedBy": "Emma Stone", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-006", "name": "Hershey Chocolate USA", "contact": "Chris Brown", "email": "sales@hersheys.com", "isExternal": True, "type": "Manufacturer", "region": "Northeast", "city": "Denver", "onboardingDate": "09-Jun-2020", "managedBy": "Sarah Jenkins", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-007", "name": "Kraft Heinz Foodservice", "contact": "David Clark", "email": "orders@kraftheinz.com", "isExternal": True, "type": "Manufacturer", "region": "Midwest", "city": "Chicago", "onboardingDate": "11-Nov-2019", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-008", "name": "PepsiCo Beverages NA", "contact": "Amanda Taylor", "email": "dispatch@pepsico.com", "isExternal": True, "type": "DSD", "region": "West", "city": "Los Angeles", "onboardingDate": "01-Apr-2020", "managedBy": "Marcus Vance", "contractStatus": "Active", "paymentTerms": "Net 15" },
  { "id": "VND-009", "name": "General Mills Inc.", "contact": "James Wilson", "email": "grocery@generalmills.com", "isExternal": True, "type": "Manufacturer", "region": "Midwest", "city": "Chicago", "onboardingDate": "15-Dec-2018", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 45" },
  { "id": "VND-010", "name": "Nestle USA Snacks", "contact": "Jessica Thomas", "email": "orders@nestle.com", "isExternal": True, "type": "Manufacturer", "region": "Northeast", "city": "Denver", "onboardingDate": "03-Mar-2019", "managedBy": "Sarah Jenkins", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-011", "name": "Mondelez International", "contact": "Brian Garcia", "email": "orders@mondelez.com", "isExternal": True, "type": "Distributor", "region": "Northeast", "city": "Denver", "onboardingDate": "20-May-2020", "managedBy": "Sarah Jenkins", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-012", "name": "Tyson Foods Distributors", "contact": "Kevin Martinez", "email": "meat@tyson.com", "isExternal": True, "type": "Manufacturer", "region": "Midwest", "city": "Chicago", "onboardingDate": "12-Sep-2019", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-013", "name": "Kellogg Sales Company", "contact": "Rachel Robinson", "email": "cereal@kelloggs.com", "isExternal": True, "type": "Manufacturer", "region": "Midwest", "city": "Chicago", "onboardingDate": "05-Aug-2019", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-014", "name": "Hostess Brands Bakery", "contact": "Jason White", "email": "cakes@hostess.com", "isExternal": True, "type": "Manufacturer", "region": "Northeast", "city": "Denver", "onboardingDate": "14-Feb-2020", "managedBy": "Sarah Jenkins", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-015", "name": "Mars Wrigley Confectionery", "contact": "Lisa Harris", "email": "sweets@mars.com", "isExternal": True, "type": "Manufacturer", "region": "Midwest", "city": "Chicago", "onboardingDate": "10-Oct-2019", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-016", "name": "Valvoline Lubricants NA", "contact": "Daniel Lewis", "email": "commercial@valvoline.com", "isExternal": True, "type": "Manufacturer", "region": "South", "city": "Houston", "onboardingDate": "04-Apr-2021", "managedBy": "Emma Stone", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-017", "name": "Chevron Lubricants USA", "contact": "Thomas Allen", "email": "industrial@chevron.com", "isExternal": True, "type": "Manufacturer", "region": "West", "city": "Los Angeles", "onboardingDate": "08-Dec-2020", "managedBy": "Marcus Vance", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-018", "name": "Shell Lubricants US", "contact": "Sandra King", "email": "fluids@shell.com", "isExternal": True, "type": "Manufacturer", "region": "South", "city": "Houston", "onboardingDate": "15-Jun-2020", "managedBy": "Emma Stone", "contractStatus": "Active", "paymentTerms": "Net 45" },
  { "id": "VND-019", "name": "ExxonMobil Lubricants Co", "contact": "Paul Wright", "email": "lubes@exxonmobil.com", "isExternal": True, "type": "Manufacturer", "region": "South", "city": "Houston", "onboardingDate": "02-Nov-2020", "managedBy": "Emma Stone", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-020", "name": "Procter & Gamble Sales", "contact": "Mark Scott", "email": "orders@pg.com", "isExternal": True, "type": "Manufacturer", "region": "Midwest", "city": "Chicago", "onboardingDate": "18-Sep-2018", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 45" },
  { "id": "VND-021", "name": "Unilever Grocery NA", "contact": "Steven Green", "email": "orders@unilever.com", "isExternal": True, "type": "Distributor", "region": "Midwest", "city": "Chicago", "onboardingDate": "01-Oct-2019", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-022", "name": "Kimberly-Clark Corp", "contact": "Karen Adams", "email": "hygiene@kcc.com", "isExternal": True, "type": "Manufacturer", "region": "Northeast", "city": "Denver", "onboardingDate": "12-Apr-2020", "managedBy": "Sarah Jenkins", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-023", "name": "Colgate-Palmolive Co", "contact": "Donald Baker", "email": "orders@colgate.com", "isExternal": True, "type": "Manufacturer", "region": "Northeast", "city": "Denver", "onboardingDate": "20-May-2020", "managedBy": "Sarah Jenkins", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-024", "name": "Clorox Professional", "contact": "Helen Nelson", "email": "sanitation@clorox.com", "isExternal": True, "type": "Manufacturer", "region": "West", "city": "Los Angeles", "onboardingDate": "10-Jul-2020", "managedBy": "Marcus Vance", "contractStatus": "Active", "paymentTerms": "Net 30" },
  { "id": "VND-025", "name": "Conagra Brands Wholesale", "contact": "Gary Carter", "email": "foods@conagra.com", "isExternal": True, "type": "Distributor", "region": "Midwest", "city": "Chicago", "onboardingDate": "08-Aug-2019", "managedBy": "Alex Rivera", "contractStatus": "Active", "paymentTerms": "Net 30" }
]

# 2. 10 Stores
stores_data = [
  { "id": "BP-CHI-1024", "name": "Loop Connect", "city": "Chicago", "address": "200 N Michigan Ave, Chicago, IL", "contact": "+1 (312) 555-0199", "activeSince": "Oct 2021" },
  { "id": "BP-CHI-1025", "name": "Lincoln Park Connect", "city": "Chicago", "address": "2400 N Halsted St, Chicago, IL", "contact": "+1 (312) 555-0210", "activeSince": "Mar 2022" },
  { "id": "BP-CHI-1026", "name": "Wrigleyville Connect", "city": "Chicago", "address": "3600 N Clark St, Chicago, IL", "contact": "+1 (312) 555-0223", "activeSince": "Jul 2022" },
  { "id": "BP-HOU-1050", "name": "Westheimer Rd ampm", "city": "Houston", "address": "8201 Westheimer Rd, Houston, TX", "contact": "+1 (713) 555-0145", "activeSince": "Jan 2022" },
  { "id": "BP-HOU-1051", "name": "Galleria Connect", "city": "Houston", "address": "5015 Westheimer Rd, Houston, TX", "contact": "+1 (713) 555-0158", "activeSince": "May 2022" },
  { "id": "BP-LAX-1088", "name": "Sunset Blvd Connect", "city": "Los Angeles", "address": "6420 Sunset Blvd, Los Angeles, CA", "contact": "+1 (323) 555-0177", "activeSince": "Apr 2022" },
  { "id": "BP-LAX-1089", "name": "Hollywood Blvd Connect", "city": "Los Angeles", "address": "7000 Hollywood Blvd, Los Angeles, CA", "contact": "+1 (323) 555-0182", "activeSince": "Sep 2022" },
  { "id": "BP-LAX-1090", "name": "Santa Monica ampm", "city": "Los Angeles", "address": "1400 Santa Monica Blvd, Santa Monica, CA", "contact": "+1 (310) 555-0300", "activeSince": "Nov 2022" },
  { "id": "BP-DEN-2001", "name": "Cherry Creek ampm", "city": "Denver", "address": "100 University Blvd, Denver, CO", "contact": "+1 (303) 555-0123", "activeSince": "Jul 2022" },
  { "id": "BP-DEN-2002", "name": "LoDo Connect", "city": "Denver", "address": "1600 Blake St, Denver, CO", "contact": "+1 (303) 555-0138", "activeSince": "Dec 2022" }
]

# 3. Base Products for catalog generation
base_products_list = [
  { "name": "Castrol GTX 5W30", "category": "Automotive", "uom": "Litres", "price": 9.99, "viscosity": "5W-30", "colour": "Golden Amber", "storage": "Shelves / Drums" },
  { "name": "Castrol GTX 10W40", "category": "Automotive", "uom": "Litres", "price": 9.99, "viscosity": "10W-40", "colour": "Golden Amber", "storage": "Shelves / Drums" },
  { "name": "Castrol Edge 5W20 Synthetic", "category": "Automotive", "uom": "Litres", "price": 12.99, "viscosity": "5W-20", "colour": "Light Amber", "storage": "Shelves" },
  { "name": "Castrol Edge 5W30 Full Syn", "category": "Automotive", "uom": "Litres", "price": 12.99, "viscosity": "5W-30", "colour": "Light Amber", "storage": "Shelves" },
  { "name": "Castrol Edge 0W20 Full Syn", "category": "Automotive", "uom": "Litres", "price": 13.49, "viscosity": "0W-20", "colour": "Light Amber", "storage": "Shelves" },
  { "name": "Castrol Transmax ATF Fluid", "category": "Automotive", "uom": "Litres", "price": 11.49, "viscosity": "ATF Fluid", "colour": "Red", "storage": "Drums (200L)" },
  { "name": "BP Coolant Green Pre-mix", "category": "Automotive", "uom": "Litres", "price": 8.99, "viscosity": "Low (Water-like)", "colour": "Fluorescent Green", "storage": "Cans (5L)" },
  { "name": "BP Coolant Orange Concentrate", "category": "Automotive", "uom": "Litres", "price": 10.99, "viscosity": "Low (Water-like)", "colour": "Fluorescent Orange", "storage": "Cans (5L)" },
  { "name": "Valvoline MaxLife 5W30", "category": "Automotive", "uom": "Litres", "price": 11.99, "viscosity": "5W-30", "colour": "Golden", "storage": "Shelves" },
  { "name": "Mobil 1 Extended Performance", "category": "Automotive", "uom": "Litres", "price": 14.99, "viscosity": "5W-30", "colour": "Amber", "storage": "Shelves" },
  { "name": "Shell Rotella T4 15W40", "category": "Automotive", "uom": "Litres", "price": 10.49, "viscosity": "15W-40", "colour": "Brownish Golden", "storage": "Drums (200L)" },
  { "name": "Brake Fluid DOT 4 Heavy", "category": "Automotive", "uom": "Litres", "price": 7.49, "viscosity": "Low", "colour": "Pale Yellow", "storage": "Bottles (1L)" },
  
  { "name": "Coca-Cola 20oz Bottle", "category": "Beverage", "uom": "Units", "price": 2.29, "viscosity": "N/A", "colour": "Dark Brown", "storage": "Cooler A" },
  { "name": "Coca-Cola Zero Sugar 20oz", "category": "Beverage", "uom": "Units", "price": 2.29, "viscosity": "N/A", "colour": "Dark Brown", "storage": "Cooler A" },
  { "name": "Diet Coke 20oz Bottle", "category": "Beverage", "uom": "Units", "price": 2.29, "viscosity": "N/A", "colour": "Dark Brown", "storage": "Cooler A" },
  { "name": "Sprite 20oz Bottle", "category": "Beverage", "uom": "Units", "price": 2.29, "viscosity": "N/A", "colour": "Clear", "storage": "Cooler A" },
  { "name": "Fanta Orange 20oz Bottle", "category": "Beverage", "uom": "Units", "price": 2.29, "viscosity": "N/A", "colour": "Bright Orange", "storage": "Cooler A" },
  { "name": "Monster Energy Original 16oz", "category": "Beverage", "uom": "Units", "price": 3.49, "viscosity": "N/A", "colour": "Greenish Gold", "storage": "Cooler B" },
  { "name": "Monster Ultra White SugarFree", "category": "Beverage", "uom": "Units", "price": 3.49, "viscosity": "N/A", "colour": "Cloudy White", "storage": "Cooler B" },
  { "name": "Red Bull Energy Drink 12oz", "category": "Beverage", "uom": "Units", "price": 3.99, "viscosity": "N/A", "colour": "Light Amber", "storage": "Cooler B" },
  { "name": "SmartWater Vapor Distilled 1L", "category": "Beverage", "uom": "Units", "price": 2.79, "viscosity": "N/A", "colour": "Clear", "storage": "Cooler C" },
  { "name": "Dr Pepper 20oz Bottle", "category": "Beverage", "uom": "Units", "price": 2.29, "viscosity": "N/A", "colour": "Dark Reddish Brown", "storage": "Cooler C" },
  { "name": "Gatorade Cool Blue 24oz", "category": "Beverage", "uom": "Units", "price": 2.49, "viscosity": "N/A", "colour": "Bright Blue", "storage": "Cooler D" },
  { "name": "Gatorade Lemon Lime 24oz", "category": "Beverage", "uom": "Units", "price": 2.49, "viscosity": "N/A", "colour": "Yellow-Green", "storage": "Cooler D" },
  
  { "name": "Doritos Nacho Cheese 9oz", "category": "Food", "uom": "Units", "price": 4.99, "viscosity": "N/A", "colour": "Orange", "storage": "Aisle 1" },
  { "name": "Doritos Cool Ranch 9oz", "category": "Food", "uom": "Units", "price": 4.99, "viscosity": "N/A", "colour": "White-dusted", "storage": "Aisle 1" },
  { "name": "Lay's Classic Potato Chips 8oz", "category": "Food", "uom": "Units", "price": 4.49, "viscosity": "N/A", "colour": "Pale Yellow", "storage": "Aisle 1" },
  { "name": "Lay's Sour Cream & Onion 8oz", "category": "Food", "uom": "Units", "price": 4.49, "viscosity": "N/A", "colour": "Speckled Green", "storage": "Aisle 1" },
  { "name": "Lay's Barbecue Chips 8oz", "category": "Food", "uom": "Units", "price": 4.49, "viscosity": "N/A", "colour": "Reddish Brown", "storage": "Aisle 1" },
  { "name": "Pringles Sour Cream & Onion", "category": "Food", "uom": "Units", "price": 2.49, "viscosity": "N/A", "colour": "Cream", "storage": "Aisle 2" },
  { "name": "Cheetos Crunchy Cheese 8.5oz", "category": "Food", "uom": "Units", "price": 4.79, "viscosity": "N/A", "colour": "Neon Orange", "storage": "Aisle 2" },
  { "name": "Snickers Chocolate Bar Standard", "category": "Food", "uom": "Units", "price": 1.89, "viscosity": "N/A", "colour": "Brown", "storage": "Register Rack" },
  { "name": "Reese's Peanut Butter Cups Std", "category": "Food", "uom": "Units", "price": 1.89, "viscosity": "N/A", "colour": "Light Brown", "storage": "Register Rack" },
  { "name": "M&M Peanut Candy King Size", "category": "Food", "uom": "Units", "price": 2.49, "viscosity": "N/A", "colour": "Multi-colour", "storage": "Register Rack" },
  { "name": "Kit Kat Crisp Wafer Standard", "category": "Food", "uom": "Units", "price": 1.89, "viscosity": "N/A", "colour": "Dark Brown", "storage": "Register Rack" },
  
  { "name": "Whole Milk Gallon Jug", "category": "Grocery", "uom": "Litres", "price": 3.99, "viscosity": "N/A", "colour": "White", "storage": "Dairy Cooler" },
  { "name": "2% Reduced Fat Milk Gallon", "category": "Grocery", "uom": "Litres", "price": 3.99, "viscosity": "N/A", "colour": "White", "storage": "Dairy Cooler" },
  { "name": "Wonder Bread White Loaf 20oz", "category": "Grocery", "uom": "Units", "price": 2.99, "viscosity": "N/A", "colour": "White/Brown Crust", "storage": "Bread Stand" },
  { "name": "Grade A Large White Eggs Dozen", "category": "Grocery", "uom": "Units", "price": 4.29, "viscosity": "N/A", "colour": "White", "storage": "Dairy Cooler" },
  { "name": "Land O Lakes Salted Butter 1lb", "category": "Grocery", "uom": "Kilograms", "price": 5.49, "viscosity": "N/A", "colour": "Yellow", "storage": "Dairy Cooler" },
  { "name": "Campbell Soup Chicken Noodle", "category": "Grocery", "uom": "Units", "price": 1.69, "viscosity": "Medium", "colour": "Yellowish", "storage": "Aisle 3" },
  { "name": "Tide Liquid Laundry Detergent", "category": "Grocery", "uom": "Litres", "price": 11.99, "viscosity": "Viscous Liquid", "colour": "Blue", "storage": "Aisle 4" },
  { "name": "Colgate Total Toothpaste 5oz", "category": "Grocery", "uom": "Units", "price": 3.89, "viscosity": "Paste", "colour": "White-Blue Striped", "storage": "Aisle 4" },
  { "name": "Dawn Platinum Dish Soap 16oz", "category": "Grocery", "uom": "Litres", "price": 3.49, "viscosity": "Viscous", "colour": "Deep Blue", "storage": "Aisle 4" }
]

def generate_master_products() -> List[Dict[str, Any]]:
    products = []
    for i in range(150):
        base = base_products_list[i % len(base_products_list)]
        size_multiplier = (i // len(base_products_list)) + 1
        
        size_tag = ""
        price_adj = 0.0
        code = f"BP-PROD-{str(i + 1).zfill(3)}"
        
        if base["uom"] == "Litres":
            if size_multiplier == 1:
                size_tag = " (1 Quart)"
                price_adj = 0.0
            elif size_multiplier == 2:
                size_tag = " (5 Quart Jug)"
                price_adj = 25.00
            else:
                size_tag = " (1 Gallon)"
                price_adj = 18.00
        elif base["category"] == "Beverage":
            if size_multiplier == 1:
                size_tag = ""
                price_adj = 0.0
            elif size_multiplier == 2:
                size_tag = " 12-Pack Cans"
                price_adj = 5.50
            else:
                size_tag = " 2-Litre Bottle"
                price_adj = 0.80
        elif base["category"] == "Food":
            if size_multiplier == 1:
                size_tag = ""
                price_adj = 0.0
            elif size_multiplier == 2:
                size_tag = " Family Size Bag"
                price_adj = 2.50
            else:
                size_tag = " Sharing Size Bar"
                price_adj = 1.00
        else:
            if size_multiplier == 1:
                size_tag = ""
                price_adj = 0.0
            else:
                size_tag = " Value Pack"
                price_adj = 4.00
                
        vendor_index = i % len(vendors_data)
        products.append({
            "code": code,
            "name": f"{base['name']}{size_tag}",
            "category": base["category"],
            "uom": base["uom"],
            "unitPrice": round(base["price"] + price_adj, 2),
            "storageLocation": base["storage"],
            "rol": int(15 + (get_seed_hash(code) % 35)),
            "roq": int(50 + (get_seed_hash(code) % 150)),
            "colour": base["colour"],
            "viscosity": base["viscosity"],
            "vendorId": vendors_data[vendor_index]["id"],
            "leadTimeDays": int(1 + (get_seed_hash(code) % 4))
        })
    return products

async def seed_convenience_data():
    # Check if we need to migrate/re-seed stores to include products dict
    first_store = await stores_collection.find_one({})
    if first_store and "products" not in first_store:
        print("Migrating/re-seeding stores and inventory collections to include products dictionary...")
        await stores_collection.drop()
        await inventory_collection.drop()

    # Generate master products first
    products = generate_master_products()

    # 1. Seed Stores
    stores_count = await stores_collection.count_documents({})
    if stores_count == 0:
        # Compute store products dictionary for each store
        for store in stores_data:
            store_seed = get_seed_hash(store["id"])
            target_count = 100 + (store_seed % 41)
            seen_codes = set()
            for i in range(target_count):
                product_idx = (store_seed + i * 7) % len(products)
                seen_codes.add(products[product_idx]["code"])
            store["products"] = {code: True for code in seen_codes}
        await stores_collection.insert_many(stores_data)
        print("Seeded Stores database successfully.")
        
    # 2. Seed Vendors
    vendors_count = await vendors_collection.count_documents({})
    if vendors_count == 0:
        await vendors_collection.insert_many(vendors_data)
        print("Seeded Vendors database successfully.")

    # 3. Seed Products
    products_count = await products_collection.count_documents({})
    if products_count == 0:
        await products_collection.insert_many(products)
        print("Seeded Master Products successfully.")

    # 4. Seed Inventory Records
    inventory_count = await inventory_collection.count_documents({})
    if inventory_count == 0:
        inventory_items = []
        for store in stores_data:
            store_id = store["id"]
            store_seed = get_seed_hash(store_id)
            target_count = 100 + (store_seed % 41)
            
            seen_codes = set()
            for i in range(target_count):
                product_idx = (store_seed + i * 7) % len(products)
                product = products[product_idx]
                
                if product["code"] in seen_codes:
                    continue
                seen_codes.add(product["code"])
                
                item_seed = get_seed_hash(store_id + product["code"])
                
                avg_consumption = 1.5 + (item_seed % 10)
                if product["category"] == "Beverage":
                    avg_consumption = 20.0 + (item_seed % 40)
                elif product["category"] == "Food":
                    avg_consumption = 10.0 + (item_seed % 25)
                    
                avg_consumption = round(avg_consumption, 1)
                
                # Check for LA non-risk store
                if store_id == "BP-LAX-1090":
                    current_stock = int(round(avg_consumption * (15 + (item_seed % 15))))
                else:
                    is_regional_shortage = product["code"] in ("BP-PROD-001", "BP-PROD-002", "BP-PROD-003", "BP-PROD-004")
                    if is_regional_shortage:
                        city_demand_skew = len(store["city"])
                        shortage_coverage = int(1 + ((item_seed + store_seed + product_idx + city_demand_skew) % 6))
                        current_stock = max(1, int(round(avg_consumption * shortage_coverage)))
                    elif i < 8:
                        local_coverage = int(1 + ((item_seed + store_seed + i) % 6))
                        current_stock = max(1, int(round(avg_consumption * local_coverage)))
                    else:
                        current_stock = int(round(avg_consumption * (5 + (item_seed % 25))))
                
                # Safety stock, ROL, ROQ
                safety_stock_level = int(math.ceil(avg_consumption * 0.5 * product["leadTimeDays"]))
                derived_rol = int(math.ceil(avg_consumption * product["leadTimeDays"]) + safety_stock_level)
                derived_roq = int(round(avg_consumption * 15))
                
                # Days to stockout
                days_to_stockout = current_stock / avg_consumption if avg_consumption > 0 else 999.0
                days_int = int(math.floor(days_to_stockout))
                
                # Predict stockout date (relative to planning baseline 07-07-2026)
                base_date = datetime(2026, 7, 7)
                stockout_date_obj = base_date + timedelta(days=days_int)
                predicted_stockout_date = stockout_date_obj.strftime("%d-%m-%Y")
                
                # Order by date
                order_by_date_obj = stockout_date_obj - timedelta(days=product["leadTimeDays"])
                order_by_date = order_by_date_obj.strftime("%d-%m-%Y")
                
                # PR/MR Status
                pr_mr_status = "Monitor"
                if current_stock <= derived_rol:
                    pr_mr_status = "PR"
                elif current_stock <= (derived_rol + avg_consumption * 3):
                    pr_mr_status = "MR"
                    
                # Risk Level
                risk_level = "Low"
                if days_to_stockout <= 7:
                    risk_level = "High"
                elif days_to_stockout <= 15:
                    risk_level = "Medium"
                    
                service_level = int(90 + (item_seed % 10))
                
                # Assemble record
                inv_item = {
                    "storeId": store_id,
                    "code": product["code"],
                    "name": product["name"],
                    "category": product["category"],
                    "uom": product["uom"],
                    "unitPrice": product["unitPrice"],
                    "storageLocation": product["storageLocation"],
                    "rol": product["rol"],
                    "roq": product["roq"],
                    "colour": product["colour"],
                    "viscosity": product["viscosity"],
                    "vendorId": product["vendorId"],
                    "leadTimeDays": product["leadTimeDays"],
                    "currentStock": current_stock,
                    "safetyStockLevel": safety_stock_level,
                    "predictedStockoutDate": predicted_stockout_date,
                    "avgDailyConsumption": avg_consumption,
                    "recommendedRoq": derived_roq,
                    "orderByDate": order_by_date,
                    "prMrStatus": pr_mr_status,
                    "riskLevel": risk_level,
                    "serviceLevel": service_level
                }
                inventory_items.append(inv_item)
                
        if inventory_items:
            await inventory_collection.insert_many(inventory_items)
            print(f"Seeded {len(inventory_items)} Store Inventory records successfully.")

        # 5. Seed Purchase Orders, Issues, and Recommendations
        po_count = await purchase_orders_collection.count_documents({})
        if po_count == 0:
            print("Seeding Purchase Orders, Issues, and Recommendations...")
            purchase_orders = []
            issues = []
            recommendations = []
            
            today = datetime(2026, 7, 8)
            statuses = ["Pending Approval", "Pending Review", "Returned", "Approved", "In Transit", "Delivered", "Delivered", "Delivered", "Delayed", "Cancelled"]
            
            for vendor in vendors_data:
                vendor_id = vendor["id"]
                vendor_name = vendor["name"]
                
                # Find products for this vendor
                v_products = [p for p in products_data if p["vendorId"] == vendor_id]
                if not v_products:
                    continue
                    
                po_count_for_vendor = 4 + (get_seed_hash(vendor_id) % 8)
                is_chicago = vendor["city"].lower() == "chicago"
                
                for i in range(po_count_for_vendor):
                    p_idx = (get_seed_hash(vendor_id) + i) % len(v_products)
                    prod = v_products[p_idx]
                    seed = get_seed_hash(f"{vendor_id}_{prod['code']}_{i}")
                    
                    status = statuses[seed % len(statuses)]
                    expected_date = today + timedelta(days=(seed % 14) - 7)
                    
                    if is_chicago and i == 0:
                        status = "Delayed"
                        expected_date = today - timedelta(days=2)
                    elif is_chicago and i == 1:
                        status = "Pending Approval"
                        
                    purchase_orders.append({
                        "id": f"PO-{10000 + len(purchase_orders) * 7}",
                        "vendorId": vendor_id,
                        "vendorName": vendor_name,
                        "items": [{"name": prod["name"], "quantity": (seed % 10 + 1) * 100}],
                        "totalAmount": round(((seed % 10 + 1) * 100) * prod["unitPrice"], 2),
                        "status": status,
                        "orderDate": (expected_date - timedelta(days=prod["leadTimeDays"] + 2)).strftime("%Y-%m-%d"),
                        "expectedDeliveryDate": expected_date.strftime("%Y-%m-%d")
                    })
                    
            # Generate Issues
            issue_types = ["Delivery delayed by 2 days", "Fill Rate below SLA", "Invoice mismatch", "Quality control failure", "Missing documentation"]
            severities = ["High", "Medium", "Low", "High", "Medium"]
            
            for v_idx, vendor in enumerate(vendors_data):
                seed = get_seed_hash(vendor["id"] + "issue")
                is_chicago = vendor["city"].lower() == "chicago"
                
                if seed % 3 == 0 or (is_chicago and v_idx % 2 == 0):
                    issue_idx = 0 if (is_chicago and v_idx % 2 == 0) else (seed % len(issue_types))
                    issues.append({
                        "id": f"ISSUE-{1000 + v_idx}",
                        "vendorId": vendor["id"],
                        "vendorName": vendor["name"],
                        "issueType": issue_types[issue_idx],
                        "description": f"Vendor has reported {issue_types[issue_idx].lower()}.",
                        "dateReported": (today - timedelta(days=(seed % 5))).strftime("%Y-%m-%d"),
                        "status": "Open",
                        "priority": severities[issue_idx],
                        "relatedPO": f"PO-{10000 + v_idx * 100}"
                    })
                    
            # Generate Recommendations
            recommendations.extend([
                {
                    "id": "REC-1",
                    "type": "Vendor Consolidation",
                    "description": f"Consolidating orders from {vendors_data[0]['name']} could save 8% in logistics.",
                    "actionLabel": "Review Consolidation",
                    "priority": "High"
                },
                {
                    "id": "REC-2",
                    "type": "SLA Alert",
                    "description": f"Chicago supplier {vendors_data[6]['name']} is trending below 90% On-Time Delivery.",
                    "actionLabel": "Send Warning",
                    "priority": "High"
                },
                {
                    "id": "REC-3",
                    "type": "Cost Optimization",
                    "description": f"New bulk discount available for {products_data[0]['name']}.",
                    "actionLabel": "View Discount",
                    "priority": "Medium"
                }
            ])
            
            if purchase_orders:
                await purchase_orders_collection.insert_many(purchase_orders)
            if issues:
                await vendor_issues_collection.insert_many(issues)
            if recommendations:
                await recommendations_collection.insert_many(recommendations)
                
            print(f"Seeded {len(purchase_orders)} POs, {len(issues)} Issues, and {len(recommendations)} Recommendations successfully.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_convenience_data())

