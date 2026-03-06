import sys
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from core.loader import load_csv_from_zip
from core.filters import filter_creditable, filter_board_name
from core.transformer import transform_inventory
from core.exporter import export_csv

# ---------------------------
# Base directory (DEV vs EXE)
# ---------------------------
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

ENTRADA = BASE_DIR / "entrada"
SAIDA = BASE_DIR / "saida"

ENTRADA.mkdir(exist_ok=True)
SAIDA.mkdir(exist_ok=True)

# ---------------------------
# FastAPI
# ---------------------------
app = FastAPI(title="Jacaré Inventory")

# Static files (CSS / JS)
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount(
        "/static",
        StaticFiles(directory=static_dir),
        name="static"
    )
else:
    import warnings
    warnings.warn(f"Static directory not found: {static_dir}. Static files will not be served.")

# Templates
templates_dir = BASE_DIR / "web" / "templates"
if templates_dir.exists():
    templates = Jinja2Templates(directory=templates_dir)
else:
    templates = None
    import warnings
    warnings.warn(f"Templates directory not found: {templates_dir}. Using fallback response.")


# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def home(request: Request):
    if templates is not None:
        return templates.TemplateResponse(
            "index.html",
            {"request": request}
        )
    return HTMLResponse(content="<html><body><h1>Jacaré Inventory</h1><p>Templates not available.</p></body></html>", status_code=200)


@app.post("/process")
def process_file(file: UploadFile = File(...), board_type: str = Form("UBBP")):
    uid = uuid.uuid4().hex

    zip_path = ENTRADA / f"{uid}.zip"
    output_path = SAIDA / f"resultado_{uid}.csv"

    # Save uploaded zip
    with zip_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Pipeline
    df = load_csv_from_zip(zip_path)
    df = filter_creditable(df)
    
    # Aplicar filtro baseado na escolha do usuário
    if board_type == "BOTH":
        df = filter_board_name(df, ["UBBP", "AIRU"])
    else:
        df = filter_board_name(df, [board_type])
        
    final_df = transform_inventory(df)

    export_csv(final_df, output_path)

    # Return CSV to user
    return FileResponse(
        path=output_path,
        filename="resultado.csv",
        media_type="text/csv"
    )
