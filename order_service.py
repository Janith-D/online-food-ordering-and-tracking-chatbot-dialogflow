from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from models import Order, OrderItem, MenuItem, OrderStatus
from datetime import datetime


# In-progress orders tracking (session-based storage)
# In production, use Redis or database for session management
inprogress_orders: Dict[str, Dict] = {}


def get_menu_item_price(db: Session, item_name: str) -> Optional[float]:
    """
    Get price of a menu item from database
    """
    menu_item = db.query(MenuItem).filter(MenuItem.item_name == item_name).first()
    if menu_item and menu_item.is_available:
        return menu_item.price
    return None


def add_to_order(session_id: str, food_items: List[str], quantities: List[int], db: Session) -> str:
    """
    Add items to in-progress order
    """
    if session_id not in inprogress_orders:
        inprogress_orders[session_id] = {}
    
    current_order = inprogress_orders[session_id]
    
    for food_item, quantity in zip(food_items, quantities):
        # Get price from database
        price = get_menu_item_price(db, food_item)
        
        if price is None:
            return f"Sorry, {food_item} is not available on our menu."
        
        # Add or update item in current order
        if food_item in current_order:
            current_order[food_item]["quantity"] += quantity
        else:
            current_order[food_item] = {
                "quantity": quantity,
                "price": price
            }
    
    # Generate order summary
    order_summary = ", ".join([f"{item}: {details['quantity']}" 
                               for item, details in current_order.items()])
    
    return f"Added to your order: {order_summary}. Would you like to add more items or complete your order?"


def remove_from_order(session_id: str, food_items: List[str]) -> str:
    """
    Remove items from in-progress order
    """
    if session_id not in inprogress_orders:
        return "You don't have any items in your order yet."
    
    current_order = inprogress_orders[session_id]
    removed_items = []
    not_found_items = []
    
    for food_item in food_items:
        if food_item in current_order:
            del current_order[food_item]
            removed_items.append(food_item)
        else:
            not_found_items.append(food_item)
    
    response = ""
    if removed_items:
        response += f"Removed from your order: {', '.join(removed_items)}. "
    
    if not_found_items:
        response += f"These items were not in your order: {', '.join(not_found_items)}. "
    
    if not current_order:
        response += "Your order is now empty."
    else:
        order_summary = ", ".join([f"{item}: {details['quantity']}" 
                                   for item, details in current_order.items()])
        response += f"Current order: {order_summary}"
    
    return response


def complete_order(session_id: str, db: Session) -> str:
    """
    Complete the order and save to database
    """
    if session_id not in inprogress_orders or not inprogress_orders[session_id]:
        return "Your order is empty. Please add items before completing the order."
    
    current_order = inprogress_orders[session_id]
    
    # Calculate total amount
    total_amount = sum(details["quantity"] * details["price"] 
                       for details in current_order.values())
    
    # Create new order
    new_order = Order(
        order_status=OrderStatus.PLACED,
        order_date=datetime.utcnow(),
        total_amount=total_amount
    )
    
    db.add(new_order)
    db.flush()  # Get the order_id
    
    # Add order items
    for item_name, details in current_order.items():
        order_item = OrderItem(
            order_id=new_order.order_id,
            item_name=item_name,
            quantity=details["quantity"],
            price=details["price"]
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(new_order)
    
    # Clear the in-progress order
    del inprogress_orders[session_id]
    
    order_details = ", ".join([f"{item}: {details['quantity']}" 
                               for item, details in current_order.items()])
    
    return f"Your order has been placed successfully! Order ID: {new_order.order_id}. Total: ${total_amount:.2f}. Items: {order_details}"


def track_order(order_id: int, db: Session) -> str:
    """
    Track order status by order ID
    """
    order = db.query(Order).filter(Order.order_id == order_id).first()
    
    if not order:
        return f"Sorry, I couldn't find any order with ID: {order_id}"
    
    # Get order items
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    item_details = ", ".join([f"{item.item_name} (x{item.quantity})" for item in items])
    
    return (f"Order ID: {order_id}\n"
            f"Status: {order.order_status.value}\n"
            f"Items: {item_details}\n"
            f"Total Amount: ${order.total_amount:.2f}\n"
            f"Order Date: {order.order_date.strftime('%Y-%m-%d %H:%M:%S')}")


def get_order_summary(session_id: str) -> str:
    """
    Get summary of current in-progress order
    """
    if session_id not in inprogress_orders or not inprogress_orders[session_id]:
        return "Your order is empty."
    
    current_order = inprogress_orders[session_id]
    total_amount = sum(details["quantity"] * details["price"] 
                       for details in current_order.values())
    
    order_summary = ", ".join([f"{item}: {details['quantity']} (${details['price'] * details['quantity']:.2f})" 
                               for item, details in current_order.items()])
    
    return f"Current order: {order_summary}. Total: ${total_amount:.2f}"
