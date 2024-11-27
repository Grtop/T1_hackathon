import pandas as pd
from datetime import datetime
import re
import csv
import sys
import os
sys.setrecursionlimit(2147000000)

class backend:
    def __init__(self, file_name):
        self.file_name = file_name
        print('r')
        self.data = pd.read_csv(file_name)
        print('p')
        self.process_data()
        print('m')
        self.merge_data()
    
    def process_data(self):
        ## Обрабатываем ФИО пользователя:
        #   - каждое новое слово должно начинаться с большой буквы, все остальные - маленькие
        self.data['client_first_name'] = self.data['client_first_name'].str.title()
        self.data['client_middle_name'] = self.data['client_middle_name'].str.title()
        self.data['client_last_name'] = self.data['client_last_name'].str.title()
        self.data['client_fio_full'] = self.data['client_last_name'] + ' ' + self.data['client_first_name'] + ' ' + self.data['client_middle_name']
        
        
        ## Обрабатываем дату рождения пользователя:
        #   - формат yyyy-mm-dd
        #   - год рождения больше, чем 1900
        #   - дата рождения меньше, чем текущая дата
        self.data['client_bday'] = pd.to_datetime(self.data['client_bday'], errors='coerce')
        now = datetime.now()

        valid_mask = (
            self.data['client_bday'].notna() &
            (self.data['client_bday'].dt.year >= 1900) &
            (self.data['client_bday'] < now)
        )
        self.data.loc[~valid_mask, 'client_bday'] = pd.NA
        
        
        ## Обрабатываем код статуса резидента пользователя:
        #   - строка состоил из Д или Н
        valid_mask = (
            self.data['client_resident_cd'].notna() &
            ((self.data['client_resident_cd'].str.strip() == 'Д') | (self.data['client_resident_cd'].str.strip() == 'Н'))
        )
        self.data.loc[~valid_mask, 'client_resident_cd'] = pd.NA
    

        ## Обрабатываем пол пользователя:
        #   - строка состоил из М или Ж
        valid_mask = (
            self.data['client_gender'].notna() &
            ((self.data['client_gender'].str.strip() == 'М') | (self.data['client_gender'].str.strip() == 'Ж'))
        )
        self.data.loc[~valid_mask, 'client_gender'] = pd.NA
        
        
        ## Обрабатываем семейное положение пользователя:
        #   - строка состоил из Д или Н
        valid_mask = (
            self.data['client_marital_cd'].notna() &
            ((self.data['client_marital_cd'].str.strip() == 'Д') | (self.data['client_marital_cd'].str.strip() == 'Н'))
        )
        self.data.loc[~valid_mask, 'client_marital_cd'] = pd.NA
        
        
        ## Обрабатываем уровень образования пользователя:
        #   - строка состоил из Д или Н
        valid_mask = (
            self.data['client_graduate'].notna() &
            ((self.data['client_graduate'].str.strip() == 'Д') | (self.data['client_graduate'].str.strip() == 'Н'))
        )
        self.data.loc[~valid_mask, 'client_graduate'] = pd.NA
        
        
        ## Обрабатываем статус военной службы пользователя:
        #   - строка состоил из Д или Н
        valid_mask = (
            self.data['client_mil_cd'].notna() &
            ((self.data['client_mil_cd'].str.strip() == 'Д') | (self.data['client_mil_cd'].str.strip() == 'Н'))
        )
        self.data.loc[~valid_mask, 'client_mil_cd'] = pd.NA
        
        
        ## Обрабатываем статус заграничного паспорта пользователя:
        #   - строка состоил из Д или Н
        valid_mask = (
            self.data['client_zagran_cd'].notna() &
            ((self.data['client_zagran_cd'].str.strip() == 'Д') | (self.data['client_zagran_cd'].str.strip() == 'Н'))
        )
        self.data.loc[~valid_mask, 'client_zagran_cd'] = pd.NA
        
        
        ## Обрабатываем ИНН пользователя:
        #   - инн состоит из 12 цифр | 14 знаков с учётом .0
        
        self.data['client_inn'] = self.data['client_inn'].astype(str)

        valid_mask = (
            self.data['client_inn'].notna() &
            (self.data['client_inn'].str.len() == 14)
        )
        self.data.loc[~valid_mask, 'client_inn'] = pd.NA
        
        
        ## Обрабатываем СНИЛС пользователя:
        #   - инн состоит из 11 цифры и удовлетворять условиям
        def validate_snils(snils):
            if pd.isna(snils):
                return False
            if not re.match('^\d{11}\.\d{1}$', snils):
                return False
            
            digits = [int(d) for d in snils[:9]]
            check_sum = int(snils[9:-2])
            
            sum = 0
            for i in range(9):
                sum += digits[i] * (9 - i)
            
            if sum < 100:
                control_number = sum
            elif sum == 100 or sum == 101:
                control_number = 0
            else:
                control_number = sum % 101
                if control_number == 100:
                    control_number = 0
            
            return control_number == check_sum
        
        self.data['client_snils'] = self.data['client_snils'].astype(str)
        valid_mask = self.data['client_snils'].apply(validate_snils)
        self.data.loc[~valid_mask, 'client_snils'] = pd.NA
        
        
        ## Обрабатываем email пользователя:
        #   - Email должен быть в формате почты
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        valid_mask = (
            self.data['contact_email'].notna() &
            self.data['contact_email'].str.match(email_pattern)
        )
        self.data.loc[~valid_mask, 'contact_email'] = pd.NA
        
        
        ## Обрабатываем телефон пользователя:
        #   - телефон должен содержать в себе +7 и 10 цифр
        def validate_phone(x):
            if pd.isna(x):
                return pd.NA
            
            phone = ''
            for el in x:
                if el in '0123456789':
                    phone += el
                    
            if len(phone) == 10:
                phone = '+7' + phone
                return phone
            elif len(phone) == 11:
                phone = '+' + phone
                return phone
            else:
                return pd.NA
        
        self.data['contact_phone'] = self.data['contact_phone'].astype(str)
        self.data['contact_phone'] = self.data['contact_phone'].apply(validate_phone)
        
        
        # Сортируем данные по последнему апдейту информации
        self.data.sort_values('update_date', ascending=False)
        self.data = self.data.replace({pd.NA: 'nan'})
        self.data = self.data.astype(str)
        self.data = self.data.replace({pd.NA: 'nan'})

        
        
    def dfs(self, ind):
        self.used[ind] = 1
        
        for i in range(47):
            if self.data_list[ind-1][-1] < self.ind_of_gold_row[i] and str(self.data_list[ind-1][i]) != 'nan':
                self.gold_row[i] = self.data_list[ind-1][i]
                self.ind_of_gold_row[i] = self.data_list[ind-1][-1]

        for el in self.list_of_link[ind]:
            if self.used[el] == 0:
                self.dfs(el)
    
    
    def merge_data(self):
        data_inn = {}
        data_snils = {}
        data_fio_plus_phone = {}
        data_email = {}
        data_fio_plus_bday = {}
        data_vc = {}
        data_tg = {}
        data_fio_addr = {}
        data_loanbegin_loanend = {}
        data_phone_plus_addr = {}
        data_bday_plus_addr = {}
        data_phone_plus_bday = {}
        
        columns = self.data.columns
        self.data['index'] = range(1, len(self.data) + 1)
        
        self.data_list = self.data.values.tolist()
        
        lst1 = [
            [15],
            [16],
            [18],
            [19],
            [21],
        ]
        lst2 = [
            [4, 22],
            [4, 5],
            [4, 34],
            [40, 41],
            [22, 34],
            [5, 34],
            [22, 5]
        ]
        
        self.list_of_link = [
            [] for i in range(len(self.data)+1)
        ]
        
        for el in lst1:
            self.data_list.sort(key=lambda x: str(x[el[0]]))
            for i in range(len(self.data_list)-1):
                row = self.data_list[i]
                n_row = self.data_list[i+1]
                if self.data_list[i][el[0]] == self.data_list[i+1][el[0]] and str(self.data_list[i][el[0]]) != 'nan':
                    self.list_of_link[self.data_list[i][-1]].append(self.data_list[i+1][-1])
                    self.list_of_link[self.data_list[i+1][-1]].append(self.data_list[i][-1])
                    
        for el in lst2:
            self.data_list.sort(key=lambda x: [str(x[el[0]]), str(x[el[1]])])
            for i in range(len(self.data_list)-1):
                row = self.data_list[i]
                n_row = self.data_list[i+1]
                if self.data_list[i][el[0]] == self.data_list[i+1][el[0]] and self.data_list[i][el[1]] == self.data_list[i+1][el[1]] and str(self.data_list[i][el[0]]) != 'nan' and str(self.data_list[i][el[1]]) != 'nan':
                    self.list_of_link[self.data_list[i][-1]].append(self.data_list[i+1][-1])
                    self.list_of_link[self.data_list[i+1][-1]].append(self.data_list[i][-1])
                    
        self.data_list.sort(key=lambda x: x[-1])
        
        
        self.used = [0 for i in range(len(self.data)+1)]
        self.gold_row = ['nan' for i in range(47)]
        self.ind_of_gold_row = [10**9 for i in range(47)]
                
        lst = []
        for i in range(len(self.data)):
            if i % 10000 == 0:
                print(i, len(self.data))
            if self.used[i] == 0:
                self.gold_row = ['nan' for j in range(47)]
                self.ind_of_gold_row = [10**9 for i in range(47)]
                self.dfs(i)
                lst.append(self.gold_row)
                
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows(lst)
            

async def all_csv_in_one():
    try:
        all_data = []
        directory = 'files'
        
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                df = pd.read_csv(file_path)
                all_data.append(df)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df.to_csv(os.path.join(directory, 'all.csv'), index=False, encoding='utf-8')
            for filename in os.listdir(directory):
                if filename != 'all.csv':
                    os.remove(os.path.join(directory, filename))
                    
        return True
    except Exception:
        return False


async def get_good_file():
    if await all_csv_in_one():
        backend('files/all.csv')
        os.makedirs('good_files', exist_ok=True)
        os.rename('output.csv', 'good_files/output.csv')

    return True