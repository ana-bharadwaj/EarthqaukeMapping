import folium
import pandas as pd
from folium import plugins

# Read earthquake data from the CSV file (replace 'earthquake_data.csv' with your filename)
df = pd.read_csv('all_month.csv')

# Create a base map centered at the mean latitude and longitude of earthquake
map_center = [df['latitude'].mean(), df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=5)

# Function to determine the circle color based on magnitude
def get_color_from_magnitude(mag):
    # Define your color-coding logic here
    return 'red' if mag > 5.0 else 'orange'

# Plot earthquake locations on the map
for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['mag'] ** 2,
        color='black',
        fill=True,
        fill_color=get_color_from_magnitude(row['mag']),
        fill_opacity=0.7,
        popup=f"mag: {row['mag']}",
    ).add_to(m)
# Custom JavaScript code to add the search bar to the map

search_js = """
var searchControl = new L.Control.Search({
    layer: m,
    propertyName: 'popup',
    marker: false,
    moveToLocation: function(latlng, title, map) {
        var zoom = map.getBoundsZoom(latlng.layer.getBounds());
        map.setView(latlng, zoom); // access the zoom
    }
});
searchControl.on('search:locationfound', function(e) {
    e.layer.openPopup();
});
m.addControl(searchControl);
"""

# Add the custom JavaScript code to the map
m.get_root().add_child(folium.Element(search_js))

# Save the map to an HTML file
m.save("earthquake_map_with_search.html")
