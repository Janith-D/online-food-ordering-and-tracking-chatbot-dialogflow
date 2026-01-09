from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class OrderStatusEnum(str, Enum):
    """Order status enum for Pydantic"""
    PLACED = "Placed"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


# Menu Item Schemas
class MenuItemBase(BaseModel):
    item_name: str
    price: float
    category: Optional[str] = None
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemResponse(MenuItemBase):
    item_id: int
    
    class Config:
        from_attributes = True


# Order Item Schemas
class OrderItemBase(BaseModel):
    item_name: str
    quantity: int = Field(gt=0, description="Quantity must be greater than 0")
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    item_id: int
    order_id: int
    
    class Config:
        from_attributes = True


# Order Schemas
class OrderBase(BaseModel):
    order_status: OrderStatusEnum = OrderStatusEnum.PLACED


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderResponse(OrderBase):
    order_id: int
    order_date: datetime
    total_amount: float
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


# Dialogflow Webhook Schemas
class DialogflowParameter(BaseModel):
    """Parameters extracted from Dialogflow intent"""
    food_items: Optional[List[str]] = []
    number: Optional[List[int]] = []
    order_id: Optional[str] = None


class DialogflowIntent(BaseModel):
    """Intent information from Dialogflow"""
    displayName: str


class DialogflowQueryResult(BaseModel):
    """Query result from Dialogflow"""
    intent: DialogflowIntent
    parameters: Dict[str, Any]
    queryText: str


class DialogflowRequest(BaseModel):
    """Incoming webhook request from Dialogflow"""
    queryResult: DialogflowQueryResult
    session: str


class DialogflowResponse(BaseModel):
    """Response to send back to Dialogflow"""
    fulfillmentText: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "fulfillmentText": "Your order has been placed successfully! Order ID: 123"
            }
        }
