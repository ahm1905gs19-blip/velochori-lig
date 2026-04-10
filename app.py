import streamlit as st
import pandas as pd
import datetime

# --- 1. SAYFA AYARLARI VE GELİŞMİŞ CSS ---
st.set_page_config(page_title="Velochori Super League", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@700&display=swap');
.stApp { background: #f1f5f9; font-family: 'Inter', sans-serif; }

.league-title {
    font-size: 34px; font-weight: 900; text-align: center; padding: 20px 0;
    color: #1e293b; letter-spacing: -1px;
}

/* PUAN TABLOSU MODERNİZASYONU */
.puan-card { background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #e2e8f0; }
.custom-table { width: 100%; border-collapse: collapse; margin: 0; }
.custom-table th { background: #1e293b; color: #ffffff; padding: 14px; font-size: 12px; text-transform: uppercase; text-align: center; }
.custom-table td { padding: 15px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 700; color: #334155; font-size: 15px; }
.custom-table tr:hover { background-color: #f8fafc; }

/* PUAN SÜTUNU VURGUSU */
.puan-col { background: #f0fdf4; color: #10b981 !important; font-size: 18px !important; }

/* MAÇ KARTLARI */
.stadium-card { background: white; border-radius: 12px; margin-bottom: 15px; border: 1px solid #e2e8f0; }
.digital-scoreboard {
    background: #1e293b; color: #00ff85; font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem; display: inline-flex; align-items: center; justify-content: center;
    height: 45px; min-width: 105px; border-radius: 8px; margin: 0 25px;
}

/* FORM SEMBOLLERİ */
.f-dot { width: 20px; height: 20px; border-radius: 4px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 4px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# --- 2. SABİT VERİLER (11. VE 12. HAFTA İŞLENDİ) ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15},
        12: {"Ev": "Prospor", "EvSkor": 20, "Dep": "Billispor", "DepSkor": 19}
    }

def calculate_stats():
    # İlk 10 maçlık lig başlangıç verisi
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    # Oynanan haftaları ekle
    for w in sorted(st.session_state.matches.keys()):
        m = st.session_state.matches[w]
        data[m["Ev"]]["O"] += 1; data[m["Dep"]]["O"] += 1
        data[m["Ev"]]["AG"] += m["EvSkor"]; data[m["Ev"]]["YG"] += m["DepSkor"]
        data[m["Dep"]]["AG"] += m["DepSkor"]; data[m["Dep"]]["YG"] += m["EvSkor"]
        
        if m["EvSkor"] > m["DepSkor"]:
            data[m["Ev"]]["P"] += 3; data[m["Ev"]]["G"] += 1; data[m["Dep"]]["M"] += 1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        elif m["EvSkor"] < m["DepSkor"]:
            data[m["Dep"]]["P"] += 3; data[m["Dep"]]["G"] += 1; data[m["Ev"]]["M"] += 1
            data[m["Ev"]]["form"].append("M"); data[m["Dep"]]["form"].append("G")
        else:
            data[m["Ev"]]["P"] += 1; data[m["Dep"]]["P"] += 1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["AV"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "AV"], ascending=False)

# --- 3. ANA EKRAN ---
st.markdown('<div class="league-title">⚽ VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = calculate_stats()
    st.markdown('<div class="puan-card">', unsafe_allow_html=True)
    
    # SENİN İSTEDİĞİN O MEŞHUR TABLO (O G B M AG YG AV P)
    html_table = f"""
    <table class="custom-table">
        <thead>
            <tr>
                <th style="text-align:left; padding-left:20px;">TAKIM</th>
                <th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th>
            </tr>
        </thead>
        <tbody>
            {"".join([f"<tr><td style='text-align:left; padding-left:20px;'>{r['Takım'].upper()}</td><td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td><td>{r['AG']}</td><td>{r['YG']}</td><td>{r['AV']}</td><td class='puan-col'>{r['P']}</td></tr>" for _, r in df.iterrows()])}
        </tbody>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FORM DURUMU
    st.markdown("<br>", unsafe_allow_html=True)
    for _, r in df.iterrows():
        dots = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"**{r['Takım']} Form:** {dots}", unsafe_allow_html=True)

with tab2:
    stadiums = ["Filia Arena", "Velochori Arena", "Olympic Center", "City Stadium"]
    # 12. Hafta Dün (9 Nisan), 13. Hafta haftaya Pazar (19 Nisan)
    for i in range(10):
        w = 11 + i
        if w == 11: m_date = datetime.date(2026, 3, 28)
        elif w == 12: m_date = datetime.date(2026, 4, 9) # Dün akşamki galibiyet
        else: m_date = datetime.date(2026, 4, 19) + datetime.timedelta(weeks=i-2)
            
        res = st.session_state.matches.get(w)
        stad = stadiums[w % len(stadiums)]
        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        
        st.markdown(f"""
        <div class="stadium-card">
            <div style="background:#f8fafc; padding:10px 15px; display:flex; justify-content:space-between; font-size:12px; font-weight:800; color:#64748b; border-bottom:1px solid #e2e8f0;">
                <span>{w}. HAFTA | 📍 {stad}</span>
                <span>{m_date.strftime('%d.%m.%Y')}</span>
            </div>
            <div style="padding:20px; display:flex; align-items:center; justify-content:center;">
                <div style="flex:1; text-align:right; font-weight:800; color:#1e293b;">{t1}</div>
                <div class="digital-scoreboard">{"VS" if not res else f'{res["EvSkor"]} - {res["DepSkor"]}'}</div>
                <div style="flex:1; text-align:left; font-weight:800; color:#1e293b;">{t2}</div>
            </div>
            <div style="background:#f8fafc; padding:8px; text-align:center; font-size:11px; font-weight:800; color:{'#10b981' if res else '#94a3b8'}; border-top:1px solid #e2e8f0;">
                {'● BİTTİ' if res else '🕒 18:30'}
            </div>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ SKOR YÖNETİMİ")
    h_sel = st.number_input("Hafta Seç", 11, 20, 13)
    ev_t, dep_t = ("Billispor", "Prospor") if h_sel % 2 != 0 else ("Prospor", "Billispor")
    s1 = st.number_input(f"{ev_t}", 0, 100, 0)
    s2 = st.number_input(f"{dep_t}", 0, 100, 0)
    if st.button("KAYDET VE GÜNCELLE"):
        st.session_state.matches[h_sel] = {"Ev": ev_t, "EvSkor": s1, "Dep": dep_t, "DepSkor": s2}
        st.rerun()
