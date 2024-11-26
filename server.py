from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import patoolib
import pandas as pd

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/view_data", response_class=HTMLResponse)
async def view_data(request: Request):
    try:
        # Поиск CSV файла в директории files
        csv_files = [f for f in os.listdir("files") if f.endswith('.csv')]
        if not csv_files:
            raise HTTPException(status_code=404, detail="CSV файл не найден")
        df = pd.read_csv(f"files/{csv_files[0]}")
        df = df.head(5)
        
        table_html = df.to_html(classes=['table', 'table-striped', 'table-hover', 'table-dark', 'sortable'], 
                               index=False,
                               border=0,
                               table_id='dataTable')
        
        return templates.TemplateResponse(
            "view_data.html",
            {
                "request": request,
                "table": table_html,
                "columns": df.columns.tolist()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.rar', '.zip', '.7z', '.csv')):
        raise HTTPException(status_code=400, detail="Только файлы RAR, ZIP, 7Z и CSV разрешены.")
    
    try:
        os.makedirs("files", exist_ok=True)
        file_location = f"files/{file.filename}"
        
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
            
        # Разархивирование если это архив
        if file.filename.endswith(('.rar', '.zip', '.7z')):
            patoolib.extract_archive(file_location, outdir="files")
            os.remove(file_location)  # Удаляем архив после распаковки
            
        return {"filename": file.filename, "status": "success"}
            
    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
