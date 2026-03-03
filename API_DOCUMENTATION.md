# API Documentation - Crop Assistant AI

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently uses no authentication (open API). For production, implement JWT tokens.

---

## 🤖 Chatbot Endpoints

### 1. Send Message to Chatbot
**POST** `/chatbot/message`

**Request Body:**
```json
{
  "message": "My tomato leaves have brown spots",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "user_message": "My tomato leaves have brown spots",
  "intent": "disease_detection",
  "confidence": 0.92,
  "chatbot_response": "I detected you want disease identification...",
  "action": "disease_detection",
  "requires_action": true
}
```

**Intent Types:**
- `disease_detection` - Plant disease identification
- `groundwater_prediction` - Water level forecasting
- `crop_recommendation` - Suitable crop suggestions
- `production_forecast` - Yield prediction
- `resource_management` - Scheduling optimization
- `general_chat` - General assistance

---

### 2. Disease Detection from Image
**POST** `/chatbot/disease-detection`

**Request:**
- Form data with file upload

**Response:**
```json
{
  "success": true,
  "disease": "Tomato___Early blight",
  "confidence": 0.94,
  "confidence_percentage": "94.23%",
  "treatments": [
    "Remove lower leaves",
    "Apply fungicide",
    "Increase air circulation",
    "Avoid overhead watering"
  ],
  "prevention": [
    "Maintain plant hygiene",
    "Ensure proper spacing",
    "Avoid overhead watering",
    "Rotate crops"
  ]
}
```

---

### 3. Get Chat History
**GET** `/chatbot/history`

**Response:**
```json
{
  "history": [
    {
      "user": "Hello",
      "intent": "general_chat",
      "confidence": 0.98,
      "parameters": {}
    }
  ]
}
```

---

### 4. Clear Chat History
**POST** `/chatbot/clear-history`

**Response:**
```json
{
  "message": "History cleared"
}
```

---

## 📊 Predictions Endpoints

### 1. Groundwater Level Prediction
**POST** `/predictions/groundwater`

**Request Body:**
```json
{
  "rainfall": 150.0,
  "soil_type": "loamy",
  "temperature": 28.5,
  "humidity": 65.0,
  "previous_level": 4.5,
  "region": "Delhi"
}
```

**Response:**
```json
{
  "success": true,
  "groundwater_level": 5.2,
  "groundwater_level_meters": "5.20m",
  "risk_level": "MEDIUM",
  "recommendations": [
    "Maintain current irrigation schedule",
    "Monitor water levels monthly",
    "Use sprinkler irrigation",
    "Plan for dry season"
  ]
}
```

**Soil Types:** loamy, sandy, clay, silty
**Risk Levels:** CRITICAL, HIGH, MEDIUM, LOW

---

### 2. Crop Production Forecast
**POST** `/predictions/production`

**Request Body:**
```json
{
  "crop_type": "rice",
  "area": 2.5,
  "rainfall": 1000.0,
  "temperature": 26.5,
  "humidity": 70.0,
  "soil_nutrients": 55.0,
  "season": "monsoon",
  "fertilizer_amount": 100.0
}
```

**Response:**
```json
{
  "success": true,
  "crop": "rice",
  "yield_per_hectare_kg": 5320.5,
  "total_production_kg": 13301.25,
  "total_production_tons": 13.30,
  "quality_score": "EXCELLENT",
  "confidence": 0.87,
  "recommendations": [
    "Maintain current farming practices",
    "Plan storage for harvest",
    "Prepare marketing channels",
    "Document best practices"
  ],
  "market_estimate": {
    "estimated_price_per_kg": 25,
    "estimated_total_revenue": 332531.25,
    "currency": "INR"
  }
}
```

**Crops Supported:** rice, wheat, corn, tomato, potato, cotton, sugarcane
**Quality Scores:** EXCELLENT, GOOD, AVERAGE

---

### 3. Irrigation Schedule Generation
**POST** `/predictions/irrigation-schedule`

**Request Body:**
```json
{
  "crop_type": "rice",
  "area": 1.0,
  "season": "monsoon",
  "rainfall": 200.0,
  "soil_type": "loamy"
}
```

**Response:**
```json
{
  "success": true,
  "crop": "rice",
  "season": "monsoon",
  "total_water_requirement_mm": 1250.0,
  "expected_rainfall_mm": 200.0,
  "irrigation_water_needed_mm": 1050.0,
  "irrigation_interval_days": 7,
  "total_irrigation_water_liters": 105000000.0,
  "schedule": [
    {
      "irrigation_number": 1,
      "date": "2024-03-10",
      "days_after_sowing": 0,
      "water_required_mm": 70.0
    }
  ],
  "recommendations": [
    "Water early morning or late evening",
    "Use drip or sprinkler irrigation",
    "Monitor soil moisture before irrigation",
    "Adjust schedule based on rainfall"
  ]
}
```

**Seasons:** monsoon, summer, winter, spring
**Soil Types:** sandy, loamy, clay, silty

---

### 4. Fertilizer Schedule Generation
**POST** `/predictions/fertilizer-schedule`

