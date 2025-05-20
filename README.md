# PathWise – AI-Powered Career Guidance System

**PathWise** is an intelligent, personalized career guidance platform designed to help individuals discover the most suitable career paths based on their strengths, interests, academic background, and aptitude. It uses AI to simulate a real career counselor through data-driven cross-examination and recommendation logic.

## 🚀 Features

- 🎯 Personalized multi-step user onboarding form  
- 🧠 AI-powered aptitude & personality assessment  
- ❓ Dynamic cross-examination for input accuracy  
- 📊 Real-time strength/weakness analysis  
- 🛣️ Custom career roadmap and skill gap suggestions  
- 💾 FastAPI backend with MongoDB  
- ⚛️ React + Tailwind CSS frontend  
- 🔐 Gemini API (Google) integration 

## 📁 Project Structure

ai-career-guide/
├── app/               # FastAPI backend
├── config/            # API keys, DB settings
├── frontend/          # React + Vite + Tailwind UI
├── schemas/           # Pydantic models
├── services/          # Gemini logic, business rules
├── .env               # API keys, secrets (excluded from repo)
├── .gitignore         # Prevents tracking of node_modules, venv, etc.

## 🛠️ Tech Stack

- **Frontend:** React, Vite, Tailwind CSS  
- **Backend:** FastAPI, Pydantic, Uvicorn  
- **AI Integration:** Gemini API (Google)  
- **Database:** MongoDB  
- **Deployment:** GitHub + Render / Vercel (optional)

🔧 Setup

### Backend

```bash
cd ai-career-guide
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload


### Frontend
```bash
cd ai-career-guide/frontend
npm install
npm run dev or yarn dev

🙋‍♀️ Made by Rashi
Connect with me on Github