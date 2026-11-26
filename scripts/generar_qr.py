import csv, io, json, re, html
from pathlib import Path
from urllib.parse import urlencode
import qrcode
import qrcode.image.svg

BASE = "https://ofi-aplicaciones.github.io/aura-andina/"
payload = json.loads(Path("data/guia.json").read_text(encoding="utf-8"))
rows = csv.DictReader(io.StringIO(payload["raw"]["Alojamientos"].lstrip("\ufeff")))
out = Path("_site/qr")
out.mkdir(parents=True, exist_ok=True)
cards = []
for row in rows:
    if row["Activo"].strip().lower() not in ("sí","si","true","1"):
        continue
    ident = row["ID"].strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", ident):
        raise ValueError("ID de alojamiento inválido: " + ident)
    url = BASE + "?" + urlencode({"alojamiento": ident})
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    n = len(matrix)
    path = "".join(f"M{x} {y}h1v1h-1z" for y,r in enumerate(matrix) for x,v in enumerate(r) if v)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}"><rect width="{n}" height="{n}" fill="white"/><path fill="#24695F" d="{path}"/></svg>'
    (out / (ident + ".svg")).write_text(svg, encoding="utf-8")
    name=html.escape(row["Nombre"])
    cards.append(f'<article><img class="logo" src="../icon-192.png" alt="Aura Andina"><h2>{name}</h2><img class="qr" src="{ident}.svg" alt="Código QR de {name}"><p>Escanea y explora Riobamba</p><a href="{html.escape(url, quote=True)}">Abrir guía</a> · <a href="{ident}.svg" download>Descargar QR</a></article>')
(out / "index.html").write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>QR · Aura Andina</title><style>body{font:16px system-ui;background:#faf8f2;color:#24695f;text-align:center}main{display:flex;flex-wrap:wrap;gap:20px;justify-content:center}article{background:white;border:1px solid #ddd;padding:20px;border-radius:16px;width:min(340px,90vw)}h2{color:#9b3018}.logo{width:80px}.qr{width:100%;max-width:300px}a{color:#24695f}@media print{article{break-inside:avoid}a{display:none}}</style><h1>Códigos QR · Aura Andina</h1><main>'+''.join(cards)+'</main></html>',encoding="utf-8")
