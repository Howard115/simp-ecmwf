import streamlit as st
import subprocess
import os
import glob
import re
import asyncio
import threading

class WeatherChartController:
    def __init__(self):
        self.initialize_session_state()
        self.image_files = self.get_sorted_image_files()
        
    def initialize_session_state(self):
        if 'scraper_running' not in st.session_state:
            st.session_state.scraper_running = False
            
        if 'has_run' not in st.session_state:
            self.run_scraper_async()
            st.session_state.has_run = True
        
        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0
    
    def run_scraper_async(self):
        if not st.session_state.scraper_running:
            st.session_state.scraper_running = True
            thread = threading.Thread(target=self._run_scraper_thread)
            thread.daemon = True
            thread.start()
    
    def _run_scraper_thread(self):
        try:
            subprocess.run(["python", "scrapy.py"])
        finally:
            st.session_state.scraper_running = False
    
    @staticmethod
    def get_t_value(filename):
        match = re.search(r'\(T\+(\d+)\)', filename)
        return int(match.group(1)) if match else 0
    
    def get_sorted_image_files(self):
        image_files = glob.glob("weather-chart/*.png")
        return sorted(image_files, key=self.get_t_value)
    
    def handle_previous_button(self):
        if st.button("← Previous"):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
    
    def handle_next_button(self):
        if st.button("Next →"):
            if st.session_state.current_index < len(self.image_files) - 1:
                st.session_state.current_index += 1
    
    def display_current_image(self):
        if self.image_files:
            current_image = self.image_files[st.session_state.current_index]
            st.image(current_image, caption=os.path.basename(current_image))
            st.write(f"Image {st.session_state.current_index + 1} of {len(self.image_files)}")
        else:
            st.write("No images found in the weather-chart directory")
    
    def render(self):
        st.title("Weather Chart Controller")
        
        if st.session_state.scraper_running:
            st.info("Scraping weather charts in background...")
            
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col1:
            self.handle_previous_button()
        with col3:
            self.handle_next_button()
        with col2:
            self.display_current_image()

# Main execution
if __name__ == "__main__":
    controller = WeatherChartController()
    controller.render()




