from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import patoolib

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

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.rar', '.zip', '.7z', '.csv')):
        raise HTTPException(status_code=400, detail="Только файлы RAR, ZIP, 7Z и CSV разрешены.")
    
    try:
        # Создаем директорию files, если она не существует
        os.makedirs("files", exist_ok=True)
        
        file_location = f"files/{file.filename}"
        
        # Читаем файл полностью перед записью
        file_content = await file.read()
        with open(file_location, "wb") as f:
            f.write(file_content)
        
        if file.filename.endswith(('.rar', '.zip')):
            try:
                patoolib.extract_archive(file_location, outdir="files")
                os.remove(file_location)
                return {"info": f"Файл '{file.filename}' загружен и разархивирован успешно."}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Ошибка распаковки: {str(e)}")
        
        else:  # CSV файл
            return {"info": f"Файл '{file.filename}' загружен успешно."}
            
    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
