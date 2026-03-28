import streamlit as st
import pandas as pd
import datetime

# --- 1. SAYFA VE TASARIM AYARLARI ---
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

/* DETAYLI TABLO TASARIMI (O G B M...) */
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; margin-bottom: 20px; }
.custom-table th { background: #1e293b; color: white; padding: 12px; font-size: 12px; text-align: center; }
.custom-table td { padding: 12px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 700; font-size: 14px; color: #1e293b; }
.custom-table tr:hover { background-color: #f8fafc; }

/* KARTLAR VE DİĞERLERİ */
.team-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 10px 15px; border-radius: 12px; margin-bottom: 8px; border: 1px solid #e2e8f0; }
.f-dot { width: 18px; height: 18px; border-radius: 4px; display: inline-flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 900; color: white; margin-right: 3px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }
.digital-scoreboard { background: #273142; color: #00ff85; font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; display: inline-flex; align-items: center; justify-content: center; height: 42px; min-width: 95px; border-radius: 10px; margin: 0 40px; line-height: 1; }
.stadium-card { background: white; border-radius: 15px; margin-bottom: 20px; border: 1px solid #e2e8f0; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ YÖNETİMİ ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15, "Stad": "Filia Arena"}
    }

def get_stats():
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

# --- 3. GÖRÜNÜM (SEKMELER) ---
st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    stats_df = get_stats()
    
    # 1. DETAYLI TABLO (O G B M AG YG AV P)
    st.markdown("### 📉 Detaylı İstatistikler")
    table_html = f"""
    <table class="custom-table">
        <thead>
            <tr>
                <th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th>
            </tr>
        </thead>
        <tbody>
            {"".join([f"<tr><td>{r['Takım']}</td><td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td><td>{r['AG']}</td><td>{r['YG']}</td><td>{r['Av']}</td><td style='color:#10b981; font-weight:900;'>{r['P']}</td></tr>" for _, r in stats_df.iterrows()])}
        </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    # 2. KOMPAKT KARTLAR (FORM DURUMU)
    st.markdown("### ⚡ Form Durumu")
    for idx, r in stats_df.reset_index(drop=True).iterrows():
        form_dots = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card">
            <div style="flex:1;"><div style="font-weight:800; font-size:1rem;">{r['Takım'].upper()}</div><div>{form_dots}</div></div>
            <div style="font-size:24px; font-weight:900; color:#10b981;">{r['P']}</div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    stadiums = ["Filia Arena", "Velochori Arena", "Olympic Center", "City Stadium"]
    for i in range(10):
        w = 11 + i
        m_date = datetime.date(2026, 3, 28) if w == 11 else datetime.date(2026, 3, 29) + datetime.timedelta(weeks=i-1)
        res = st.session_state.matches.get(w)
        stad = stadiums[w % len(stadiums)]
        
        if res:
            status = '● BİTTİ'; score_text = f'{res["EvSkor"]} - {res["DepSkor"]}'
        else:
            status = '🕒 18:30'; score_text = 'VS'

        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        st.markdown(f"""
        <div class="stadium-card">
            <div style="background:#f8fafc; padding:8px 15px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; font-size:11px; font-weight:800; color:#64748b;">
                <span>{w}. HAFTA</span><span>📍 {stad}</span><span>{m_date.strftime('%d.%m.%Y')}</span>
            </div>
            <div style="padding:25px; display:flex; align-items:center; justify-content:center;">
                <div style="flex:1; text-align:right; font-weight:800;">{t1}</div>
                <div class="digital-scoreboard">{score_text}</div>
                <div style="flex:1; text-align:left; font-weight:800;">{t2}</div>
            </div>
            <div style="background:#f8fafc; padding:8px; text-align:center; font-size:11px; font-weight:800; color:#64748b;">{status}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.write("### ⚙️ YÖNETİCİ")
    with st.form("admin"):
        h_sel = st.number_input("Hafta", 11, 20, 11)
        t1_a, t2_a = ("Billispor", "Prospor") if h_sel % 2 != 0 else ("Prospor", "Billispor")
        s1 = st.number_input(f"{t1_a}", 0, 100, 0); s2 = st.number_input(f"{t2_a}", 0, 100, 0)
        if st.form_submit_button("KAYDET"):
            st.session_state.matches[h_sel] = {"Ev": t1_a, "EvSkor": s1, "Dep": t2_a, "DepSkor": s2}
            st.rerun()
