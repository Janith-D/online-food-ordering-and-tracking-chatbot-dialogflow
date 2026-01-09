from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any
import uvicorn

from database import get_db, init_db
from schemas import DialogflowRequest, DialogflowResponse
from order_service import (
    add_to_order, 
    remove_from_order, 
    complete_order, 
    track_order,
    get_order_summary
)
from config import settings


# Create FastAPI app
app = FastAPI(
    title="Food Ordering Chatbot API",
    description="Backend API for Dialogflow-based food ordering chatbot",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✓ Application started successfully")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Food Ordering Chatbot API is running",
        "version": "1.0.0"
    }


@app.post("/webhook", response_model=DialogflowResponse)
async def dialogflow_webhook(request: DialogflowRequest, db: Session = Depends(get_db)):
    """
    Main webhook endpoint for Dialogflow
    Handles all intents from Dialogflow and returns appropriate responses
    """
    try:
        # Extract intent and parameters
        intent_name = request.queryResult.intent.displayName
        parameters = request.queryResult.parameters
        session_id = request.session
        
        print(f"Intent: {intent_name}")
        print(f"Parameters: {parameters}")
        print(f"Session: {session_id}")
        
        # Route to appropriate handler based on intent
        if intent_name == "order.add - context: ongoing-order":
            return handle_add_to_order(parameters, session_id, db)
        
        elif intent_name == "order.remove - context: ongoing-order":
            return handle_remove_from_order(parameters, session_id, db)
        
        elif intent_name == "order.complete - context: ongoing-order":
            return handle_complete_order(session_id, db)
        
        elif intent_name == "track.order":
            return handle_track_order(parameters, db)
        
        elif intent_name == "new.order":
            return handle_new_order(parameters, session_id, db)
        
        else:
            return DialogflowResponse(
                fulfillmentText="I'm not sure how to help with that. You can place a new order or track an existing one."
            )
    
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return DialogflowResponse(
            fulfillmentText="Sorry, something went wrong. Please try again."
        )


def handle_new_order(parameters: Dict[str, Any], session_id: str, db: Session) -> DialogflowResponse:
    """Handle new order intent"""
    food_items = parameters.get("food-item", [])
    numbers = parameters.get("number", [])
    
    if not food_items:
        return DialogflowResponse(
            fulfillmentText="What would you like to order?"
        )
    
    # If no quantities specified, assume 1 for each item
    if not numbers:
        numbers = [1] * len(food_items)
    
    # If quantities don't match items, pad with 1s
    if len(numbers) < len(food_items):
        numbers.extend([1] * (len(food_items) - len(numbers)))
    
    response_text = add_to_order(session_id, food_items, numbers, db)
    
    return DialogflowResponse(fulfillmentText=response_text)


def handle_add_to_order(parameters: Dict[str, Any], session_id: str, db: Session) -> DialogflowResponse:
    """Handle adding items to ongoing order"""
    food_items = parameters.get("food-item", [])
    numbers = parameters.get("number", [])
    
    if not food_items:
        return DialogflowResponse(
            fulfillmentText="What would you like to add to your order?"
        )
    
    # If no quantities specified, assume 1 for each item
    if not numbers:
        numbers = [1] * len(food_items)
    
    # If quantities don't match items, pad with 1s
    if len(numbers) < len(food_items):
        numbers.extend([1] * (len(food_items) - len(numbers)))
    
    response_text = add_to_order(session_id, food_items, numbers, db)
    
    return DialogflowResponse(fulfillmentText=response_text)


def handle_remove_from_order(parameters: Dict[str, Any], session_id: str, db: Session) -> DialogflowResponse:
    """Handle removing items from ongoing order"""
    food_items = parameters.get("food-item", [])
    
    if not food_items:
        return DialogflowResponse(
            fulfillmentText="What would you like to remove from your order?"
        )
    
    response_text = remove_from_order(session_id, food_items)
    
    return DialogflowResponse(fulfillmentText=response_text)


def handle_complete_order(session_id: str, db: Session) -> DialogflowResponse:
    """Handle order completion"""
    response_text = complete_order(session_id, db)
    
    return DialogflowResponse(fulfillmentText=response_text)


def handle_track_order(parameters: Dict[str, Any], db: Session) -> DialogflowResponse:
    """Handle order tracking"""
    order_id = parameters.get("number")
    
    if not order_id:
        return DialogflowResponse(
            fulfillmentText="Please provide your order ID to track your order."
        )
    
    # Handle if order_id is a list
    if isinstance(order_id, list):
        order_id = order_id[0] if order_id else None
    
    if order_id is None:
        return DialogflowResponse(
            fulfillmentText="Please provide a valid order ID."
        )
    
    try:
        order_id = int(order_id)
        response_text = track_order(order_id, db)
    except (ValueError, TypeError):
        response_text = "Please provide a valid order ID number."
    
    return DialogflowResponse(fulfillmentText=response_text)


@app.get("/orders/{order_id}")
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    REST API endpoint to get order details
    Can be used for testing or external integrations
    """
    response_text = track_order(order_id, db)
    return {"order_id": order_id, "details": response_text}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.APP_HOST, 
        port=settings.APP_PORT, 
        reload=True
    )
