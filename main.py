from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],  # Adjust this to your frontend's origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def handle_request(request: Request, db: Session = Depends(get_db)):
   """Handle Dialogflow webhook requests"""
   try:
       # Retrieve the JSON data from the request
       payload = await request.json()

       # Extract the necessary information from payload
       # based on the structure of the WebhookRequest from Dialogflow
       intent = payload['queryResult']['intent']['displayName']
       parameters = payload['queryResult']['parameters']
       query_text = payload['queryResult'].get('queryText', '')
       
       # Extract session ID from the session path
       session_path = payload.get('session', '')
       if session_path:
           # Extract session ID from path like "projects/.../sessions/SESSION_ID"
           session_id = session_path.split('/')[-1] if '/' in session_path else session_path
       else:
           session_id = 'default-session'
       
       print(f"Intent: {intent}")
       print(f"Query Text: {query_text}")
       print(f"Session ID: {session_id}")
       print(f"Parameters: {parameters}")
       
       # Use original values from parameters if available for better matching
       food_items = parameters.get("food-item", [])
       food_items_original = parameters.get("food-item.original", [])
       
       # Prefer original values for better menu item matching
       if food_items_original:
           # Capitalize each word for better matching (e.g., "chicken pizza" -> "Chicken Pizza")
           food_items = [item.title() for item in food_items_original]
       elif food_items:
           # If no original, try to use the extracted values
           food_items = [item if isinstance(item, str) else str(item) for item in food_items]

       # Handle different intents
       if intent == "track.order - context: ongoing-tracking" or intent == "track.order":
           order_id = parameters.get("number")
           if order_id:
               if isinstance(order_id, list):
                   order_id = order_id[0]
               try:
                   order_id = int(order_id)
                   response_text = track_order(order_id, db)
               except (ValueError, TypeError):
                   response_text = "Please provide a valid order ID number."
           else:
               response_text = "Please provide your order ID to track your order."
           
           return JSONResponse(content={
               "fulfillmentText": response_text
           })
       
       elif intent == "new.order":
           numbers = parameters.get("number", [])
           
           if not food_items:
               response_text = "What would you like to order?"
           else:
               if not numbers:
                   numbers = [1] * len(food_items)
               if len(numbers) < len(food_items):
                   numbers.extend([1] * (len(food_items) - len(numbers)))
               
               response_text = add_to_order(session_id, food_items, numbers, db)
           
           return JSONResponse(content={
               "fulfillmentText": response_text
           })
       
       elif intent == "order.add - context: ongoing-order":
           numbers = parameters.get("number", [])
           
           if not food_items:
               response_text = "What would you like to add to your order?"
           else:
               if not numbers:
                   numbers = [1] * len(food_items)
               if len(numbers) < len(food_items):
                   numbers.extend([1] * (len(food_items) - len(numbers)))
               
               response_text = add_to_order(session_id, food_items, numbers, db)
           
           return JSONResponse(content={
               "fulfillmentText": response_text
           })
       
       elif intent == "order.remove - context: ongoing-order" or intent == "order.remove-context: ongoing-order":
           if not food_items:
               response_text = "What would you like to remove from your order?"
           else:
               # Extract numbers from parameters, but validate against query text
               numbers = parameters.get("number", [])
               
               # Parse the query text to extract actual numbers mentioned
               import re
               query_lower = query_text.lower()
               
               # Number word mapping
               number_words = {
                   'one': 1, 'a': 1, 'an': 1,
                   'two': 2, 'three': 3, 'four': 4, 'five': 5,
                   'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
               }
               
               # Extract numbers from query text
               actual_quantities = []
               
               # Check for number words in query
               for word, value in number_words.items():
                   if re.search(r'\b' + word + r'\b', query_lower):
                       actual_quantities.append(value)
                       break
               
               # Check for digit numbers in query
               digit_matches = re.findall(r'\b\d+\b', query_text)
               if digit_matches and not actual_quantities:
                   actual_quantities = [int(d) for d in digit_matches]
               
               # Use actual quantities from query text if found, otherwise use parameter numbers
               # But default to None (remove all) if no explicit quantity found
               if actual_quantities:
                   quantities = actual_quantities
               elif numbers and 'remove all' not in query_lower:
                   # Only use parameter numbers if query suggests using them
                   # and it's not a "remove all" command
                   quantities = None  # Default to remove all to avoid confusion
               else:
                   quantities = None  # Remove all
               
               response_text = remove_from_order(session_id, food_items, quantities)
           
           return JSONResponse(content={
               "fulfillmentText": response_text
           })
       
       elif intent == "order.complete - context: ongoing-order" or intent == "order.complete-context: ongoing-order":
           response_text = complete_order(session_id, db)
           
           return JSONResponse(content={
               "fulfillmentText": response_text
           })
       
       elif intent == "store.hours" or intent == "store hours":
           # Fixed response for store hours
           response_text = """Here are our store hours:
Monday - Friday: 10:00 AM to 10:00 PM
Saturday - Sunday: 11:00 AM to 11:00 PM

We're open every day! You can place orders anytime during these hours."""
           
           return JSONResponse(content={
               "fulfillmentText": response_text
           })
       
       else:
           # Default response for unhandled intents
           return JSONResponse(content={
               "fulfillmentText": "I'm not sure how to help with that. You can:\n1. Place a new order\n2. Track an existing order\n3. Ask about store hours"
           })
   
   except Exception as e:
       print(f"Error processing request: {str(e)}")
       return JSONResponse(content={
           "fulfillmentText": "Sorry, something went wrong. Please try again."
       })


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
        "version": "1.0.0",
        "features": [
            "1. Place new food orders",
            "2. Track existing orders",
            "3. Check store hours"
        ]
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
    numbers = parameters.get("number", [])
    
    if not food_items:
        return DialogflowResponse(
            fulfillmentText="What would you like to remove from your order?"
        )
    
    # Extract quantities if provided (e.g., "remove 2 pizzas")
    quantities = numbers if numbers else None
    
    response_text = remove_from_order(session_id, food_items, quantities)
    
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
