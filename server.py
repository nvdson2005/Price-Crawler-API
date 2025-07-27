from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from streaming_crawl import streaming_crawl_prod
from parallel_crawler import crawl_prod
# import asyncio
import json
app = FastAPI()

@app.get('/crawl')
async def crawl_controller(name: str = ""):
    if not name:
        return {"error": True, "message": "Product name is required."}
    print(f"Received request to crawl product: {name}")
    try:
        products = await crawl_prod(name)
        if not products:
            return {"error": True, "message": "No products found."}
        return {"error": False, "message": "Data crawled successfully.", "data": products}
    except Exception as e:    
        return {"error": True, "message": str(e)}


# Streaming response for incremental data generation
async def generate_streaming_crawl_prod(name: str):
    yield '['
    first_item = True
    async for product in streaming_crawl_prod(name):
        if first_item:
            first_item = False
            yield json.dumps(product, ensure_ascii=False)
        yield "," + json.dumps(product, ensure_ascii=False)
    # Remove the last comma and close the JSON array
    yield ']'

@app.get('/streaming-crawl')
async def streaming_crawl_controller(name: str = ""):
    if not name:
        return {"error": True, "message": "Product name is required."}
    print(f"Received request to streaming-crawl product: {name}")
    try:
        return StreamingResponse(generate_streaming_crawl_prod(name), media_type='application/json')
    except Exception as e:    
        return {"error": True, "message": str(e)}
    
    
# Example of incrementally generating NDJSON data with StreamingResponse
# only for testing purposes
# async def generate_ndjson():
#     yield '['
#     for i in range(1000):
#         item = {"index": i}
#         yield json.dumps(item) 
#         if i < 999:
#             yield ','
#         await asyncio.sleep(0.01)  # simulate delay
#     yield ']'
    
# @app.get('/stream-ndjson')
# async def stream_ndjson_controller():
#     return StreamingResponse(generate_ndjson(), media_type='application/json') 