import streamlit as st
import pandas as pd

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Super League", page_icon="⚽", layout="wide")

# --- CSS: SOFASCORE STYLE & PITCH ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
.stApp { background: #f8fafc; font-family: 'Inter', sans-serif; }

/* BAŞLIK */
.league-title {
    font-size: clamp(24px, 7vw, 36px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* PUAN DURUMU KARTLARI (BOZULMADI) */
.team-card { 
    display: flex; justify-content: space-between; align-items: center; 
    background: white; padding: 12px 20px; border-radius: 15px; 
    margin-bottom: 10px; border: 1px solid #e2e8f0;
}
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }
.f-dot { width: 18px; height: 18px; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 4px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* SOFASCORE STYLE FİKSTÜR */
.sofa-fixture-card {
    background: white; border-radius: 16px; border: 1px solid #e2e8f0;
    margin-bottom: 15px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}
.fixture-header {
    background: #f1f5f9; padding: 8px 15px; border-bottom: 1px solid #e2e8f0;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase;
}
.fixture-body {
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 10px; text-align: center;
}
.team-info { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; }
.team-logo-placeholder {
    width: 45px; height: 45px; background: #f8fafc; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 18px; color: #1e293b; border: 1px solid #e2e8f0;
}
.score-area {
    flex: 0.5; display: flex; flex-direction: column; align-items: center; gap: 4px;
}
.big-score { font-size: 32px; font-weight: 900; color: #1e293b; letter-spacing: -1px; }
.match-status { font-size: 10px; font-weight: 800; color: #10b981; background: #ecfdf5; padding: 2px 8px; border-radius: 4px; }

/* SAHA TASARIMI */
.pitch-container {
    background: #1a3a16; padding: 20px; border-radius: 12px; margin: 10px;
    background-image: repeating-linear-gradient(90deg, transparent, transparent 40px, rgba(255,255,255,0.03) 40px, rgba(255,255,255,0.03) 80px);
    border: 2px solid #2d5a27; position: relative;
}
.line-up-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; position: relative; }
.player-node {
    width: 30px; height: 30px; background: white; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 900; color: #1e293b; border: 2px solid #fbbf24;
    margin: 5px auto; box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* TABLO */
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; }
.custom-table th { background: #1e293b; color: white; padding: 10px; font-size: 11px; }
.custom-table td { padding: 10px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# --- VERİ & HESAPLAMA (DOKUNULMADI) ---
if 'matches' not in st.session_state: st.session_state.matches = {}

def get_stats():
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    for w, m in st.session_state.matches.items():
        data[m["Ev"]]["O"]+=1; data[m["Dep"]]["O"]+=1
        data[m["Ev"]]["AG"]+=m["EvS"]; data[m["Ev"]]["YG"]+=m["DepS"]
        data[m["Dep"]]["AG"]+=m["DepS"]; data[m["Dep"]]["YG"]+=m["EvS"]
        res = "G" if m["EvS"] > m["DepS"] else "M" if m["EvS"] < m["DepS"] else "B"
        data[m["Ev"]]["form"].append(res)
        data[m["Dep"]]["form"].append("G" if res=="M" else "M" if res=="G" else "B")
        if res=="G": data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
        elif res=="M": data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
        else: data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- TABS ---
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = (idx == 0)
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_l else ''}">
            <div style="flex:1;">
                <div style="font-size:10px; font-weight:900; color:#94a3b8;">{ "🥇 LİDER" if is_l else f"SIRA {idx+1}"}</div>
                <div style="font-size:18px; font-weight:900; color:#1e293b;">{r['Takım'].upper()}</div>
                <div style="display:flex;">{f_html}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:28px; font-weight:900; color:#10b981; line-height:1;">{r['P']}<small style="font-size:11px; color:#94a3b8; margin-left:3px;">P</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h5 style='font-size:14px; margin-top:15px;'>İSTATİSTİK DETAYI</h5>", unsafe_allow_html=True)
    t_html = f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{r['Takım']}</td><td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td><td>{r['AG']}</td><td>{r['YG']}</td><td>{r['Av']}</td><td style='color:#10b981; font-weight:900;'>{r['P']}</td></tr>" for _, r in df.iterrows()])}</tbody></table>"""
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    for i in range(2):
        week = 11 + i
        ev, dep = ("Billispor", "Prospor") if week % 2 != 0 else ("Prospor", "Billispor")
        res = st.session_state.matches.get(week)
        score_display = f"{res['EvS']} - {res['DepS']}" if res else "VS"
        status = "BİTTİ" if res else "21:00"

        st.markdown(f"""
        <div class="sofa-fixture-card">
            <div class="fixture-header">
                <span>📍 Filia Arena</span>
                <span>{week}. HAFTA • BUGÜN</span>
            </div>
            <div class="fixture-body">
                <div class="team-info">
                    <div class="team-logo-placeholder">{ev[0]}</div>
                    <div style="font-weight:900; font-size:14px; color:#1e293b;">{ev.upper()}</div>
                </div>
                <div class="score-area">
                    <div class="match-status">{status}</div>
                    <div class="big-score">{score_display}</div>
                </div>
                <div class="team-info">
                    <div class="team-logo-placeholder">{dep[0]}</div>
                    <div style="font-weight:900; font-size:14px; color:#1e293b;">{dep.upper()}</div>
                </div>
            </div>
            <div class="pitch-container">
                <div style="text-align:center; color:rgba(255,255,255,0.5); font-size:9px; font-weight:800; margin-bottom:10px; letter-spacing:1px;">MUHTEMEL KADROLAR</div>
                <div class="line-up-grid">
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">
                        <div class="player-node">?</div><div class="player-node">?</div>
                        <div class="player-node">?</div><div class="player-node">?</div>
                        <div class="player-node">?</div><div class="player-node">?</div>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">
                        <div class="player-node">?</div><div class="player-node">?</div>
                        <div class="player-node">?</div><div class="player-node">?</div>
                        <div class="player-node">?</div><div class="player-node">?</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- ADMIN PANEL ---
with st.sidebar:
    st.header("⚙️ ADMİN")
    with st.form("sc_form"):
        h = st.number_input("Hafta", 11, 20)
        s1 = st.number_input("Ev", 0); s2 = st.number_input("Dep", 0)
        if st.form_submit_button("KAYDET"):
            st.session_state.matches[h] = {"Ev": "Billispor" if h%2!=0 else "Prospor", "Dep": "Prospor" if h%2!=0 else "Billispor", "EvS": s1, "DepS": s2}
            st.rerun()
