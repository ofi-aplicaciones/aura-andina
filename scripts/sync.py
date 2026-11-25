import csv, io, json, urllib.request
from pathlib import Path
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[1]
sources = json.loads((root / "scripts/sources.json").read_text(encoding="utf-8"))
schema = {'Alojamientos': ['ID', 'Nombre', 'Google Maps', 'Airbnb', 'Foto', 'Activo', 'Orden'], 'Recomendaciones': ['ID', 'Nombre', 'Categorías', 'Google Maps', 'Notas', 'Activo', 'Destacado', 'Orden'], 'Categorías': ['Nombre', 'Activo', 'Orden'], 'Configuración': ['Clave', 'Valor']}
raw = {}
for name, url in sources.items():
    req = urllib.request.Request(url, headers={"User-Agent": "AuraAndinaSync/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        content = response.read(5_000_001)
    if len(content) > 5_000_000:
        raise ValueError(f"{name}: archivo demasiado grande")
    text = content.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text), strict=True)
    headers = [h.strip() for h in next(reader)]
    if not set(schema[name]).issubset(headers):
        raise ValueError(f"{name}: columnas incorrectas: {headers}")
    for row in reader:
        if any(v.strip() for v in row) and len(row) != len(headers):
            raise ValueError(f"{name}: fila con número incorrecto de columnas")
    raw[name] = text
    print(f"{name}: CSV válido")
target = root / "data/guia.json"
payload = {"raw": raw, "updated_at": datetime.now(timezone.utc).isoformat()}
temp = target.with_suffix(".tmp")
temp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
temp.replace(target)
