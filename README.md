# ✈️ AI-Travel-Planner-MCP

* A Streamlit-based AI travel planning application that generates extremely detailed, personalized itineraries using Groq LLMs with MCP servers and Google Maps integration.
* The app connects to Airbnb MCP for real accommodation data and a Google Maps MCP for precise distance and travel time calculations. It also uses Google Search integration for weather, restaurants, attractions, and local insights.

## 🚀 Features

- **🗺️ AI-Generated Travel Itineraries**
  - Automatically generates full itineraries with day-by-day plans  
  - Includes suggested activities, addresses, timings, prices, and local info  

- **📅 Calendar Export**
  - Download itinerary as `.ics` file for easy integration with Google Calendar, Outlook, etc.  

- **🎯 Travel Preferences**
  - Customize itineraries based on user preferences (e.g., adventure, culture, food)  
  - Quick select options: Adventure, Relaxation, Sightseeing, Food, Shopping, Nightlife  

- **🌍 Trip Details Input**
  - Destination, number of days, budget, and start date input via Streamlit UI  

- **🔑 API Integration**
  - **Groq API** for generating detailed AI itineraries  
  - **Google Maps MCP** for location-based calculations (via AI prompts)  
  - Airbnb MCP mentioned in prompts (used via AI)  

- **💻 Tech Stack**
  - Python 3.x  
  - Streamlit for UI  
  - Groq LLM   
  - MCP Tools (`MultiMCPTools`)  
  - Google Search Tools  
  - ICalendar (`icalendar`) for `.ics` export  



## ⚙️ Setup

### Requirements
- **API Keys (Required):**
  - `GROQ_API_KEY` → Get from [Groq Console](https://console.groq.com/)
  - `GOOGLE_MAPS_API_KEY` → Get from [Google Cloud Console](https://console.cloud.google.com/)  
- **Python 3.8+**



# Installation

## 1 :  Navigate to Project Directory:
```bash
cd Ai-travel-MCP
```

## 2 : Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

## 3 : Install the required Python packages:
```bash
pip install -r requirements.txt
```

## 4 : Add a ```.env``` file in the project root:
```bash
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

## 5 : Running the App:
```bash
streamlit run app.py
```



# 🧠 How It Works

* AI Agent (Groq) : Core reasoning & itinerary creation

* Airbnb MCP : Fetches real accommodation listings

* Google Maps MCP : Handles distance, travel times, and location validation

* Google Search Tools : Provides weather, restaurants, and local tips

* Direct Response Generation : Always produces a full itinerary without follow-up questions



