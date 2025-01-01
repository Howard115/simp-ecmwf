import streamlit as st
import os
import glob
import re
import datetime


class WeatherChartController:
    def __init__(self):
        self.initialize_session_state()
        self.image_files = self.get_sorted_image_files()

    def initialize_session_state(self):
        if "current_index" not in st.session_state:
            st.session_state.current_index = 0
    @staticmethod
    def get_t_value(filename):
        match = re.search(r"\(T\+(\d+)\)", filename)
        return int(match.group(1)) if match else 0

    def get_sorted_image_files(self):
        image_files = glob.glob("weather-chart/*.png")
        return sorted(image_files, key=self.get_t_value)

    def handle_previous_button(self):
        if st.button("← 上一張"):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1

    def handle_next_button(self):
        if st.button("下一張 →"):
            if st.session_state.current_index < len(self.image_files) - 1:
                st.session_state.current_index += 1

    def display_current_image(self):
        if self.image_files:
            current_image = self.image_files[st.session_state.current_index]

            # Extract date and time from filename
            filename = os.path.basename(current_image)
            date_match = re.match(
                r"([A-Za-z]+)_(\d+)_([A-Za-z]+)_(\d+)_(\d+)_UTC", filename
            )
            if date_match:
                weekday, day, month, year, utc_hour = date_match.groups()
                # Convert UTC to UTC+8
                utc_time = datetime.datetime(
                    int(year),
                    datetime.datetime.strptime(month, "%b").month,
                    int(day),
                    int(utc_hour),
                )
                local_time = utc_time + datetime.timedelta(hours=8)

                # Format the display
                st.markdown(
                    f"""
                    <div style='text-align: center;'>
                        <h5>{local_time.strftime('%Y-%m-%d-%H:00')} (台灣時間)</h5>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            st.image(current_image)
            st.write(
                f"第 {st.session_state.current_index + 1} / 共{len(self.image_files)}"
            )
        else:
            st.write("目錄中找不到氣象圖")

    def render(self):
        st.title("AI 氣象圖")

        if len(self.image_files) < 61:
            progress = len(self.image_files) / 61
            st.progress(progress)
            st.info("正在爬取氣象圖...")

        # Add reset button
        if st.button("回到第一張"):
            st.session_state.current_index = 0

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
