# 🎯 GETTING STARTED CHECKLIST

Follow this checklist to get your Food Ordering Chatbot up and running!

## Phase 1: Prerequisites ✅

- [ ] **Install Python 3.8+**
  - Download from: https://www.python.org/downloads/
  - Verify: `python --version`

- [ ] **Install MySQL 8.0+**
  - Download from: https://dev.mysql.com/downloads/mysql/
  - Note your root password during installation
  - Verify: `mysql --version`

- [ ] **Install Git** (Optional, for version control)
  - Download from: https://git-scm.com/downloads

## Phase 2: Database Setup 📊

- [ ] **Start MySQL Server**
  ```bash
  # Windows: Services → Start MySQL80
  # Or: net start MySQL80
  ```

- [ ] **Create Database**
  ```bash
  mysql -u root -p
  ```
  ```sql
  CREATE DATABASE food_ordering_db;
  EXIT;
  ```

- [ ] **Verify Database Created**
  ```bash
  mysql -u root -p -e "SHOW DATABASES;"
  ```
  You should see `food_ordering_db` in the list

## Phase 3: Project Setup 🔧

- [ ] **Navigate to Project Directory**
  ```bash
  cd "d:\python\nlp project\chatbot"
  ```

- [ ] **Create Virtual Environment** (Recommended)
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- [ ] **Install Dependencies**
  ```bash
  pip install -r requirements.txt
  ```
  This installs: FastAPI, SQLAlchemy, MySQL drivers, etc.

- [ ] **Create .env File**
  ```bash
  copy .env.example .env
  ```

- [ ] **Edit .env File**
  Open `.env` in a text editor and update:
  ```env
  DB_PASSWORD=your_mysql_root_password
  ```
  Save the file

## Phase 4: Initialize Database 🗄️

- [ ] **Run Database Initialization**
  ```bash
  python init_db.py
  ```
  
  Expected output:
  ```
  Creating database tables...
  Database tables created successfully!
  ✓ Successfully added 22 menu items to the database
  ✓ Database initialization complete!
  ```

- [ ] **Verify Tables Created**
  ```bash
  mysql -u root -p food_ordering_db -e "SHOW TABLES;"
  ```
  Should show: `menu_items`, `order_items`, `orders`

- [ ] **Verify Menu Items**
  ```bash
  python db_utils.py list_menu
  ```
  Should display 22 food items

## Phase 5: Start the Server 🚀

- [ ] **Start FastAPI Server**
  
  **Option 1: Using Python**
  ```bash
  python main.py
  ```
  
  **Option 2: Using Batch Script (Windows)**
  ```bash
  start_server.bat
  ```
  Or double-click `start_server.bat` in File Explorer

- [ ] **Verify Server Running**
  Open browser and visit:
  - Health Check: http://localhost:8000/
  - API Docs: http://localhost:8000/docs
  
  You should see JSON response or Swagger UI

## Phase 6: Test the API 🧪

- [ ] **Run Automated Tests**
  Open a NEW terminal window:
  ```bash
  cd "d:\python\nlp project\chatbot"
  python test_api.py
  ```
  
  All 5 tests should pass:
  - ✓ Health Check
  - ✓ New Order
  - ✓ Add to Order
  - ✓ Complete Order
  - ✓ Track Order

- [ ] **Test Health Endpoint Manually**
  ```bash
  curl http://localhost:8000/
  ```
  Or visit in browser

- [ ] **Check API Documentation**
  Visit: http://localhost:8000/docs
  Try the interactive API testing

## Phase 7: Dialogflow Setup 🤖

- [ ] **Install ngrok**
  - Download from: https://ngrok.com/download
  - Extract and add to PATH
  - Sign up for free account (optional but recommended)

- [ ] **Start ngrok Tunnel**
  Open a NEW terminal:
  ```bash
  ngrok http 8000
  ```
  
  Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

- [ ] **Configure Dialogflow Webhook**
  1. Go to https://dialogflow.cloud.google.com/
  2. Open your agent
  3. Click "Fulfillment" in left menu
  4. Enable "Webhook"
  5. Enter webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
  6. Click "Save"

