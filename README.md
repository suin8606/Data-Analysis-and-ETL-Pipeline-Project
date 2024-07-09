Data Analysis and ETL Pipeline Project
Overview
This project contains two main scripts: one for analyzing the effectiveness of promotional campaigns and another for performing ETL (Extract, Transform, Load) operations on sales data. The analysis is performed using Python, showcasing different aspects of data handling, merging, and processing.

Files
Promotion_Effectiveness_Analysis.py: A Python script that analyzes the effectiveness of promotional campaigns by comparing pre-promo and promo sales quantities.
ETL_Data_Wrangling_Pipeline.py: A Python script that performs ETL operations on sales data from multiple sources, cleaning and merging the data for further analysis.
Project Details
Promotion Effectiveness Analysis (Python)
This script performs the following tasks:

Data Loading: Reads promotion data from an Excel file.
Data Processing: Cleans and preprocesses the promotion data, including date handling and column renaming.
Price Calculation: Computes the final price based on various promotion conditions.
SQL Extraction: Extracts Point of Sale (POS) data from a SQL database.
Data Merging: Merges POS data with promotion data.
Quantity Comparison: Compares sales quantities before and during promotions.
Final Output: Produces a DataFrame with the analysis results.
ETL Data Wrangling Pipeline (Python)
This script performs the following tasks:

Data Loading: Reads sales data from multiple Excel files.
Data Concatenation: Combines data from multiple sources into a single DataFrame.
Data Cleaning: Identifies and removes duplicate entries.
SQL Integration: Connects to a SQL database to store cleaned data.
Receipt Processing: Processes receipt data to ensure consistency with POS data.
Summary and Reporting: Summarizes sales data by date and month for reporting.
