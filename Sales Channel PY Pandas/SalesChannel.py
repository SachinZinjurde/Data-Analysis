import pandas as pd

# Load the data from the provided Excel file
file_path = r'\DataTransfer\INVLINES2 03_13_2024.xlsx'
sales_data_df = pd.read_excel(file_path)

# Convert invoice date to datetime
sales_data_df['INVOICE_DATE'] = pd.to_datetime(sales_data_df['INVOICE_DATE'], format='%Y%m%d')

# Filter data for FY2022 and FY2023
fy_data_df = sales_data_df[sales_data_df['INVOICE_DATE'].dt.year.isin([2022, 2023])]

# Calculate profit margin and highest profit margin part
fy_data_df['PROFIT_MARGIN'] = fy_data_df['SALES'] - fy_data_df['COSTS']
highest_profit_margin_part = fy_data_df.loc[fy_data_df['PROFIT_MARGIN'].idxmax()]

# Aggregate sales data by month and channel
fy_data_df['MONTH'] = fy_data_df['INVOICE_DATE'].dt.to_period('M')
monthly_sales = fy_data_df.groupby(['MONTH', 'CUSTOMER_CODE'])['SALES'].sum().reset_index()
monthly_sales['MONTH'] = monthly_sales['MONTH'].dt.to_timestamp()

# Calculate Year-over-Year (YOY) and Month-over-Month (MOM) growth
monthly_sales['YOY_growth'] = monthly_sales.groupby('CUSTOMER_CODE')['SALES'].pct_change(periods=12)
monthly_sales['MOM_growth'] = monthly_sales.groupby('CUSTOMER_CODE')['SALES'].pct_change()

# Aggregate customer performance data
customer_performance = fy_data_df.groupby(['CUSTOMER_CODE'])['SALES'].sum().reset_index()

# Identify top and low-performing customers
top_customers = customer_performance.sort_values(by='SALES', ascending=False).head(10)
low_customers = customer_performance.sort_values(by='SALES', ascending=True).head(10)

# Areas for growth analysis (example: channels with highest sales growth potential)
channel_performance = customer_performance.groupby('CUSTOMER_CODE')['SALES'].sum().reset_index()

# Save the processed data to CSV files for Power BI
monthly_sales.to_csv(r'\DataTransfer\monthly_sales.csv', index=False)
customer_performance.to_csv(r'\DataTransfer\customer_performance.csv', index=False)
channel_performance.to_csv(r'\DataTransfer\channel_performance.csv', index=False)
top_customers.to_csv(r'\DataTransfer\top_customers.csv', index=False)
low_customers.to_csv(r'\DataTransfer\low_customers.csv', index=False)
