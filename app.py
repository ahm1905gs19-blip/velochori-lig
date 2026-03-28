import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- CSS: TÜM TASARIM SİSTEMİ ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* TABLO KARTLARI */
.team-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 20px; border-radius: 15px; margin-bottom: 10px; border: 1px solid #e2e8f0; }
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }
.f-dot { width: 22px; height: 22px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 900; color: white; margin-right: 4px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* MAÇ KARTI VE SAHA */
.match-card-premium { background: white; border-radius: 20px; padding: 20px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.scoreboard-flex { display: flex; justify-content: space-around; align-items: center; margin-bottom: 15px; }
.score-box { font-size: 28px; font-weight: 900; color: #1e293b; background: #f1f5f9; padding: 8px 20px; border-radius: 12px; }
.venue-tag { background: #0f172a; color: #34d399; padding: 5px 15px; border-radius: 100px; font-size: 12px; font-weight: 800; margin-bottom: 15px; display: inline-block; }

.pitch-area { 
    background: #2d5a27; border-radius: 15px; padding: 20px; border: 2px solid rgba(255,255,255,0.2);
    background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 40px 40px; position: relative;
}
.formation-container { display: flex; justify-content: space-between; position: relative; }
.player-slot { 
    width: 35px; height: 35px; background: white; color: #1e293b; border-radius: 50%; 
    display: flex; align-items: center; justify-content: center; font-weight: 900; 
    font-size: 16px; border: 2px solid #fbbf24; margin: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* TABLO */
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; }
.custom-table th { background: #1e293b; color: white; padding: 12px; font-size: 12px; }
.custom-table td { padding: 12px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; color:#1e293b; font-weight:900;">⚽ VELOCHORI ULTIMATE</h1>', unsafe_allow_html=True)

# --- VERİ VE SESSION STATE ---
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
t1, t2, t3 = st.tabs(["📊 LİG TABLOSU", "🗓️ MAÇ MERKEZİ", "🏆 ŞAMPİYONLUK"])

with t1:
    df = get_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = (idx == 0)
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_l else ''}">
            <div style="flex:1;">
                <span style="font-size:10px; font-weight:900; color:#64748b;">#{idx+1}</span>
                <h3 style="margin:2px 0; color:#1e293b;">{r['Takım'].upper()}</h3>
                <div style="display:flex;">{f_html}</div>
            </div>
            <div style="font-size:32px; font-weight:900; color:#10b981;">{r['P']}<small style="font-size:12px; color:#94a3b8; margin-left:4px;">P</small></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### DETAYLI PUAN DURUMU")
    st.markdown(f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{r['Takım']}</td><td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td><td>{r['Av']}</td><td style='color:#10b981; font-weight:900;'>{r['P']}</td></tr>" for _, r in df.iterrows()])}</tbody></table>""", unsafe_allow_html=True)

with t2:
    for i in range(10):
        w = 11 + i
        ev, dep = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        res = st.session_state.matches.get(w)
        score = f"{res['EvS']} - {res['DepS']}" if res else "VS"
        
        with st.expander(f"📍 {w}. HAFTA DETAYI", expanded=(i==0)):
            st.markdown(f"""
            <div class="match-card-premium">
                <div class="scoreboard-flex">
                    <div style="flex:1; font-weight:900; font-size:20px;">{ev}</div>
                    <div class="score-box">{score}</div>
                    <div style="flex:1; font-weight:900; font-size:20px; text-align:right;">{dep}</div>
                </div>
                <div style="text-align:center;"><div class="venue-tag">📍 Filia Arena</div></div>
                <div class="pitch-area">
                    <div style="text-align:center; color:white; font-size:10px; font-weight:800; margin-bottom:10px; opacity:0.7;">SAHA DİZİLİŞLERİ (İLK 6)</div>
                    <div class="formation-container">
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">
                            <div class="player-slot">?</div><div class="player-slot">?</div>
                            <div class="player-slot">?</div><div class="player-slot">?</div>
                            <div class="player-slot">?</div><div class="player-slot">?</div>
                        </div>
                        <div style="border-left:2px dashed rgba(255,255,255,0.2); height:150px;"></div>
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">
                            <div class="player-slot">?</div><div class="player-slot">?</div>
                            <div class="player-slot">?</div><div class="player-slot">?</div>
                            <div class="player-slot">?</div><div class="player-slot">?</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with t3:
    lider = get_stats().iloc[0]
    st.markdown(f"""
    <div style="background:#0f172a; padding:40px; border-radius:30px; text-align:center; border:2px solid #fbbf24;">
        <h1 style="color:white; margin:0;">{lider['Takım'].upper()}</h1>
        <p style="color:#fbbf24; font-weight:800; letter-spacing:2px;">ŞAMPİYONLUK YOLUNDA LİDER!</p>
        <div style="display:flex; justify-content:center; gap:20px; margin-top:30px;">
            <div style="background:rgba(255,255,255,0.1); padding:15px; border-radius:15px; min-width:80px;">
                <div style="font-size:24px; font-weight:900; color:white;">{lider['P']}</div>
                <div style="font-size:10px; color:#94a3b8;">PUAN</div>
            </div>
            <div style="background:rgba(255,255,255,0.1); padding:15px; border-radius:15px; min-width:80px;">
                <div style="font-size:24px; font-weight:900; color:white;">{lider['Av']}</div>
                <div style="font-size:10px; color:#94a3b8;">AVERAJ</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL ---
with st.sidebar:
    st.header("⚙️ ADMİN PANELİ")
    with st.form("score_entry"):
        h = st.number_input("Hafta", 11, 20)
        s1 = st.number_input("Ev Skor", 0)
        s2 = st.number_input("Dep Skor", 0)
        if st.form_submit_button("SKORU KAYDET"):
            st.session_state.matches[h] = {"Ev": "Prospor" if h%2==0 else "Billispor", "Dep": "Billispor" if h%2==0 else "Prospor", "EvS": s1, "DepS": s2}
            st.rerun()
