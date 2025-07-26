from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from main import crawl_prod
app = FastAPI()

@app.get('/crawl/')
async def crawl_controller(name: str = ""):
    if not name:
        return {"error": True, "message": "Product name is required."}
    print(f"Received request to crawl product: {name}")
    try:
        # products = [product async for product in crawl_prod(name)]
        products = await crawl_prod(name)
        if not products:
            return {"error": True, "message": "No products found."}
        return {"error": False, "message": "Data crawled successfully.", "data": products}
    except Exception as e:    
        return {"error": True, "message": str(e)}
