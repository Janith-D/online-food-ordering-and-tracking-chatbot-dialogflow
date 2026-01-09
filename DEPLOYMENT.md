# Deployment Guide

This guide covers deploying your Food Ordering Chatbot backend to production.

## Pre-Deployment Checklist

- [ ] All code tested locally
- [ ] Database schema finalized
- [ ] Environment variables documented
- [ ] Security best practices implemented
- [ ] API documentation complete
- [ ] Dialogflow intents configured
- [ ] Error handling tested
- [ ] Logging configured

## Deployment Options

### Option 1: Traditional VPS (DigitalOcean, Linode, AWS EC2)

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install MySQL
sudo apt install mysql-server -y
sudo mysql_secure_installation
```

#### 2. Application Setup

```bash
# Create app directory
sudo mkdir -p /var/www/chatbot
cd /var/www/chatbot

# Clone or upload your code
# Option: Use git, scp, or FTP

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

#### 3. Database Setup

```bash
# Login to MySQL
sudo mysql -u root -p

# Create database and user
CREATE DATABASE food_ordering_db;
CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON food_ordering_db.* TO 'chatbot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Initialize database
python init_db.py
```

#### 4. Environment Configuration

```bash
# Create production .env file
nano .env
```

```env
# Production settings
DB_HOST=localhost
DB_PORT=3306
DB_USER=chatbot_user
DB_PASSWORD=your_strong_password
DB_NAME=food_ordering_db

APP_HOST=0.0.0.0
APP_PORT=8000
```

#### 5. Systemd Service

Create `/etc/systemd/system/chatbot.service`:

```ini
[Unit]
Description=Food Ordering Chatbot API
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/chatbot
Environment="PATH=/var/www/chatbot/venv/bin"
ExecStart=/var/www/chatbot/venv/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable chatbot
sudo systemctl start chatbot
sudo systemctl status chatbot
```

#### 6. Nginx Reverse Proxy

Install Nginx:
```bash
sudo apt install nginx -y
```

Create `/etc/nginx/sites-available/chatbot`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: food_ordering_db
      MYSQL_USER: chatbot_user
      MYSQL_PASSWORD: chatbot_password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DB_HOST: mysql
      DB_PORT: 3306
      DB_USER: chatbot_user
      DB_PASSWORD: chatbot_password
      DB_NAME: food_ordering_db
    depends_on:
      mysql:
        condition: service_healthy
    volumes:
      - .:/app
    command: sh -c "python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"

volumes:
  mysql_data:
```

#### 3. Build and Run

```bash
docker-compose up -d
```

### Option 3: Cloud Platform (Heroku, Railway, Render)

#### Railway Deployment

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Initialize Project**:
```bash
railway login
railway init
```

3. **Add MySQL Database**:
- Go to Railway dashboard
- Add MySQL plugin
- Copy connection details

4. **Set Environment Variables**:
```bash
railway variables set DB_HOST=<mysql_host>
railway variables set DB_USER=<mysql_user>
railway variables set DB_PASSWORD=<mysql_password>
railway variables set DB_NAME=<database_name>
```

5. **Deploy**:
```bash
railway up
```

### Option 4: AWS Elastic Beanstalk

1. **Install EB CLI**:
```bash
pip install awsebcli
```

2. **Initialize**:
```bash
eb init -p python-3.11 chatbot-api
```

3. **Create environment**:
```bash
eb create chatbot-prod
```

4. **Configure RDS**:
- Create RDS MySQL instance
- Configure security groups
- Update environment variables

5. **Deploy**:
```bash
eb deploy
```

## Production Configuration

### Security Best Practices

1. **Use Strong Passwords**:
   - Database passwords: 32+ characters
   - Use password managers

2. **Environment Variables**:
   - Never commit .env to git
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault)

3. **HTTPS Only**:
   - Force HTTPS redirects
   - Use valid SSL certificates

4. **Rate Limiting**:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/webhook")
@limiter.limit("100/minute")
async def webhook(...):
    ...
```

5. **CORS Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-website.com"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
```

### Performance Optimization

1. **Database Connection Pooling**:
```python
engine = create_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=40,
    pool_recycle=3600,
    pool_pre_ping=True
)
```

2. **Caching** (Redis):
```python
import redis
from functools import lru_cache

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=1000)
def get_menu_item_price(item_name: str):
    # Cache menu prices
    ...
```

3. **Production Workers**:
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --graceful-timeout 30
```

### Logging Configuration

Add to `main.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('chatbot.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Monitoring

1. **Health Check Endpoint**:
```python
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Check database connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

2. **Error Tracking** (Sentry):
```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### Backup Strategy

1. **Automated Database Backups**:
```bash
#!/bin/bash
# backup_db.sh
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u chatbot_user -p food_ordering_db > /backups/db_$DATE.sql
# Delete backups older than 30 days
find /backups -name "db_*.sql" -mtime +30 -delete
```

2. **Cron Job**:
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup_db.sh
```

## Post-Deployment

### 1. Update Dialogflow Webhook URL

In Dialogflow Console:
```
https://your-domain.com/webhook
```

### 2. Test Production Deployment

```bash
# Health check
curl https://your-domain.com/

# Test webhook
curl -X POST https://your-domain.com/webhook \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

### 3. Monitor Logs

```bash
# Systemd service
sudo journalctl -u chatbot -f

# Application logs
tail -f /var/www/chatbot/chatbot.log
```

### 4. Performance Testing

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Load test
ab -n 1000 -c 10 https://your-domain.com/
```

## Scaling

### Horizontal Scaling

1. **Load Balancer**: Use Nginx or AWS ALB
2. **Multiple App Servers**: Run multiple instances
3. **Session Store**: Use Redis for shared sessions
4. **Database**: Read replicas for scaling reads

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Optimize database queries
3. Add database indexes

## Maintenance

### Regular Tasks

- [ ] Weekly: Review logs for errors
- [ ] Weekly: Check disk space
- [ ] Monthly: Update dependencies
- [ ] Monthly: Review and optimize database
- [ ] Quarterly: Security audit
- [ ] Yearly: SSL certificate renewal

### Update Procedure

```bash
# Backup database
./backup_db.sh

# Pull latest code
cd /var/www/chatbot
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations (if any)
# python migrate.py

# Restart service
sudo systemctl restart chatbot

# Check status
sudo systemctl status chatbot
```

## Troubleshooting

### Service Won't Start
```bash
sudo systemctl status chatbot
sudo journalctl -u chatbot -n 50
```

### Database Connection Issues
```bash
# Test connection
mysql -h localhost -u chatbot_user -p food_ordering_db

# Check MySQL status
sudo systemctl status mysql
```

### High Memory Usage
```bash
# Check processes
htop

# Restart service
sudo systemctl restart chatbot
```

## Cost Estimation

### Basic Setup (Small Business)
- VPS (2GB RAM, 1 CPU): $10-15/month
- Domain: $12/year
- SSL Certificate: Free (Let's Encrypt)
- **Total**: ~$15/month

### Medium Setup
- VPS (4GB RAM, 2 CPU): $20-30/month
- Managed MySQL: $15/month
- **Total**: ~$45/month

### Enterprise Setup
- Multiple app servers: $100+/month
- Load balancer: $20/month
- Database cluster: $50+/month
- **Total**: $170+/month

## Support

For deployment issues:
1. Check application logs
2. Review Dialogflow webhook logs
3. Verify environment variables
4. Test database connectivity
5. Review server resources

Good luck with your deployment! 🚀
