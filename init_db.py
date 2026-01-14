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
            
            # sandwiches
            MenuItem(item_name="Chicken Sandwich", price=6.99, category="Sandwich", is_available=1),
            MenuItem(item_name="Turkey Sandwich", price=7.49, category="Sandwich", is_available=1),
            MenuItem(item_name="Veggie Sandwich", price=6.49, category="Sandwich", is_available=1),
            MenuItem(item_name="BLT Sandwich", price=7.99, category="Sandwich", is_available=1),

            #Fries
            MenuItem(item_name="Regular Fries", price=2.99, category="Fries", is_available=1),
            MenuItem(item_name="Cheese Fries", price=3.99, category="Fries", is_available=1),
            MenuItem(item_name="Bacon Fries", price=4.49, category="Fries", is_available=1),
            MenuItem(item_name="Sweet Potato Fries", price=3.49, category="Fries", is_available=1),

            #Rice
            MenuItem(item_name="Steamed Rice", price=2.49, category="Rice", is_available=1),
            MenuItem(item_name="Fried Rice", price=4.99, category="Rice", is_available=1),
            MenuItem(item_name="Rice Bowl with Chicken", price=6.99, category="Rice", is_available=1),
            MenuItem(item_name="Rice Bowl with Veggies", price=6.49, category="Rice", is_available=1),

            #Biriyani
            MenuItem(item_name="Chicken Biriyani", price=9.99, category="Biriyani", is_available=1),
            MenuItem(item_name="Mutton Biriyani", price=11.99, category="Biriyani", is_available=1),
            MenuItem(item_name="Veggie Biriyani", price=8.99, category="Biriyani", is_available=1),
            MenuItem(item_name="Egg Biriyani", price=9.49, category="Biriyani", is_available=1),

            #Cola
            MenuItem(item_name="Coca Cola", price=1.99, category="Cola", is_available=1),
            MenuItem(item_name="Pepsi", price=1.99, category="Cola", is_available=1),
            MenuItem(item_name="Sprite", price=1.99, category="Cola", is_available=1),
            MenuItem(item_name="Fanta", price=1.99, category="Cola", is_available=1),

            #Noodles
            MenuItem(item_name="Chicken Noodles", price=5.99, category="Noodles", is_available=1),
            MenuItem(item_name="Veggie Noodles", price=5.49, category="Noodles", is_available=1),
            MenuItem(item_name="Shrimp Noodles", price=6.99, category="Noodles", is_available=1),
            MenuItem(item_name="Beef Noodles", price=6.49, category="Noodles", is_available=1),

            #Ice Cream
            MenuItem(item_name="Vanilla Ice Cream", price=2.99, category="Ice Cream", is_available=1),
            MenuItem(item_name="Chocolate Ice Cream", price=2.99, category="Ice Cream", is_available=1),
            MenuItem(item_name="Strawberry Ice Cream", price=2.99, category ="Ice Cream", is_available=1),
            MenuItem(item_name="Mint Ice Cream", price=2.99, category="Ice Cream", is_available=1),
           
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
