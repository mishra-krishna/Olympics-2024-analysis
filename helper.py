import pandas as pd
import re

def get_countries(df_atheletes):
    return df_atheletes['country_code'].astype(str).unique().tolist()

def get_overall_cards(df_atheletes,df_events):
    total_sports = df_events['sport'].nunique()
    total_events = df_events['event'].nunique()
    total_participants = df_atheletes['code'].nunique()
    total_countries = df_atheletes['country'].nunique()
    return total_sports, total_events, total_participants, total_countries

def filter_by_country(df, country_code):
    return df if country_code == 'All' else df[df['country_code'] == country_code]


def get_medal_cards(df_medals_total, selected_country):
    
    country_data = filter_by_country(df_medals_total, selected_country)
    total_gold = country_data['Gold Medal'].sum()
    total_silver = country_data['Silver Medal'].sum()
    total_bronze = country_data['Bronze Medal'].sum()
    return total_gold, total_silver, total_bronze   


def calculate_medalists_age(df_medalists):
    df_medalists['birth_date'] = pd.to_datetime(df_medalists['birth_date'], errors='coerce')
    df_medalists['medal_date'] = pd.to_datetime(df_medalists['medal_date'], errors='coerce')

    df_medalists['age'] = (df_medalists['medal_date'] - df_medalists['birth_date']).dt.days // 365

    return df_medalists

def get_top_medalists_df(df_medallists,selected_country):
    df_medallists = filter_by_country(df_medallists, selected_country)
    df_pivot = df_medallists.pivot_table(index='name', columns='medal_type', aggfunc='size', fill_value=0)

    df_pivot['Total Medals'] = df_pivot.sum(axis=1)

    df_pivot = df_pivot[df_pivot['Total Medals'] >= 2]

    df_pivot = df_pivot.sort_values(by='Total Medals', ascending=False)

    df_pivot = df_pivot.reset_index()

    df_pivot = df_pivot[['name', 'Gold Medal', 'Silver Medal', 'Bronze Medal', 'Total Medals']]
    
    return df_pivot

def fetch_by_discipline(df_medallists, discipline,selected_country):
    df_medallists_by_discipline = filter_by_country(df_medallists,selected_country)[df_medallists['discipline']==discipline][['name','medal_type','event']]
    return df_medallists_by_discipline

def calculate_age(df_atheletes, selected_country):
    df_atheletes['birth_date'] = pd.to_datetime(filter_by_country(df_atheletes,selected_country)['birth_date'], errors='coerce')
    df_atheletes['age'] = (pd.to_datetime('2024-8-11') - df_atheletes['birth_date']).dt.days // 365
    return df_atheletes['age']

def clean_birth_place(birth_place):
    if pd.isna(birth_place):
        return None
    
    birth_place = re.sub(r'\(.*?\)', '', birth_place)
    
    birth_place = re.sub(r',.*', '', birth_place)
    
    birth_place = birth_place.replace('-', '')
    
    birth_place = re.sub(r'\d+', '', birth_place)
    
    birth_place = birth_place.strip()
    
    return birth_place

def split_by_deli(df,column):
    df_split = df[column].str.lower().str.split(',', expand=True).apply(lambda x: x.str.strip())
    return df_split

def get_top(df):
    val_list_list = df.values.flatten()
    val_list_list = [column for column in val_list_list if pd.notna(column)]

    df_val_count = pd.DataFrame({'column': val_list_list})
    df_val_count['frequency'] = df_val_count.groupby('column')['column'].transform('count')

    df_val_count = df_val_count.drop_duplicates().reset_index(drop=True)

    return df_val_count.sort_values(by='frequency', ascending=False).reset_index(drop=True)

    