# Project Files Overview

## Core Application Files

### main.py
**Purpose**: Main FastAPI application with webhook endpoints
- Handles all Dialogflow webhook requests
- Routes intents to appropriate handlers
- Implements intent handlers for:
  - new.order: Start new order
  - order.add: Add items to ongoing order
  - order.remove: Remove items from order
  - order.complete: Finalize and save order
  - track.order: Track order status
- Provides REST API endpoints for order management

### models.py
**Purpose**: SQLAlchemy database models
- **Order**: Main order table (order_id, status, date, total_amount)
- **OrderItem**: Order items with quantities and prices
- **MenuItem**: Available food items menu
- **OrderStatus**: Enum for order statuses
- Defines relationships between tables

### schemas.py
**Purpose**: Pydantic models for validation and serialization
- Request/response validation schemas
- Dialogflow webhook request/response models
- API data transfer objects (DTOs)
- Ensures type safety and data validation

### database.py
**Purpose**: Database connection and session management
- Creates SQLAlchemy engine
- Provides database session factory
- Dependency injection for FastAPI routes
- Database initialization functions

### order_service.py
**Purpose**: Business logic for order management
- add_to_order(): Add items to in-progress order
- remove_from_order(): Remove items from order
- complete_order(): Finalize and save order to DB
- track_order(): Retrieve order status
- get_order_summary(): Get current order summary
- Session-based order tracking

### config.py
**Purpose**: Application configuration management
- Loads environment variables from .env
- Database connection settings
- Application settings (host, port)
- Constructs database URL

## Setup & Utility Files

### init_db.py
**Purpose**: Database initialization script
- Creates all database tables
- Populates menu with sample items
- Can reset database (with --reset flag)
- Run once during initial setup

### db_utils.py
**Purpose**: Database management utilities
- Add/update/delete menu items
- Update order statuses
- View orders and sales reports
- Command-line database management tool

### requirements.txt
**Purpose**: Python package dependencies
- FastAPI, Uvicorn (web framework)
- SQLAlchemy, PyMySQL (database)
- Pydantic (validation)
- All required Python packages

### .env.example
**Purpose**: Environment variables template
- Database configuration template
- Copy to .env and fill in your values
- Never commit .env to version control

### .gitignore
**Purpose**: Git ignore rules
- Excludes .env, __pycache__, virtual environments
- Prevents sensitive data from being committed

## Testing & Documentation

### test_api.py
**Purpose**: API testing script
- Tests all webhook endpoints
- Simulates Dialogflow requests
- Verifies order flow (create → add → complete → track)
- Run after starting server to verify setup

### README.md
**Purpose**: Comprehensive project documentation
- Complete setup instructions
- API endpoint documentation
- Database schema details
- Dialogflow integration guide
- Troubleshooting tips

### QUICKSTART.md
**Purpose**: Quick start guide
- Step-by-step setup instructions
- Essential commands
- Common issues and solutions
- Minimal steps to get running

### start_server.bat
**Purpose**: Windows startup script
- One-click server startup
- Checks for dependencies
- Activates virtual environment
- Double-click to start server

## Data Flow

```
User Message
    ↓
Dialogflow (NLP)
    ↓
Webhook Request → main.py
    ↓
Intent Handler (main.py)
    ↓
Business Logic (order_service.py)
    ↓
Database Operations (models.py + database.py)
    ↓
Response → Dialogflow
    ↓
User
```

## File Dependencies

```
main.py
├── imports: database.py, schemas.py, order_service.py, config.py
├── uses: get_db() for database sessions
└── handles: Dialogflow webhook requests

order_service.py
├── imports: models.py, database.py
├── uses: Order, OrderItem, MenuItem models
└── implements: Order management logic

models.py
├── imports: sqlalchemy
└── defines: Database table structures

database.py
├── imports: models.py, config.py
├── uses: Base from models
└── provides: Database sessions

config.py
├── imports: pydantic_settings
└── loads: Environment variables

schemas.py
├── imports: pydantic
└── defines: API request/response models
```

## Development Workflow

1. **Initial Setup**:
   - Copy .env.example → .env
   - Configure database credentials
   - Run: `pip install -r requirements.txt`
   - Run: `python init_db.py`

2. **Development**:
   - Start server: `python main.py` or `start_server.bat`
   - Test endpoints: `python test_api.py`
   - Check API docs: http://localhost:8000/docs

3. **Database Management**:
   - Add menu items: `python db_utils.py add_item "Name" price category`
   - View menu: `python db_utils.py list_menu`
   - View orders: `python db_utils.py recent_orders`
   - Sales report: `python db_utils.py sales_summary`

4. **Testing with Dialogflow**:
   - Start ngrok: `ngrok http 8000`
   - Configure webhook in Dialogflow
   - Test through Dialogflow console or integration

5. **Deployment**:
   - Set production environment variables
   - Use production database
   - Deploy to cloud (AWS, GCP, Azure)
   - Configure HTTPS and domain

## Key Features

✅ RESTful API with FastAPI
✅ MySQL database with SQLAlchemy ORM
✅ Pydantic data validation
✅ Session-based order management
✅ Dialogflow webhook integration
✅ Automatic API documentation
✅ Database utilities and management
✅ Comprehensive testing suite
✅ Production-ready structure
