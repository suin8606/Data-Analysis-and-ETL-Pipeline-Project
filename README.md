# Data Analysis and ETL Pipeline Project
## Overview
This project contains two main scripts: one for analyzing the effectiveness of promotional campaigns and another for performing ETL (Extract, Transform, Load) operations on sales data. The analysis is performed using Python, showcasing different aspects of data handling, merging, and processing.

## Files
* Promotion_Effectiveness_Analysis.py: A Python script that analyzes the effectiveness of promotional campaigns by comparing pre-promo and promo sales quantities.
* ETL_Data_Wrangling_Pipeline.py: A Python script that performs ETL operations on sales data from multiple sources, cleaning and merging the data for further analysis.

## Project Details
### Promotion Effectiveness Analysis (Python)
This script performs the following tasks:

1. Data Loading: Reads promotion data from an Excel file.
2. Data Processing: Cleans and preprocesses the promotion data, including date handling and column renaming.
3. Price Calculation: Computes the final price based on various promotion conditions.
4. SQL Extraction: Extracts Point of Sale (POS) data from a SQL database.
5. Data Merging: Merges POS data with promotion data.
6. Quantity Comparison: Compares sales quantities before and during promotions.
7. Final Output: Produces a DataFrame with the analysis results.

## ETL Data Wrangling Pipeline (Python)
This script performs the following tasks:

1. Data Loading: Reads sales data from multiple Excel files.
2. Data Concatenation: Combines data from multiple sources into a single DataFrame.
3. Data Cleaning: Identifies and removes duplicate entries.
4. SQL Integration: Connects to a SQL database to store cleaned data.
5. Receipt Processing: Processes receipt data to ensure consistency with POS data.
6. Summary and Reporting: Summarizes sales data by date and month for reporting.
