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
            self.backward_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.MuiButtonBase-root.MuiIconButton-root[title="Previous"]'))
            )
        except Exception as e:
            print(f"Error initializing controls: {e}")
            raise
        
        # Create directory if it doesn't exist
        self.save_dir = "weather-chart"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
    def save_image(self, current_img_index):
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Wait for image with specific alt text based on index
                expected_alt = f"T+{current_img_index * 6}"
                
                # Use a more specific wait condition
                image = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt*="{expected_alt}"]'))
                )
                
                # Wait for the image to be visible and interactable
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'img[alt*="{expected_alt}"]'))
                )
                
                # Re-fetch the element to avoid stale reference
                image = self.driver.find_element(By.CSS_SELECTOR, f'img[alt*="{expected_alt}"]')
                
                # Find the text element containing the timestamp
                text_element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div.MuiGrid-root.MuiGrid-container > div > div > div.MuiGrid-root.MuiGrid-item > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-lg-9.MuiGrid-grid-xl-10 > div.MuiBox-root > div > div > div > div.MuiBox-root > div.MuiBox-root > div > div.MuiBox-root > p'))
                )
                timestamp_text = text_element.text
                filename = f"{timestamp_text.replace(' ', '_')}.png"
                
                # Add a small delay to ensure the image is fully loaded
                time.sleep(0.1)
                
                # Take screenshot of the specific element
                image.screenshot(os.path.join(self.save_dir, filename))
                print(f"Saved image: {filename}")
                
                # Add a small delay after successful screenshot
                time.sleep(0.5)
                return
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    # Refresh the page if we encounter an error
                    self.driver.refresh()
                    # Handle popup dialog again after refresh
                    handle_popup_dialog(self.driver)
                    # Wait for page to stabilize after refresh
                    time.sleep(0.1)
                else:
                    print(f"Failed to save image after {max_retries} attempts: {str(e)}")
                    raise

    def click_forward_button(self):
        self.forward_button.click()
        

    def click_backward_button(self):
        self.backward_button.click()

def main():
    clean_up_images()
    driver = initialize_browser()
    handle_popup_dialog(driver)
    controller = Controller(driver)
    
    for i in range(61):
        controller.save_image(i)
        controller.click_forward_button()

    driver.quit()
if __name__ == "__main__":
    main()
