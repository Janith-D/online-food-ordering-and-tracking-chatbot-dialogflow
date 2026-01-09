from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


Base = declarative_base()


class OrderStatus(enum.Enum):
    """Enum for order status"""
    PLACED = "Placed"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class Order(Base):
    """Orders table model"""
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    order_status = Column(Enum(OrderStatus), default=OrderStatus.PLACED, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    
    # Relationship with order items
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(order_id={self.order_id}, status={self.order_status.value}, date={self.order_date})>"


class OrderItem(Base):
    """Order items table model"""
    __tablename__ = "order_items"
    
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    item_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    # Relationship with orders
    order = relationship("Order", back_populates="items")
    
    def __repr__(self):
        return f"<OrderItem(item_name={self.item_name}, quantity={self.quantity}, price={self.price})>"


class MenuItem(Base):
    """Menu items table for available food items"""
    __tablename__ = "menu_items"
    
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(100), unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    category = Column(String(50))
    is_available = Column(Integer, default=1)  # 1 for available, 0 for unavailable
    
    def __repr__(self):
        return f"<MenuItem(item_name={self.item_name}, price={self.price})>"
