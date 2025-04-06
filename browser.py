import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def open_headless_chromium():
    # Configure Chromium options for headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser"  # Path to Chromium on Ubuntu
    
    try:
        # For older Selenium versions compatible with Chromium 97
        driver = webdriver.Chrome(options=options)
        
        # Open the URL
        url = "http://localhost:8080/vexcode.html"
        print(f"Opening {url} in headless Chromium...")
        driver.get(url)
        
        # Wait for a moment to ensure the page loads
        time.sleep(2)
        
        # Optional: Print the page title to confirm it loaded
        print(f"Page title: {driver.title}")
        
        # Optional: Take a screenshot as proof the page loaded
        driver.save_screenshot("vexcode_screenshot.png")
        print("Screenshot saved as vexcode_screenshot.png")
        
        # Keep the browser open
        input("Press Enter to close the browser...")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()
            print("Browser closed")

if __name__ == "__main__":
    open_headless_chromium()
