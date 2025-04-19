import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import textwrap

def wrap_labels(labels, width=20):
    return ['\n'.join(textwrap.wrap(label, width=width)) for label in labels]

sns.set(style='dark')

# Load data
main_data_df = pd.read_csv("main_data.csv")
main_data_df['order_purchase_timestamp'] = pd.to_datetime(main_data_df['order_purchase_timestamp'])

# Sidebar filter
min_date = main_data_df['order_purchase_timestamp'].min()
max_date = main_data_df['order_purchase_timestamp'].max()

with st.sidebar:
    st.image("https://github.com/hldfiadn/tren-penjualan-app/raw/main/logo_dashboard.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = main_data_df[(main_data_df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & 
                       (main_data_df['order_purchase_timestamp'] <= pd.to_datetime(end_date))]

# ===== Tab Utama: Dashboard & RFM =====
main_tabs = st.tabs(["Dashboard Utama", "RFM Analysis"])

# ==== TAB 1: DASHBOARD UTAMA ====
with main_tabs[0]:
    
    # ==== Tab 1.1: Tren Pembelian Berdasarkan Waktu ====
    st.subheader("A. Tren Pembelian Berdasarkan Waktu")
    tabs = st.tabs(["Tahunan", "Bulanan", "Mingguan", "Harian"])

    # Tahunan
    with tabs[0]:
        yearly_orders = main_df.groupby(main_df['order_purchase_timestamp'].dt.to_period("Y")).order_id.nunique()
        fig, ax = plt.subplots(figsize=(10, 4))
        yearly_orders.index = yearly_orders.index.to_timestamp()
        sns.lineplot(x=yearly_orders.index, y=yearly_orders.values, marker='o', ax=ax)
        ax.set_title('Tren Pembelian Tahunan')
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Jumlah Pesanan')
        ax.grid(True)
        st.pyplot(fig)

    # Bulanan
    with tabs[1]:
        monthly_orders = main_df.groupby(main_df['order_purchase_timestamp'].dt.to_period("M")).order_id.nunique()
        monthly_orders.index = monthly_orders.index.to_timestamp()
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.lineplot(x=monthly_orders.index, y=monthly_orders.values, marker='o', ax=ax)
        ax.set_title('Tren Pembelian Bulanan')
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Jumlah Pesanan')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        st.pyplot(fig)

    # Mingguan
    with tabs[2]:
        weekly_orders = main_df.groupby(main_df['order_purchase_timestamp'].dt.to_period("W")).order_id.nunique()
        weekly_orders.index = weekly_orders.index.to_timestamp()
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.lineplot(x=weekly_orders.index, y=weekly_orders.values, marker='o', ax=ax)
        ax.set_title('Tren Pembelian Mingguan')
        ax.set_xlabel('Minggu')
        ax.set_ylabel('Jumlah Pesanan')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        st.pyplot(fig)

    # Harian
    with tabs[3]:
        daily_orders = main_df.groupby(main_df['order_purchase_timestamp'].dt.date).order_id.nunique()
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.lineplot(x=daily_orders.index, y=daily_orders.values, linewidth=1, ax=ax)
        ax.set_title('Tren Pembelian Harian')
        ax.set_xlabel('Tanggal')
        ax.set_ylabel('Jumlah Pesanan')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        st.pyplot(fig)

        
    # ==== Tab 1.2: Produk dengan Penjualan Terbaik & Terburuk ====
    st.subheader("B. Produk dengan Penjualan Terbaik & Terburuk")
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    # Kategori terlaris
    top_categories = main_df['product_category_name_english'].value_counts().head(5)
    sns.barplot(x=top_categories.values, y=top_categories.index, palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Number of Sales", fontsize=30)
    ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)
    
    # Kategori kurang laris
    bottom_categories = main_df['product_category_name_english'].value_counts().sort_values().head(5)
    short_labels = [label[:25] for label in bottom_categories.index]
    
    sns.barplot(x=bottom_categories.values, y=short_labels, palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Number of Sales", fontsize=30)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)
    
    st.pyplot(fig)


    # ==== Tab 1.3: Distribusi Jumlah Pesanan per Lokasi (State) ====
    st.subheader("C. Distribusi Jumlah Pesanan per Lokasi (State)")
    
    # Jumlah pesanan per state
    state_orders = main_df.groupby('customer_state')['order_id'].nunique().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=state_orders.index, y=state_orders.values, ax=ax)
    ax.set_title('Jumlah Pesanan per Lokasi (State)')
    ax.set_xlabel('State')
    ax.set_ylabel('Jumlah Pesanan')
    st.pyplot(fig)


    # ==== Tab 1.4: Tren Bulanan (Jumlah Pesanan) Berdasarkan Lokasi ====
    st.subheader("D. Tren Bulanan (Jumlah Pesanan) Berdasarkan Lokasi")
    
    main_df['order_month'] = main_df['order_purchase_timestamp'].dt.to_period('M')
    
    # Multiselect state
    available_states = main_df['customer_state'].unique().tolist()
    selected_states = st.multiselect("Pilih Lokasi (State):", options=available_states, default=state_orders.head(5).index.tolist())
    
    state_filtered_df = main_df[main_df['customer_state'].isin(selected_states)]
    state_monthly = state_filtered_df.groupby(['order_month', 'customer_state'])['order_id'].nunique().unstack().fillna(0)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    state_monthly.index = state_monthly.index.to_timestamp()
    state_monthly.plot(ax=ax)
    ax.set_title('Tren Bulanan Jumlah Pesanan per Lokasi')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Pesanan')
    ax.grid(True)
    st.pyplot(fig)

    
    # ==== Tab 1.5: Analisis Metode Pembayaran ====
    st.subheader("E. Analisis Metode Pembayaran")
    tabs = st.tabs(["Total Nilai", "Rata-rata"])

    payment_summary = main_df.groupby('payment_type')['payment_value'].agg(['count', 'sum', 'mean']).sort_values(by='sum', ascending=False)

    # Total Nilai
    with tabs[0]:
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        sns.barplot(x=payment_summary.index, y=payment_summary['sum'], ax=ax1)
        ax1.set_xlabel('Metode Pembayaran')
        ax1.set_ylabel('Total Nilai Transaksi (BRL)')
        ax1.set_title('Total Nilai Transaksi per Metode Pembayaran')
        ax1.tick_params(axis='x', rotation=45)
        st.pyplot(fig1)

    # Rata-rata
    with tabs[1]:
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.barplot(x=payment_summary.index, y=payment_summary['mean'], ax=ax2)
        ax2.set_xlabel('Metode Pembayaran')
        ax2.set_ylabel('Rata-rata Nilai Transaksi')
        ax2.set_title('Rata-rata Nilai Transaksi per Metode Pembayaran')
        ax2.tick_params(axis='x', rotation=45)
        st.pyplot(fig2)



