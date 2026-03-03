# ⚡ Quick Start Guide - Crop Assistant AI

Get your AI agricultural assistant running in minutes!

## 🎯 5-Minute Setup

### Option 1: Using Docker Compose (Recommended)

```bash
# 1. Navigate to project directory
cd crop-predictor

# 2. Start all services
docker-compose up -d

# 3. Access the application
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

**That's it!** The entire stack is now running.

---

## 🎯 10-Minute Setup (Local Development)

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run server
python -m uvicorn app.main:app --reload

# Backend running at: http://localhost:8000
```

### Frontend Setup

```bash
# 1. Open new terminal, navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
set REACT_APP_API_URL=http://localhost:8000/api/v1
npm start

# Frontend running at: http://localhost:3000
```

---

## 📝 First Test

### Test 1: Chatbot
```bash
curl -X POST http://localhost:8000/api/v1/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, can you help me with crop diseases?"}'
```

### Test 2: Groundwater Prediction
```bash
curl -X POST http://localhost:8000/api/v1/predictions/groundwater \
  -H "Content-Type: application/json" \
  -d '{
    "rainfall": 150,
    "soil_type": "loamy",
    "temperature": 28,
    "humidity": 65,
    "previous_level": 5.0
  }'
```

### Test 3: Production Forecast
```bash
curl -X POST http://localhost:8000/api/v1/predictions/production \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "rice",
    "area": 1.0,
    "rainfall": 1000,
    "temperature": 26,
    "soil_nutrients": 50
  }'
```

---

## 🖥️ Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | User interface |
| API | http://localhost:8000 | REST API backend |
| API Docs | http://localhost:8000/docs | Swagger UI documentation |
| Database | localhost:5432 | PostgreSQL |
| MongoDB | localhost:27017 | NoSQL database |
| Redis | localhost:6379 | Caching |

---

## 🌐 Web Interface

### Home Page
Landing page with quick access to:
- 💬 Chat Assistant
- 📊 Predictions Dashboard

### Chat Assistant (`/chatbot`)
- Real-time chatbot interface
- Disease detection from images
- Intent-based conversation
- Multi-turn context awareness

**Sample Queries:**
- "My tomato leaves have brown spots"
- "Will groundwater be available this season?"
- "Which crop should I grow?"
- "What's the expected yield?"

### Predictions Dashboard (`/predictions`)
- **Groundwater Prediction**: Water level forecasting
- **Crop Yield Forecast**: Production estimation
- **Irrigation Schedule**: Optimal watering plan
- **Fertilizer Schedule**: Nutrient application plan

---

## 🔧 Configuration

### Environment Variables

**Backend (backend/.env):**
```env
DEBUG=True                          # Set to False in production
DATABASE_URL=postgresql://...       # Database connection
MONGODB_URL=mongodb://localhost     # MongoDB connection
SECRET_KEY=dev-key                  # Change in production
LLM_API_KEY=optional                # For advanced chatbot features
```

**Frontend (frontend/.env):**
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Ports
- Backend API: `8000` (change in `.env` if needed)
- Frontend: `3000` (change in `.env` if needed)
- PostgreSQL: `5432`
- MongoDB: `27017`
- Redis: `6379`

---

## 📊 Using the Chatbot

### Example Conversation 1: Disease Detection
```
User: "My rice plant looks sick"
Bot: "I can help identify plant diseases. Please upload a leaf image 
      or describe the symptoms (color, spots, patterns)."
User: "It has brown spots on the leaves"
Bot: "Based on your description, this might be Early Blight. 
      Here are treatments:..."
```

### Example Conversation 2: Resource Planning
```
User: "How much water does rice need?"
Bot: "Rice typically needs 1000-1500mm per season. 
      Would you like an irrigation schedule?"
User: "Yes, I have 2 hectares"
Bot: "I'll generate an optimal schedule for your conditions..."
```

---

## 📈 Using Predictions

