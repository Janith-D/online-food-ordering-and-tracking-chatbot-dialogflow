# 🔧 WAMP Server Manual Database Setup Guide

This guide explains how to manually set up the database using WAMP Server and which files handle database connections.

## 📁 Database Connection Files in Your Project

### 1. **config.py** - Database Configuration Settings
**Location:** `d:\python\nlp project\chatbot\config.py`

**Purpose:** Stores database connection parameters
```python
DB_HOST = "localhost"      # WAMP MySQL host
DB_PORT = 3306            # WAMP MySQL port (default)
DB_USER = "root"          # WAMP default user
DB_PASSWORD = ""          # WAMP default password (empty or 'root')
DB_NAME = "food_ordering_db"
```

**For WAMP, update your .env file:**
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=food_ordering_db
```

---

### 2. **database.py** - Database Connection Engine
**Location:** `d:\python\nlp project\chatbot\database.py`

**Purpose:** Creates SQLAlchemy engine and manages sessions
- Creates database connection pool
- Provides session management
- Handles database initialization

**Key function:**
```python
engine = create_engine(settings.database_url)  # Uses config from .env
```

---

### 3. **models.py** - Database Schema Definition
**Location:** `d:\python\nlp project\chatbot\models.py`

**Purpose:** Defines table structures (ORM models)
- `Order` table structure
- `OrderItem` table structure
- `MenuItem` table structure

---

## 🚀 Step-by-Step: Manual Database Setup with WAMP

### Step 1: Start WAMP Server

1. Launch WAMP Server (green icon in system tray)
2. Wait for icon to turn **green** (not orange/yellow)
3. Click WAMP icon → MySQL → Service → Start/Resume Service

### Step 2: Open phpMyAdmin

**Option A: Via Browser**
```
http://localhost/phpmyadmin
```

**Option B: Via WAMP Menu**
- Click WAMP icon → phpMyAdmin

**Login Credentials (WAMP defaults):**
- Username: `root`
- Password: (leave empty) or try `root`

### Step 3: Create Database

In phpMyAdmin:

1. Click **"New"** or **"Databases"** tab
2. Database name: `food_ordering_db`
3. Collation: `utf8mb4_unicode_ci` (recommended)
4. Click **"Create"**

**Or use SQL tab:**
```sql
CREATE DATABASE food_ordering_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### Step 4: Import SQL Schema

**Method 1: Using SQL Script File**

1. In phpMyAdmin, select database `food_ordering_db`
2. Click **"Import"** tab
3. Click **"Choose File"**
4. Select: `d:\python\nlp project\chatbot\database_setup.sql`
5. Click **"Go"**

**Method 2: Copy-Paste SQL**

1. In phpMyAdmin, select `food_ordering_db`
2. Click **"SQL"** tab
3. Open `database_setup.sql` in a text editor
4. Copy all SQL code
5. Paste into SQL query box
6. Click **"Go"**

### Step 5: Verify Tables Created

In phpMyAdmin, you should see **3 tables:**

```
✓ orders          (0 rows initially)
✓ order_items     (0 rows initially)
✓ menu_items      (22 rows - pre-populated)
```

Click on `menu_items` to verify 22 food items are inserted.

### Step 6: Configure Your Application

**Create .env file:**

```bash
# In PowerShell
cd "d:\python\nlp project\chatbot"
copy .env.example .env
```

**Edit .env file with WAMP settings:**
```env
# WAMP Server Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=food_ordering_db

APP_HOST=0.0.0.0
APP_PORT=8000
```

**Note:** WAMP default password is usually **empty** (blank). If you set a password, update it here.

### Step 7: Test Database Connection

```bash
# In PowerShell
cd "d:\python\nlp project\chatbot"
python -c "from database import engine; print('Connection successful!' if engine else 'Failed')"
```

Or run:
```bash
python db_utils.py list_menu
```

You should see all 22 menu items listed.

---

## 🔍 Understanding Database Connection Flow

```
Your Application (main.py)
        ↓
Uses config.py settings
        ↓
database.py creates engine
        ↓
Connects to WAMP MySQL
        ↓
Uses models.py for queries
        ↓
Interacts with food_ordering_db
```

### Connection String Format

The application builds this connection URL:
```
mysql+pymysql://root:@localhost:3306/food_ordering_db
                 ↑    ↑    ↑        ↑         ↑
              user  pass  host    port    database
```

