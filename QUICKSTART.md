# Quick Start Guide - Food Ordering Chatbot

Follow these steps to get your chatbot backend up and running:

## Step 1: Install MySQL

If you don't have MySQL installed:
- Download from: https://dev.mysql.com/downloads/mysql/
- Install and remember your root password

## Step 2: Create Database

Open MySQL command line or MySQL Workbench and run:
```sql
CREATE DATABASE food_ordering_db;
```

## Step 3: Set Up Python Environment (Optional but Recommended)

Create a virtual environment:
```bash
cd "d:\python\nlp project\chatbot"
python -m venv venv
venv\Scripts\activate
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Configure Environment

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

2. Edit `.env` file with your MySQL credentials:
```
DB_PASSWORD=your_mysql_password
```

## Step 6: Initialize Database

Run the initialization script:
```bash
python init_db.py
```

This will:
- Create all necessary tables
- Populate the menu with sample items

## Step 7: Start the Server

```bash
python main.py
```

You should see:
```
✓ Application started successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 8: Test the API

Open a new terminal and run:
```bash
python test_api.py
```

Or visit in your browser:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/

## Step 9: Set Up ngrok (For Dialogflow Testing)

Download ngrok from: https://ngrok.com/download

Run:
```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., https://abc123.ngrok.io) and use it in Dialogflow webhook settings:
```
https://abc123.ngrok.io/webhook
```

## Step 10: Configure Dialogflow Webhook

1. Go to your Dialogflow agent
2. Click on "Fulfillment" in the left menu
3. Enable "Webhook"
4. Enter your webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
5. Save

## Common Issues

### "Access denied for user"
- Check your MySQL password in `.env`
- Ensure MySQL is running
- Verify database exists

### "Module not found"
- Make sure you installed requirements: `pip install -r requirements.txt`
- Activate virtual environment if using one

### "Port 8000 already in use"
- Change APP_PORT in `.env` file
- Or kill the process using port 8000

## Next Steps

1. Test your chatbot through Dialogflow
2. Customize menu items in `init_db.py`
3. Modify intents in `main.py` to match your Dialogflow setup
4. Deploy to production server

## Need Help?

Check the README.md for detailed documentation.
