# -*- coding: utf-8 -*-
"""ETL_month.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VPcqosqweMTa-iwlJyjBT7YA-V9XYYmk
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

#2024 file 3rd
def data_wrangle():
    prlst = os.listdir(r'Z:\POS\Sales\3rd\2024\3rd_2024')
    #Import multiple excel files
    #rex=re.compile(r'3rd_2024_(05_14|05_16)')
    rex=re.compile(r'3rd_2024_05_16')
    dframe=[]
    for x in prlst:
        if rex.match(x):
            print(x)
            file_path=os.path.join('Z:/POS/Sales/3rd/2024/3rd_2024',x)
            df_list=pd.read_excel(file_path)
            dframe.append(df_list)
    combined_df=pd.concat(dframe,ignore_index=True)
    return combined_df
df_final=data_wrangle()

#2024 file 3rd
def item_concat(cols):
    prlst=os.listdir(r'Z:\POS\Product\3rd\Master_Item_Info')
    rex=re.compile(r'POS_.*')
    print(rex)
    dframe=[]
    for x in prlst:
        if rex.match(x):
            print(x)
            file_path=os.path.join('Z:/POS/Product/3rd/Master_Item_Info',x)
            df_list=pd.read_excel(file_path)
            dframe.append(df_list)
    combined_df=pd.concat(dframe,ignore_index=True)
    duplicated_val=combined_df.duplicated(subset=cols, keep=False)
    if duplicated_val.any():
        print('duplicated values are detected:')
        print(combined_df[cols][duplicated_val])

        combined_df=combined_df.drop_duplicates(subset=cols, keep='first')
        print('duplicated values are removed')
    else:
        print('no duplicated val')
    return combined_df
cols=['UPC']
item_info=item_concat(cols)

# 2nd branch
def data_wrangle():
    prlst = os.listdir(r'Z:\POS\Sales\2nd\2024\2nd_2024')
    rex=re.compile(r'2nd_2024_05_13')
    dframe=[]
    for x in prlst:
        if rex.match(x):
            print(x)
            file_path=os.path.join('Z:/POS/Sales/2nd/2024/2nd_2024',x)
            df_list=pd.read_excel(file_path)
            dframe.append(df_list)
    combined_df=pd.concat(dframe,ignore_index=True)
    return combined_df
df_final=data_wrangle()

# 2nd branch
def item_concat(cols):
    prlst=os.listdir(r'Z:\POS\Product\2nd\Master_Item_Info')
    rex=re.compile(r'POS_.*')
    print(rex)
    dframe=[]
    for x in prlst:
        if rex.match(x):
            print(x)
            file_path=os.path.join('Z:/POS/Product/2nd/Master_Item_Info',x)
            df_list=pd.read_excel(file_path)
            dframe.append(df_list)
    combined_df=pd.concat(dframe,ignore_index=True)
    duplicated_val=combined_df.duplicated(subset=cols, keep=False)
    if duplicated_val.any():
        print('duplicated values are detected:')
        print(combined_df[cols][duplicated_val])

        combined_df=combined_df.drop_duplicates(subset=cols, keep='first')
        print('duplicated values are removed')
    else:
        print('no duplicated val')
    return combined_df
cols=['UPC']
item_info=item_concat(cols)

merged_df=pd.merge(df_final, item_info, on='UPC',how='inner')
merged_pos=merged_df[['Invoice#','Account#','Date','Time','Total','UPC','Qty','Price','Discount','Total.1','Paid By','Type','Description','Sold Qty','Brand',"Vendor",'Category1','Category2','Category3','Food Stamp','Active']]

#remaning mapping
rename_mapping={"Account#":"Account","Paid By":"Payment","Invoice#":"Invoice","Total.1":"Amount"}
merged_pos.rename(columns=rename_mapping, inplace=True)
merged_pos=merged_pos.loc[:,~merged_pos.columns.duplicated()]
merged_pos["Date"]=pd.to_datetime(merged_pos["Date"], format='%Y%m%d')

def clean_brand(col):
    col=col.str.upper()
    col=col.str.strip()
    return col
merged_pos["Brand"]=clean_brand(merged_pos["Brand"])

host = '192.168.0.191'  # Replace with your MySQL host #192.168.0.103
user = 'root'  # Replace with your MySQL user #remote_user
password = '####'  # Replace with your MySQL password
database = 'hana'  # Replace with your MySQL database name

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
merged_pos.to_sql(name='pos_second', con=engine, if_exists='append', index=False, chunksize=50000000000)

#Receipt
#Data Cleaning for receipt
merged_pos_receipt=merged_pos.sort_values(by=['Invoice','Date','Total'])
merged_pos_receipt=merged_pos_receipt.drop_duplicates(subset='Invoice', keep='first')
merged_pos_receipt=merged_pos_receipt[["Invoice","Account","Date","Total"]].reset_index(drop=True)

#checking subtotal is correct with POS.
receipt_sum=merged_pos.groupby(["Date","Invoice","Total"])["Qty"].sum()
receipt_sum=pd.DataFrame(receipt_sum)
receipt_sum.reset_index(inplace=True)
receipt_sum=pd.DataFrame(receipt_sum.groupby("Date").agg({"Invoice":"nunique","Total":"sum","Qty":"sum"}))
receipt_sum_group=receipt_sum.groupby(by=[receipt_sum.index.month])["Total"].sum(); receipt_sum_group

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
merged_pos_receipt.to_sql(name='invoice_receipt_second', con=engine, if_exists='append', index=False, chunksize=50000000000)