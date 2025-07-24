import streamlit as st
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES
import io
import numpy as np

st.title("Stadtplan: City Map Generator")
st.write("Enter a city name and generate a beautiful map!")

city = st.text_input("City name", placeholder="e.g. Rabat, Morocco")

style_options = list(STYLES.keys())
selected_style = st.selectbox(
    "Select Map Style",
    options=style_options,
    index=style_options.index("Peach")  # Default style
)

def mask_logo(fig, logo_height_frac=0.09, logo_width_frac=0.19):
    # Render the figure to a NumPy array (RGB image)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight', pad_inches=0.5)
    buf.seek(0)
    import PIL.Image
    img = PIL.Image.open(buf).convert("RGB")
    arr = np.array(img)

    # Compute the mask rectangle pixel coordinates (bottom-right corner)
    h, w, _ = arr.shape
    logo_h = int(logo_height_frac * h)
    logo_w = int(logo_width_frac * w)
    # Fill the rectangle with white
    arr[h-logo_h:h, w-logo_w:w, :] = 255
    
    # Convert back to PIL Image and update buffer
    img_masked = PIL.Image.fromarray(arr)
    buf_masked = io.BytesIO()
    img_masked.save(buf_masked, format="PNG")
    buf_masked.seek(0)
    return buf_masked, img_masked

if st.button("Generate Map"):
    if city:
        with st.spinner(f"Generating map for {city} using {selected_style} style..."):
            try:
                aoi = get_aoi(address=city)
                df = get_osm_geometries(aoi=aoi)
                plot = Plot(
                    df=df,
                    aoi_bounds=aoi.bounds,
                    draw_settings=STYLES[selected_style]
                )
                fig = plot.plot_all()
                
                # Mask the image in pixel space
                masked_buf, masked_img = mask_logo(fig)
                st.image(masked_img)

                st.download_button(
                    label="Download Map Image",
                    data=masked_buf,
                    file_name=f"{city.replace(' ', '_')}_map.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error(f"Error generating map: {e}")
                st.info("Please try a different city name or ensure it's a valid location.")
    else:
        st.error("Please enter a city name.")



