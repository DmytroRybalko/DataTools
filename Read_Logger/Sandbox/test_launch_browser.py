import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

# async def main():
#     async with async_playwright() as p:
#         browser = await p.webkit.launch()
#         page = await browser.new_page()
#         await page.goto("https://playwright.dev/")
#         await page.screenshot(path="example.png")
#         #await browser.close()

# asyncio.run(main())



# playwright = sync_playwright().start()
# # Use playwright.chromium, playwright.firefox or playwright.webkit
# # Pass headless=False to launch() to see the browser UI
# browser = playwright.chromium.launch(headless=False)
# page = browser.new_page()
# page.goto("https://playwright.dev/")
# page.screenshot(path="example.png")
# browser.close()
# playwright.stop()


# Launch the browser and navigate to the page
def launch_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://playwright.dev/")
        page.screenshot(path="example.png")
        input("Press Enter to exit and close the browser...")
        browser.close()

def get_table_links():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://192.168.0.102")
        page.click('//*[@id="Storage"]')
        
        # Wait for the table to load (adjust selector if needed)
        page.wait_for_selector('//*[@id="contents"]/tbody/tr[1]/td[3]/a')
        
        # Get all <a> elements in the 3rd <td> of each row
        links = page.query_selector_all('//*[@id="contents"]/tbody/tr/td[3]/a')

        for link in links:
            text = link.inner_text()
            print(text)

        input("Press Enter to exit...")
        browser.close()

if __name__ == "__main__":
    # launch_browser()
    get_table_links()
