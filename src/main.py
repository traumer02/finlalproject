import json

from fastapi import FastAPI, Response
import uvicorn

from utils import logger
from crawler import Crawler

app = FastAPI()
crawler = Crawler()


@app.get("/status")
async def main():
    return {"status": "ok"}


@app.get("/get_data/{search_name}")
async def get_data_by_search_name(search_name: str):
    logger.info(f'Getting data by name: {search_name}')
    result = crawler.main(search_name=search_name)

    content = json.dumps(result, indent=4, default=str)
    return Response(content=content, media_type='application/json')


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