- [ ] **Create Required Intents**
  Follow instructions in `DIALOGFLOW_INTENTS.md`:
  
  **Intent 1: new.order**
  - Training phrases: "I want to order pizza"
  - Entities: food-item, number
  - Enable webhook
  - Set output context: ongoing-order
  
  **Intent 2: order.add - context: ongoing-order**
  - Training phrases: "Add french fries"
  - Input context: ongoing-order
  - Enable webhook
  
  **Intent 3: order.remove - context: ongoing-order**
  - Training phrases: "Remove the pizza"
  - Input context: ongoing-order
  - Enable webhook
  
  **Intent 4: order.complete - context: ongoing-order**
  - Training phrases: "That's it", "Complete my order"
  - Input context: ongoing-order
  - Enable webhook
  
  **Intent 5: track.order**
  - Training phrases: "Track order 123"
  - Entity: number (order ID)
  - Enable webhook

## Phase 8: Test End-to-End 🎉

- [ ] **Test in Dialogflow Console**
  Try this conversation:
  ```
  You: I want 2 pepperoni pizzas and a coke
  Bot: [Should confirm items added]
  
  You: Add french fries
  Bot: [Should add fries to order]
  
  You: That's it
  Bot: [Should complete order and give order ID]
  
  You: Track order [order_id]
  Bot: [Should show order details]
  ```

- [ ] **Verify in Database**
  ```bash
  python db_utils.py recent_orders
  ```
  Should show your test order

- [ ] **Check Server Logs**
  Review terminal where server is running
  Should show webhook requests

## Phase 9: Customization (Optional) 🎨

- [ ] **Customize Menu Items**
  ```bash
  python db_utils.py add_item "New Item" 9.99 Category
  python db_utils.py list_menu
  ```

- [ ] **Update Prices**
  ```bash
  python db_utils.py update_price "Item Name" 12.99
  ```

- [ ] **Modify Response Messages**
  Edit messages in:
  - `order_service.py` (business logic responses)
  - `main.py` (intent handler responses)

- [ ] **Add More Intents**
  - Create new intents in Dialogflow
  - Add handlers in `main.py`

## Phase 10: Production Ready (When Ready) 🚀

- [ ] **Choose Hosting Provider**
  - DigitalOcean, AWS, Heroku, Railway, etc.
  - See `DEPLOYMENT.md` for options

- [ ] **Set Up Production Database**
  - Create production MySQL instance
  - Update .env with production credentials

- [ ] **Deploy Application**
  - Follow deployment guide in `DEPLOYMENT.md`
  - Set up SSL certificate
  - Configure domain

- [ ] **Update Dialogflow Webhook**
  - Change from ngrok URL to production URL
  - Format: `https://your-domain.com/webhook`

- [ ] **Monitor and Maintain**
  - Set up logging
  - Configure backups
  - Monitor performance

## 🎊 Congratulations!

If you've completed all checkmarks, your Food Ordering Chatbot is fully functional!

## 📚 Reference Documentation

| Document | Purpose |
|----------|---------|
| QUICKSTART.md | Quick setup guide |
| README.md | Technical documentation |
| DIALOGFLOW_INTENTS.md | Intent configuration |
| PROJECT_STRUCTURE.md | File organization |
| DEPLOYMENT.md | Production deployment |
| IMPLEMENTATION_SUMMARY.md | Complete project overview |

## 🆘 Troubleshooting

### Problem: "Access denied for user"
**Solution**: Check MySQL password in `.env` file

### Problem: "No module named 'fastapi'"
**Solution**: Run `pip install -r requirements.txt`

### Problem: "Port 8000 already in use"
**Solution**: Change `APP_PORT` in `.env` or kill process on port 8000

### Problem: "Database not found"
**Solution**: Run `CREATE DATABASE food_ordering_db;` in MySQL

### Problem: Webhook not responding
**Solution**: 
1. Verify ngrok is running
2. Check ngrok URL in Dialogflow
3. Ensure server is running
4. Check server logs for errors

### Problem: Order not saving
**Solution**: 
1. Verify database connection
2. Check server logs
3. Ensure `order.complete` intent has webhook enabled

## 📞 Need Help?

1. Check the documentation files
2. Review error messages in terminal
3. Test API using `python test_api.py`
4. Check Dialogflow fulfillment logs
5. Verify all prerequisites are installed

## 🎯 Next Steps

After completing this checklist:
1. Experiment with different food items
2. Test various conversation flows
3. Customize the menu for your business
4. Add new features (payment, delivery tracking, etc.)
5. Deploy to production when ready

**Happy Coding!** 🚀
