!pip install folium
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Amsterdam Itinerary",
    page_icon="🇳🇱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #ff6b35, #f7931e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .day-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid;
    }
    .day1-card { border-left-color: #e74c3c; background-color: rgba(231, 76, 60, 0.1); }
    .day2-card { border-left-color: #3498db; background-color: rgba(52, 152, 219, 0.1); }
    .day3-card { border-left-color: #2ecc71; background-color: rgba(46, 204, 113, 0.1); }
    .tip-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
        color: #333333;
    }
    .tip-box h4 {
        color: #333333;
        margin-top: 0;
    }
    .tip-box ul {
        color: #333333;
    }
    .tip-box li {
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div class="main-header">
    <h1>🇳🇱 Amsterdam 3-Day Budget Itinerary</h1>
    <p>Your complete guide to exploring Amsterdam on a budget</p>
</div>
""", unsafe_allow_html=True)

# Itinerary data
@st.cache_data
def load_itinerary_data():
    return {
        'day1': {
            'name': 'Day 1: Historic Center & Museums (11am+)',
            'color': '#e74c3c',
            'locations': [
                {'name': 'Dam Square', 'coords': [52.3732, 4.8931], 'marker': '1', 'time': '11am-12pm', 'desc': 'Royal Palace & National Monument'},
                {'name': 'Red Light District', 'coords': [52.3740, 4.8965], 'marker': '2', 'time': '11am-12pm', 'desc': 'Historic atmosphere & architecture'},
                {'name': 'Canal Ring (Herengracht)', 'coords': [52.3645, 4.8848], 'marker': '3', 'time': '12pm-5pm', 'desc': 'UNESCO World Heritage canals'},
                {'name': 'Anne Frank House Area', 'coords': [52.3752, 4.8840], 'marker': '4', 'time': '12pm-5pm', 'desc': 'Historic neighborhood'},
                {'name': 'Westerkerk', 'coords': [52.3744, 4.8831], 'marker': '5', 'time': '12pm-5pm', 'desc': "Rembrandt's burial place"},
                {'name': 'Van Gogh Museum', 'coords': [52.3584, 4.8811], 'marker': '6', 'time': '5pm-7pm', 'desc': 'World-famous art collection'},
                {'name': 'Jordaan District', 'coords': [52.3767, 4.8776], 'marker': '7', 'time': '7pm+', 'desc': 'Dinner & brown cafés'}
            ]
        },
        'day2': {
            'name': 'Day 2: Walking Tour, Parks & Shopping (10:30am-evening)',
            'color': '#3498db',
            'locations': [
                {'name': 'Walking Tour Start (Dam Square)', 'coords': [52.3732, 4.8931], 'marker': 'A', 'time': '10:30am-12:30pm', 'desc': 'Guided walking tour'},
                {'name': 'Vondelpark', 'coords': [52.3579, 4.8686], 'marker': 'B', 'time': '12:30pm-4pm', 'desc': "Amsterdam's most famous park"},
                {'name': 'Miffy Store', 'coords': [52.3507, 4.8944], 'marker': 'C', 'time': '12:30pm-4pm', 'desc': 'Scheldestraat 61 - Dutch souvenirs'},
                {'name': 'Museum Quarter', 'coords': [52.3584, 4.8811], 'marker': 'D', 'time': '4pm-5pm', 'desc': 'Cultural district'},
                {'name': 'Leidseplein', 'coords': [52.3644, 4.8825], 'marker': 'E', 'time': '4pm-5pm', 'desc': 'Street performers & atmosphere'},
                {'name': 'Bloemenmarkt (Flower Market)', 'coords': [52.3672, 4.8907], 'marker': 'F', 'time': '4pm-5pm', 'desc': 'Famous flower market'},
                {'name': 'Nieuwmarkt', 'coords': [52.3720, 4.9009], 'marker': 'G', 'time': '5pm+', 'desc': 'Dinner & evening atmosphere'}
            ]
        },
        'day3': {
            'name': 'Day 3: Markets & Local Life (9am-2pm)',
            'color': '#2ecc71',
            'locations': [
                {'name': 'Albert Cuyp Market', 'coords': [52.3565, 4.8913], 'marker': 'i', 'time': '9am-11am', 'desc': "Amsterdam's famous street market"},
                {'name': 'Sarphatipark', 'coords': [52.3543, 4.8965], 'marker': 'ii', 'time': '11am-1pm', 'desc': 'Local park in De Pijp'},
                {'name': 'De Pijp Neighborhood', 'coords': [52.3540, 4.8910], 'marker': 'iii', 'time': '11am-1pm', 'desc': 'Trendy area with street art & cafés'},
                {'name': 'Museumplein', 'coords': [52.3598, 4.8810], 'marker': 'iv', 'time': '1pm-2pm', 'desc': 'Final photos & souvenir shopping'}
            ]
        }
    }

@st.cache_data
def create_map(locations_data, selected_days):
    """Create the folium map with selected days"""
    m = folium.Map(
        location=[52.3676, 4.9041],
        zoom_start=13,
        tiles='OpenStreetMap'
    )
    
    # Add markers and routes for selected days
    for day_key in selected_days:
        if day_key in locations_data:
            day_data = locations_data[day_key]
            color = day_data['color']
            locations = day_data['locations']
            day_name = day_data['name']
            
            # Create route coordinates
            route_coords = [loc['coords'] for loc in locations]
            
            # Add walking route
            folium.PolyLine(
                locations=route_coords,
                color=color,
                weight=3,
                opacity=0.8,
                dash_array='10,5',
                popup=f"Walking route for {day_name}"
            ).add_to(m)
            
            # Add markers
            for loc in locations:
                # Create popup content
                popup_html = f"""
                <div style="font-family: Arial, sans-serif; width: 280px; max-width: 280px;">
                    <h3 style="margin: 0 0 10px 0; color: {color}; font-size: 18px; border-bottom: 2px solid {color}; padding-bottom: 5px;">
                        <strong>{loc['marker']}. {loc['name']}</strong>
                    </h3>
                    <div style="margin: 10px 0; padding: 8px; background-color: #f8f9fa; border-radius: 5px;">
                        <p style="margin: 2px 0; font-weight: bold; color: #495057;">
                            📅 {day_name.split(':')[0]}
                        </p>
                        <p style="margin: 2px 0; font-weight: bold; color: #6c757d;">
                            ⏰ {loc['time']}
                        </p>
                    </div>
                    <p style="margin: 8px 0; color: #212529; font-size: 14px;">
                        📍 {loc['desc']}
                    </p>
                </div>
                """
                
                # Create custom marker icon
                icon_html = f'''
                <div style="
                    background-color: {color};
                    border: 3px solid white;
                    border-radius: 50%;
                    width: 35px;
                    height: 35px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-weight: bold;
                    color: white;
                    font-size: 16px;
                    box-shadow: 0 3px 8px rgba(0,0,0,0.4);
                    font-family: Arial, sans-serif;
                ">
                    {loc['marker']}
                </div>
                '''
                
                # Add marker
                folium.Marker(
                    location=loc['coords'],
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.DivIcon(html=icon_html, icon_size=(35, 35), icon_anchor=(17, 17)),
                    tooltip=f"{loc['marker']}. {loc['name']} ({loc['time']})"
                ).add_to(m)
    
    return m

# Load data
locations_data = load_itinerary_data()

# Sidebar
with st.sidebar:
    st.header("🗺️ Map Controls")
    
    # Day selector
    st.subheader("Select Days to Display")
    day_options = {
        'day1': '🔴 Day 1: Historic Center',
        'day2': '🔵 Day 2: Walking Tour & Parks', 
        'day3': '🟢 Day 3: Markets & Local Life'
    }
    
    selected_days = []
    for day_key, day_label in day_options.items():
        if st.checkbox(day_label, value=True, key=day_key):
            selected_days.append(day_key)
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📊 Trip Overview")
    total_locations = sum(len(locations_data[day]['locations']) for day in selected_days)
    st.metric("Total Locations", total_locations)
    st.metric("Duration", "3 Days")
    st.metric("Budget Level", "💰 Low")
    
    st.markdown("---")
    
    # Export options
    st.subheader("📥 Export Options")
    if st.button("📋 Download Itinerary", type="secondary"):
        # Create summary DataFrame
        summary_data = []
        for day_key in selected_days:
            day_data = locations_data[day_key]
            for loc in day_data['locations']:
                summary_data.append({
                    'Day': day_data['name'].split(':')[0],
                    'Marker': loc['marker'],
                    'Location': loc['name'],
                    'Time': loc['time'],
                    'Description': loc['desc']
                })
        
        df = pd.DataFrame(summary_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="amsterdam_itinerary.csv",
            mime="text/csv"
        )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Interactive Map")
    
    if selected_days:
        # Create and display map
        map_obj = create_map(locations_data, selected_days)
        map_data = st_folium(map_obj, width=700, height=500, returned_objects=["last_object_clicked"])
        
        # Show clicked location info
        if map_data['last_object_clicked']:
            st.success("💡 Click on map markers for detailed information!")
    else:
        st.warning("⚠️ Please select at least one day to display on the map.")

with col2:
    st.subheader("📅 Daily Itinerary")
    
    # Day tabs
    if selected_days:
        for day_key in selected_days:
            day_data = locations_data[day_key]
            
            # Day header
            day_class = f"{day_key}-card"
            st.markdown(f"""
            <div class="day-card {day_class}">
                <h4>{day_data['name']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Locations for this day
            with st.expander(f"View {day_data['name'].split(':')[0]} Details", expanded=True):
                for loc in day_data['locations']:
                    st.markdown(f"""
                    **{loc['marker']}. {loc['name']}**  
                    ⏰ {loc['time']}  
                    📍 {loc['desc']}
                    """)
                    st.markdown("---")

# Budget Tips Section
st.markdown("---")
st.subheader("💡 Budget Tips")

tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown("""
    <div class="tip-box">
        <h4>🚶 Transportation</h4>
        <ul>
            <li>Walk or rent a bike instead of public transport</li>
            <li>Amsterdam is very walkable</li>
            <li>Bike rentals: €10-15/day</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tip-box">
        <h4>🏛️ Attractions</h4>
        <ul>
            <li>Many churches and markets are free</li>
            <li>Book Van Gogh Museum online for discounts</li>
            <li>Free walking tours available (tip-based)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tips_col2:
    st.markdown("""
    <div class="tip-box">
        <h4>🍽️ Food & Drink</h4>
        <ul>
            <li>Pack snacks and drinks</li>
            <li>Look for lunch deals at local cafés</li>
            <li>Happy hour: 4-6pm at many bars</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tip-box">
        <h4>🛍️ Shopping</h4>
        <ul>
            <li>Albert Cuyp Market: cheapest souvenirs</li>
            <li>Bloemenmarkt: free to browse</li>
            <li>Miffy Store: unique Dutch gifts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🇳🇱 <strong>Amsterdam 3-Day Budget Itinerary</strong> 🇳🇱</p>
    <p>Made with ❤️ using Streamlit • Total locations: {total} • Walking distance: Perfect for exploring!</p>
</div>
""".format(total=sum(len(locations_data[day]['locations']) for day in locations_data.keys())), unsafe_allow_html=True)
