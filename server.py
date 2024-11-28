from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import patoolib
import pandas as pd
from datetime import datetime
import re
from backend import get_good_file
import functools

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

# Создаем кеш для данных таблицы
table_cache = {
    'html': None,
    'columns': None
}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    os.makedirs('files', exist_ok=True)
    os.makedirs('good_files', exist_ok=True)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/view_data", response_class=HTMLResponse)
async def view_data(request: Request, refresh: bool = Query(False)):
    try:
        # If there's cached data and refresh is not requested, return cached data
        if table_cache['html'] is not None and not refresh:
            return templates.TemplateResponse(
                "view_data.html",
                {
                    "request": request,
                    "table": table_cache['html'],
                    "columns": table_cache['columns']
                }
            )

        # Otherwise, read data again
        directory = 'good_files'
        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        if not csv_files:
            raise HTTPException(status_code=404, detail="CSV файл не найден")

        # Read CSV file
        df = pd.read_csv(f"{directory}/{csv_files[0]}")

        # Take only a subset of rows (e.g., first 1000)
        df = df.head(1000)

        # Optimize DataFrame column data types to reduce memory usage
        for col in df.select_dtypes(include=['object']).columns:
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio < 0.5:  # Convert to 'category' if unique values are relatively few
                df[col] = df[col].astype('category')

        # Use a faster HTML rendering library (jinja2 for templating)
        table_html = render_html_table(df)

        # Cache the generated table and column names
        table_cache['html'] = table_html
        table_cache['columns'] = df.columns.tolist()

        # Return the rendered response
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


def render_html_table(df):
    """Custom HTML table generator for faster rendering."""
    # Generate headers
    headers = ''.join(f'<th>{col}</th>' for col in df.columns)

    # Generate rows
    rows = ''.join(
        f'<tr>{"".join(f"<td>{val}</td>" for val in row)}</tr>' for row in df.itertuples(index=False)
    )

    # Combine into a table with the required classes
    return f"""
    <table class="table table-striped table-hover table-dark sortable" id="dataTable" border="0">
        <thead><tr>{headers}</tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """


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


@app.post("/link-files/")
async def link_files():
    try:
        # Проверяем наличие файлов в директории
        directory = 'files'
        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        if not csv_files:
            return {"status": "error",
                    "message": "Файлы для связывания не найдены. Пожалуйста, загрузите файлы сначала."}
        os.makedirs("good_files", exist_ok=True)
        if await get_good_file():
            return {"status": "success", "message": "Файлы успешно связаны"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/")
async def download_file():
    file_path = "good_files\output.csv"
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="output.csv",
            media_type="text/csv",
            headers={"Content-Disposition": "attachment"}
        )
    raise HTTPException(status_code=404, detail="Файл не найден")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)