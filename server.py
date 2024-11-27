from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import patoolib
import pandas as pd
from datetime import datetime
import re

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
    
    file_location = ""
    try:
        os.makedirs("files", exist_ok=True)
        
        # Проверяем наличие даты/времени в имени файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_parts = os.path.splitext(file.filename)
        base_name = filename_parts[0]
        extension = filename_parts[1]
        
        # Проверяем есть ли дата/время в конце имени файла
        if not re.search(r'\d{8}_\d{6}$', base_name):
            # Если нет - обрезаем имя до 8 символов и добавляем дату/время
            base_name = base_name[:8] if len(base_name) > 8 else base_name
            new_filename = f"{base_name}_{timestamp}{extension}"
        else:
            new_filename = file.filename
            
        file_location = f"files/{new_filename}"
        
        # Сохраняем файл
        with open(file_location, "wb+") as file_object:
            content = await file.read()
            file_object.write(content)

        # Разархивирование если это архив
        if file.filename.endswith(('.rar', '.zip', '.7z')):
            patoolib.extract_archive(file_location, outdir="files")
            os.remove(file_location)  # Удаляем архив после распаковки

            # Для извлеченных CSV файлов применяем ту же логику переименования
            for filename in os.listdir("files"):
                if filename.endswith('.csv'):
                    fname_parts = os.path.splitext(filename)
                    base = fname_parts[0]
                    ext = fname_parts[1]
                    
                    if not re.search(r'\d{8}_\d{6}$', base):
                        base = base[:8] if len(base) > 8 else base
                        new_name = f"{base}_{timestamp}{ext}"
                        old_path = os.path.join("files", filename)
                        new_path = os.path.join("files", new_name)
                        os.rename(old_path, new_path)
        
        # Удаляем все файлы кроме CSV
        for filename in os.listdir("files"):
            if not filename.endswith('.csv'):
                os.remove(os.path.join("files", filename))

        return {"filename": new_filename, "status": "success"}
            
    except Exception as e:
        if file_location and os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/")
async def get_files():
    try:
        files = []
        for filename in os.listdir("files"):
            files.append({
                "name": filename,
                "extension": filename.split('.')[-1],
                "uploadTime": os.path.getctime(f"files/{filename}")
            })
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/files/{filename}")
async def delete_file(filename: str):
    try:
        file_path = f"files/{filename}"
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"status": "success"}
        raise HTTPException(status_code=404, detail="Файл не найден")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear-files/")
async def clear_files():
    try:
        for filename in os.listdir("files"):
            file_path = os.path.join("files", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
