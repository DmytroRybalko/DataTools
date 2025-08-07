import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# URL of the page to parse
#page_url = "http://192.168.0.102/cgi-bin/download"

#%%
page_url = "http://192.168.0.102"

response = requests.get(page_url, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
#%%


playwright = sync_playwright().start()
# Use playwright.chromium, playwright.firefox or playwright.webkit
# Pass headless=False to launch() to see the browser UI
browser = playwright.chromium.launch()
page = browser.new_page()
page.goto("https://playwright.dev/")
page.screenshot(path="example.png")
browser.close()
playwright.stop()

#%%


#%%

//*[@id="Storage"]
/html/body/nav/a[3]

//*[@id="contents"]/tbody/tr[1]/td[3]/a

//*[@id="contents"]/tbody/tr[2]/td[3]/a

//*[@id="contents"]/tbody/tr[3]/td[3]/a


<a href="javascript:void(0);" id="Storage" onclick="loadContent(onloadStorage, this);" class="active">Storage</a>


try:
    response = requests.get(page_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links that match the logger download pattern
    urls = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if "M2001887-" in href:
            if href.startswith("http"):
                full_url = href
            else:
                full_url = f"http://192.168.0.102{href}"
            urls.append(full_url)


    # for a in soup.find_all('a', href=True):
    #     href = a['href']
    #     if href.startswith('/cgi-bin/download?M2001887-'):  # Adjust pattern as needed
    #         full_url = f"http://192.168.0.102{href}"
    #         urls.append(full_url)

    print(f"Found {len(urls)} logger URLs:")
    for url in urls:
        print(url)
except Exception as e:
    print(f"[!] Error: {e}")
