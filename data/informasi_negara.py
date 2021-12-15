import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd

def cetak_data(nama_negara,kode_negara,region,sub_region,input_tahun,jumlah_nol):
    col_kiri, col_kanan = st.columns([1,3])
    col_kiri.markdown('Nama Negara')
    col_kanan.markdown(f'=  {nama_negara}')
    col_kiri.markdown('kode Negara')
    col_kanan.markdown(f'=  {kode_negara}')
    col_kiri.markdown('Region')
    col_kanan.markdown(f'=  {region}')
    col_kiri.markdown('Subregion')
    col_kanan.markdown(f'=  {sub_region}')
    st.markdown(f'Jumlah produksi terbesar tahun {input_tahun} = **{jumlah_nol}**')
    st.markdown('**Produksi Keseluruhan Tahun**')

def app():
    nav=st.sidebar.container()

    with nav:
        st.markdown('Pilihan Tampilan')
        tabel = st.checkbox('Tabel Negara Tahun', value=True)
        mm = st.checkbox('Median dan Mean')
        grafik = st.checkbox('Grafik')
        info = st.checkbox('Informasi Negara Terbesar-Terkecil-Nol')

    st.header("Informasi Produksi Minyak Mentah Negara")
    input_tahun = st.slider('Tahun Negara', 1971,2021)
    minyak_data = pd.read_csv('produksi_minyak_mentah.csv')
    info_json = pd.read_json('kode_negara_lengkap.json')


    if(input_tahun>0):
        tahun_data = minyak_data[minyak_data['tahun'] == input_tahun]
        if(tahun_data.size>0):

            data_terbesar = tahun_data.groupby('kode_negara').sum().sort_values(['produksi'], ascending=False)
            
            mask_nol = data_terbesar['produksi']==0
            mask = data_terbesar['produksi']!=0
            df_terkecil = pd.DataFrame()
            df_terkecil = data_terbesar[mask].sort_values('produksi', ascending=True)
            df_nol = pd.DataFrame()
            df_nol = data_terbesar[mask_nol].sort_values('kode_negara', ascending=True)
            df_nol = df_nol.reset_index()
            df_terbesar = pd.DataFrame()
            df_terbesar = data_terbesar[mask]
            df_terbesar = df_terbesar.reset_index()
            
            tabel_terbesar = pd.DataFrame()
            tabel_nol = pd.DataFrame()
            
            if tabel:
                for x in range (len(df_terbesar)):
                    get_kode = df_terbesar['kode_negara'].iloc[x]
                    json_kode = info_json[info_json['alpha-3']==get_kode]
                    if(json_kode.size>0):
                        nama_negara = json_kode['name'].iloc[0]
                        region = json_kode['region'].iloc[0]
                        sub_region = json_kode['sub-region'].iloc[0]
                    else:
                        nama_negara = "Tidak Ada"
                        region = "Tidak Ada"
                        sub_region = "Tidak Ada"
                    kode_negara = get_kode

                    row_baru = {
                        'Nama Negara':nama_negara, 
                        'Kode Negara': get_kode, 
                        'Region':region,
                        'Sub-Region':sub_region,
                        'Jumlah Produksi':df_terbesar['produksi'].iloc[x]
                        }
                    tabel_terbesar = tabel_terbesar.append(row_baru, ignore_index=True)

                
                st.subheader(f'Data Produksi Negara Terbesar tahun {input_tahun}')
                tabel_terbesar.index = np.arange(1, len(tabel_terbesar)+1)
                st.write(tabel_terbesar)

            # ----------------
                tabel_terkecil = tabel_terbesar.sort_values(['Jumlah Produksi'], ascending=True)
                st.subheader(f'Data Produksi Negara Terkecil tahun {input_tahun}')
                tabel_terkecil.index = np.arange(1, len(tabel_terkecil)+1)
                st.write(tabel_terkecil)
            
            # ----------------
                for x in range (len(df_nol)):
                    get_kode = df_nol['kode_negara'].iloc[x]
                    json_kode = info_json[info_json['alpha-3']==get_kode]
                    if(json_kode.size>0):
                        nama_negara = json_kode['name'].iloc[0]
                        region = json_kode['region'].iloc[0]
                        sub_region = json_kode['sub-region'].iloc[0]
                    else:
                        nama_negara = "Tidak Ada"
                        region = "Tidak Ada"
                        sub_region = "Tidak Ada"
                    kode_negara = get_kode

                    row_baru = {
                        'Nama Negara':nama_negara, 
                        'Kode Negara': get_kode, 
                        'Region':region,
                        'Sub-Region':sub_region,
                        'Jumlah Produksi':df_nol['produksi'].iloc[x]
                        }
                    tabel_nol = tabel_nol.append(row_baru, ignore_index=True)

                
                st.subheader(f'Data Produksi Negara Nol tahun {input_tahun}')
                tabel_nol.index = np.arange(1, len(tabel_nol)+1)
                st.write(tabel_nol)



            output_data = pd.DataFrame(data_terbesar.head(1)).reset_index()
            output_kecil=pd.DataFrame(df_terkecil.head(1)).reset_index()
            output_nol=pd.DataFrame(df_nol.head(1)).reset_index()

            jumlah_terbesar = output_data['produksi'].iloc[0]
            jumlah_terkecil = output_kecil['produksi'].iloc[0]
            jumlah_nol = output_nol['produksi'].iloc[0]

            get_kode = output_data['kode_negara'].iloc[0]
            get_kode_nol = output_nol['kode_negara'].iloc[0]
            get_kode_kecil = output_kecil['kode_negara'].iloc[0]


            # median mean
            df_data = pd.DataFrame(tahun_data['produksi'])
            data_mean = df_data.mean()
            data_median = df_data.median()

            mean_median = pd.DataFrame({
                'mean': data_mean,
                'median': data_median
            })

            if mm:
                st.subheader(f'Median Mean Data pada tahun {input_tahun}')
                st.table(mean_median)

            recap_data = pd.DataFrame({
                'kode_negara': (get_kode, get_kode_kecil, get_kode_nol),
                'produksi': (jumlah_terbesar, jumlah_terkecil, jumlah_nol)
            })

            recap_data.index = recap_data['kode_negara']
            
            fig = plt.figure(figsize = (16, 8))
            plt.title('Data Produksi Minyak Mentah')
            plt.plot(recap_data['produksi'])
            plt.xlabel('Kode Negara', fontsize=18)
            plt.ylabel('Produksi', fontsize =18)

            
            if grafik:
                st.subheader(f'Grafik Terbesar-Terkecil Produksi Minyak Mentah Negara tahun {input_tahun}')
                st.pyplot(fig)
            
            # ---
            if info:
                st.subheader(f'Produksi Terbesar Pada Tahun {input_tahun}')
                json_kode = info_json[info_json['alpha-3']== get_kode]

                if(json_kode.size>0):
                    nama_negara = json_kode['name'].iloc[0]
                    region = json_kode['region'].iloc[0]
                    sub_region = json_kode['sub-region'].iloc[0]
                else:
                    nama_negara = "Tidak ada dalam json"
                    region = "Tidak ada dalam json"
                    sub_region = "Tidak ada dalam json"
                kode_negara = get_kode

                negara_tahun = minyak_data[minyak_data['kode_negara']==kode_negara]

                negara_tahun.index = np.arange(1, len(negara_tahun)+1)

                cetak_data(
                    nama_negara,
                    kode_negara,
                    region,
                    sub_region,
                    input_tahun,
                    jumlah_terbesar
                )
                st.write(negara_tahun)

                # ----
                st.subheader(f"Produksi Terkecil Pada Tahun {input_tahun}")
                json_kode = info_json[info_json['alpha-3']== get_kode_kecil]
                if(json_kode.size>0):
                    nama_negara = json_kode['name'].iloc[0]
                    region = json_kode['region'].iloc[0]
                    sub_region = json_kode['sub-region'].iloc[0]
                else:
                    nama_negara = "Tidak ada dalam json"
                    region = "Tidak ada dalam json"
                    sub_region = "Tidak ada dalam json"
                kode_negara = get_kode_kecil

                negara_tahun = minyak_data[minyak_data['kode_negara']==kode_negara]
                negara_tahun.index = np.arange(1, len(negara_tahun)+1)

                cetak_data(
                    nama_negara,
                    kode_negara,
                    region,
                    sub_region,
                    input_tahun,
                    jumlah_terkecil
                )
                st.write(negara_tahun)

                # ---
                st.subheader(f"Produksi Nol Pada Tahun {input_tahun}")
                json_kode = info_json[info_json['alpha-3']==get_kode_nol]
                if(json_kode.size>0):
                    nama_negara = json_kode['name'].iloc[0]
                    region = json_kode['region'].iloc[0]
                    sub_region = json_kode['sub-region'].iloc[0]
                else:
                    nama_negara = "Tidak ada dalam json"
                    region = "Tidak ada dalam json"
                    sub_region = "Tidak ada dalam json"

                kode_negara = get_kode_nol

                negara_tahun = minyak_data[minyak_data['kode_negara']==kode_negara]
                negara_tahun.index = np.arange(1, len(negara_tahun)+1)

                cetak_data(
                    nama_negara,
                    kode_negara,
                    region,
                    sub_region,
                    input_tahun,
                    jumlah_nol
                )
                st.write(negara_tahun)
            
        
        else:
            st.error("Data Tidak Ada!")