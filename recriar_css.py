css = """/* ===== VARIÁVEIS DE TEMA ===== */
:root, [data-theme="dark"] {
    --bg: #0d0d0f;
    --bg-elev: #17171b;
    --border: #26262c;
    --text: #f5f5f7;
    --text-dim: #9a9aa6;
    --accent: #f97316;
    --accent-soft: rgba(249, 115, 22, 0.15);
}

[data-theme="light"] {
    --bg: #f4f4f6;
    --bg-elev: #ffffff;
    --border: #e2e2e8;
    --text: #14141a;
    --text-dim: #5c5c6a;
    --accent: #ea580c;
    --accent-soft: rgba(234, 88, 12, 0.12);
}

/* ===== RESET ===== */
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--text);
    transition: background 0.2s, color 0.2s;
}

/* ===== TOPBAR ===== */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    background: var(--bg-elev);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.brand { display: flex; align-items: center; gap: 12px; font-weight: 700; letter-spacing: 1px; }
.brand-mark { color: var(--accent); font-size: 20px; }
.brand-name { font-size: 14px; }

/* Botão Hambúrguer */
.menu-btn {
    background: none;
    border: none;
    color: var(--text);
    font-size: 24px;
    cursor: pointer;
    padding: 0;
    margin-right: 5px;
    line-height: 1;
}

/* Botão de Tema */
.theme-btn {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 10px;
    cursor: pointer;
    font-size: 16px;
    transition: border-color 0.2s;
}
.theme-btn:hover { border-color: var(--accent); }

/* ===== MENU LATERAL (SIDEBAR) ===== */
.overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    z-index: 998;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s;
}
.overlay.open {
    opacity: 1;
    pointer-events: all;
}

.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 280px;
    height: 100vh;
    background: var(--bg-elev);
    border-right: 1px solid var(--border);
    z-index: 999;
    transform: translateX(-100%); /* Começa escondido */
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
}
.sidebar.open { transform: translateX(0); }

.sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid var(--border);
}
.sidebar-header h2 { margin: 0; font-size: 18px; }
.close-btn {
    background: none;
    border: none;
    color: var(--text);
    font-size: 28px;
    cursor: pointer;
}

.sidebar-list {
    list-style: none;
    padding: 10px 0;
    margin: 0;
    overflow-y: auto;
}
.sidebar-list li a {
    display: block;
    padding: 14px 20px;
    color: var(--text);
    text-decoration: none;
    font-size: 15px;
    transition: background 0.2s, color 0.2s;
    border-left: 3px solid transparent;
}
.sidebar-list li a:hover {
    background: var(--accent-soft);
    color: var(--accent);
    border-left-color: var(--accent);
}

/* ===== CONTAINER PRINCIPAL ===== */
.container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 30px 20px 80px;
}

/* ===== HERO ===== */
.hero h1 { font-size: 38px; margin: 0 0 6px; letter-spacing: -0.5px; }
.hero .accent { color: var(--accent); }
.subtitle { color: var(--text-dim); margin: 0 0 32px; }

/* ===== BOTÃO VOLTAR ===== */
.back-link {
    display: inline-block;
    color: var(--text-dim);
    text-decoration: none;
    font-size: 14px;
    margin-bottom: 16px;
    transition: color 0.2s;
}
.back-link:hover { color: var(--accent); }

/* ===== SEÇÕES E CARDS ===== */
.section-title {
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-dim);
    margin: 0 0 16px;
    font-weight: 600;
    display: flex;
    align-items: center;
}
.section-title::before {
    content: '';
    display: inline-block;
    width: 8px;
    height: 8px;
    background: var(--accent);
    border-radius: 50%;
    margin-right: 8px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
}

.card {
    background: var(--bg-elev);
    border: 1px solid var(--border);
    border-left: 4px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    text-decoration: none;
    color: var(--text);
    transition: all 0.2s;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}
.card:hover {
    transform: translateY(-2px);
    border-left-color: var(--accent);
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2);
}
.card-tag {
    display: inline-block;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--accent);
    background: var(--accent-soft);
    padding: 3px 8px;
    border-radius: 4px;
    margin-bottom: 12px;
    font-weight: 600;
}
.card h3 { margin: 0 0 6px; font-size: 16px; }
.card p { margin: 0; color: var(--text-dim); font-size: 13px; line-height: 1.4; }

/* ===== PÁGINA DE TAREFA ===== */
.acoes-tarefa {
    margin-top: 20px;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.btn-editar, .btn-excluir {
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    border: 1px solid var(--border);
    background: var(--bg-elev);
    color: var(--text);
    transition: all 0.2s;
    font-family: inherit;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.btn-editar:hover {
    border-color: var(--accent);
    color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(249,115,22,0.2);
}
.btn-excluir:hover {
    border-color: #dc2626;
    color: #dc2626;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(220,38,38,0.2);
}

.bloco {
    margin-top: 24px;
    padding: 24px;
    background: var(--bg-elev);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    transition: transform 0.2s;
}
.bloco:hover { transform: translateX(4px); }
.bloco p { margin: 0; color: var(--text-dim); line-height: 1.6; }
.passos, .atencao { margin: 0; padding-left: 20px; color: var(--text-dim); line-height: 1.7; }
.passos li, .atencao li { margin-bottom: 8px; }

/* ===== FORMULÁRIO ===== */
.form-manual {
    background: var(--bg-elev);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 28px;
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { font-size: 14px; font-weight: 600; color: var(--text); }
.form-group input, .form-group select, .form-group textarea {
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 12px;
    border-radius: 6px;
    font-family: inherit;
    font-size: 14px;
    transition: border-color 0.2s;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
    outline: none;
    border-color: var(--accent);
}
.form-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 10px; }
.btn-primary {
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
}
.btn-primary:hover { opacity: 0.9; }
.btn-cancel { color: var(--text-dim); text-decoration: none; padding: 12px 24px; font-size: 14px; }
.btn-cancel:hover { color: var(--text); }

/* ===== RESPONSIVO PARA CELULAR ===== */
@media (max-width: 600px) {
    .container { padding: 20px 16px; }
    .hero h1 { font-size: 30px; }
    .topbar { padding: 12px 16px; }
    .acoes-tarefa { flex-direction: column; }
    .btn-editar, .btn-excluir { width: 100%; justify-content: center; }
    .grid { grid-template-columns: 1fr; }
}
"""

with open("app/static/css/style.css", "w", encoding="utf-8") as f:
    f.write(css)
print("[ok] CSS recriado do zero com sucesso!")
