import streamlit as st
import pandas as pd
import datetime

# --- 1. SAYFA VE TASARIM (CSS) ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* LİG BAŞLIĞI */
.league-title {
    font-size: 32px; font-weight: 900; text-align: center; padding: 20px 0;
    background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* GENİŞ PUAN DURUMU TABLOSU */
.puan-tablosu { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
.puan-tablosu th { background: #1e293b; color: white; padding: 15px 10px; font-size: 13px; text-align: center; border: none; }
.puan-tablosu td { padding: 15px 10px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 700; font-size: 15px; color: #1e293b; }
.puan-tablosu tr:nth-child(even) { background-color: #f8fafc; }

/* MAÇ KARTLARI VE SKOR (DÜZELTİLMİŞ) */
.stadium-card { background: white; border-radius: 15px; margin-bottom: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.03); }
.match-header { background: #f8fafc; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; font-size: 11px; font-weight: 800; color: #64748b; }

.score-box { 
    background: #273142; color: #00ff85; font-family: 'JetBrains Mono', monospace; 
    font-size: 1.2rem; display: inline-flex; align-items: center; justify-content: center; 
    height: 48px; min-width: 110px; border-radius: 10px; margin: 0 40px; 
    line-height: 1; border: 1px solid #334155;
}

.team-label { font-size: 1.1rem; font-weight: 800; color: #1e293b; text-transform: uppercase; flex: 1; }

/* FORM NOKTALARI */
.f-dot { width: 20px; height: 20px; border-radius: 4px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 4px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ YÖNETİMİ VE MATEMATİK ---
if 'matches' not in st.session_state:
    # 11. Hafta Billispor Galibiyeti Sabitlendi
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15, "Stad": "Filia Arena"}
    }

def calculate_league():
    # 10 maçlık statik temel (Ligi başlatan veriler)
    stats = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    # Dinamik maçları işle
    for h, m in st.session_state.matches.items():
        stats[m["Ev"]]["O"] += 1; stats[m["Dep"]]["O"] += 1
        stats[m["Ev"]]["AG"] += m["EvSkor"]; stats[m["Ev"]]["YG"] += m["DepSkor"]
        stats[m["Dep"]]["AG"] += m["DepSkor"]; stats[m["Dep"]]["YG"] += m["EvSkor"]
        
        if m["EvSkor"] > m["DepSkor"]:
            stats[m["Ev"]]["P"] += 3; stats[m["Ev"]]["G"] += 1; stats[m["Dep"]]["M"] += 1
            stats[m["Ev"]]["form"].append("G"); stats[m["Dep"]]["form"].append("M")
        elif m["EvSkor"] < m["DepSkor"]:
            stats[m["Dep"]]["P"] += 3; stats[m["Dep"]]["G"] += 1; stats[m["Ev"]]["M"] += 1
            stats[m["Ev"]]["form"].append("M"); stats[m["Dep"]]["form"].append("G")
        else:
            stats[m["Ev"]]["P"] += 1; stats[m["Dep"]]["P"] += 1; stats[m["Ev"]]["B"] += 1; stats[m["Dep"]]["B"] += 1
            stats[m["Ev"]]["form"].append("B"); stats[m["Dep"]]["form"].append("B")
            
    df = pd.DataFrame.from_dict(stats, orient='index').reset_index().rename(columns={'index':'TAKIM'})
    df["AV"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "AV"], ascending=False)

# --- 3. ARAYÜZ ---
st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = calculate_league()
    # TAM PUAN TABLOSU (O G B M AG YG AV P)
    table_html = f"""
    <table class="puan-tablosu">
        <thead>
            <tr>
                <th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th>
            </tr>
        </thead>
        <tbody>
            {"".join([f"<tr><td>{r['TAKIM']}</td><td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td><td>{r['AG']}</td><td>{r['YG']}</td><td>{r['AV']}</td><td style='color:#10b981; font-weight:900;'>{r['P']}</td></tr>" for _, r in df.iterrows()])}
        </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    
    # SON 5 MAÇ (FORM)
    st.markdown("### ⚡ Son 5 Maç")
    for _, r in df.iterrows():
        dots = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"**{r['TAKIM']}:** {dots}", unsafe_allow_html=True)

with tab2:
    stadiums = ["Filia Arena", "Velochori Arena", "Olympic Center", "City Stadium"]
    # 12. Hafta ve sonrası her Pazar (29.03.2026'dan başlayarak)
    for i in range(10):
        w = 11 + i
        if w == 11:
            m_date = datetime.date(2026, 3, 28) # Bu haftanın maçı
        else:
            m_date = datetime.date(2026, 3, 29) + datetime.timedelta(weeks=i-1)
            
        res = st.session_state.matches.get(w)
        stad = stadiums[w % len(stadiums)]
        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        
        st.markdown(f"""
        <div class="stadium-card">
            <div class="match-header">
                <span>{w}. HAFTA</span>
                <span>📍 {stad}</span>
                <span>{m_date.strftime('%d.%m.%Y')}</span>
            </div>
            <div style="padding:25px; display:flex; align-items:center; justify-content:center; text-align:center;">
                <div class="team-label" style="text-align:right;">{t1}</div>
                <div class="score-box">{"VS" if not res else f'{res["EvSkor"]} - {res["DepSkor"]}'}</div>
                <div class="team-label" style="text-align:left;">{t2}</div>
            </div>
            <div style="background:#f8fafc; padding:8px; text-align:center; font-size:11px; font-weight:800; color:{'#10b981' if res else '#64748b'}; border-top:1px solid #f1f5f9;">
                {'● BİTTİ' if res else '🕒 18:30 (GELECEK MAÇ)'}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 4. YÖNETİCİ ---
with st.sidebar:
    st.markdown("### ⚙️ SKOR GİRİŞİ")
    with st.form("admin"):
        h_in = st.number_input("Hafta Seç", 11, 20, 11)
        ev_t, dep_t = ("Billispor", "Prospor") if h_in % 2 != 0 else ("Prospor", "Billispor")
        s1 = st.number_input(f"{ev_t}", 0, 100, 0)
        s2 = st.number_input(f"{dep_t}", 0, 100, 0)
        if st.form_submit_button("KAYDET"):
            st.session_state.matches[h_in] = {"Ev": ev_t, "EvSkor": s1, "Dep": dep_t, "DepSkor": s2}
            st.rerun()
