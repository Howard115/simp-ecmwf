import time
import subprocess

def run_crawler():
    while True:
        # Run the crawler script
        subprocess.run(["python", "scrapy.py"])
        # Wait for 6 hours
        time.sleep(21600)  # 6 hours in seconds

if __name__ == "__main__":
    run_crawler()
