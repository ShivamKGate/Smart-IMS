from database.db import SessionLocal, Category, Product, Warehouse, Inventory, Supplier

def seed_database():
    """Populate the database with sample data for testing"""
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - remove if you want to keep existing data)
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.query(Category).delete()
        db.query(Warehouse).delete()
        db.query(Supplier).delete()
        
        # Create categories
        categories = [
            Category(name="Electronics"),
            Category(name="Clothing"),
            Category(name="Home & Garden"),
            Category(name="Sports & Outdoors"),
            Category(name="Books")
        ]
        db.add_all(categories)
        db.commit()
        
        # Create warehouses
        warehouses = [
            Warehouse(location="Main Warehouse - Downtown"),
            Warehouse(location="North Branch"),
            Warehouse(location="South Distribution Center")
        ]
        db.add_all(warehouses)
        db.commit()
        
        # Create suppliers
        suppliers = [
            Supplier(name="TechSupply Co", contact="tech@supply.com"),
            Supplier(name="Fashion Distributors", contact="orders@fashion.com"),
            Supplier(name="HomeGoods Inc", contact="wholesale@homegoods.com"),
            Supplier(name="SportWorld", contact="sales@sportworld.com"),
            Supplier(name="BookSource", contact="orders@booksource.com")
        ]
        db.add_all(suppliers)
        db.commit()
        
        # Create products
        products = [
            # Electronics
            Product(name="Laptop", category_id=1, price=999.99, reorder_level=10),
            Product(name="Smartphone", category_id=1, price=699.99, reorder_level=15),
            Product(name="Tablet", category_id=1, price=399.99, reorder_level=12),
            Product(name="Headphones", category_id=1, price=149.99, reorder_level=25),
            
            # Clothing
            Product(name="T-Shirt", category_id=2, price=19.99, reorder_level=50),
            Product(name="Jeans", category_id=2, price=79.99, reorder_level=30),
            Product(name="Sneakers", category_id=2, price=129.99, reorder_level=20),
            
            # Home & Garden
            Product(name="Coffee Maker", category_id=3, price=89.99, reorder_level=15),
            Product(name="Garden Hose", category_id=3, price=24.99, reorder_level=20),
            Product(name="Dining Chair", category_id=3, price=159.99, reorder_level=8),
            
            # Sports & Outdoors
            Product(name="Basketball", category_id=4, price=29.99, reorder_level=30),
            Product(name="Tent", category_id=4, price=249.99, reorder_level=5),
            Product(name="Hiking Boots", category_id=4, price=179.99, reorder_level=12),
            
            # Books
            Product(name="Programming Guide", category_id=5, price=49.99, reorder_level=25),
            Product(name="Fiction Novel", category_id=5, price=14.99, reorder_level=40)
        ]
        db.add_all(products)
        db.commit()
        
        # Create inventory (some items will be low stock for testing)
        inventory_items = [
            # Main Warehouse
            Inventory(product_id=1, warehouse_id=1, quantity=15),  # Laptop - OK
            Inventory(product_id=2, warehouse_id=1, quantity=8),   # Smartphone - LOW
            Inventory(product_id=3, warehouse_id=1, quantity=20),  # Tablet - OK
            Inventory(product_id=4, warehouse_id=1, quantity=35),  # Headphones - OK
            Inventory(product_id=5, warehouse_id=1, quantity=45),  # T-Shirt - LOW
            Inventory(product_id=6, warehouse_id=1, quantity=25),  # Jeans - LOW
            Inventory(product_id=7, warehouse_id=1, quantity=22),  # Sneakers - OK
            Inventory(product_id=8, warehouse_id=1, quantity=18),  # Coffee Maker - OK
            
            # North Branch
            Inventory(product_id=1, warehouse_id=2, quantity=5),   # Laptop - LOW
            Inventory(product_id=2, warehouse_id=2, quantity=12),  # Smartphone - LOW
            Inventory(product_id=9, warehouse_id=2, quantity=25),  # Garden Hose - OK
            Inventory(product_id=10, warehouse_id=2, quantity=6),  # Dining Chair - LOW
            Inventory(product_id=11, warehouse_id=2, quantity=28), # Basketball - LOW
            Inventory(product_id=12, warehouse_id=2, quantity=3),  # Tent - LOW
            
            # South Distribution Center
            Inventory(product_id=3, warehouse_id=3, quantity=8),   # Tablet - LOW
            Inventory(product_id=4, warehouse_id=3, quantity=40),  # Headphones - OK
            Inventory(product_id=13, warehouse_id=3, quantity=10), # Hiking Boots - LOW
            Inventory(product_id=14, warehouse_id=3, quantity=30), # Programming Guide - OK
            Inventory(product_id=15, warehouse_id=3, quantity=35), # Fiction Novel - LOW
        ]
        
        db.add_all(inventory_items)
        db.commit()
        
        print("✅ Database seeded successfully!")
        print("\nSample data created:")
        print(f"- {len(categories)} categories")
        print(f"- {len(warehouses)} warehouses")
        print(f"- {len(suppliers)} suppliers")
        print(f"- {len(products)} products")
        print(f"- {len(inventory_items)} inventory entries")
        print("\nSome items have been set to low stock for testing purposes.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_database() 