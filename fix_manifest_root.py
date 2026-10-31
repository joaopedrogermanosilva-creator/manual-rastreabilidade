# ============ 1. ADICIONA A ROTA DO MANIFEST NA RAIZ NO MAIN.PY ============
with open("main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

if "/manifest.json" not in main_code:
    # Adiciona a rota logo após a rota do sw.js
    rota_manifest = '''

@app.get("/manifest.json")
def manifest():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/manifest.json", media_type="application/json")
'''
    # Coloca depois da rota do sw.js (ou no final)
    if "/sw.js" in main_code:
        main_code = main_code.replace("return FileResponse(\"app/static/js/sw.js\", media_type=\"application/javascript\")", 
                                      "return FileResponse(\"app/static/js/sw.js\", media_type=\"application/javascript\")\n" + rota_manifest)
    else:
        main_code += rota_manifest
        
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(main_code)
    print("[ok] Rota /manifest.json adicionada no main.py")

# ============ 2. ARRUMA O BASE.HTML ============
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    html = f.read()

# Troca o link do manifest para a raiz
html = html.replace('href="/static/manifest.json"', 'href="/manifest.json"')

with open("app/templates/base.html", "w", encoding="utf-8") as f:
    f.write(html)
print("[ok] base.html ajustado para buscar o manifest na raiz")
