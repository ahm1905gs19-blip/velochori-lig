import streamlit as st
import pandas as pd

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Super League", page_icon="⚽", layout="wide")

# --- CSS: DENGELİ VE MODERN TASARIM ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
.stApp { background: #f8fafc; font-family: 'Inter', sans-serif; }

/* BAŞLIK: ORTA BOY VE PARLAK */
.league-title {
    font-size: clamp(24px, 6vw, 36px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* DENGELİ TAKIM KARTLARI */
.team-card { 
    display: flex; justify-content: space-between; align-items: center; 
    background: white; padding: 12px 20px; border-radius: 12px; 
    margin-bottom: 8px; border: 1px solid #e2e8f0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.leader-card { border-left: 5px solid #fbbf24; background: #fffdf5; }
.f-dot { width: 20px; height: 20px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 800; color: white; margin-right: 4px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* MAÇ MERKEZİ: SOFASCORE ESTETİĞİ */
.match-box { 
    background: white; border-radius: 16px; padding: 15px; 
    border: 1px solid #e2e8f0; text-align: center;
}
.score-pill { 
    background: #1e293b; color: #34d399; font-size: 22px; font-weight: 900;
    padding: 4px 15px; border-radius: 8px; margin: 0 10px;
}
.pitch-bg {
    background: #2d5a27; border-radius: 12px; padding: 15px; 
    margin-top: 10px; border: 1px solid rgba(255,255,255,0.2);
    background-image: radial-gradient(rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 20px 20px;
}
.player-q {
    width: 28px; height: 28px; background: white; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 14px; color: #1e293b; border: 1.5px solid #fbbf24;
}

/* DETAYLI TABLO: SIKI VE OKUNAKLI */
.custom-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.custom-table th { background: #f1f5f9; color: #475569; padding: 10px; text-align: center; border-bottom: 2px solid #e2e8f0; }
.custom-table td { padding: 10px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA ---
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

# --- TABLAR ---
tab1, tab2, tab3 = st.tabs(["📊 TABLO", "🗓️ FİKSTÜR", "🏆 ZİRVE"])

with tab1:
    df = get_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = (idx == 0)
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_l else ''}">
            <div style="flex:1;">
                <div style="font-size:16px; font-weight:800; color:#1e293b;">{r['Takım']}</div>
                <div style="display:flex; margin-top:4px;">{f_html}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:24px; font-weight:900; color:#10b981;">{r['P']} <span style="font-size:12px; color:#94a3b8;">PKT</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    t_html = f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{r['Takım']}</td><td>{r['O']}</td><td>{r['Av']}</td><td style='color:#10b981;'>{r['P']}</td></tr>" for _, r in df.iterrows()])}</tbody></table>"""
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    for i in range(5):
        w = 11 + i
        ev, dep = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        res = st.session_state.matches.get(w)
        score = f"{res['EvS']} - {res['DepS']}" if res else "VS"
        
        with st.expander(f"📍 {w}. HAFTA | {ev} - {dep}", expanded=(i==0)):
            st.markdown(f"""
            <div class="match-box">
                <div style="font-size:11px; font-weight:700; color:#94a3b8; margin-bottom:8px;">FILIA ARENA</div>
                <div style="display:flex; justify-content:center; align-items:center;">
                    <span style="font-weight:800; flex:1;">{ev}</span>
                    <span class="score-pill">{score}</span>
                    <span style="font-weight:800; flex:1;">{dep}</span>
                </div>
                <div class="pitch-bg">
                    <div style="display:flex; justify-content:space-around;">
                        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:8px;">
                            <div class="player-q">?</div><div class="player-q">?</div><div class="player-q">?</div>
                            <div class="player-q">?</div><div class="player-q">?</div><div class="player-q">?</div>
                        </div>
                        <div style="border-left:1px dashed rgba(255,255,255,0.2);"></div>
                        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:8px;">
                            <div class="player-q">?</div><div class="player-q">?</div><div class="player-q">?</div>
                            <div class="player-q">?</div><div class="player-q">?</div><div class="player-q">?</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    lider = get_stats().iloc[0]
    st.markdown(f"""
    <div style="background:#0f172a; padding:30px; border-radius:20px; text-align:center; border:2px solid #fbbf24;">
        <h2 style="color:white; margin:0;">🏆 {lider['Takım']}</h2>
        <p style="color:#fbbf24; font-size:12px; font-weight:800; margin-top:5px;">LİDERLİK TABLOSU</p>
        <div style="display:flex; justify-content:center; gap:15px; margin-top:20px;">
            <div style="background:rgba(255,255,255,0.1); padding:10px; border-radius:10px; min-width:80px;">
                <div style="font-size:20px; font-weight:900; color:white;">{lider['P']}</div>
                <div style="font-size:10px; color:#94a3b8;">PUAN</div>
            </div>
            <div style="background:rgba(255,255,255,0.1); padding:10px; border-radius:10px; min-width:80px;">
                <div style="font-size:20px; font-weight:900; color:white;">{lider['Av']}</div>
                <div style="font-size:10px; color:#94a3b8;">AVERAJ</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ADMIN ---
with st.sidebar:
    st.header("⚙️ PANEL")
    with st.form("score_form"):
        h = st.number_input("Hafta", 11, 20)
        s1 = st.number_input("Ev", 0); s2 = st.number_input("Dep", 0)
        if st.form_submit_button("KAYDET"):
            st.session_state.matches[h] = {"Ev": "Prospor" if h%2==0 else "Billispor", "Dep": "Billispor" if h%2==0 else "Prospor", "EvS": s1, "DepS": s2}
            st.rerun()
