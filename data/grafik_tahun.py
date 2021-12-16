import streamlit as st
import pandas as pd


def app():
    st.header("Data Minyak Mentah Negara Dunia")
    input_feature = st.text_input('Pilih Negara', '')
    minyak_data = pd.read_csv('produksi_minyak_mentah.csv')
    info_json = pd.read_json('kode_negara_lengkap.json')

    if(input_feature!=''):
        json_negara = info_json[info_json['name']== input_feature]
        
        if(json_negara.size>0):
            json_kode = json_negara['alpha-3'].values[0]
            negara_data = minyak_data[minyak_data['kode_negara'] == json_kode]

            if not (negara_data.empty):
                st.subheader(f'Grafik Jumlah Produksi Minyak Mentah Negara {input_feature}')
                chart_data = pd.DataFrame(negara_data.produksi).set_index(negara_data.tahun)
                st.bar_chart(chart_data)
            else:
                st.error('Data negara tidak ada pada csv')
        else:
            st.error('Data Tidak Ada!')
  

    

    
    