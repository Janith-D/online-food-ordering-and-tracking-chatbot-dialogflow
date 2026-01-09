"""
Database management utilities
Provides helper functions for database operations
"""
from sqlalchemy.orm import Session
from models import Order, OrderItem, MenuItem, OrderStatus
from database import SessionLocal
from typing import List, Optional
from datetime import datetime


def add_menu_item(item_name: str, price: float, category: str = None) -> bool:
    """Add a new menu item"""
    db = SessionLocal()
    try:
        # Check if item already exists
        existing = db.query(MenuItem).filter(MenuItem.item_name == item_name).first()
        if existing:
            print(f"Menu item '{item_name}' already exists")
            return False
        
        menu_item = MenuItem(
            item_name=item_name,
            price=price,
            category=category,
            is_available=1
        )
        db.add(menu_item)
        db.commit()
        print(f"✓ Added menu item: {item_name} - ${price}")
        return True
    except Exception as e:
        print(f"Error adding menu item: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def update_menu_item_price(item_name: str, new_price: float) -> bool:
    """Update price of a menu item"""
    db = SessionLocal()
    try:
        menu_item = db.query(MenuItem).filter(MenuItem.item_name == item_name).first()
        if not menu_item:
            print(f"Menu item '{item_name}' not found")
            return False
        
        old_price = menu_item.price
        menu_item.price = new_price
        db.commit()
        print(f"✓ Updated {item_name}: ${old_price} → ${new_price}")
        return True
    except Exception as e:
        print(f"Error updating menu item: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def toggle_menu_item_availability(item_name: str) -> bool:
    """Toggle availability of a menu item"""
    db = SessionLocal()
    try:
        menu_item = db.query(MenuItem).filter(MenuItem.item_name == item_name).first()
        if not menu_item:
            print(f"Menu item '{item_name}' not found")
            return False
        
        menu_item.is_available = 1 if menu_item.is_available == 0 else 0
        status = "available" if menu_item.is_available == 1 else "unavailable"
        db.commit()
        print(f"✓ {item_name} is now {status}")
        return True
    except Exception as e:
        print(f"Error toggling availability: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def list_all_menu_items(category: str = None) -> List[MenuItem]:
    """List all menu items, optionally filtered by category"""
    db = SessionLocal()
    try:
        query = db.query(MenuItem)
        if category:
            query = query.filter(MenuItem.category == category)
        
        items = query.all()
        
        print(f"\n{'='*60}")
        print(f"Menu Items" + (f" - {category}" if category else ""))
        print(f"{'='*60}")
        
        for item in items:
            status = "✓" if item.is_available else "✗"
            print(f"{status} {item.item_name:<30} ${item.price:>6.2f}  [{item.category}]")
        
        print(f"{'='*60}")
        print(f"Total items: {len(items)}")
        
        return items
    finally:
        db.close()


def get_order_details(order_id: int) -> Optional[Order]:
    """Get detailed information about an order"""
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            print(f"Order {order_id} not found")
            return None
        
        print(f"\n{'='*60}")
        print(f"Order Details - ID: {order_id}")
        print(f"{'='*60}")
        print(f"Status:       {order.order_status.value}")
        print(f"Date:         {order.order_date}")
        print(f"Total Amount: ${order.total_amount:.2f}")
        print(f"\nItems:")
        
        for item in order.items:
            print(f"  - {item.item_name:<30} x{item.quantity}  ${item.price * item.quantity:.2f}")
        
        print(f"{'='*60}\n")
        
        return order
    finally:
        db.close()


def update_order_status(order_id: int, new_status: str) -> bool:
    """Update the status of an order"""
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            print(f"Order {order_id} not found")
            return False
        
        # Convert string to OrderStatus enum
        try:
            status_enum = OrderStatus[new_status.upper().replace(" ", "_")]
        except KeyError:
            print(f"Invalid status: {new_status}")
            print(f"Valid statuses: {[s.name for s in OrderStatus]}")
            return False
        
        old_status = order.order_status.value
        order.order_status = status_enum
        db.commit()
        print(f"✓ Order {order_id} status: {old_status} → {status_enum.value}")
        return True
    except Exception as e:
        print(f"Error updating order status: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def list_recent_orders(limit: int = 10) -> List[Order]:
    """List recent orders"""
    db = SessionLocal()
    try:
        orders = db.query(Order).order_by(Order.order_date.desc()).limit(limit).all()
        
        print(f"\n{'='*60}")
        print(f"Recent Orders (Last {limit})")
        print(f"{'='*60}")
        print(f"{'ID':<6} {'Status':<20} {'Total':<10} {'Date'}")
        print(f"{'-'*60}")
        
        for order in orders:
            print(f"{order.order_id:<6} {order.order_status.value:<20} ${order.total_amount:<9.2f} {order.order_date}")
        
        print(f"{'='*60}\n")
        
        return orders
    finally:
        db.close()


def get_sales_summary():
    """Get sales summary statistics"""
    db = SessionLocal()
    try:
        total_orders = db.query(Order).count()
        total_revenue = db.query(Order).with_entities(Order.total_amount).all()
        total_revenue = sum(order[0] for order in total_revenue)
        
        print(f"\n{'='*60}")
        print(f"Sales Summary")
        print(f"{'='*60}")
        print(f"Total Orders:    {total_orders}")
        print(f"Total Revenue:   ${total_revenue:.2f}")
        print(f"Average Order:   ${total_revenue/total_orders if total_orders > 0 else 0:.2f}")
        print(f"{'='*60}\n")
        
        # Orders by status
        print("Orders by Status:")
        for status in OrderStatus:
            count = db.query(Order).filter(Order.order_status == status).count()
            print(f"  {status.value:<20} {count}")
        
        print(f"{'='*60}\n")
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Database Management Utilities")
        print("=" * 60)
        print("\nUsage:")
        print("  python db_utils.py list_menu [category]")
        print("  python db_utils.py add_item <name> <price> [category]")
        print("  python db_utils.py update_price <name> <new_price>")
        print("  python db_utils.py toggle_item <name>")
        print("  python db_utils.py get_order <order_id>")
        print("  python db_utils.py update_status <order_id> <status>")
        print("  python db_utils.py recent_orders [limit]")
        print("  python db_utils.py sales_summary")
        print("\nExamples:")
        print('  python db_utils.py add_item "Hawaiian Pizza" 12.99 Pizza')
        print('  python db_utils.py update_price "Hawaiian Pizza" 13.99')
        print('  python db_utils.py toggle_item "Hawaiian Pizza"')
        print('  python db_utils.py update_status 1 PREPARING')
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "list_menu":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        list_all_menu_items(category)
    
    elif command == "add_item":
        if len(sys.argv) < 4:
            print("Usage: python db_utils.py add_item <name> <price> [category]")
        else:
            name = sys.argv[2]
            price = float(sys.argv[3])
            category = sys.argv[4] if len(sys.argv) > 4 else None
            add_menu_item(name, price, category)
    
    elif command == "update_price":
        if len(sys.argv) < 4:
            print("Usage: python db_utils.py update_price <name> <new_price>")
        else:
            name = sys.argv[2]
            price = float(sys.argv[3])
            update_menu_item_price(name, price)
    
    elif command == "toggle_item":
        if len(sys.argv) < 3:
            print("Usage: python db_utils.py toggle_item <name>")
        else:
            name = sys.argv[2]
            toggle_menu_item_availability(name)
    
    elif command == "get_order":
        if len(sys.argv) < 3:
            print("Usage: python db_utils.py get_order <order_id>")
        else:
            order_id = int(sys.argv[2])
            get_order_details(order_id)
    
    elif command == "update_status":
        if len(sys.argv) < 4:
            print("Usage: python db_utils.py update_status <order_id> <status>")
        else:
            order_id = int(sys.argv[2])
            status = sys.argv[3]
            update_order_status(order_id, status)
    
    elif command == "recent_orders":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        list_recent_orders(limit)
    
    elif command == "sales_summary":
        get_sales_summary()
    
    else:
        print(f"Unknown command: {command}")
