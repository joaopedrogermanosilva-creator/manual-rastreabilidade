import os

# ============ 1. CRIA A ROTA DO SERVICE WORKER NO MAIN.PY ============
with open("main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

if "/sw.js" not in main_code:
    # Adiciona o import do FileResponse
    if "from fastapi.responses import FileResponse" not in main_code:
        main_code = main_code.replace(
            "from fastapi import FastAPI",
            "from fastapi import FastAPI\nfrom fastapi.responses import FileResponse"
        )
    
    # Adiciona a rota para o sw.js na raiz
    rota_sw = '''

@app.get("/sw.js")
def service_worker():
    return FileResponse("app/static/js/sw.js", media_type="application/javascript")
'''
    main_code = main_code.replace("app.include_router(router)", "app.include_router(router)\n" + rota_sw)
    
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(main_code)
    print("[ok] Rota /sw.js criada no main.py")

# ============ 2. ARRUMA O REGISTRO NO BASE.HTML ============
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    html = f.read()

# Troca a url de registro de /static/sw.js para /sw.js
html = html.replace("navigator.serviceWorker.register('/static/sw.js', { scope: '/' })", "navigator.serviceWorker.register('/sw.js', { scope: '/' })")
html = html.replace("navigator.serviceWorker.register('/static/js/sw.js', { scope: '/' })", "navigator.serviceWorker.register('/sw.js', { scope: '/' })")

with open("app/templates/base.html", "w", encoding="utf-8") as f:
    f.write(html)
print("[ok] base.html ajustado para registrar /sw.js")

print("\nAgora rode: git add . ; git commit -m 'fix pwa root'; git push")
