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
        
        # Добавляем дату и время к имени файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_parts = os.path.splitext(file.filename)
        new_filename = f"{filename_parts[0]}_{timestamp}{filename_parts[1]}"
        file_location = f"files/{new_filename}"
        
        # Сохраняем файл
        with open(file_location, "wb+") as file_object:
            content = await file.read()
            file_object.write(content)

        # Разархивирование если это архив
        if file.filename.endswith(('.rar', '.zip', '.7z')):
            patoolib.extract_archive(file_location, outdir="files")
            os.remove(file_location)  # Удаляем архив после распаковки
            
            # Переименовываем распакованные CSV файлы
            for filename in os.listdir("files"):
                if filename.endswith('.csv'):
                    old_path = os.path.join("files", filename)
                    filename_parts = os.path.splitext(filename)
                    new_filename = f"{filename_parts[0]}_{timestamp}{filename_parts[1]}"
                    new_path = os.path.join("files", new_filename)
                    os.rename(old_path, new_path)
        
        # Удаляем все файлы кроме CSV
        for filename in os.listdir("files"):
            if not filename.endswith('.csv'):
                os.remove(os.path.join("files", filename))

        return {"filename": new_filename, "status": "success"}
            
    except Exception as e:
        if os.path.exists(file_location):
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
