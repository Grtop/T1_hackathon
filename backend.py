import pandas as pd
from datetime import datetime
import re
import csv
import sys
import os
import numpy as np
sys.setrecursionlimit(2147000000)

class backend:
    def __init__(self, file_name):
        self.file_name = file_name
        print('r')
        self.data = pd.read_csv(file_name, low_memory=False)
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
            
            phone = ''.join(filter(str.isdigit, x))
                    
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

        
    def dfs(self, ind):
        self.used[ind] = 1

        for i in range(47):
            if self.data_list[ind][-1] < self.ind_of_gold_row[i] and str(self.data_list[ind][i]) != 'nan':
                self.gold_row[i] = self.data_list[ind][i]
                self.ind_of_gold_row[i] = self.data_list[ind][-1]

        for el in self.list_of_link[ind]:
            if self.used[el] == 0:
                self.dfs(el)
    
    
    def merge_data(self):        
        columns = [el for el in self.data.columns]
        self.data['index'] = range(len(self.data))
        
        self.data_list = np.array(self.data.values)
        
        lst1 = np.array([
            [columns.index('client_inn')],
            [columns.index('client_snils')],
            [columns.index('contact_vc')],
            [columns.index('contact_tg')],
            [columns.index('contact_email')],
            [columns.index('contact_phone')]
        ])
        
        lst2 = np.array([
            [columns.index('client_fio_full'), columns.index('client_bday')],
            [columns.index('fin_loan_begin_dt'), columns.index('fin_loan_end_dt')],
            [columns.index('client_bday'), columns.index('addr_str')],
        ])


        self.list_of_link = [[] for i in range(len(self.data))]
        
        for el in lst1:
            print(el)
            self.data_list = self.data_list[np.argsort(self.data_list[:, el[0]], kind='stable')]
            for i in range(len(self.data_list)-1):
                if (self.data_list[i][el[0]] == self.data_list[i+1][el[0]] and 
                    str(self.data_list[i][el[0]]) != 'nan'):
                    self.list_of_link[int(self.data_list[i][-1])].append(int(self.data_list[i+1][-1]))
                    self.list_of_link[int(self.data_list[i+1][-1])].append(int(self.data_list[i][-1]))
                    
        for el in lst2:
            print(el)
            sort_idx = np.lexsort((self.data_list[:, el[1]], self.data_list[:, el[0]]))
            self.data_list = self.data_list[sort_idx]
            
            for i in range(len(self.data_list)-1):
                if (self.data_list[i][el[0]] == self.data_list[i+1][el[0]] and 
                    self.data_list[i][el[1]] == self.data_list[i+1][el[1]] and 
                    str(self.data_list[i][el[0]]) != 'nan' and 
                    str(self.data_list[i][el[1]]) != 'nan'):
                    self.list_of_link[int(self.data_list[i][-1])].append(int(self.data_list[i+1][-1]))
                    self.list_of_link[int(self.data_list[i+1][-1])].append(int(self.data_list[i][-1]))
                    
        self.data_list = self.data_list[np.argsort(self.data_list[:, -1], kind='stable')]
        
        
        self.used = [0 for i in range(len(self.data))]
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
                
        with open('good_files\\output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows(lst)
            

async def all_csv_in_one():
    try:
        df_pandas = pd.DataFrame(columns=[
            'client_id',
            'client_first_name',
            'client_middle_name',
            'client_last_name',
            'client_fio_full',
            'client_bday',
            'client_bplace',
            'client_cityzen',
            'client_resident_cd',
            'client_gender',
            'client_marital_cd',
            'client_graduate',
            'client_child_cnt',
            'client_mil_cd',
            'client_zagran_cd',
            'client_inn',
            'client_snils',
            'client_vip_cd',
            'contact_vc',
            'contact_tg',
            'contact_other',
            'contact_email',
            'contact_phone',
            'addr_region',
            'addr_country',
            'addr_zip',
            'addr_street',
            'addr_house',
            'addr_body',
            'addr_flat',
            'addr_area',
            'addr_loc',
            'addr_city',
            'addr_reg_dt',
            'addr_str',
            'fin_rating',
            'fin_loan_limit',
            'fin_loan_value',
            'fin_loan_debt',
            'fin_loan_percent',
            'fin_loan_begin_dt',
            'fin_loan_end_dt',
            'stream_favorite_show',
            'stream_duration',
            'create_date',
            'update_date',
            'source_cd'
        ])

        directory = 'files'
        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        for i in range(len(csv_files)):
            if csv_files[i] == 'all.csv':
                continue
            df_pandas = pd.concat([
                df_pandas,
                pd.read_csv(f"{directory}/{csv_files[i]}")
            ])
        df_pandas.to_csv(f"{directory}/all.csv", index=False)

        for filename in os.listdir(directory):
            if filename != 'all.csv':
                os.remove(os.path.join(directory, filename))
                    
        return True
    except Exception as e:
        return False


async def get_good_file():
    if await all_csv_in_one():
        backend('files/all.csv')
        os.makedirs('good_files', exist_ok=True)
        os.rename('output.csv', 'good_files/output.csv')

    return True