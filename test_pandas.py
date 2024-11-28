import os
import pandas as pd

def save_first_five_rows():
    files_dir = 'files'
    csv_files = [f for f in os.listdir(files_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("CSV файлы не найдены")
        return
    
    # Берем первый CSV файл
    first_csv = csv_files[0]
    file_path = os.path.join(files_dir, first_csv)
    
    try:
        df = pd.read_csv(file_path)
        first_hundred = df.head(100)
        # Сохраняем в новый файл
        output_path = 'good_files/first_hundred_rows.csv'
        first_hundred.to_csv(output_path, index=False)
        print(f"Первые 100 строк сохранены в {output_path}")
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")

if __name__ == "__main__":
    save_first_five_rows()
