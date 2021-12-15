import matplotlib.pyplot as plt
import streamlit as st
from multiapp import MultiApp
from data import grafik_tahun, grafik_terbesar, grafik_kumulatif, informasi_negara


app = MultiApp()

app.add_app("Grafik Tahun", grafik_tahun.app)
app.add_app("Produksi Terbesar", grafik_terbesar.app)
app.add_app("Produksi Kumulatif", grafik_kumulatif.app)
app.add_app("Informasi Produksi Negara", informasi_negara.app)

app.run()
