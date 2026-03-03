# Environment Setup

## Backend (FastAPI)
```bash
cd backend
python -m venv .venv

# Linux/macOS (bash/zsh)
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

pip install -r requirements.txt
cp .env.example .env 2>/dev/null || true
DATABASE_URL=sqlite:///./crop_assistant.db python -m uvicorn app.main:app --reload
```

> If PowerShell blocks script execution, run once (as current user):
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Frontend (React)
```bash
cd frontend
npm install
REACT_APP_API_URL=http://localhost:8000/api/v1 npm start
```

## Optional Docker
```bash
docker compose up --build
```

## Retrain ML models
```bash
cd backend
python ml/training/groundwater_train.py
python ml/training/crop_yield_train.py
# requires tensorflow:
python ml/training/crop_disease_train.py
# optional hybrid recommender:
python ml/training/train_resource_recommender.py
```


## Preview production build (frontend)
```bash
cd frontend
npm install
npm run build:preview
# opens static preview at http://localhost:4173
```
