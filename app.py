import re
import asyncio
from textwrap import dedent
from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.groq import Groq
from icalendar import Calendar, Event
from datetime import datetime, timedelta, date
import streamlit as st
import os
from dotenv import load_dotenv

# -------------------- Load API Keys from Env --------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not GROQ_API_KEY or not GOOGLE_MAPS_API_KEY:
    st.error("❌ Missing API keys. Please set GROQ_API_KEY and GOOGLE_MAPS_API_KEY in your environment.")
    st.stop()

# -------------------- Helper: Generate ICS --------------------
def generate_ics_content(plan_text: str, start_date: datetime = None) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//AI Travel Planner//github.com//")
    cal.add("version", "2.0")

    if start_date is None:
        start_date = datetime.today()

    day_pattern = re.compile(r"Day (\d+)[:\s]+(.*?)(?=Day \d+|$)", re.DOTALL)
    days = day_pattern.findall(plan_text)

    if not days:
        event = Event()
        event.add("summary", "Travel Itinerary")
        event.add("description", plan_text)
        event.add("dtstart", start_date.date())
        event.add("dtend", start_date.date())
        event.add("dtstamp", datetime.now())
        cal.add_component(event)
    else:
        for day_num, day_content in days:
            day_num = int(day_num)
            current_date = start_date + timedelta(days=day_num - 1)

            event = Event()
            event.add("summary", f"Day {day_num} Itinerary")
            event.add("description", day_content.strip())
            event.add("dtstart", current_date.date())
            event.add("dtend", current_date.date())
            event.add("dtstamp", datetime.now())
            cal.add_component(event)

    return cal.to_ical()

# -------------------- Async Travel Planner --------------------
async def run_mcp_travel_planner(destination: str, num_days: int, preferences: str, budget: int):
    try:
        os.environ["GOOGLE_MAPS_API_KEY"] = GOOGLE_MAPS_API_KEY

        mcp_tools = MultiMCPTools(
            [
                "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt",
                "npx @gongrzhe/server-travelplanner-mcp",
            ],
            env={"GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY},
            timeout_seconds=60,
        )
        await mcp_tools.connect()

        travel_planner = Agent(
            name="Travel Planner",
            role="Creates travel itineraries using Airbnb, Google Maps, and Google Search",
            model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY),
            description=dedent(
                """\
                You are a professional travel consultant AI that creates highly detailed travel itineraries directly.
                You have access to:
                🏨 Airbnb listings
                🗺️ Google Maps MCP
                🔍 Web search for current info
                Always generate a complete itinerary immediately.
                """
            ),
            instructions=[
                "Never ask questions - always generate a complete itinerary",
                "Use Google Maps MCP for distances & travel times",
                "Find Airbnb options within budget",
                "Detailed day-by-day itineraries with addresses, timings, prices",
                "Include weather, safety, packing, and local info",
            ],
            tools=[mcp_tools, GoogleSearchTools()],
            markdown=True,
        )

        prompt = f"""
        Create a very detailed travel itinerary:

        **Destination:** {destination}
        **Duration:** {num_days} days
        **Budget:** ${budget} USD total
        **Preferences:** {preferences}
        """

        response = await travel_planner.arun(prompt)
        return response.content

    finally:
        await mcp_tools.close()

def run_travel_planner(destination: str, num_days: int, preferences: str, budget: int):
    return asyncio.run(run_mcp_travel_planner(destination, num_days, preferences, budget))

# -------------------- Streamlit App --------------------
st.set_page_config(page_title="MCP AI Travel Planner", page_icon="✈️", layout="wide")

if "itinerary" not in st.session_state:
    st.session_state.itinerary = None

st.title("✈️ MCP AI Travel Planner")
st.caption("Plan your next adventure with AI Travel Planner using MCP servers + Groq.")

st.header("🌍 Trip Details")
col1, col2 = st.columns(2)

with col1:
    destination = st.text_input("Destination", placeholder="e.g., Paris, Tokyo, New York")
    num_days = st.number_input("Number of Days", min_value=1, max_value=30, value=7)

with col2:
    budget = st.number_input("Budget (USD)", min_value=100, max_value=10000, step=100, value=2000)
    start_date = st.date_input("Start Date", min_value=date.today(), value=date.today())

preferences_input = st.text_area("🎯 Travel Preferences", placeholder="e.g., adventure, culture, food...")
quick_prefs = st.multiselect(
    "Quick Preferences (optional)",
    ["Adventure", "Relaxation", "Sightseeing", "Food", "Shopping", "Nightlife"],
)
preferences = ", ".join(filter(None, [preferences_input] + quick_prefs)) or "General sightseeing"

# -------------------- Start Button --------------------
if st.button("🚀 Start Planning", type="primary"):
    if not destination:
        st.error("Please enter a destination.")
    else:
        with st.spinner("Generating itinerary with Groq + MCP..."):
            try:
                response = run_travel_planner(destination, num_days, preferences, budget)
                st.session_state.itinerary = response
                st.success("✅ Your itinerary is ready!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

if st.session_state.itinerary:
    ics_content = generate_ics_content(st.session_state.itinerary, datetime.combine(start_date, datetime.min.time()))
    st.download_button("📅 Download as Calendar", data=ics_content, file_name="travel_itinerary.ics", mime="text/calendar")

    st.header("📋 Your Travel Itinerary")
    st.markdown(st.session_state.itinerary)