### Step-by-Step: Groundwater Prediction
1. Go to Predictions Dashboard
2. Select **Groundwater** tab
3. Enter:
   - Rainfall (mm): 150
   - Soil type: loamy
   - Temperature (°C): 28
   - Humidity (%): 65
   - Previous level (m): 5
4. Click **Generate Prediction**
5. View results and recommendations

### Step-by-Step: Crop Yield Forecast
1. Go to Predictions Dashboard
2. Select **Crop Yield** tab
3. Enter:
   - Crop type: rice
   - Area (hectares): 1.5
   - Rainfall (mm): 1000
   - Temperature (°C): 26
   - Soil nutrients: 50
4. Click **Generate Prediction**
5. See yield forecast and market estimate

---

## 🚀 Advanced Features

### Disease Detection from Image
1. Click upload button in chatbot
2. Select leaf image (JPG/PNG)
3. Get:
   - Disease name
   - Confidence score
   - Treatment recommendations
   - Prevention measures

### Custom Optimization
Link: `/api/v1/predictions/optimize-resources`

Provides comprehensive planning:
- Water requirements
- Fertilizer schedule
- Cost estimation
- Budget feasibility

---

## 🧹 Maintenance Commands

### Docker Commands
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# Clean up everything
docker-compose down -v
```

### Database Commands
```bash
# Access PostgreSQL
docker-compose exec db psql -U user -d cropdb

# Backup database
docker-compose exec db pg_dump -U user cropdb > backup.sql

# View MongoDB
docker-compose exec mongodb mongosh
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Services Won't Start
```bash
# Check error logs
docker-compose logs -f

# Rebuild images
docker-compose build --no-cache

# Restart
docker-compose restart
```

### Connection Refused
```bash
# Ensure all services are running
docker-compose ps

# Check if services are healthy
docker-compose logs

# Restart specific service
docker-compose restart backend
```

---

## 📚 Key APIs

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chatbot/message` | POST | Send message to chatbot |
| `/chatbot/disease-detection` | POST | Detect disease from image |
| `/predictions/groundwater` | POST | Predict water levels |
| `/predictions/production` | POST | Forecast crop yield |
| `/predictions/irrigation-schedule` | POST | Generate irrigation plan |
| `/predictions/fertilizer-schedule` | POST | Generate fertilizer plan |
| `/predictions/optimize-resources` | POST | Complete optimization |

---

## 📞 Need Help?

### Documentation
- Full API docs: `/docs` (Swagger UI)
- Detailed guide: See `API_DOCUMENTATION.md`
- Deployment: See `DEPLOYMENT.md`

### Common Issues
1. **Database connection fails**: Check DATABASE_URL in .env
2. **Frontend won't load**: Verify REACT_APP_API_URL in frontend/.env
3. **Models not loading**: Check ML model paths in config
4. **Image upload fails**: Ensure file is JPG/PNG and < 10MB

### Debug Mode
```bash
# Run backend with debug logging
DEBUG=True docker-compose up backend

# Check API health
curl http://localhost:8000/health
```

---

## 🎉 Next Steps

1. ✅ **Explore the UI** - Familiarize with interface
2. ✅ **Test chatbot** - Try various queries
3. ✅ **Run predictions** - Generate forecasts
4. ✅ **Upload images** - Test disease detection
5. ✅ **Review API docs** - Understand endpoints
6. ✅ **Run tests** - Verify functionality
7. ✅ **Deploy** - Follow deployment guide

---

## 📦 Project Structure (Quick Reference)

```
crop-predictor/
├── backend/               # Python FastAPI backend
├── frontend/              # React.js frontend
├── docker-compose.yml     # Multi-service orchestration
├── README.md              # Full documentation
├── API_DOCUMENTATION.md   # API reference
└── DEPLOYMENT.md          # Deployment guide
```

---

## 🚀 Quick Command Reference

```bash
# Start everything
docker-compose up -d

# View all logs
docker-compose logs -f

# Stop everything
docker-compose down

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec db psql -U user -d cropdb
```

---

**You're all set!** Start with the frontend at http://localhost:3000 🎉

For detailed documentation, see the main README.md

