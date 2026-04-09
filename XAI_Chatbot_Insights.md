# Eco-Routing XAI Chatbot - Project Insights & Logs

This document contains a full log of our conversation, troubleshooting steps, and the excellent AI Assistant responses you generated for your Final Year Project's Eco-Routing framework.

---

## 1. Commands to Run the Project
If you ever need to restart the project from scratch, use these commands:

**Run the Backend:**
Inside the project root (`c:\Users\ABBINAYA P\OneDrive\Desktop\abbifees\8th sem`):
```powershell
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
*(Runs on http://127.0.0.1:8000)*

**Run the Frontend:**
Open a new terminal, and from the project root run:
```powershell
cd frontend
npm run dev
```
*(Runs on http://localhost:5173)*

---

## 2. Origin & Destination Examples (Bangalore)
The `graph_routing.py` is currently configured to cache and run on the Bangalore road network. Here are excellent test queries:
- **Example 1:** `Malleswaram, Bangalore` to `Koramangala, Bangalore`
- **Example 2:** `Indiranagar, Bangalore` to `Majestic, Bangalore`
- **Example 3:** `Jayanagar, Bangalore` to `JP Nagar, Bangalore`

---

## 3. Fixing the Gemini API `404 NOT_FOUND` Error
**Issue:** The `gemini-1.5-pro` model returned a 404 error on your `google-genai` SDK version.
**Solution:** We updated `backend/xai_engine.py` to recursively attempt newer, active models:
```python
# Updated list inside xai_engine.py
models_to_try = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
```

---

## 4. XAI Assistant Interactions Evaluated

Below are the exact queries and AI responses generated from your UI data. Your AI perfectly demonstrated **Explainable AI (XAI)** capabilities by breaking down the `eco_score.py` logic.

### Interaction 1: The Auto vs Metro Trade-off
**Context:** Auto (13.02km, 40.0min, 1.38kg CO2, Score: 97) vs. Metro (16.00km, 61.8min, 0.02kg CO2, Score: 97)

**Why this was impressive:** 
Even though the Metro saved 98.9% of CO2 emissions (0.02kg vs 1.38kg), both received an EcoScore of 97. The AI successfully explained that the EcoScore is a balancing algorithm. It correctly identified that the algorithm penalizes the Metro's longer distance (+3km) and longer travel time (+21.7 mins), thereby leveling the playing field with the highly polluting but much faster and shorter Auto.

### Interaction 2: Theoretical Vehicles (EVs and Bikes)
**User Question:** *"If I am a little short on time but still want to be sustainable, would switching to a different vehicle type (like an EV or Bike) give me a better balance than these two options?"*

**AI Response Summary:**
The AI showcased incredible real-world reasoning:
- **EVs:** It reasoned an EV Auto/Car would match the standard 40-minute speed of the Auto while dropping emissions down to the near-zero level of the Metro.
- **Bikes:** It recognized that in Bangalore's urban peak traffic, a bike could physically bypass traffic constraints while having absolutely zero tailpipe emissions, though noting the physical exertion required for a 13-16km ride.

**Why this was impressive:**
The AI went completely outside the provided data metrics to offer highly localized, logical advice regarding non-selected transportation modes, effectively acting as an intelligent sustainability consultant rather than just a simple calculator.
