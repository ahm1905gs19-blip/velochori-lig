import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Velochori Lig", layout="centered")

# CSS: Daha Açık ve Modern Tasarım
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    h1, h2, h3 { color: #1e293b; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 20px; border: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Velochori Süper Lig")

# Logoları Görüntüleme
col1, col2 = st.columns(2)
# Dosyaların GitHub'da doğru isimle (billispor.jpg, prospor.jpg) yüklü olduğundan emin ol
if os.path.exists("billispor.jpg"):
    col1.image("billispor.jpg", caption="Billispor", width=120)
if os.path.exists("prospor.jpg"):
    col2.image("prospor.jpg", caption="Prospor", width=120)

# Puan Durumu (Örnek)
st.subheader("📊 Puan Durumu")
data = {
    "Takım": ["Billispor", "Prospor"],
    "O": [10, 10], "G": [6, 4], "B": [0, 0], "M": [4, 6], "P": [18, 12]
}
df = pd.DataFrame(data)
st.table(df)

# Fikstür
st.subheader("🗓️ Gelecek Maçlar")
with st.container():
    st.markdown('<div class="card">11. Hafta: Billispor vs Prospor - 22.03.2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">12. Hafta: Prospor vs Billispor - 29.03.2026</div>', unsafe_allow_html=True)