**Request Body:**
```json
{
  "crop_type": "rice",
  "area": 1.0,
  "current_soil_nutrients": {
    "N": 20,
    "P": 10,
    "K": 15
  }
}
```

**Response:**
```json
{
  "success": true,
  "crop": "rice",
  "current_soil_nutrients": {
    "N": 20,
    "P": 10,
    "K": 15
  },
  "required_nutrients": {
    "N": 80,
    "P": 40,
    "K": 40
  },
  "nutrient_deficiency": {
    "N": 60.0,
    "P": 30.0,
    "K": 25.0
  },
  "total_fertilizer_needed_kg": 1150.0,
  "schedule": [
    {
      "stage": "basal",
      "date": "2024-03-10",
      "nutrients": {
        "N": 18.0,
        "P": 30.0,
        "K": 12.5
      },
      "total_kg": 60.5
    }
  ],
  "recommendations": [
    "Apply organic fertilizers for soil health",
    "Use NPK ratio suitable for crop",
    "Split applications across growth stages",
    "Monitor soil pH"
  ]
}
```

---

### 5. Resource Optimization
**POST** `/predictions/optimize-resources`

**Request Body:**
```json
{
  "crop_type": "rice",
  "area": 2.0,
  "budget": 50000.0,
  "season": "monsoon",
  "rainfall": 200.0,
  "soil_type": "loamy",
  "temperature": 28.0,
  "humidity": 70.0,
  "current_soil_nutrients": {
    "N": 20,
    "P": 10,
    "K": 15
  }
}
```

**Response:**
```json
{
  "success": true,
  "crop": "rice",
  "area": 2.0,
  "total_budget": 50000.0,
  "estimated_cost": {
    "water_cost": 1000.0,
    "fertilizer_cost": 57500.0,
    "labor_cost": 800.0,
    "pesticide_cost": 600.0,
    "equipment_cost": 100.0,
    "total_cost": 60000.0
  },
  "feasibility": "OVER_BUDGET",
  "irrigation_schedule": {...},
  "fertilizer_schedule": {...},
  "optimization_tips": [
    "Consider deficit irrigation",
    "Use organic fertilizers",
    "Apply fertilizer in fewer stages",
    "Use cooperative labor"
  ]
}
```

**Feasibility:** FEASIBLE, OVER_BUDGET

---

## 📋 Data Schemas

### Soil Types
- `loamy` - Balanced, ideal for most crops
- `sandy` - Well-draining, low nutrients
- `clay` - High nutrients, poor drainage
- `silty` - Fine particles, moderate drainage

### Crop Types
- `rice` - Monsoon crop, high water needs
- `wheat` - Rabi crop, moderate water
- `corn` - Needs warm weather
- `tomato` - Vegetable crop
- `potato` - Underground tuber crop
- `cotton` - Long-cycle crop
- `sugarcane` - High water requirements

### Seasons
- `monsoon` - High rainfall, high humidity
- `summer` - High temperature, low rainfall
- `winter` - Low temperature, variable rainfall
- `spring` - Moderate conditions

---

## 🔄 Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 422 | Validation Error |
| 500 | Server Error |

---

## 📱 Chatbot Sample Conversations

### 1. Disease Detection
```
User: "My tomato leaves have brown spots"
Bot: "I detected disease identification. Please upload a leaf image..."
```

### 2. Crop Recommendation
```
User: "What crop should I grow?"
Bot: "I can recommend suitable crops. Tell me your soil type..."
```

### 3. Production Forecast
```
User: "What will be the yield this season?"
Bot: "For yield prediction, share crop type, area, and soil nutrients..."
```

---

## 🚀 Quick Test Commands

```bash
# Test chatbot
curl -X POST http://localhost:8000/api/v1/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'

# Test groundwater prediction
curl -X POST http://localhost:8000/api/v1/predictions/groundwater \
  -H "Content-Type: application/json" \
  -d '{
    "rainfall": 150,
    "soil_type": "loamy",
    "temperature": 28,
    "humidity": 65,
    "previous_level": 5
  }'

# Test production forecast
curl -X POST http://localhost:8000/api/v1/predictions/production \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "rice",
    "area": 1,
    "rainfall": 1000,
    "temperature": 26,
    "humidity": 70,
    "soil_nutrients": 50
  }'
```

---

## 📚 Integration Examples

### JavaScript/React
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// Send chatbot message
const response = await axios.post(`${API_URL}/chatbot/message`, {
  message: 'Disease detection for tomato',
});

// Groundwater prediction
const gw = await axios.post(`${API_URL}/predictions/groundwater`, {
  rainfall: 150,
  soil_type: 'loamy',
  temperature: 28,
  humidity: 65,
  previous_level: 5,
});
```

### Python
```python
import requests

API_URL = 'http://localhost:8000/api/v1'

# Send message
response = requests.post(
    f'{API_URL}/chatbot/message',
    json={'message': 'My plants are dying'}
)
print(response.json())

# Production forecast
forecast = requests.post(
    f'{API_URL}/predictions/production',
    json={
        'crop_type': 'rice',
        'area': 2.5,
        'rainfall': 1000,
        'temperature': 26,
    }
)
print(forecast.json())
```

---

**Last Updated:** March 2024
**API Version:** v1.0
