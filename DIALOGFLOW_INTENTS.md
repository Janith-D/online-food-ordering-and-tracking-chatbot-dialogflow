# Dialogflow Intent Configuration Guide

This document describes the required Dialogflow intents for your chatbot.

## Intent 1: new.order

**Description**: User wants to start a new food order

### Training Phrases
- I want to order 2 pizzas
- I'd like a burger and fries
- Can I get 3 pepperoni pizzas and 2 cokes
- Order me a veggie pizza
- I want to order food

### Entities to Extract
- `@sys.any:food-item` (list) - Food items to order
- `@sys.number:number` (list) - Quantities for each item

### Parameters
| Parameter | Entity | Required | Prompts |
|-----------|--------|----------|---------|
| food-item | @sys.any | No | What would you like to order? |
| number | @sys.number | No | - |

### Contexts
- **Output Context**: `ongoing-order` (lifespan: 5)

### Webhook
✅ Enable webhook call for this intent

---

## Intent 2: order.add - context: ongoing-order

**Description**: Add more items to an ongoing order

### Training Phrases
- Add 2 burgers
- I also want french fries
- Add a coke to my order
- Also add 3 pizzas

### Entities to Extract
- `@sys.any:food-item` (list) - Additional food items
- `@sys.number:number` (list) - Quantities

### Input Contexts Required
- `ongoing-order`

### Contexts
- **Output Context**: `ongoing-order` (lifespan: 5)

### Webhook
✅ Enable webhook call for this intent

---

## Intent 3: order.remove - context: ongoing-order

**Description**: Remove items from ongoing order

### Training Phrases
- Remove the pizza
- Take out the burger
- Remove 2 cokes
- Delete the fries from my order

### Entities to Extract
- `@sys.any:food-item` (list) - Items to remove

### Input Contexts Required
- `ongoing-order`

### Contexts
- **Output Context**: `ongoing-order` (lifespan: 5)

### Webhook
✅ Enable webhook call for this intent

---

## Intent 4: order.complete - context: ongoing-order

**Description**: Finalize and place the order

### Training Phrases
- That's it
- Place my order
- Complete the order
- I'm done ordering
- Confirm my order
- Checkout

### Entities to Extract
- None

### Input Contexts Required
- `ongoing-order`

### Contexts
- **Output Context**: None (order is complete)

### Webhook
✅ Enable webhook call for this intent

---

## Intent 5: track.order

**Description**: Track an existing order by order ID

### Training Phrases
- Track my order
- Where is order 123
- Track order number 456
- Status of order 789
- Check my order 101

### Entities to Extract
- `@sys.number:number` - Order ID

### Parameters
| Parameter | Entity | Required | Prompts |
|-----------|--------|----------|---------|
| number | @sys.number | Yes | What is your order ID? |

### Contexts
- No specific contexts required

### Webhook
✅ Enable webhook call for this intent

---

## Webhook Configuration

### Webhook URL
```
https://your-domain.com/webhook
```

For local development with ngrok:
```
https://your-ngrok-id.ngrok.io/webhook
```

### Steps to Configure Webhook
1. In Dialogflow Console, click "Fulfillment" in left menu
2. Enable "Webhook"
3. Enter your webhook URL
4. Click "Save"

### Request Format
Your webhook will receive requests in this format:
```json
{
  "queryResult": {
    "intent": {
      "displayName": "new.order"
    },
    "parameters": {
      "food-item": ["Pizza", "Coke"],
      "number": [2, 1]
    },
    "queryText": "I want 2 pizzas and 1 coke"
  },
  "session": "projects/.../sessions/abc123"
}
```

### Response Format
Your webhook should return:
```json
{
  "fulfillmentText": "Added to your order: Pizza: 2, Coke: 1. Would you like to add more items?"
}
```

---

## Optional: Default Fallback Intent

**Description**: Handle unrecognized input

### Response
```
I'm sorry, I didn't understand that. You can:
- Start a new order by saying "I want to order"
- Track an order by saying "Track order" followed by your order ID
```

---

## Testing Your Intents

### Test Conversation Flow

**Scenario 1: Complete Order**
```
User: I want 2 pizzas and a coke
Bot: Added to your order: Pepperoni Pizza: 2, Coca Cola: 1. Would you like to add more items?

User: Add french fries
Bot: Added to your order: Pepperoni Pizza: 2, Coca Cola: 1, French Fries: 1. Would you like to add more?

User: Remove the coke
Bot: Removed from your order: Coca Cola. Current order: Pepperoni Pizza: 2, French Fries: 1

User: That's it
Bot: Your order has been placed successfully! Order ID: 123. Total: $25.97
```

**Scenario 2: Track Order**
```
User: Track order 123
Bot: Order ID: 123
     Status: Placed
     Items: Pepperoni Pizza (x2), French Fries (x1)
     Total Amount: $25.97
     Order Date: 2026-01-10 14:30:00
```

---

## Entity Configuration

### @sys.any (for food-item)
- System entity
- Captures any text
- Used to extract food item names

### @sys.number (for number)
- System entity
- Captures numeric values
- Used for quantities and order IDs

---

## Context Management

### ongoing-order Context
- **Lifespan**: 5 (5 interactions)
- **Purpose**: Maintain order session state
- **Set by**: new.order intent
- **Used by**: order.add, order.remove, order.complete
- **Cleared by**: order.complete (completion of order)

This ensures that add/remove operations only work when there's an active order session.

---

## Tips for Better Performance

1. **Add More Training Phrases**: The more varied training phrases, the better recognition
2. **Use Synonyms**: Add common synonyms for food items
3. **Test Edge Cases**: Test with typos, different phrasings
4. **Monitor Analytics**: Check which phrases aren't being recognized
5. **Regular Updates**: Update intents based on user interactions

---

## Webhook Testing

Use the test_api.py script to verify webhook functionality:
```bash
python test_api.py
```

Or use curl:
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d @test_request.json
```
