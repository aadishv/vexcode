import asyncio
import time

import pyautogui
from playwright.async_api import async_playwright

import receiver

# type 4 == ring??
#
# blue
# [{'id': 2, 'type': 4, 'location': {'xPos': 143, 'yPos': 44, 'width': 135, 'height': 69}, 'score': 74}]
# red
# [{'id': 1, 'type': 4, 'location': {'xPos': 48, 'yPos': 93, 'width': 135, 'height': 56}, 'score': 97}]
# mogo
# [{'id': 0, 'type': 4, 'location': {'xPos': 33, 'yPos': 46, 'width': 133, 'height': 191}, 'score': 98}]


async def open_page_headless():
    # Launch Playwright
    async with async_playwright() as p:
        # Launch a browser with headless=False to make it visible
        browser = await p.chromium.launch(headless=False)
        # Create a new page
        context = await browser.new_context(permissions=["camera"])
        page = await context.new_page()

        # Navigate to the specified URL
        url = "http://localhost:8000/vexcode.html"
        print(f"Navigating to {url}")

        try:
            response = await page.goto(url)

            # Check if the navigation was successful
            if response and response.ok:
                print(f"Successfully loaded the page. Status: {response.status}")

                # Get page title
                title = await page.title()
                print(f"Page title: {title}")
                await page.evaluate(f"() => {{ {open('test.js', 'r').read()} }}")
                time.sleep(0.1)
                pyautogui.press("tab")
                time.sleep(0.1)
                pyautogui.press("up")
                time.sleep(0.1)
                pyautogui.press("enter")
                time.sleep(0.1)
                await page.evaluate(f"() => {{ {open('test2.js', 'r').read()} }}")
                # Wait longer since we're viewing the browser visually
                print("Browser is visible. Press Ctrl+C to close...")
                receiver.start_app()
            else:
                status = response.status if response else "unknown"
                print(f"Failed to load the page. Status: {status}")

        except Exception as e:
            print(f"An error occurre  {e}")

        finally:
            # Close the browser
            await browser.close()
            print("Browser closed")


# Run the async function
if __name__ == "__main__":
    asyncio.run(open_page_headless())
