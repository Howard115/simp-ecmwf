import streamlit as st
import subprocess
import os
from PIL import Image
import glob
import re

st.title("Weather Chart Controller")

# Run the scrapy.py script to get images
if 'has_run' not in st.session_state:
    with st.spinner('Running scrapy.py to generate weather chart images...'):
        subprocess.run(["python", "scrapy.py"])
    st.session_state.has_run = True
    
# Initialize current image index in session state
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Get list of all weather chart images and sort by T+ value
def get_t_value(filename):
    match = re.search(r'\(T\+(\d+)\)', filename)
    return int(match.group(1)) if match else 0

# Get and sort image files
image_files = glob.glob("weather-chart/*.png")
image_files.sort(key=get_t_value)

# Rest of the code remains the same
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    if st.button("← Previous"):
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1

with col3:
    if st.button("Next →"):
        if st.session_state.current_index < len(image_files) - 1:
            st.session_state.current_index += 1

with col2:
    if image_files:
        current_image = image_files[st.session_state.current_index]
        st.image(current_image, caption=os.path.basename(current_image))
        st.write(f"Image {st.session_state.current_index + 1} of {len(image_files)}")
    else:
        st.write("No images found in the weather-chart directory")




