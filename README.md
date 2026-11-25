# Aura Andina V1.0
Guía turística con Google Sheets y GitHub Pages, sin Apps Script ni Cloudflare.

1. Crear repositorio público `aura-andina`, rama `main`.
2. Descomprimir el ZIP y subir **todos** los archivos, incluida la carpeta oculta `.github`. Preferir Git o GitHub Desktop.
3. Settings → Pages → Build and deployment → Source → GitHub Actions.
4. Actions → Sincronizar y publicar Aura Andina → Run workflow → main.
5. Abrir la URL que muestra el despliegue.

La automatización descarga los cuatro CSV publicados cada 15 minutos aproximadamente y valida las columnas antes de publicar. Si falla, no despliega y se conserva la última versión publicada. La aplicación contiene una copia inicial y puede guardar la última consulta en el navegador. Los datos publicados son públicos. No introducir datos privados. El botón de actualización lee la última versión desplegada, no fuerza una descarga de Google Sheets.
Los cambios programados pueden retrasarse y GitHub puede desactivar workflows programados por inactividad. Revisar las condiciones de GitHub Pages para usos comerciales: este proyecto está pensado como guía informativa, no como sistema de reservas o transacciones.
Para probar localmente: `python -m http.server 8000` desde esta carpeta, abrir `http://localhost:8000`. Para sincronizar localmente: `python scripts/sync.py`.
