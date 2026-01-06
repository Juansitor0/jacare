from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
import uuid

from core.loader import load_csv_from_zip
from core.filters import filter_creditable, filter_board_name
from core.transformer import transform_inventory
from core.exporter import export_csv

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
ENTRADA = BASE_DIR / "entrada"
SAIDA = BASE_DIR / "saida"

ENTRADA.mkdir(exist_ok=True)
SAIDA.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=BASE_DIR / "web" / "templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/process")
def process_file(file: UploadFile = File(...)):
    uid = uuid.uuid4().hex
    zip_path = ENTRADA / f"{uid}.zip"
    output_path = SAIDA / f"resultado_{uid}.csv"

    with zip_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = load_csv_from_zip(zip_path)
    df = filter_creditable(df)
    df = filter_board_name(df)
    final_df = transform_inventory(df)

    export_csv(final_df, output_path)

    retu
