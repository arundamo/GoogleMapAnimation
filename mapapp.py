import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapi")

def get_coordinates(city_name):
    """Get latitude and longitude for a city name."""
    try:
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except Exception as e:
        st.error(f"Error getting coordinates for {city_name}: {e}")
        return None

def generate_map(from_coords, to_coords):
    """Generate a map with markers and a line between two points."""
    # Initialize map centered at the midpoint
    mid_lat = (from_coords[0] + to_coords[0]) / 2
    mid_lon = (from_coords[1] + to_coords[1]) / 2
    travel_map = folium.Map(location=[mid_lat, mid_lon], zoom_start=4)

    # Add markers
    folium.Marker(location=from_coords, tooltip="From").add_to(travel_map)
    folium.Marker(location=to_coords, tooltip="To").add_to(travel_map)

    # Add a line connecting the two points
    folium.PolyLine([from_coords, to_coords], color="blue", weight=2.5, opacity=1).add_to(travel_map)

    return travel_map

# Streamlit app interface
st.title("Travel Map Generator")
st.write("Enter two city names to generate a travel map.")

# Input for cities
from_city = st.text_input("From City", placeholder="e.g., New York")
to_city = st.text_input("To City", placeholder="e.g., Los Angeles")

# Placeholder to retain the map in the UI
map_placeholder = st.empty()

if st.button("Generate Map"):
    if from_city and to_city:
        # Get coordinates for both cities
        from_coords = get_coordinates(from_city)
        to_coords = get_coordinates(to_city)

        if from_coords and to_coords:
            st.success(f"Generating travel map from {from_city} to {to_city}...")
            # Generate map
            travel_map = generate_map(from_coords, to_coords)

            # Use placeholder to display the map
            with map_placeholder:
                st_folium(travel_map, width=700, height=500)
        else:
            st.error("Could not find coordinates for one or both cities. Please try again.")
    else:
        st.error("Both city fields are required!")