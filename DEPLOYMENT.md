# Deployment Guide - Crop Assistant AI

## 🚀 Local Development Deployment

### Prerequisites Checklist
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] Git installed
- [ ] Python 3.11+ (for local backend dev)
- [ ] Node.js 18+ (for local frontend dev)

### Step 1: Clone & Setup
```bash
git clone <repository-url>
cd crop-predictor
```

### Step 2: Configure Environment
Create `.env` files with your settings:

**backend/.env**
```env
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/cropdb
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=dev-key-change-in-production
LLM_API_KEY=optional-api-key
```

**frontend/.env**
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Step 3: Start Services
```bash
# Start all services with Docker Compose
docker-compose up -d

# Verify services are running
docker-compose ps
```

### Step 4: Access Application
- **Frontend**: http://localhost:3000
- **API Swagger Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

### Step 5: Database Setup (if needed)
```bash
# Access PostgreSQL
docker-compose exec db psql -U user -d cropdb

# Run migrations
docker-compose exec backend python -m alembic upgrade head
```

---

## 🌐 Production Deployment

### AWS EC2 Deployment

#### Requirements
- EC2 instance (t3.medium or larger)
- Ubuntu 22.04 LTS
- 20GB+ storage
- Security groups configured

#### Installation Steps

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone <repository-url>
cd crop-predictor

# Create production .env
cat > .env.prod << EOF
DEBUG=False
DATABASE_URL=postgresql://user:secure_password@db/cropdb
MONGODB_URL=mongodb://mongodb/
SECRET_KEY=$(openssl rand -hex 32)
LLM_API_KEY=your-production-api-key
EOF

# Start services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Setup SSL with Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot certonly --standalone -d your-domain.com
```

### Google Cloud Run Deployment

```bash
# Authenticate
gcloud auth login
gcloud config set project PROJECT_ID

# Build and push backend
docker tag crop-predictor-backend gcr.io/PROJECT_ID/crop-predictor-backend:latest
docker push gcr.io/PROJECT_ID/crop-predictor-backend:latest

gcloud run deploy crop-predictor-backend \
  --image gcr.io/PROJECT_ID/crop-predictor-backend:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars "DATABASE_URL=<your-db-url>,SECRET_KEY=<your-key>"

# Build and push frontend
docker tag crop-predictor-frontend gcr.io/PROJECT_ID/crop-predictor-frontend:latest
docker push gcr.io/PROJECT_ID/crop-predictor-frontend:latest

gcloud run deploy crop-predictor-frontend \
  --image gcr.io/PROJECT_ID/crop-predictor-frontend:latest \
  --platform managed \
  --region us-central1
```

### Azure App Service Deployment

```bash
# Login to Azure
az login

# Create resource group
az group create --name crop-predictor --location eastus

# Create App Service with Docker
az appservice plan create --name crop-plan --resource-group crop-predictor --sku B1 --is-linux

# Deploy backend
az webapp create \
  --resource-group crop-predictor \
  --plan crop-plan \
  --name crop-backend \
  --deployment-container-image-name-user-provided

# Deploy frontend
az webapp create \
  --resource-group crop-predictor \
  --plan crop-plan \
  --name crop-frontend \
  --deployment-container-image-name-user-provided
```

---

## 🐳 Docker Production Configuration

**docker-compose.prod.yml**
```yaml
version: '3.8'

services:
  backend:
    image: crop-predictor-backend:latest
    restart: always
    environment:
      DEBUG: "False"
      DATABASE_URL: postgresql://user:password@db/cropdb_prod
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 1G
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: crop-predictor-frontend:latest
    restart: always
    deploy:
      replicas: 2

  db:
    image: postgres:15-alpine
    restart: always
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - frontend
      - backend

volumes:
  postgres_prod_data:
```

---

## 🔒 Security Checklist

- [ ] Change all default passwords
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Use environment variables for secrets
- [ ] Enable CORS properly for your domain
- [ ] Implement rate limiting
- [ ] Setup database backups
- [ ] Enable logging and monitoring
- [ ] Regular security updates
- [ ] Use non-root user in containers

---

## 📊 Monitoring & Logging

### ELK Stack Setup
```bash
# Add to docker-compose.yml
elasticsearch:
  image: elasticsearch:8.0.0
  environment:
    - discovery.type=single-node

logstash:
  image: logstash:8.0.0
  volumes:
    - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

kibana:
  image: kibana:8.0.0
  ports:
    - "5601:5601"
```

### Application Logging
```python
# In backend/app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions (.github/workflows/deploy.yml)
```yaml
name: Deploy Crop Assistant

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Backend
      run: |
        docker build -t crop-predictor-backend:latest ./backend
        docker tag crop-predictor-backend gcr.io/${{ secrets.GCP_PROJECT }}/crop-predictor-backend:${{ github.sha }}
    
    - name: Push to GCR
      run: |
        echo ${{ secrets.GCP_SA_KEY }} | docker login -u _json_key --password-stdin https://gcr.io
        docker push gcr.io/${{ secrets.GCP_PROJECT }}/crop-predictor-backend:${{ github.sha }}
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy crop-predictor-backend \
          --image gcr.io/${{ secrets.GCP_PROJECT }}/crop-predictor-backend:${{ github.sha }}
```

---

## 📈 Scaling

### Horizontal Scaling with Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml crop

# Scale services
docker service scale crop_backend=3
docker service scale crop_frontend=2
```

### Vertical Scaling
- Increase container memory limits
- Increase CPU allocation
- Use faster instances (t3.large → t3.xlarge)

---

## 🔧 Troubleshooting

### Services Not Starting
```bash
# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Complete rebuild
docker-compose down --volumes
docker-compose up -d --build
```

### Database Connection Issues
```bash
# Check database status
docker-compose exec db pg_isready

# Reset PostgreSQL
docker-compose exec db psql -U user -d cropdb -c "DROP DATABASE IF EXISTS cropdb;"
docker-compose exec db psql -U user -c "CREATE DATABASE cropdb;"
```

### High Latency
```bash
# Check resource usage
docker stats

# Monitor network
docker-compose exec backend netstat -an | grep ESTABLISHED

# Optimize with caching
# Enable Redis caching in settings
```

---

## 💾 Backup & Recovery

### Database Backup
```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U user cropdb > backup_$(date +%Y%m%d).sql

# Restore
docker-compose exec -T db psql -U user cropdb < backup_20240310.sql

# Backup MongoDB
docker-compose exec mongodb mongodump --out=/backup
```

### Volume Backup
```bash
# Backup Docker volumes
tar czf backup_$(date +%Y%m%d).tar.gz /var/lib/docker/volumes/

# Restore
tar xzf backup_20240310.tar.gz -C /var/lib/docker/volumes/
```

---

## 📋 Maintenance

### Regular Updates
```bash
# Update base images
docker pull postgres:15
docker pull mongodb:7.0
docker pull node:18

# Rebuild services
docker-compose build --pull
docker-compose down
docker-compose up -d
```

### Health Checks
```bash
# Monitor API
curl http://your-domain/health

# Check database
docker-compose exec db pg_isready

# Verify frontend
curl http://your-domain/
```

---

## 📞 Support & Help

- Check logs: `docker-compose logs -f`
- Review documentation: See README.md & API_DOCUMENTATION.md
- GitHub Issues: Report bugs and feature requests
- Community: Join agricultural tech forums

---

**Last Updated:** March 2024
**Version:** 1.0
