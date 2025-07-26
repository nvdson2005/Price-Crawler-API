# Food Price Crawler API
## Information
This is an API for crawling food prices from the three most popular food e-commerce sites in Viet Nam, including Bach Hoa Xanh, Winmart and Co.op Online.
## Packages Used
* `FastAPI` for building APIs.
* `Playwright` for automating browser tasks and web scraping.
* Other packages can be seen in `requirements.txt`.
## Usage
Run the FastAPI server (in development mode):
```python
fastapi dev server.py
``` 
The endpoint for crawling is located in:
```url
http://127.0.0.1:8000/crawl
```
Accept one query parameter, `name` for the name of the food.

The api documentation can be seen at:
```
http://127.0.0.1:8000/docs
```
