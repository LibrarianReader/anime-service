from fastapi import FastAPI
from app.api.animes import animes
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/animes/openapi.json", docs_url="/api/v1/animes/docs")

animes = [
    {'casts_id': 1, 'name':'Naruto', 'plot': 'Аниме для людей от 12+', 'genres': 'боевик'},
    {'casts_id': 2, 'name':'Слабый герой', 'plot': 'Дорама для вечернего просмотра', 'genres': 'приключения'}
]

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(animes, prefix='/api/v1/animes', tags=['animes'])

if __name__ == '__main__':
    import uvicorn
    import os
    app = FastAPI()
    try:
        PORT = int(os.environ['PORT'])
    except KeyError as keyerr:
        PORT = 8000
    uvicorn.run(app, host='0.0.0.0', port=PORT)