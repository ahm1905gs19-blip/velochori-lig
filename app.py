import streamlit as st
import pandas as pd

# --- 1. AYARLAR VE KIRILMAZ CSS ---
st.set_page_config(page_title="Velochori Pro", page_icon="⚽", layout="wide")

# CSS'i tek parça ve en basit haliyle gömüyoruz
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    .main-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }

    .league-title {
        font-size: 32px; font-weight: 900; color: #1e293b;
        text-align: center; margin-bottom: 30px; letter-spacing: -1px;
    }

    /* TABLO TASARIMI */
    .puan-tablosu {
        width: 100%; border-collapse: collapse; margin-top: 10px;
    }
    .puan-tablosu th {
        background: #1e293b; color: white; padding: 12px;
        font-size: 12px; text-transform: uppercase; text-align: center;
    }
    .puan-tablosu td {
        padding: 15px 10px; text-align: center; border-bottom: 1px solid #f1f5f9;
        font-weight: 700; color: #334155;
    }
    .team-name { text-align: left !important; padding-left: 20px !important; color: #1e293b; }
    .points { color: #10b981; font-size: 18px; }
    
    /* FORM IŞIKLARI */
    .form-box { display: flex; justify-content: center; gap: 4px; }
    .dot { width: 10px; height: 10px; border-radius: 3px; }
    .G { background: #10b981; } .M { background: #ef4444; } .B { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ HESAPLAMA ---
# Manuel olarak 12. haftayı (Prospor 20-19) ekledik
data = {
    "Billispor": {"O": 12, "G": 7, "B": 0, "M": 5, "AG": 185, "YG": 189, "P": 21, "form": ["G","G","M","G","M"]},
    "Prospor": {"O": 12, "G": 5, "B": 0, "M": 7, "AG": 189, "YG": 185, "P": 15, "form": ["M","M","G","M","G"]}
}

df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
df["AV"] = df["AG"] - df["YG"]
df = df.sort_values(["P", "AV"], ascending=False)

# --- 3. GÖRÜNÜM ---
st.markdown('<div class="league-title">VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# PUAN DURUMU KARTI
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Genel Sıralama")
    
    # HTML Tabloyu tek bir f-string içinde, hata riskini sıfırlayarak oluşturuyoruz
    table_html = """
    <table class="puan-tablosu">
        <thead>
            <tr>
                <th style="text-align:left; padding-left:20px;">TAKIM</th>
                <th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>PUAN</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for _, r in df.iterrows():
        table_html += f"""
            <tr>
                <td class="team-name">{r['Takım']}</td>
                <td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td>
                <td>{r['AG']}</td><td>{r['YG']}</td><td>{r['AV']}</td>
                <td class="points">{r['P']}</td>
            </tr>
        """
    
    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

# ALT KISIM: FORM VE GELECEK MAÇ
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Son Form")
    for _, r in df.iterrows():
        dots = "".join([f'<span class="dot {f}" style="display:inline-block; width:12px; height:12px; margin-right:5px; border-radius:3px;"></span>' for f in r["form"]])
        st.markdown(f"**{r['Takım']}:** {dots}", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 🗓️ Sıradaki Maç")
    st.write("**13. Hafta | 19 Nisan Pazar**")
    st.info("Billispor vs Prospor - 18:30")
    st.markdown('</div>', unsafe_allow_html=True)
