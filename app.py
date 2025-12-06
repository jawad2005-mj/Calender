import streamlit as st
import calendar
from datetime import datetime, date
import json
import os

# Page configuration
st.set_page_config(
    page_title="Interactive Calendar App",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    
    .main-header {
        text-align: center;
        animation: fadeIn 1s ease-in;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .calendar-container {
        animation: fadeIn 1.2s ease-in;
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .event-card {
        animation: slideIn 0.5s ease-out;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .event-card:hover {
        transform: translateX(10px);
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

def load_events():
    """Load events from JSON file"""
    if os.path.exists('events.json'):
        with open('events.json', 'r') as f:
            return json.load(f)
    return {}

def save_events():
    """Save events to JSON file"""
    with open('events.json', 'w') as f:
        json.dump(st.session_state.events, f, indent=2)

def main():
    # Initialize session state for events
    if 'events' not in st.session_state:
        st.session_state.events = load_events()
    # Header
    st.markdown('<div class="main-header"><h1>📅 Interactive Calendar App</h1><p>Manage your events with style!</p></div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.radio(
        "Choose an option:",
        ["📆 Year Calendar", "📅 Month Calendar", "➕ Add Event", "👀 View Events"]
    )
    
    if page == "📆 Year Calendar":
        show_year_calendar()
    elif page == "📅 Month Calendar":
        show_month_calendar()
    elif page == "➕ Add Event":
        add_event()
    elif page == "👀 View Events":
        view_events()

def show_year_calendar():
    st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
    st.subheader("📆 Full Year Calendar")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        year = st.number_input("Select Year", min_value=1900, max_value=2100, value=datetime.now().year, step=1)
    
    if st.button("🔍 Show Calendar"):
        cal = calendar.calendar(year)
        st.text(cal)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_month_calendar():
    st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
    st.subheader("📅 Monthly Calendar")
    
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Select Year", min_value=1900, max_value=2100, value=datetime.now().year, step=1, key="month_year")
    with col2:
        month = st.selectbox("Select Month", range(1, 13), index=datetime.now().month-1, 
                            format_func=lambda x: calendar.month_name[x])
    
    if st.button("🔍 Show Month"):
        cal = calendar.month(year, month)
        st.text(cal)
        
        # Show events for this month
        month_events = {k: v for k, v in st.session_state.events.items() if k.startswith(f"{year}-{month:02d}")}
        if month_events:
            st.success(f"📌 {len(month_events)} event(s) in this month")
    
    st.markdown('</div>', unsafe_allow_html=True)

def add_event():
    st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
    st.subheader("➕ Add New Event")
    
    col1, col2 = st.columns(2)
    with col1:
        event_date = st.date_input("Select Date", value=date.today())
    with col2:
        event_name = st.text_input("Event Name", placeholder="Enter event description...")
    
    event_time = st.time_input("Event Time (Optional)")
    event_notes = st.text_area("Additional Notes", placeholder="Add any extra details...")
    
    if st.button("💾 Save Event"):
        if event_name:
            date_str = event_date.strftime("%Y-%m-%d")
            st.session_state.events[date_str] = {
                "name": event_name,
                "time": event_time.strftime("%H:%M"),
                "notes": event_notes
            }
            save_events()
            st.success(f"✅ Event '{event_name}' added successfully for {date_str}!")
            st.balloons()
        else:
            st.error("⚠️ Please enter an event name!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def view_events():
    st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
    st.subheader("👀 Your Events")
    
    if not st.session_state.events:
        st.info("📭 No events added yet. Start by adding your first event!")
    else:
        # Sort events by date
        sorted_events = sorted(st.session_state.events.items())
        
        for date_str, event_data in sorted_events:
            # Handle both old and new event formats
            if isinstance(event_data, dict):
                event_name = event_data.get("name", "Unnamed Event")
                event_time = event_data.get("time", "")
                event_notes = event_data.get("notes", "")
            else:
                event_name = event_data
                event_time = ""
                event_notes = ""
            
            with st.expander(f"📅 {date_str} - {event_name}"):
                if event_time:
                    st.write(f"⏰ Time: {event_time}")
                if event_notes:
                    st.write(f"📝 Notes: {event_notes}")
                
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("🗑️ Delete", key=f"del_{date_str}"):
                        del st.session_state.events[date_str]
                        save_events()
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
