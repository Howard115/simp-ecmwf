from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time



def initialize_browser():
    """
    Initialize Chrome webdriver with additional options for AWS environment
    """
    url = "https://charts.ecmwf.int/products/aifs_medium-mslp-wind850?projection=opencharts_south_east_asia_and_indonesia"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # Add these additional arguments for AWS environment
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.binary_location = '/usr/bin/google-chrome'  # Specify Chrome binary location
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def handle_popup_dialog(driver):
    """
    Handle the popup dialog by waiting for it and closing it
    处理弹出对话框：等待对话框出现并关闭它
    """
    try:
        # Increased wait time and added error handling
        dialog_actions = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.MuiDialogActions-root.MuiDialogActions-spacing"))
        )
        close_button = dialog_actions.find_element(By.CSS_SELECTOR, 'button.MuiButtonBase-root span.MuiButton-label')
        close_button.click()
    except Exception as e:
        print(f"Warning: Could not handle popup dialog: {e}")
        # Continue execution even if popup handling fails

def clean_up_images():
    """
    Clean up all files in the weather-chart directory
    清理weather-chart目录中的所有文件
    """
    if os.path.exists("weather-chart"):
        for file in os.listdir("weather-chart"):
            file_path = os.path.join("weather-chart", file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error: {e}")

#--------------------------------
#--------------------------------
class Controller:
    def __init__(self, driver):
        self.driver = driver
        # Added longer wait time and error handling
        try:
            self.forward_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.MuiButtonBase-root.MuiIconButton-root[title="Next"]'))
            )
        except Exception as e:
            print(f"Error initializing controls: {e}")
            raise
        self.backward_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.MuiButtonBase-root.MuiIconButton-root.jss89.jss90[title="Previous"]'))
        )
        
        # Create directory if it doesn't exist
        self.save_dir = "weather-chart"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
    def save_image(self):
        # Wait for image to be present
        image = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img.jss193.jss65.jss197.jss68'))
        )
        
        
        # Find the text element containing the timestamp
        text_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiBox-root.jss73.jss70 div.MuiBox-root.jss93.jss88 div.MuiBox-root.jss94.jss92 p.MuiTypography-root.MuiTypography-body2'))
        )
        timestamp_text = text_element.text
        filename = f"{timestamp_text.replace(' ', '_')}.png"
        
        # Save screenshot of the image
        image.screenshot(os.path.join(self.save_dir, filename))
        print(f"Saved image: {filename}")
        
    def click_forward_button(self):
        self.forward_button.click()
        

    def click_backward_button(self):
        self.backward_button.click()

def main():
    clean_up_images()
    driver = initialize_browser()
    handle_popup_dialog(driver)
    controller = Controller(driver)
    
    for _ in range(61):
        controller.save_image()
        controller.click_forward_button()

    driver.quit()
if __name__ == "__main__":
    main()