---

## 📊 Manual Table Verification

### Check Tables Exist:
```sql
USE food_ordering_db;
SHOW TABLES;
```

Expected output:
```
+----------------------------+
| Tables_in_food_ordering_db |
+----------------------------+
| menu_items                 |
| order_items                |
| orders                     |
+----------------------------+
```

### Check Table Structure:

**Orders Table:**
```sql
DESCRIBE orders;
```

**OrderItems Table:**
```sql
DESCRIBE order_items;
```

**Menu Items:**
```sql
SELECT * FROM menu_items;
```

Should show 22 items across 6 categories.

---

## 🎨 Customize Your Menu (Manual)

### Add New Item:
```sql
INSERT INTO menu_items (item_name, price, category, is_available) 
VALUES ('Hawaiian Pizza', 12.99, 'Pizza', 1);
```

### Update Price:
```sql
UPDATE menu_items 
SET price = 13.99 
WHERE item_name = 'Hawaiian Pizza';
```

### Disable Item:
```sql
UPDATE menu_items 
SET is_available = 0 
WHERE item_name = 'Hawaiian Pizza';
```

### Delete Item:
```sql
DELETE FROM menu_items 
WHERE item_name = 'Hawaiian Pizza';
```

### View by Category:
```sql
SELECT * FROM menu_items 
WHERE category = 'Pizza' 
ORDER BY price;
```

---

## 🔐 Security: Create Dedicated User (Optional)

Instead of using `root`, create a dedicated user:

```sql
-- Create user
CREATE USER 'chatbot_user'@'localhost' 
IDENTIFIED BY 'YourSecurePassword123!';

-- Grant permissions
GRANT ALL PRIVILEGES ON food_ordering_db.* 
TO 'chatbot_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
```

Then update .env:
```env
DB_USER=chatbot_user
DB_PASSWORD=YourSecurePassword123!
```

---

## 🛠️ Common WAMP Issues & Solutions

### Issue 1: "Can't connect to MySQL server"
**Solution:**
- Ensure WAMP icon is **green**
- Check MySQL service is running: WAMP icon → MySQL → Service
- Test port: `netstat -an | findstr 3306`

### Issue 2: "Access denied for user 'root'"
**Solution:**
- Check password in .env (WAMP default is usually empty)
- Or set password in phpMyAdmin: User accounts → root → Edit privileges

### Issue 3: Port 3306 already in use
**Solution:**
- Close other MySQL instances
- Or change MySQL port in WAMP config and .env

### Issue 4: "Database doesn't exist"
**Solution:**
```sql
SHOW DATABASES;  -- Check if food_ordering_db exists
```

If missing, create it manually.

### Issue 5: WAMP icon stays orange/yellow
**Solution:**
- Check if port 80 is blocked (Skype, other web servers)
- Or change Apache port in WAMP settings

---

## ✅ Verification Checklist

- [ ] WAMP Server running (green icon)
- [ ] MySQL service active
- [ ] phpMyAdmin accessible
- [ ] Database `food_ordering_db` created
- [ ] 3 tables created (orders, order_items, menu_items)
- [ ] 22 menu items inserted
- [ ] .env file configured with WAMP credentials
- [ ] Database connection tested
- [ ] Application can query database

---

## 🚀 After Database Setup

Once your database is set up manually, you can:

1. **Skip init_db.py** - Tables already exist
2. **Start your server:**
   ```bash
   python main.py
   ```
3. **Test API:**
   ```bash
   python test_api.py
   ```

---

## 📞 WAMP Server Tools

### Access MySQL via Command Line:
```bash
# WAMP MySQL path (adjust version number)
cd C:\wamp64\bin\mysql\mysql8.0.27\bin
mysql -u root -p
```

### WAMP Configuration Files:
- **MySQL Config:** `C:\wamp64\bin\mysql\mysql8.0.x\my.ini`
- **PHP Config:** `C:\wamp64\bin\php\php8.x.x\php.ini`

### View MySQL Error Log:
```
C:\wamp64\logs\mysql.log
```

---

## 🎓 Next Steps

1. ✅ Database is now set up manually with WAMP
2. Configure .env with WAMP credentials
3. Test connection: `python db_utils.py list_menu`
4. Start server: `python main.py`
5. Test with Dialogflow webhook

**Your database is ready!** The application will now use your manually created WAMP database. 🎉
