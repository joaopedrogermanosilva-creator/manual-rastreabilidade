main_code = """from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import router

app = FastAPI(title="Manual de Rastreabilidade")

# Arquivos estáticos (CSS, JS, imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Rota do Service Worker na raiz
@app.get("/sw.js")
def service_worker():
    return FileResponse("app/static/sw.js", media_type="application/javascript")

# Rota do Manifest na raiz
@app.get("/manifest.json")
def manifest():
    return FileResponse("app/static/manifest.json", media_type="application/json")

# Rotas do app
app.include_router(router)
"""

with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_code)
print("[ok] main.py reescrito do zero e seguro com rotas na raiz")
