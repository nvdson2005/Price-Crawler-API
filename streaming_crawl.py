from playwright.async_api import async_playwright, Browser, Playwright
from urllib.parse import urljoin
from base_crawler import CrawlSite

class BachHoaXanhCrawler(CrawlSite):
    base_url = "https://bachhoaxanh.com"
    site_name = "BachHoaXanh"
    def __init__(self):
        super().__init__(self.base_url, self.site_name)
        
    async def crawl_prod_prices(self, prod_name: str, current_browser: Browser):
        context = await current_browser.new_context()
        page = await context.new_page()
        await page.goto(f"{self.base_url}/tim-kiem?key={prod_name}")
        await page.wait_for_load_state('networkidle')
        products = await page.locator('xpath=//html/body/div[1]/div/div[2]/div/main/div/div[2]/div').all()
        print(f"Found {len(products)} products on BachHoaXanh") 
        for i, product in enumerate(products):
            if i >= 5:
                break
            try:
                p_name = (await product.locator('css=h3').text_content()).strip()
                price_and_per = (await product.locator('css=div.product_price').text_content()).strip().split('đ')
                p_price = price_and_per[0].strip()
                p_per = price_and_per[1].strip()[1:] if len(price_and_per) > 1 else ''
                p_url_elements = await product.locator('css=a').all()
                p_url = await p_url_elements[0].get_attribute('href') if len(p_url_elements) > 0 else await product.locator('css=a').get_attribute('href')
                p_url = (p_url).strip()
                p_img_elements = await product.locator('css=img').all()
                p_img = await p_img_elements[0].get_attribute('src') if len(p_img_elements) > 0 else await product.locator('css=img').get_attribute('src')
                yield {
                    'name': p_name,
                    'price': p_price,
                    'per': p_per,
                    'url': urljoin(self.base_url, p_url),
                    'img': p_img,
                    'source': self.site_name
                }
            except Exception as e:
                print(f"Error processing product {i}: {e}")
        await page.close()
        await context.close()
        if page.is_closed():
            print(f"Stop crawling from {self.base_url}")

class WinmartCrawler(CrawlSite):
    base_url = "https://winmart.vn"
    site_name = "Winmart"
    
    def __init__(self):
        super().__init__(self.base_url, self.site_name)
    
    async def crawl_prod_prices(self, prod_name, current_browser):
        context = await current_browser.new_context()
        page = await context.new_page()
        await page.goto(f"{self.base_url}/search/{prod_name}") 
        await page.wait_for_load_state('networkidle')
        products = await page.locator('xpath=/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div').all()
        print(f"Found {len(products)} products on Winmart")
        for i, product in enumerate(products):
            if i >= 5:
                break
            p_name = (await product.locator('css=div.product-card-two__Title-sc-1lvbgq2-6').inner_text()).strip()
            p_price = (await product.locator('css=div.product-card-two__Price-sc-1lvbgq2-9').inner_text())[:-2].strip()
            p_per = (await product.locator('xpath=./div/div[2]').inner_text()).strip()
            p_url_elements = await product.locator('css=a').all()
            p_url = await p_url_elements[0].get_attribute('href') if len(p_url_elements) > 0 else await product.locator('css=a').get_attribute('href')
            p_url = (p_url).strip()
            p_img = (await product.locator('css=img.product-image').get_attribute('src')).strip()
            yield {
                'name': p_name,
                'price': p_price,
                'per': p_per,
                'url': urljoin(self.base_url, p_url),
                'img': p_img,
                'source': self.site_name
            }
        await page.close()
        await context.close()
        if page.is_closed():
            print(f"Stop crawling from {self.base_url}")

class CoopOnlineCrawler(CrawlSite):
    base_url = "https://cooponline.vn"
    site_name = "Co.op Online"
    
    def __init__(self):
        super().__init__(self.base_url, self.site_name)
    
    async def crawl_prod_prices(self, prod_name, current_browser):
        context = await current_browser.new_context()
        page = await context.new_page()
        await page.goto(f"{self.base_url}/search?router=productListing&query={prod_name}") 
        await page.wait_for_load_state('networkidle')
        products = await page.locator('css=div.css-1y2krk0 div.css-13w7uog').all()
        print(f"Found {len(products)} products on Coop Online")
        for i, product in enumerate(products):
            if i >= 5:
                break
            p_name = (await product.locator('css=h3.css-1xdyrhj').inner_text()).strip()
            p_price = (await product.locator('css=div.att-product-detail-latest-price').inner_text())[:-2].strip()
            p_per = (await product.locator('css=div.css-1f5a6jh').inner_text())[13:].strip()
            p_url_elements = await product.locator('css=a').all()
            p_url = await p_url_elements[0].get_attribute('href') if len(p_url_elements) > 0 else await product.locator('css=a').get_attribute('href')
            p_url = (p_url).strip()
            p_img = (await product.locator('css=img').get_attribute('src')).strip()
            yield {
                'name': p_name,
                'price': p_price,
                'per': p_per,
                'url': urljoin(self.base_url, p_url),
                'img': p_img,
                'source': self.site_name
            }
        await page.close()
        await context.close()
        if page.is_closed():
            print(f"Stop crawling from {self.base_url}")
        
async def streaming_crawl_prod(prod_name: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        crawl_sites = [BachHoaXanhCrawler(), WinmartCrawler(), CoopOnlineCrawler()]
        for site in crawl_sites:
            print(f"Crawling site: {site.site_name}")
            # For each site, yield products as they are found
            async for product in site.crawl_prod_prices(prod_name, browser):
                yield product        
        await browser.close()
        print("Browser closed, finished crawling.")
        
# asyncio.run(crawl_prod('trà sữa trân châu'))