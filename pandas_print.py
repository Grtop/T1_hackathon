import pandas as pd

def print_csv_data(file_path):
        df = pd.read_csv(file_path)
        df = df.sort_values(['create_date', 'update_date'], ascending=False)
        print("\nПервые 5 строк данных:")
        print(df.head())
        # print("\nСтатистические характеристики:")
        # print(df.describe())

        return df
print(print_csv_data('C:/Users/Kirill/PycharmProjects/gold_sign_hackathon/ds_dirty_fin_202410041147.csv'))
