import streamlit as st
import pandas as pd
import datetime

# --- 1. TASARIM VE CSS ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

.league-title {
    font-size: 32px; font-weight: 900; text-align: center; padding: 15px 0;
    background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* DETAYLI PUAN TABLOSU */
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; margin-top: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.custom-table th { background: #1e293b; color: white; padding: 12px; font-size: 11px; text-align: center; }
.custom-table td { padding: 12px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 700; font-size: 14px; color: #1e293b; }

/* MAÇ KARTLARI */
.stadium-card { background: white; border-radius: 15px; margin-bottom: 20px; border: 1px solid #e2e8f0; overflow: hidden; }
.digital-scoreboard {
    background: #273142; color: #00ff85; font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem; display: inline-flex; align-items: center; justify-content: center;
    height: 45px; min-width: 100px; border-radius: 10px; border: 1px solid #334155;
    margin: 0 30px; line-height: 1;
}
.team-name { font-size: 1rem; font-weight: 800; color: #1e293b; text-transform: uppercase; flex: 1; }

/* FORM NOKTALARI */
.f-dot { width: 18px; height: 18px; border-radius: 4px; display: inline-flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 900; color: white; margin-right: 3px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ YÖNETİMİ (GÜNCEL SKORLAR) ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15},
        12: {"Ev": "Prospor", "EvSkor": 20, "Dep": "Billispor", "DepSkor": 19} # Dün akşamki maç
    }

def get_live_stats():
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    for w in sorted(st.session_state.matches.keys()):
        m = st.session_state.matches[w]
        data[m["Ev"]]["O"] += 1; data[m["Dep"]]["O"] += 1
        data[m["Ev"]]["AG"] += m["EvSkor"]; data[m["Ev"]]["YG"] += m["DepSkor"]
        data[m["Dep"]]["AG"] += m["DepSkor"]; data[m["Dep"]]["YG"] += m["EvSkor"]
        res = "G" if m["EvSkor"] > m["DepSkor"] else "M" if m["EvSkor"] < m["DepSkor"] else "B"
        data[m["Ev"]]["form"].append(res); data[m["Dep"]]["form"].append("G" if res=="M" else "M" if res=="G" else "B")
        if res == "G": data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
        elif res == "M": data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
        else: data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- 3. ANA PANEL ---
st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_live_stats()
    st.markdown("### 📉 LİG SIRALAMASI")
    st.markdown(f"""
    <table class="custom-table">
        <thead>
            <tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr>
        </thead>
        <tbody>
            {"".join([f"<tr><td>{r['Takım']}</td><td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td><td>{r['AG']}</td><td>{r['YG']}</td><td>{r['Av']}</td><td style='color:#10b981; font-weight:900;'>{r['P']}</td></tr>" for _, r in df.iterrows()])}
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    for _, r in df.iterrows():
        form_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"**{r['Takım']} Son 5 Maç:** <div style='display:inline-flex;'>{form_html}</div>", unsafe_allow_html=True)

with tab2:
    stadiums = ["Filia Arena", "Velochori Arena", "Olympic Center", "City Stadium"]
    # 11. Hafta (28 Mart), 12. Hafta (9 Nisan Perşembe), 13. Hafta haftaya Pazar (19 Nisan)
    for i in range(10):
        w = 11 + i
        if w == 11: m_date = datetime.date(2026, 3, 28)
        elif w == 12: m_date = datetime.date(2026, 4, 9) # Dün akşam
        else:
            # 13. Haftadan itibaren her Pazar (19 Nisan, 26 Nisan...)
            m_date = datetime.date(2026, 4, 19) + datetime.timedelta(weeks=i-2)
            
        res = st.session_state.matches.get(w)
        stad = stadiums[w % len(stadiums)]
        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        
        st.markdown(f"""
        <div class="stadium-card">
            <div style="background:#f8fafc; padding:8px 15px; display:flex; justify-content:space-between; font-size:10px; font-weight:800; color:#64748b; border-bottom:1px solid #f1f5f9;">
                <span>{w}. HAFTA | 📍 {stad}</span>
                <span>{m_date.strftime('%d.%m.%Y')}</span>
            </div>
            <div style="padding:20px; display:flex; align-items:center; justify-content:center;">
                <div class="team-name" style="text-align:right;">{t1}</div>
                <div class="digital-scoreboard">{"VS" if not res else f'{res["EvSkor"]} - {res["DepSkor"]}'}</div>
                <div class="team-name" style="text-align:left;">{t2}</div>
            </div>
            <div style="background:#f8fafc; padding:8px; text-align:center; font-size:10px; font-weight:800; color:{'#10b981' if res else '#94a3b8'}; border-top:1px solid #f1f5f9;">
                {'● BİTTİ' if res else '🕒 18:30'}
            </div>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ YÖNETİCİ")
    with st.form("admin"):
        h_sel = st.number_input("Hafta", 11, 20, 12)
        t1_a, t2_a = ("Billispor", "Prospor") if h_sel % 2 != 0 else ("Prospor", "Billispor")
        s1 = st.number_input(f"{t1_a}", 0, 100, 0); s2 = st.number_input(f"{t2_a}", 0, 100, 0)
        if st.form_submit_button("GÜNCELLE"):
            st.session_state.matches[h_sel] = {"Ev": t1_a, "EvSkor": s1, "Dep": t2_a, "DepSkor": s2}
            st.rerun()
