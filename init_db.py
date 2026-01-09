"""
Database initialization script
Run this script to create tables and populate initial data
"""
from database import init_db, engine, SessionLocal
from models import MenuItem, Base
from sqlalchemy import text


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    init_db()


def populate_menu_items():
    """Populate menu with sample food items"""
    db = SessionLocal()
    
    try:
        # Check if menu items already exist
        existing_items = db.query(MenuItem).count()
        
        if existing_items > 0:
            print(f"Menu already has {existing_items} items. Skipping population.")
            return
        
        # Sample menu items
        menu_items = [
            # Pizzas
            MenuItem(item_name="Margherita Pizza", price=8.99, category="Pizza", is_available=1),
            MenuItem(item_name="Pepperoni Pizza", price=10.99, category="Pizza", is_available=1),
            MenuItem(item_name="Veggie Pizza", price=9.99, category="Pizza", is_available=1),
            MenuItem(item_name="BBQ Chicken Pizza", price=11.99, category="Pizza", is_available=1),
            
            # Burgers
            MenuItem(item_name="Classic Burger", price=7.99, category="Burger", is_available=1),
            MenuItem(item_name="Cheese Burger", price=8.99, category="Burger", is_available=1),
            MenuItem(item_name="Veggie Burger", price=7.49, category="Burger", is_available=1),
            MenuItem(item_name="Bacon Burger", price=9.99, category="Burger", is_available=1),
            
            # Pasta
            MenuItem(item_name="Spaghetti Carbonara", price=12.99, category="Pasta", is_available=1),
            MenuItem(item_name="Penne Arrabbiata", price=11.99, category="Pasta", is_available=1),
            MenuItem(item_name="Fettuccine Alfredo", price=13.99, category="Pasta", is_available=1),
            
            # Sides
            MenuItem(item_name="French Fries", price=3.99, category="Sides", is_available=1),
            MenuItem(item_name="Garlic Bread", price=4.99, category="Sides", is_available=1),
            MenuItem(item_name="Onion Rings", price=4.49, category="Sides", is_available=1),
            MenuItem(item_name="Caesar Salad", price=5.99, category="Sides", is_available=1),
            
            # Drinks
            MenuItem(item_name="Coca Cola", price=1.99, category="Drinks", is_available=1),
            MenuItem(item_name="Pepsi", price=1.99, category="Drinks", is_available=1),
            MenuItem(item_name="Orange Juice", price=2.99, category="Drinks", is_available=1),
            MenuItem(item_name="Water", price=0.99, category="Drinks", is_available=1),
            
            # Desserts
            MenuItem(item_name="Chocolate Cake", price=5.99, category="Desserts", is_available=1),
            MenuItem(item_name="Ice Cream", price=3.99, category="Desserts", is_available=1),
            MenuItem(item_name="Cheesecake", price=6.99, category="Desserts", is_available=1),
        ]
        
        # Add all items to database
        db.add_all(menu_items)
        db.commit()
        
        print(f"✓ Successfully added {len(menu_items)} menu items to the database")
        
    except Exception as e:
        print(f"Error populating menu items: {str(e)}")
        db.rollback()
    finally:
        db.close()


def reset_database():
    """Drop and recreate all tables (use with caution!)"""
    print("WARNING: This will delete all data!")
    response = input("Are you sure you want to reset the database? (yes/no): ")
    
    if response.lower() == 'yes':
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("Recreating tables...")
        create_tables()
        print("✓ Database reset complete")
    else:
        print("Database reset cancelled")


def main():
    """Main initialization function"""
    print("=" * 50)
    print("Food Ordering Chatbot - Database Setup")
    print("=" * 50)
    
    # Create tables
    create_tables()
    
    # Populate menu items
    populate_menu_items()
    
    print("=" * 50)
    print("✓ Database initialization complete!")
    print("=" * 50)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        main()
