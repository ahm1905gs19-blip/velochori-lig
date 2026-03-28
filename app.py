import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- KADRO VE SAHA VERİLERİ ---
teams_squads = {
    "Billispor": {"Kadro": ["Ahmet", "Mehmet", "Can", "Hüseyin", "Burak", "Efe"], "Renk": "#ef4444"},
    "Prospor": {"Kadro": ["Murat", "Selim", "Deniz", "Arda", "Volkan", "Gökhan"], "Renk": "#3b82f6"}
}

# --- CSS: TÜM TASARIM SİSTEMİ (TABLO + MAÇ MERKEZİ + ŞAMPİYONLUK) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* BAŞLIK */
.league-title {
    font-size: clamp(24px, 5vw, 45px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* TABLO KARTLARI (GERİ GETİRİLEN KISIM) */
.team-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 20px; border-radius: 15px; margin-bottom: 10px; border: 1px solid #e2e8f0; }
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }
.f-dot { width: 20px; height: 20px; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 3px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* MAÇ MERKEZİ PREMIUM (VİDEODAKİ GİBİ) */
.match-card-premium { background: white; border-radius: 16px; padding: 20px; border: 1px solid #e2e8f0; margin-top: 10px; }
.scoreboard-flex { display: flex; justify-content: space-around; align-items: center; text-align: center; }
.score-box-premium { font-size: 28px; font-weight: 900; color: #1e293b; background: #f8fafc; padding: 8px 20px; border-radius: 12px; }
.pitch-container { background: #2d5a27; border-radius: 12px; padding: 15px; border: 2px solid #fff; margin-top: 15px; }
.player-pill { background: white; color: #1e293b; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; margin-bottom: 4px; }

/* ŞAMPİYONLUK KARTI */
.champ-container { background: #0f172a; border-radius: 20px; padding: 30px; color: white; text-align: center; border: 2px solid #fbbf24; }
.stat-item { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; min-width: 70px; }

/* GENEL TABLO */
.custom-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; margin-top: 20px; }
.custom-table th { background: #1e293b; color: white; padding: 10px; font-size: 11px; text-align: center; }
.custom-table td { padding: 10px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA ---
if 'matches' not in st.session_state: st.session_state.matches = {}

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
        data[m["Ev"]]["form"].append(res)
        data[m["Dep"]]["form"].append("G" if res=="M" else "M" if res=="G" else "B")
        if res == "G": data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
        elif res == "M": data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
        else: data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- ANA EKRAN ---
tab1, tab2, tab3 = st.tabs(["📊 LİG TABLOSU", "🗓️ MAÇ MERKEZİ", "🏆 ŞAMPİYONLUK YOLU"])

with tab1:
    df = get_live_stats()
    # ŞIK KARTLI GÖRÜNÜM (DEMİNKİ GİBİ)
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = idx == 0
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_l else ''}">
            <div style="flex:1;">
                <span style="background:{'#fbbf24' if is_l else '#f1f5f9'}; padding:2px 8px; border-radius:6px; font-size:10px; font-weight:900;">
                    { "🏆 LİDER" if is_l else f"SIRA {idx+1}"}
                </span>
                <h3 style="margin:5px 0; color:#1e293b; font-size:1.1rem;">{r["Takım"].upper()}</h3>
                <div style="display:flex;">{f_html}</div>
            </div>
            <div style="font-size:32px; font-weight:900; color:#10b981;">{r["P"]}<small style="font-size:12px; color:#94a3b8; margin-left:2px;">P</small></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### 📈 DETAYLI ANALİZ")
    t_html = f"""<table class="custom-table"><thead><tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr></thead><tbody>{"".join([f"<tr><td>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-weight:900;'>{row['P']}</td></tr>" for _, row in df.iterrows()])}</tbody></table>"""
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    today = datetime.date.today()
    for i in range(10):
        w = 11 + i
        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        res = st.session_state.matches.get(w)
        score_txt = f"{res['EvSkor']} - {res['DepSkor']}" if res else "18:30"
        
        with st.expander(f"📍 {w}. HAFTA | {ev_t} vs {dep_t}", expanded=(i==0)):
            st.markdown(f"""
            <div class="match-card-premium">
                <div class="scoreboard-flex">
                    <div style="flex:1;"><div style="font-weight:900;">{ev_t}</div></div>
                    <div class="score-box-premium">{score_txt}</div>
                    <div style="flex:1;"><div style="font-weight:900;">{dep_t}</div></div>
                </div>
                <div class="pitch-container">
                    <div class="scoreboard-flex" style="color:white; font-size:10px; margin-bottom:10px;"><span>İLK 6</span><span>DİZİLİŞ</span><span>İLK 6</span></div>
                    <div style="display:flex; justify-content:space-between;">
                        <div>{"".join([f'<div class="player-pill">{p}</div>' for p in teams_squads[ev_t]['Kadro']])}</div>
                        <div style="text-align:right;">{"".join([f'<div class="player-pill">{p}</div>' for p in teams_squads[dep_t]['Kadro']])}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    df = get_live_stats()
    lider = df.iloc[0]
    st.markdown(f"""
    <div class="champ-container">
        <div style="font-size:40px;">🏆</div>
        <h1 style="color:white; margin:0;">{lider['Takım'].upper()}</h1>
        <p style="color:#fbbf24; font-weight:800;">ŞAMPİYONLUĞA EN YAKIN</p>
        <div style="display:flex; justify-content:center; gap:10px; margin-top:20px;">
            <div class="stat-item"><div style="font-size:18px; font-weight:900;">{lider['P']}</div><div style="font-size:9px;">PUAN</div></div>
            <div class="stat-item"><div style="font-size:18px; font-weight:900;">{lider['Av']}</div><div style="font-size:9px;">AVERAY</div></div>
            <div class="stat-item"><div style="font-size:18px; font-weight:900;">{20-lider['O']}</div><div style="font-size:9px;">KALAN</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# SIDEBAR ADMIN
with st.sidebar:
    st.title("⚙️ PANEL")
    with st.form("score"):
        h = st.number_input("Hafta", 11, 20)
        s1 = st.number_input("Ev", 0); s2 = st.number_input("Dep", 0)
        if st.form_submit_button("KAYDET"):
            st.session_state.matches[h] = {"Ev": "Prospor" if h%2==0 else "Billispor", "EvSkor": s1, "Dep": "Billispor" if h%2==0 else "Prospor", "DepSkor": s2}
            st.rerun()