with main_tabs[1]:

    # ==== Tab 2.1: RFM Analysis ====
    st.subheader("A. RFM (Recency, Frequency, Monetary) Analysis")
    st.markdown("""
    **RFM digunakan untuk mengelompokkan pelanggan dan mengidentifikasi pelanggan.**
    
    - **Recency**: Seberapa *baru* pelanggan melakukan pembelian terakhir  
    - **Frequency**: Seberapa *sering* pelanggan melakukan pembelian  
    - **Monetary**: Seberapa *besar* pelanggan mengeluarkan uang
    """)

    main_df['order_purchase_timestamp'] = pd.to_datetime(main_df['order_purchase_timestamp'])
    snapshot_date = main_df['order_purchase_timestamp'].max()

    # RFM dataframe
    rfm_df = main_df.groupby('customer_id').agg({
        'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'nunique',
        'payment_value': 'sum'
    }).reset_index()

    rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']

    # Skor RFM
    rfm_df['r_score'] = pd.qcut(rfm_df['recency'], 4, labels=[4,3,2,1])
    rfm_df['f_score'] = pd.qcut(rfm_df['frequency'].rank(method='first'), 1, labels=[1])
    rfm_df['m_score'] = pd.qcut(rfm_df['monetary'], 4, labels=[1,2,3,4])
    rfm_df['rfm_score'] = rfm_df[['r_score','f_score','m_score']].sum(axis=1).astype(int)

    # Segmentasi RFM
    def segment_customer(score):
        if score >= 7:
            return 'Gold'
        elif score >= 5:
            return 'Silver'
        elif score >= 3:
            return 'Bronze'
        else:
            return 'Inactive'
    
    rfm_df['segment'] = rfm_df['rfm_score'].apply(segment_customer)

    
    # ==== Tab 2.2: Kategori Segmentasi RFM ====
    st.subheader("B. Kategori Segmentasi RFM")
    st.markdown("""
    - 🥇 **Gold**: Pelanggan terbaik, sering belanja dan mengeluarkan banyak uang  
    - 🥈 **Silver**: Cukup aktif, potensi menjadi loyal customer  
    - 🥉 **Bronze**: Mulai tidak aktif, pembelanjaan rendah  
    - 💤 **Inactive**: Tidak aktif, jarang belanja, hampir hilang  
    """)

    
    # ==== Tab 2.3: Distribusi Jumlah Pelanggan per Segmen ====
    st.subheader("C. Distribusi Jumlah Pelanggan per Segmen")

    # Jumlah customer per segmen
    segment_order = ['Gold', 'Silver', 'Bronze', 'Inactive']
    segment_counts = rfm_df['segment'].value_counts().reindex(segment_order).reset_index()
    segment_counts.columns = ['Segment', 'Jumlah Customer']
    
    st.dataframe(segment_counts)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=segment_counts, x='Segment', y='Jumlah Customer', palette=['#FFD700', '#999999', '#CD7F32', '#000000'], ax=ax)
    ax.set_title("Jumlah Customer per Segmen", fontsize=16)
    ax.set_xlabel("Segment")
    ax.set_ylabel("Jumlah Customer")
    st.pyplot(fig)


    # ==== Tab 2.4: Tren Order Bulanan berdasarkan Segmen Pelanggan ====
    st.subheader("D. Tren Order Bulanan Berdasarkan Segmen Pelanggan")

    main_df['order_month'] = main_df['order_purchase_timestamp'].dt.to_period('M')
    main_with_segment = main_df.merge(rfm_df[['customer_id', 'segment']], on='customer_id', how='left')
    
    # Multiselect segment
    segment_options = st.multiselect(
        "Pilih Segmentasi Pelanggan:",
        options=['Gold', 'Silver', 'Bronze', 'Inactive'],
        default=['Gold', 'Silver', 'Bronze', 'Inactive']
    )
  
    # Filter data sesuai segmen
    filtered_df = main_with_segment[main_with_segment['segment'].isin(segment_options)]
    
    monthly_segment_orders = (
        filtered_df.groupby(['order_month', 'segment'])['order_id']
        .nunique()
        .unstack()
        .fillna(0)
    )
    monthly_segment_orders.index = monthly_segment_orders.index.to_timestamp()

    segment_colors = {
        'Gold': '#FFD700',
        'Silver': '#707070',
        'Bronze': '#CD7F32',
        'Inactive': '#000000'
    }
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(12, 5))
    for segment in segment_options:
        if segment in monthly_segment_orders.columns:
            ax.plot(
                monthly_segment_orders.index,
                monthly_segment_orders[segment],
                label=segment,
                color=segment_colors[segment],
                marker='o'
            )
    
    ax.set_title("Tren Order Bulanan Berdasarkan Segmen Pelanggan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Order")
    ax.legend(title="Segment")
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)


    # ==== Tab 2.5: Distribusi Produk berdasarkan Segmentasi RFM ====    
    st.subheader("E. Distribusi Produk berdasarkan Segmentasi RFM")

    selected_segment = st.selectbox("Pilih Segmen Pelanggan:", options=['Gold', 'Silver', 'Bronze', 'Inactive'])
    product_type = st.selectbox("Pilih Jenis Produk:", options=['Terlaris', 'Kurang Laku'])
    main_with_segment = main_df.merge(rfm_df[['customer_id', 'segment']], on='customer_id', how='left')
    segment_df = main_with_segment[main_with_segment['segment'] == selected_segment]
    
    # Jumlah order per produk
    product_counts = (
        segment_df['product_category_name_english']
        .value_counts()
        .dropna()
    )
    
    if product_type == 'Terlaris':
        product_counts = product_counts.head(10)
    else:  # Kurang Laku
        product_counts = product_counts.sort_values(ascending=True).head(10)
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 5))
    highlight_color = "#90CAF9"
    bar_colors = [highlight_color] + ['#D3D3D3'] * (len(product_counts) - 1)
    sns.barplot(x=product_counts.values, y=product_counts.index, palette=bar_colors, ax=ax)
    ax.set_title(f"{product_type} - Segmen {selected_segment}", fontsize=16)
    ax.set_xlabel("Jumlah Order")
    ax.set_ylabel("Kategori Produk")
    st.pyplot(fig)
