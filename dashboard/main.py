import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load your data (ganti dengan kode pengambilan data Anda)
customer = pd.read_csv('../dataset/customers_dataset.csv')
geolocation = pd.read_csv('../dataset/geolocation_dataset.csv')
order_item = pd.read_csv('../dataset/order_items_dataset.csv')
order_payment = pd.read_csv('../dataset/order_payments_dataset.csv')
order_review = pd.read_csv('../dataset/order_reviews_dataset.csv')
orders = pd.read_csv('../dataset/orders_dataset.csv')
product_category = pd.read_csv('../dataset/product_category_name_translation.csv')
products = pd.read_csv('../dataset/products_dataset.csv')
sellers = pd.read_csv('../dataset/sellers_dataset.csv')

order_review.fillna(value="Prefer not to say", inplace=True)
order_review.isna().sum()
for index, row in orders.iterrows():
    if pd.isna(row['order_approved_at']) or pd.isna(row['order_delivered_carrier_date']) or pd.isna(row['order_delivered_customer_date']):
        if not pd.isna(row['order_purchase_timestamp']):
            date_other = datetime.strptime(row['order_purchase_timestamp'], '%Y-%m-%d %H:%M:%S')
            new_date_other = date_other + timedelta(minutes=10)
            orders.at[index, 'order_approved_at'] = new_date_other.strftime('%Y-%m-%d %H:%M:%S')
            orders.at[index, 'order_delivered_carrier_date'] = new_date_other.strftime('%Y-%m-%d %H:%M:%S')
            orders.at[index, 'order_delivered_customer_date'] = new_date_other.strftime('%Y-%m-%d %H:%M:%S')

products.dropna(inplace=True)

# Menghitung jumlah payment_type
data_order_payment = order_payment.groupby(by="payment_type").size()
# Menghitung jumlah payment_type berdasarkan customer_state
df_merged = pd.merge(order_payment, order_item, on='order_id', how='inner')
df_merged = pd.merge(df_merged, orders, on='order_id', how='inner')
df_merged = pd.merge(df_merged, customer, on='customer_id', how='inner')
df_merged = pd.merge(df_merged, geolocation, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='inner')

result = df_merged.groupby(['customer_city', 'customer_state', 'payment_type'])['payment_value'].sum().reset_index()
result.sort_values(by='customer_state', ascending=True)

# menghitung uang yang dibelanjakan pelanggan
merge = pd.merge(order_item, orders, on="order_id", how="inner")
merge2 = merge.groupby('customer_id')['price'].sum().reset_index()
data_merge2 = merge2.sort_values(by="price", ascending=False)

# menghitung produk yang terjual pada setiap kategori produk
merge_orderItem_products = pd.merge(order_item, products, on="product_id", how="inner")
item_orderItem_products = merge_orderItem_products.groupby('product_category_name')['product_id'].count().reset_index()
data_item_orderItem_products = item_orderItem_products.sort_values(by='product_id', ascending=False)

     
st.title('Belajar Analisis Data')

st.header('Grafik Distribusi Jenis Pembayaran')
st.write('Distribusi Jumlah Transaksi per Jenis Pembayaran:')
fig, ax = plt.subplots(figsize=(8, 6))
data_order_payment.plot(kind='bar', ax=ax)
plt.title('Distribusi Jumlah Transaksi per Jenis Pembayaran')
plt.xlabel('Jenis Pembayaran')
plt.ylabel('Jumlah Transaksi')
plt.xticks(rotation=45)
st.pyplot(fig)

# Display the data using Streamlit
st.header('Data Total Pengeluaran Pelanggan:')
st.write('5 Pelanggan dengan Total Pengeluaran Tertinggi:')
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(data_merge2['customer_id'], data_merge2['price'])
ax.set_title('5 Pelanggan dengan Total Pengeluaran Tertinggi')
ax.set_xlabel('Customer ID')
ax.set_ylabel('Total Pengeluaran (Price)')
plt.xticks(rotation=45)
st.pyplot(fig)

st.header('Data Kategori Produk Yang Sering Terjual:')
# Create and display a bar chart using Matplotlib and st.pyplot()
st.write('5 Kategori Produk Yang Sering Terjual:')
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(data_item_orderItem_products['product_category_name'], data_item_orderItem_products['product_id'])
ax.set_title('5 Kategori Produk Yang Sering Terjual')
ax.set_xlabel('Nama Kategori')
ax.set_ylabel('Total Produk')
plt.xticks(rotation=45)
st.pyplot(fig)

st.caption('Copyright (c) 2023')
