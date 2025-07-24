import streamlit as st
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES
import io

st.title("Stadtplan: City Map Generator")
st.write("Enter a city name and generate a beautiful map!")

city = st.text_input("City name", placeholder="e.g. Rabat, Morocco")

#Add a selectbox for map styles
style_options = list(STYLES.keys())
selected_style = st.selectbox(
    "Select Map Style",
    options=style_options,
    index=style_options.index("Peach") # Default to Peach
)

if st.button("Generate Map"):
    if city:
        with st.spinner(f"Generating map for {city} using {selected_style} style..."):
            try:
                # 1. Get Area of Interest (AOI)
                aoi = get_aoi(address=city)
                
                # 2. Get OSM geometries within the AOI
                df = get_osm_geometries(aoi=aoi)
                
                # 3. Plot the map
                plot = Plot(
                    df=df,
                    aoi_bounds=aoi.bounds,
                    draw_settings=STYLES[selected_style]
                )
                fig = plot.plot_all()
                
                # 4. Display the map in Streamlit
                st.pyplot(fig)
                
                # 5. Prepare map for download
                buf = io.BytesIO()
                fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.5, dpi=300)
                buf.seek(0) # Reset buffer position to the beginning
                
                st.download_button(
                    label="Download Map Image",
                    data=buf,
                    file_name=f"{city.replace(' ', '_')}_map.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"Error generating map: {e}")
                st.info("Please try a different city name or ensure it's a valid location.")
    else:
        st.error("Please enter a city name.")

        #Sag mir, was du brauchst!
