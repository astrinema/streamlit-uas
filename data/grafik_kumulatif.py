import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd


def app():
    st.header("Data Jumlah Kumulatif Mintak Bumi Terbesar")

    input_besar = st.number_input('Berapa Banyak Negara', min_value=0)

    minyak_data = pd.read_csv('produksi_minyak_mentah.csv')
    info_json = pd.read_json('kode_negara_lengkap.json')

    data_grp = minyak_data.groupby('kode_negara').sum()

    sort_data = data_grp.sort_values(['produksi'], ascending=False)
    
    if(input_besar!=0):

        output_data = pd.DataFrame(sort_data.head(input_besar))

        st.subheader(f'Grafik {input_besar} Terbesar Total Produksi Minyak Mentah Negara')
        fig = plt.figure(figsize = (16, 8))
    
        plt.title('Kumulatif')
        plt.plot(output_data['produksi'])
        plt.xlabel('Kode Negara', fontsize=18)
        plt.ylabel('Produksi', fontsize =18)
        st.pyplot(fig)

        st.session_state['type'] = st.radio('Apakah Menunjukkan Keterangan?',['Tidak', 'Iya'])
        
        df = pd.DataFrame()
        output_data = output_data.reset_index()

        if st.session_state['type']=='Iya':
            for x in range(input_besar):
                get_kode = output_data['kode_negara'].iloc[x]
                json_kode = info_json[info_json['alpha-3']== get_kode]
                
                if(json_kode.size>0):
                    json_negara = json_kode['name'].iloc[0]
                else:
                    json_negara = "Tidak ada dalam json"
                
                
                
                row_baru = {'Kode Negara': output_data['kode_negara'].iloc[x], 'Nama Negara':json_negara, 'Total Produksi':output_data['produksi'].iloc[x]}
                df = df.append(row_baru, ignore_index=True)
            

            st.subheader(f'{input_besar} Negara Jumlah Produksi Minyak Mentah Terbesar')
            df.index = np.arange(1, len(df)+1)
            st.table(df)
        
        

        

    


 

  