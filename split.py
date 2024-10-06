import pandas as pd

# Загрузка данных
felony_df = pd.read_csv("/Users/k.chervaneva/Desktop/Econometric/filtered_data/felony.csv")
education_df = pd.read_csv("/Users/k.chervaneva/Desktop/Econometric/filtered_data/high_education.csv")
population_df = pd.read_csv("/Users/k.chervaneva/Desktop/Econometric/filtered_data/population.csv")
revenue_df = pd.read_csv("/Users/k.chervaneva/Desktop/Econometric/filtered_data/revenue.csv")
unemployment_df = pd.read_csv("/Users/k.chervaneva/Desktop/Econometric/filtered_data/unemployment.csv")
birthrate_df = pd.read_csv("/Users/k.chervaneva/Desktop/Econometric/filtered_data/birthrate.csv")

def unify_region_names(region):
    region = region.strip().lower()
    if 'москва' in region:
        return 'г. Москва'
    elif 'петербург' in region:
        return 'г. Санкт-Петербург'
    elif 'севастополь' in region:
        return 'г. Севастополь'
    return region

# Приведение названий регионов к единому виду
felony_df['Region'] = felony_df['Region'].apply(unify_region_names)
education_df['Region'] = education_df['Region'].apply(unify_region_names)
population_df['Region'] = population_df['Region'].apply(unify_region_names)
revenue_df['Region'] = revenue_df['Region'].apply(unify_region_names)
unemployment_df['Region'] = unemployment_df['Region'].apply(unify_region_names)
birthrate_df['Region'] = birthrate_df['Region'].apply(unify_region_names)

# Объединение данных
merged_df = felony_df
dataframes = [
    education_df,
    population_df,
    revenue_df,
    unemployment_df,
    birthrate_df
]

for df in dataframes:
    merged_df = pd.merge(
        merged_df,
        df,
        left_on='Region',
        right_on='Region',
        how='outer',
        suffixes=('', f'_{df.columns[1]}')  # добавление суффиксов к столбцам
    )

# Удаление дублирующегося столбца 'Region' и переименование столбцов по необходимости
# merged_df.drop(columns=['Region'], inplace=True)

# Обработка пропущенных значений: замена на 'пусто'
merged_df.fillna('пусто', inplace=True)

# Приведение типов данных к необходимым (например, к float), если это необходимо
# Примечание: Проверьте, нужно ли преобразовывать столбцы к float после замены пропущенных значений на строки.
# Например, если вы хотите преобразовать 'Уровень безработицы':
if 'Уровень безработицы' in merged_df.columns:
    merged_df['Уровень безработицы'] = merged_df['Уровень безработицы'].str.replace(',', '.').replace('пусто', '0').astype(float)

# Сохранение результата в файл
merged_df.to_csv("merged_data.csv", index=False, sep=','
                #  , encoding='utf-8'
                 )


# merged_df.to_csv("merged_data_windows_1251.csv", index=False, sep=',', encoding='windows-1251')  # Для Windows-1251

print("Данные успешно объединены и сохранены в 'merged_data.csv'")
