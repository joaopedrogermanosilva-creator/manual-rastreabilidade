from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import router

app = FastAPI(title="Manual de Rastreabilidade")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)


@app.get("/sw.js")
def service_worker():
    return FileResponse("app/static/js/sw.js", media_type="application/javascript")


@app.get("/manifest.json")
def manifest():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/manifest.json", media_type="application/json")


