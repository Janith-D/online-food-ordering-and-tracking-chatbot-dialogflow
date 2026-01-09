# Food Ordering Chatbot - Backend

Complete FastAPI backend with MySQL database for Dialogflow-based food ordering chatbot.

## Features

- ✅ Order placement with multiple items
- ✅ Add/remove items from ongoing orders
- ✅ Order completion and tracking
- ✅ Menu item management
- ✅ Session-based order management
- ✅ MySQL database integration
- ✅ Dialogflow webhook integration

## Project Structure

```
chatbot/
├── main.py                 # FastAPI application and webhook endpoints
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic validation schemas
├── database.py            # Database connection and session management
├── order_service.py       # Business logic for order management
├── config.py              # Application configuration
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
cd "d:\python\nlp project\chatbot"
pip install -r requirements.txt
```

### 3. Configure Database

1. Create a MySQL database:
```sql
CREATE DATABASE food_ordering_db;
```

2. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

3. Edit `.env` with your database credentials:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=food_ordering_db
```

### 4. Initialize Database

Run the initialization script to create tables and populate menu items:

```bash
python init_db.py
```

To reset the database (deletes all data):
```bash
python init_db.py --reset
```

### 5. Run the Application

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/` - Check if API is running

### Webhook
- **POST** `/webhook` - Main Dialogflow webhook endpoint

### Order Management (REST)
- **GET** `/orders/{order_id}` - Get order details by ID

## Dialogflow Integration

### Webhook URL
Configure in Dialogflow:
```
https://your-domain.com/webhook
```

For local testing with ngrok:
```bash
ngrok http 8000
```

### Required Intents

The backend handles these Dialogflow intents:

1. **new.order** - Start a new order
   - Entities: `food-item`, `number`

2. **order.add - context: ongoing-order** - Add items to current order
   - Entities: `food-item`, `number`

3. **order.remove - context: ongoing-order** - Remove items from order
   - Entities: `food-item`

4. **order.complete - context: ongoing-order** - Complete the order
   - No entities required

5. **track.order** - Track order status
   - Entities: `number` (order ID)

## Database Schema

### Orders Table
```sql
- order_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- order_status (ENUM: Placed, Preparing, Out for Delivery, Delivered, Cancelled)
- order_date (DATETIME)
- total_amount (FLOAT)
```

### Order Items Table
```sql
- item_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- order_id (INT, FOREIGN KEY)
- item_name (VARCHAR)
- quantity (INT)
- price (FLOAT)
```

### Menu Items Table
```sql
- item_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- item_name (VARCHAR, UNIQUE)
- price (FLOAT)
- category (VARCHAR)
- is_available (INT)
```

## Testing

### Test Health Endpoint
```bash
curl http://localhost:8000/
```

### Test Webhook (Sample Request)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "queryResult": {
      "intent": {
        "displayName": "new.order"
      },
      "parameters": {
        "food-item": ["Pepperoni Pizza", "Coca Cola"],
        "number": [2, 1]
      },
      "queryText": "I want 2 pizzas and 1 coke"
    },
    "session": "test-session-123"
  }'
```

## Sample Menu Items

The database is populated with these categories:
- **Pizzas**: Margherita, Pepperoni, Veggie, BBQ Chicken
- **Burgers**: Classic, Cheese, Veggie, Bacon
- **Pasta**: Carbonara, Arrabbiata, Alfredo
- **Sides**: French Fries, Garlic Bread, Onion Rings, Caesar Salad
- **Drinks**: Coca Cola, Pepsi, Orange Juice, Water
- **Desserts**: Chocolate Cake, Ice Cream, Cheesecake

## Session Management

Currently uses in-memory dictionary for session management. For production:
- Use Redis for distributed session storage
- Or implement database-backed sessions
- Consider using Dialogflow contexts for session state

## Development

### Enable SQL Query Logging
In `database.py`, set:
```python
engine = create_engine(settings.database_url, echo=True)
```

### API Documentation
FastAPI provides automatic interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Production Deployment

1. **Use environment variables** for all sensitive data
2. **Set up proper database connection pooling**
3. **Implement Redis for session management**
4. **Enable CORS** if frontend is on different domain
5. **Use HTTPS** with valid SSL certificate
6. **Set up logging** and monitoring
7. **Use a production WSGI server** (gunicorn with uvicorn workers)

Example production command:
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check credentials in `.env`
- Ensure database exists
- Check firewall settings

### Import Errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version`

### Webhook Not Responding
- Verify ngrok is running (for local testing)
- Check Dialogflow webhook URL configuration
- Review logs for errors

## License

MIT License

## Support

For issues or questions, please create an issue in the project repository.
