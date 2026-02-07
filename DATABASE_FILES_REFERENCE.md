# 📋 Quick Reference: Database Connection Files

## 🔗 Files That Handle Database Connections

| File | Purpose | What It Does |
|------|---------|--------------|
| **config.py** | Configuration | Loads DB credentials from .env file |
| **database.py** | Connection Engine | Creates SQLAlchemy engine & sessions |
| **models.py** | Schema Definition | Defines table structures (ORM) |
| **.env** | Credentials | Stores DB host, user, password, etc. |
| **database_setup.sql** | Manual Setup | SQL script for WAMP phpMyAdmin |

---

## ⚙️ How They Work Together

```
.env file
  ↓
config.py reads environment variables
  ↓
database.py creates connection using config
  ↓
models.py defines table structures
  ↓
Application (main.py, order_service.py) uses database
```

---

## 🔧 For WAMP Server Setup

### 1. **Create Database in phpMyAdmin**
```
http://localhost/phpmyadmin
→ New Database
→ Name: food_ordering_db
→ Create
```

### 2. **Import SQL File**
```
→ Select database: food_ordering_db
→ Import tab
→ Choose file: database_setup.sql
→ Go
```

### 3. **Configure .env**
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=food_ordering_db
```

### 4. **Test Connection**
```bash
python db_utils.py list_menu
```

---

## 📂 File Locations

```
d:\python\nlp project\chatbot\
│
├── config.py              ← Database configuration
├── database.py            ← Connection engine
├── models.py              ← Table definitions
├── .env                   ← Your credentials (create this)
├── .env.example           ← Template
└── database_setup.sql     ← SQL for manual setup
```

---

## 🎯 WAMP Default Settings

| Setting | Value |
|---------|-------|
| Host | localhost |
| Port | 3306 |
| User | root |
| Password | (empty) or `root` |
| phpMyAdmin | http://localhost/phpmyadmin |

---

## ✅ Quick Setup Commands

```bash
# 1. Copy environment template
copy .env.example .env

# 2. Edit .env with WAMP settings
notepad .env

# 3. Test connection
python -c "from database import engine; print('OK' if engine else 'FAIL')"

# 4. View menu
python db_utils.py list_menu

# 5. Start server
python main.py
```

---

## 🔍 Verify Database

```sql
-- In phpMyAdmin SQL tab:
USE food_ordering_db;
SHOW TABLES;
SELECT COUNT(*) FROM menu_items;  -- Should be 22
```

---

## 📖 Full Guides

- **WAMP Setup:** See `WAMP_SETUP_GUIDE.md`
- **SQL Script:** Use `database_setup.sql`
- **Quick Start:** See `QUICKSTART.md`
