import matplotlib.pyplot as plt
from pandas.io.formats import style
import numpy as np
import streamlit as st
import pandas as pd


def app():
    st.header("Informasi Produksi Minyak Mentah Negara")
    input_tahun = st.number_input('Tahun Negara', min_value=0)
    minyak_data = pd.read_csv('produksi_minyak_mentah.csv')
    info_json = pd.read_json('kode_negara_lengkap.json')

    if(input_tahun>0):
        tahun_data = minyak_data[minyak_data['tahun'] == input_tahun]

        if(tahun_data.size>0):

            data_terbesar = tahun_data.groupby('kode_negara').sum().sort_values(['produksi'], ascending=False)
            data_nol = tahun_data.groupby('kode_negara').sum().sort_values(['produksi'], ascending=True)
            
            mask = data_nol['produksi']!=0
            df_terkecil = pd.DataFrame()
            df_terkecil = data_nol[mask].sort_values('produksi', ascending=True)

            output_data = pd.DataFrame(data_terbesar.head(1)).reset_index()
            output_kecil=pd.DataFrame(df_terkecil.head(1)).reset_index()
            output_nol=pd.DataFrame(data_nol.head(1)).reset_index()

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

            st.subheader(f'Grafik Terbesar-Terkecil Produksi Minyak Mentah Negara tahun {input_tahun}')
            st.pyplot(fig)
            
            
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

            st.markdown(f'Nama Negara = {nama_negara}')
            st.markdown(f'kode Negara = {kode_negara}')
            st.markdown(f'Region = {region}')
            st.markdown(f'Subregion = {sub_region}')
            st.markdown(f'Jumlah produksi terbesar tahun {input_tahun} = **{jumlah_terbesar}**')
            st.markdown(f'**Produksi Keseluruhan Tahun**')
            st.write(negara_tahun)

            
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

            st.markdown(f'Nama Negara = {nama_negara}')
            st.markdown(f'kode Negara = {kode_negara}')
            st.markdown(f'Region = {region}')
            st.markdown(f'Subregion = {sub_region}')
            st.markdown(f'Jumlah produksi terbesar tahun {input_tahun} = **{jumlah_terkecil}**')
            st.markdown(f'**Produksi Keseluruhan Tahun**')
            st.write(negara_tahun)


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

            st.markdown(f'Nama Negara = {nama_negara}')
            st.markdown(f'kode Negara = {kode_negara}')
            st.markdown(f'Region = {region}')
            st.markdown(f'Subregion = {sub_region}')
            st.markdown(f'Jumlah produksi terbesar tahun {input_tahun} = **{jumlah_nol}**')
            st.markdown(f'**Produksi Keseluruhan Tahun**')
            st.write(negara_tahun)
            
        
        else:
            st.error("Data Tidak Ada!")