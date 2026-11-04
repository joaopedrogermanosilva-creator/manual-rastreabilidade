import logging
import os
import secrets

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth_router, router

logger = logging.getLogger(__name__)
error_templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title="Manual de Rastreabilidade",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception) -> HTMLResponse:
    logger.exception(
        "Unhandled exception while handling %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )
    return error_templates.TemplateResponse(
        request=request,
        name="erro.html",
        context={},
        status_code=500,
    )


session_secret = os.getenv("SESSION_SECRET_KEY")
if not session_secret:
    session_secret = secrets.token_urlsafe(32)
    logging.getLogger(__name__).warning(
        "SESSION_SECRET_KEY is not configured; sessions will expire when the process restarts."
    )

app.add_middleware(
    SessionMiddleware,
    secret_key=session_secret,
    same_site="lax",
    https_only=os.getenv(
        "SESSION_HTTPS_ONLY",
        "true" if os.getenv("RENDER", "").lower() == "true" else "false",
    ).lower() == "true",
)

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


@app.head("/")
def head_root():
    return Response(status_code=200)


# Rotas do app
app.include_router(auth_router)
app.include_router(router)
