# -*- coding: utf-8 -*-
"""promo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_4-6hndg1fsOulIdLpyVecb8hOSSp85A
"""

import pandas as pd
import numpy as np
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import mysql.connector
import datetime as dt
from pathlib import Path
from dateutil.relativedelta import relativedelta

#3rd
df=pd.read_excel(r'Z:\POS\Promotion\3rd\Promo_041624.xlsx')

def data_processing(df):
    df = df[['UPC','Receipt Description','Price 1','Start','End','Promotion','Promo.Prc','Qty $ Off Name','$ Off Qty','$ Off Prc','$ Off Qty2','$ Off Prc2']]
    df["Promotion"] = df["Promotion"].map({True:1, False:0})
    df = df[~(df["Price 1"] < 0.0) | (df["Price 1"] == 0.0)]
    df = df.loc[:, ~df.columns.duplicated()]
    df["start"] = pd.to_datetime(df["Start"], format='%Y%m%d', errors='coerce')
    df["end"] = pd.to_datetime(df["End"], format='%Y%m%d',errors='coerce')
    df["diff"] = (df["end"] - df["start"]).dt.days
    df["diff"] = df["diff"].fillna(0).astype(int)
    df = df.drop(["Start","End"],axis=1)

    rename_mapping={
        "Receipt Description":"description","Price 1":"origPrice","Promo.Prc":"promoPrice",'Qty $ Off Name':'off_name','Promotion':'promo',
        '$ Off Qty':'off_qty','$ Off Prc':'off_prc','$ Off Qty2':'off_qty2','$ Off Prc2':'off_prc2'
    }
    df.rename(columns=rename_mapping, inplace=True)
    return df
df = data_processing(df)

def compute_new_value(row):
    if not row['promo'] and row['promoPrice'] != 0:
        # If there is no promotion and the promo price is not zero, return the promo price
        return row['promoPrice']
        # If there is promotion and the promo price is not zero AND off_price IS ZERO
    elif row['promo'] and row['promoPrice'] != 0 and row['off_prc'] == 0:
        return row["promoPrice"]
    elif row['promo'] and row['promoPrice'] == 0:
        # If there is a promotion and the promo price is zero, compare $ Off Pr and $ Off Pr2
        price1 = row['origPrice']
        price_after_off1 = price1 - row['off_prc']
        price_after_off2 = price1 - row['off_prc2']
        return min(price_after_off1, price_after_off2)
    elif row['promo'] and row['promoPrice'] != 0:
        # If there is a promotion, regardless of PromoPrice, compare Price1 and the larger value between $ Off Pr and $ Off Pr2
        price1 = row['origPrice']
        price_after_off1 = price1 - row['off_prc']
        price_after_off2 = price1 - row['off_prc2']
        return price1 - max(row['off_prc'], row['off_prc2'], key=lambda x: (x is not None, x))
    else:
        # If none of the above conditions are met, return the original price
        return row['origPrice']
df['final_prc'] = df.apply(compute_new_value, axis=1)

#SQL connect
host = '192.168.0.191'  # Replace with your MySQL host #192.168.0.103
user = 'root'  # Replace with your MySQL user #remote_user
password = '####'  # Replace with your MySQL password
database = 'hana'  # Replace with your MySQL database name

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

#Extracting POS data from SQL
dff=pd.read_sql("""
                SELECT *
                FROM hana.pos
                WHERE YEAR(date) = 2024 AND
                category1 = 'ASIAN GROCERY'
                """, con=engine)

#Merging Promo & POS
merged_df = pd.merge(dff, df, on='UPC', how='inner')

merged_df=merged_df[["UPC","Date","description","Qty","start","end","diff","final_prc"]]

def compare_qty(row, sales_data):
    pre_promo_start = row['start'] - pd.to_timedelta(row['diff'], unit='days')
    pre_promo_end = row['start']
    upc_sales_data = sales_data[sales_data['UPC'] == row['UPC']]
    pre_promo_qty = upc_sales_data.loc[(sales_data['Date'] >= pre_promo_start) & (upc_sales_data['Date'] < pre_promo_end), 'Qty'].sum()
    promo_qty = upc_sales_data.loc[(sales_data['Date'] >= row['start']) & (upc_sales_data['Date'] <= row['end']), 'Qty'].sum()
    return pre_promo_qty, promo_qty
# Applying the fcn, ensuring result_type is set to 'expand' to split into columns
merged_df[['pre_promo_qty', 'promo_qty']] = merged_df.apply(lambda row: compare_qty(row, merged_df), axis=1, result_type='expand')
merged_df=merged_df[merged_df["pre_promo_qty"]!=0]

promo_final = merged_df.drop_duplicates('UPC')

promo_final.sort_values(by='promo_qty', ascending=False)