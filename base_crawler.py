from abc import ABC, abstractmethod
from playwright.async_api import Browser
from typing import Literal
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
    async def crawl_prod_prices(self, prod_name: str, current_browser: Browser, crawl_mode: Literal["top-products", "all-products"] = "top-products"):
        """Subclass must implement this method to crawl product prices."""
        pass