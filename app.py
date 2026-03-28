import streamlit as st
import pandas as pd

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Super League", page_icon="⚽", layout="wide")

# --- CSS: ANA TASARIM SİSTEMİ (HATASIZ) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* BAŞLIK: PARLAYAN VE BÜYÜK */
.league-title {
    font-size: clamp(30px, 10vw, 50px); font-weight: 900; text-align: center;
    padding: 25px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* GENİŞ VE ŞIK PUAN DURUMU KARTLARI */
.team-card { 
    display: flex; justify-content: space-between; align-items: center; 
    background: white; padding: 25px 35px; border-radius: 25px; 
    margin-bottom: 15px; border: 1px solid #e2e8f0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
}
.leader-card { border: 3px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }
.f-dot { width: 24px; height: 24px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 900; color: white; margin-right: 6px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* FİKSTÜR VE HALI SAHA TASARIMI */
.match-detail-box { background: white; border-radius: 30px; padding: 30px; border: 1px solid #e2e8f0; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
.score-pill { 
    background: #1e293b; color: #34d399; font-size: 34px; font-weight: 900;
    padding: 10px 35px; border-radius: 20px; min-width: 140px; text-align: center;
}
.football-pitch {
    background: #2d5a27; border-radius: 25px; padding: 35px; border: 4px solid rgba(255,255,255,0.3);
    background-image: linear-gradient(rgba(255,255,255,0.1) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.1) 2px, transparent 2px);
    background-size: 50px 50px; margin-top: 20px;
}
.player-q {
    width: 48px; height: 48px; background: white; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 24px; color: #1e293b; border: 3px solid #fbbf24;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

/* TABLO TASARIMI */
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 20px; overflow: hidden; margin-top: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.custom-table th { background: #1e293b; color: white; padding: 18px; font-size: 14px; text-align: center; }
.custom-table td { padding: 18px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown('<div class="league-title">VELOCHORI SUPER LEAGUE</div>', unsafe_allow_html=True)

# --- VERİ HESAPLAMA ---
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

# --- SEKMELER ---
tab1, tab2, tab3 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ", "🏆 ŞAMPİYONLUK"])

with tab1:
    df = get_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = (idx == 0)
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_l else ''}">
            <div style="flex:1;">
                <div style="font-size:13px; font-weight:900; color:#94a3b8; text-transform:uppercase;">{ "🥇 LİDER" if is_l else f"SIRA {idx+1}"}</div>
                <div style="font-size:28px; font-weight:900; color:#1e293b; margin:8px 0;">{r['Takım'].upper()}</div>
                <div style="display:flex;">{f_html}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:48px; font-weight:900; color:#10b981; line-height:1;">{r['P']}<small style="font-size:16px; color:#94a3b8; margin-left:5px;">P</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><h4>📈 DETAYLI ANALİZ</h4>", unsafe_allow_html=True)
    t_html = f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{r['Takım']}</td><td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td><td>{r['AG']}</td><td>{r['YG']}</td><td>{r['Av']}</td><td style='color:#10b981; font-weight:900;'>{r['P']}</td></tr>" for _, r in df.iterrows()])}</tbody></table>"""
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    for i in range(5):
        w = 11 + i
        ev, dep = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        res = st.session_state.matches.get(w)
        score_val = f"{res['EvS']} - {res['DepS']}" if res else "18:30"
        
        with st.expander(f"🏟️ {w}. HAFTA DETAYI", expanded=(i==0)):
            st.markdown(f"""
            <div class="match-detail-box">
                <div style="text-align:center;"><div style="background:#f1f5f9; color:#475569; padding:8px 25px; border-radius:100px; font-size:16px; font-weight:800; display:inline-block; margin-bottom:25px;">📍 Filia Arena</div></div>
                <div style="display:flex; justify-content:space-around; align-items:center; margin-bottom:25px;">
                    <div style="flex:1; text-align:center;"><h2 style="margin:0; font-weight:900; font-size:32px;">{ev}</h2></div>
                    <div class="score-pill">{score_val}</div>
                    <div style="flex:1; text-align:center;"><h2 style="margin:0; font-weight:900; font-size:32px;">{dep}</h2></div>
                </div>
                <div class="football-pitch">
                    <div style="display:flex; justify-content:space-around; align-items:center;">
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                            <div class="player-q">?</div><div class="player-q">?</div><div class="player-q">?</div>
                            <div class="player-q">?</div><div class="player-q">?</div><div class="player-q">?</div>
                        </div>
                        <div style="height:180px; border-left:4px dashed rgba(255,255,255,0.2);"></div>
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
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
    <div style="background:#0f172a; padding:60px; border-radius:35px; text-align:center; border:4px solid #fbbf24; box-shadow: 0 15px 30px rgba(0,0,0,0.2);">
        <div style="font-size:70px; margin-bottom:15px;">🏆</div>
        <h1 style="color:white; margin:0; font-size:56px; font-weight:900;">{lider['Takım'].upper()}</h1>
        <p style="color:#fbbf24; font-weight:800; letter-spacing:4px; font-size:18px;">ŞAMPİYONLUĞA EN YAKIN!</p>
        <div style="display:flex; justify-content:center; gap:30px; margin-top:40px;">
            <div style="background:rgba(255,255,255,0.05); padding:25px; border-radius:25px; min-width:120px; border:1px solid rgba(255,255,255,0.1);">
                <div style="font-size:38px; font-weight:900; color:white;">{lider['P']}</div>
                <div style="font-size:14px; color:#94a3b8; font-weight:700;">TOPLAM PUAN</div>
            </div>
            <div style="background:rgba(255,255,255,0.05); padding:25px; border-radius:25px; min-width:120px; border:1px solid rgba(255,255,255,0.1);">
                <div style="font-size:38px; font-weight:900; color:white;">{lider['Av']}</div>
                <div style="font-size:14px; color:#94a3b8; font-weight:700;">AVERAY</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ADMIN PANEL ---
with st.sidebar:
    st.header("⚙️ ADMİN PANELİ")
    with st.form("score_input"):
        h = st.number_input("Hafta", 11, 20)
        s1 = st.number_input("Ev", 0); s2 = st.number_input("Dep", 0)
        if st.form_submit_button("SKORU KAYDET"):
            st.session_state.matches[h] = {"Ev": "Prospor" if h%2==0 else "Billispor", "Dep": "Billispor" if h%2==0 else "Prospor", "EvS": s1, "DepS": s2}
            st.rerun()
