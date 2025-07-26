from playwright.async_api import async_playwright, Browser, Playwright
# from playwright.sync_api import sync_playwright, Playwright, Browser
from urllib.parse import urljoin
from abc import ABC, abstractmethod 
import asyncio
import json
class CrawlSite(ABC):
    base_url = None
    site_name = None
    def __init__(self, base_url: str, site_name: str):
        self.base_url = base_url
        self.site_name = site_name
        super().__init__() 
    def __init_subclass__(cls):
        if(cls.base_url is None or cls.site_name is None):
            raise NotImplementedError(f"Class {cls.__name__} must define base_url and site_name attributes.")

    @abstractmethod
    async def crawl_prod_prices(self, prod_name: str, current_browser: Browser):
        """Subclass must implement this method to crawl product prices."""
        pass


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
        if not products:
            return []
        return_info = []
        for i, product in enumerate(products):
            if i >= 5:
                break
            try:
                p_name = (await product.locator('css=h3').text_content()).strip()
                price_and_per = (await product.locator('css=div.product_price').text_content()).strip().split('đ')
                p_price = price_and_per[0].strip()
                p_per = price_and_per[1].strip()[1:] if len(price_and_per) > 1 else ''
                p_url_elements = await product.locator('css=a').all()
                p_url = p_url_elements[0].get_attribute('href') if len(p_url_elements) > 0 else await product.locator('css=a').get_attribute('href')
                p_url = (await p_url).strip()
                p_img_elements = await product.locator('css=img').all()
                p_img = await p_img_elements[0].get_attribute('src') if len(p_img_elements) > 0 else await product.locator('css=img').get_attribute('src')
                return_info.append({
                    'name': p_name,
                    'price': p_price,
                    'per': p_per,
                    'url': urljoin(self.base_url, p_url),
                    'img': p_img,
                    'source': self.site_name
                })
            except Exception as e:
                print(f"Error processing product {i}: {e}")
        await page.close()
        await context.close()
        if page.is_closed():
            print(f"Stop crawling from {self.base_url}")
        return return_info

class WinmartCrawler(CrawlSite):
    base_url = "https://winmart.vn"
    site_name = "Winmart"
    
    def __init__(self):
        super().__init__(self.base_url, self.site_name)
    
    async def crawl_prod_prices(self, prod_name, current_browser):
        context = await current_browser.new_context()
        page = await context.new_page()
        await page.goto(f"{self.base_url}/search/{prod_name}") 
        await page.wait_for_load_state('domcontentloaded')
        # products = await page.locator('xpath=//html/body/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div').all()
        # products = await page.locator('css=product-search__Grid-sc-j0v2h4-0').all()
        products = await page.locator('xpath=/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div').all()
        print(f"Found {len(products)} products on Winmart")
        if not products:
            return []
        return_info = []
        for i, product in enumerate(products):
            if i >= 5:
                break
            p_name = (await product.locator('css=div.product-card-two__Title-sc-1lvbgq2-6').inner_text()).strip()
            p_price = (await product.locator('css=div.product-card-two__Price-sc-1lvbgq2-9').inner_text())[:-2].strip()
            p_per = (await product.locator('xpath=./div/div[2]').inner_text()).strip()
            p_url_elements = await product.locator('css=a').all()
            # print(f"Product URL elements: {len(p_url_elements)}")
            # p_url = await p_url_elements[0].get_attribute('href') if len(p_url_elements) > 0 else await product.locator('css=a').get_attribute('href')
            # p_url = (await p_url).strip()
            p_img = (await product.locator('css=img.product-image').get_attribute('src')).strip()
            return_info.append({
                'name': p_name,
                'price': p_price,
                'per': p_per,
                # 'url': urljoin(self.base_url, p_url),
                'img': p_img,
                'source': self.site_name
            })
        await page.close()
        await context.close()
        if page.is_closed():
            print(f"Stop crawling from {self.base_url}")
        return return_info

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
        if not products:
            return []
        return_info = []
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
            return_info.append({
                'name': p_name,
                'price': p_price,
                'per': p_per,
                'url': urljoin(self.base_url, p_url),
                'img': p_img,
                'source': self.site_name
            }) 
        await page.close()
        await context.close()
        if page.is_closed():
            print(f"Stop crawling from {self.base_url}")
        return return_info

async def crawl_prod(prod_name: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        crawl_sites = [BachHoaXanhCrawler(), WinmartCrawler(), CoopOnlineCrawler()]
        # crawl_sites = [WinmartCrawler()]
        return_info = []
        for crawl_site in crawl_sites:
            print(f"Crawling site: {crawl_site.site_name}")
            return_list = await crawl_site.crawl_prod_prices(prod_name, browser)
            for product in return_list:
                return_info.append(product)
        await browser.close()
        print("Browser closed, finished crawling.")
        # print(f"Results: {json.dumps(return_info, indent=2)}")
        return return_info    
# async def crawl_prod(prod_name: str):
#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
        # crawl_sites : CrawlSite = [BachHoaXanhCrawler(), WinmartCrawler(), CoopOnlineCrawler()]
#         return_info = []
#         for crawl_site in crawl_sites:
#             print(f"Crawling site: {crawl_site.site_name}")
#             return_info.extend(await crawl_site.crawl_prod_prices(prod_name, browser))
#         # print(return_info)
#         await browser.close()
#         print("Browser closed, finished crawling.")
        # return return_info
        
        
# asyncio.run(crawl_prod('trà sữa trân châu'))