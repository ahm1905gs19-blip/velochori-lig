import streamlit as st
import pandas as pd
import datetime

# --- 1. SADE, NET VE PROFESYONEL BEYAZ TASARIM ---
st.set_page_config(page_title="Velochori Ligi", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');

/* Arka planı tamamen beyaz ve ferah yapıyoruz */
.stApp { background-color: #ffffff; font-family: 'Roboto', sans-serif; }

/* Başlık alanı */
.main-title {
    font-size: 40px; font-weight: 900; color: #1a202c;
    text-align: center; padding: 20px 0; border-bottom: 4px solid #f1f5f9;
    margin-bottom: 30px; text-transform: uppercase;
}

/* PUAN DURUMU TABLOSU - Klasik ve Net */
.stats-container { margin-bottom: 50px; }
.league-table {
    width: 100%; border-collapse: collapse; font-size: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;
}
.league-table th {
    background-color: #1a202c; color: #ffffff; padding: 15px;
    text-align: center; font-weight: 700; text-transform: uppercase;
}
.league-table td {
    padding: 15px; text-align: center; border-bottom: 1px solid #edf2f7;
    font-weight: 700; color: #2d3748;
}
.league-table tr:nth-child(even) { background-color: #f8fafc; }
.team-name-cell { text-align: left !important; padding-left: 30px !important; font-size: 18px; color: #1a202c !important; }

/* PUAN SÜTUNU VURGUSU */
.p-bold { color: #2f855a !important; font-size: 20px !important; background-color: #f0fff4; }

/* FİKSTÜR LİSTESİ */
.fixture-section { background: #f1f5f9; padding: 30px; border-radius: 20px; }
.match-row {
    background: white; padding: 20px; border-radius: 12px;
    margin-bottom: 10px; display: flex; align-items: center;
    border: 1px solid #e2e8f0;
}
.match-date { font-weight: 800; color: #718096; width: 120px; font-size: 14px; }
.match-teams { flex: 1; display: flex; justify-content: center; align-items: center; gap: 20px; }
.team-label { font-size: 18px; font-weight: 800; width: 150px; }
.score-badge {
    background: #2d3748; color: #ffffff; padding: 10px 20px;
    border-radius: 8px; font-family: monospace; font-size: 22px; min-width: 100px; text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ MERKEZİ ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15, "Stad": "Filia Arena", "Tarih": "28.03.2026"},
        12: {"Ev": "Prospor", "EvSkor": 20, "Dep": "Billispor", "DepSkor": 19, "Stad": "Velochori Arena", "Tarih": "09.04.2026"}
    }

def calculate_league():
    base = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12}
    }
    for h, m in st.session_state.matches.items():
        base[m["Ev"]]["O"] += 1; base[m["Dep"]]["O"] += 1
        base[m["Ev"]]["AG"] += m["EvSkor"]; base[m["Ev"]]["YG"] += m["DepSkor"]
        base[m["Dep"]]["AG"] += m["DepSkor"]; base[m["Dep"]]["YG"] += m["EvSkor"]
        if m["EvSkor"] > m["DepSkor"]:
            base[m["Ev"]]["P"] += 3; base[m["Ev"]]["G"] += 1; base[m["Dep"]]["M"] += 1
        elif m["EvSkor"] < m["DepSkor"]:
            base[m["Dep"]]["P"] += 3; base[m["Dep"]]["G"] += 1; base[m["Ev"]]["M"] += 1
        else:
            base[m["Ev"]]["P"] += 1; base[m["Dep"]]["P"] += 1; base[m["Ev"]]["B"] += 1; base[m["Dep"]]["B"] += 1
    
    df = pd.DataFrame.from_dict(base, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["AV"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "AV"], ascending=False)

# --- 3. EKRAN ÇIKTISI ---
st.markdown('<div class="main-title">Velochori Super League</div>', unsafe_allow_html=True)

# PUAN DURUMU (EN ÜSTTE VE GENİŞ)
df = calculate_league()
rows = ""
for idx, r in df.reset_index(drop=True).iterrows():
    rows += f"""
    <tr>
        <td class="team-name-cell">{idx+1}. {r['Takım']}</td>
        <td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td>
        <td>{r['AG']}</td><td>{r['YG']}</td><td>{r['AV']}</td>
        <td class="p-bold">{r['P']}</td>
    </tr>
    """

st.markdown(f"""
<div class="stats-container">
    <h3 style="color:#1a202c; border-left: 5px solid #1a202c; padding-left: 15px;">📊 PUAN DURUMU</h3>
    <table class="league-table">
        <thead>
            <tr>
                <th style="text-align:left; padding-left:30px;">TAKIMLAR</th>
                <th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
</div>
""", unsafe_allow_html=True)

# FİKSTÜR (ALTTA LİSTE HALİNDE)
st.markdown('<h3 style="color:#1a202c; border-left: 5px solid #1a202c; padding-left: 15px;">🗓️ FİKSTÜR VE SONUÇLAR</h3>', unsafe_allow_html=True)
st.markdown('<div class="fixture-section">', unsafe_allow_html=True)

# Geçmiş Maçlar
for h in sorted(st.session_state.matches.keys(), reverse=True):
    m = st.session_state.matches[h]
    st.markdown(f"""
    <div class="match-row">
        <div class="match-date">{m['Tarih']}<br><small style="color:#10b981">BİTTİ</small></div>
        <div class="match-teams">
            <div class="team-label" style="text-align:right;">{m['Ev']}</div>
            <div class="score-badge">{m['EvSkor']} - {m['DepSkor']}</div>
            <div class="team-label" style="text-align:left;">{m['Dep']}</div>
        </div>
        <div style="font-size:12px; color:#a0aec0; width:150px; text-align:right;">📍 {m['Stad']}</div>
    </div>
    """, unsafe_allow_html=True)

# Gelecek Maç (Örnek 13. Hafta)
st.markdown(f"""
<div class="match-row" style="border: 2px dashed #cbd5e0; background: #f8fafc;">
    <div class="match-date">19.04.2026<br><small style="color:#3182ce">GELECEK</small></div>
    <div class="match-teams">
        <div class="team-label" style="text-align:right;">Billispor</div>
        <div class="score-badge" style="background:#edf2f7; color:#a0aec0;">VS</div>
        <div class="team-label" style="text-align:left;">Prospor</div>
    </div>
    <div style="font-size:12px; color:#a0aec0; width:150px; text-align:right;">📍 Olympic Center</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# YÖNETİM PANELİ (SAYFA SONUNDA)
with st.expander("🛠️ Veri Girişi / Skor Kaydet"):
    h_sel = st.number_input("Hafta", 11, 20, 13)
    ev_t, dep_t = ("Billispor", "Prospor") if h_sel % 2 != 0 else ("Prospor", "Billispor")
    s1 = st.number_input(f"{ev_t}", 0, 100, 0)
    s2 = st.number_input(f"{dep_t}", 0, 100, 0)
    tarih = st.text_input("Tarih (GG.AA.YYYY)", "19.04.2026")
    if st.button("KAYDET"):
        st.session_state.matches[h_sel] = {"Ev": ev_t, "EvSkor": s1, "Dep": dep_t, "DepSkor": s2, "Stad": "City Stadium", "Tarih": tarih}
        st.rerun()
