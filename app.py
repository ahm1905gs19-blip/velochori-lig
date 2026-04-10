import streamlit as st
import pandas as pd
import datetime

# --- 1. WOW FAKTÖRÜ CSS & ANİMASYONLAR ---
st.set_page_config(page_title="Velochori Super League", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@800&family=Poppins:wght@900&display=swap');

.stApp { background: #0c1017; font-family: 'Inter', sans-serif; }

/* ANİMASYONLAR */
@keyframes glow-leader { 0% { box-shadow: 0 0 10px #fbbf24; } 50% { box-shadow: 0 0 30px #fbbf24; } 100% { box-shadow: 0 0 10px #fbbf24; } }
@keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-5px); } 100% { transform: translateY(0px); } }
@keyframes points-blink { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }

.league-title {
    font-family: 'Poppins', sans-serif; font-size: 48px; font-weight: 900; text-align: center;
    background: linear-gradient(135deg, #fbbf24 0%, #ffffff 50%, #fbbf24 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    padding: 30px 0; letter-spacing: -2px; text-transform: uppercase;
}

/* PUAN DURUMU (ŞAMPİYONLAR LİGİ STYLE) */
.standings-header {
    background: #1e293b; color: #94a3b8; font-weight: 800; font-size: 11px;
    text-transform: uppercase; letter-spacing: 1px; padding: 12px 20px;
    border-radius: 12px; display: flex; text-align: center; margin-bottom: 15px;
}

.team-card {
    background: #1e293b; border-radius: 16px; padding: 20px;
    margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between;
    transition: all 0.3s ease; border: 1px solid #334155;
}
.team-card:hover { transform: scale(1.02); }

/* LİDER KARTI (WOW) */
.leader-card {
    background: linear-gradient(135deg, #1a2333 0%, #273142 100%);
    border: 2px solid #fbbf24; animation: glow-leader 2s infinite;
}

.team-info { display: flex; align-items: center; flex: 1; }
.team-rank { font-size: 24px; font-weight: 900; color: #94a3b8; margin-right: 20px; font-family: 'Poppins', serif; }
.team-title { font-size: 1.3rem; font-weight: 800; color: white; text-transform: uppercase; letter-spacing: -0.5px; }

.points-card {
    font-size: 32px; font-weight: 900; color: #22c55e;
    font-family: 'Poppins', sans-serif; line-height: 1;
    animation: points-blink 1.5s infinite; text-shadow: 0 0 10px rgba(34,197,94,0.5);
}

.details-row { display: flex; gap: 15px; text-align: center; color: #94a3b8; font-size: 14px; margin-top: 5px; font-weight: 600; }
.form-icon { width: 22px; height: 22px; border-radius: 6px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-left: 5px; box-shadow: 0 0 5px rgba(255,255,255,0.1); }
.W { background: #22c55e; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* MAÇ MERKEZİ (STADYUM LED SKORBORD) */
.stadium-led-card {
    background: #080a10; border-radius: 20px; margin-bottom: 25px;
    border: 3px solid #1e293b; overflow: hidden; position: relative;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.stadium-label { background: #1e293b; color: white; padding: 10px 20px; font-size: 12px; font-weight: 800; display: flex; justify-content: space-between; text-transform: uppercase; }

.led-score {
    font-family: 'JetBrains Mono', monospace; font-size: 2.2rem;
    color: #22c55e; text-shadow: 0 0 15px #22c55e;
    background: rgba(0,0,0,0.8); padding: 5px 25px; border-radius: 10px;
    animation: points-blink 1.5s infinite;
}
.live-badge { background: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 900; font-size: 10px; animation: blink 1s infinite; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ YÖNETİMİ ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15},
        12: {"Ev": "Prospor", "EvSkor": 20, "Dep": "Billispor", "DepSkor": 19}
    }

def get_super_data():
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    for h, m in sorted(st.session_state.matches.items()):
        data[m["Ev"]]["O"] += 1; data[m["Dep"]]["O"] += 1
        data[m["Ev"]]["AG"] += m["EvSkor"]; data[m["Ev"]]["YG"] += m["DepSkor"]
        data[m["Dep"]]["AG"] += m["DepSkor"]; data[m["Dep"]]["YG"] += m["EvSkor"]
        
        if m["EvSkor"] > m["DepSkor"]:
            data[m["Ev"]]["P"] += 3; data[m["Ev"]]["G"] += 1; data[m["Dep"]]["M"] += 1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        elif m["EvSkor"] < m["DepSkor"]:
            data[m["Dep"]]["P"] += 3; data[m["Dep"]]["G"] += 1; data[m["Ev"]]["M"] += 1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        else:
            data[m["Ev"]]["P"] += 1; data[m["Dep"]]["P"] += 1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
            
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["AV"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "AV"], ascending=False)

# --- 3. ANA EKRAN (WOW BAŞLIYOR) ---
st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 SIRALAMA VE FORM", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_super_data()
    # SIRALAMA BAŞLIKLARI (DAHA TEKNİK DURMALI)
    st.markdown("""
    <div class="standings-header">
        <div style="flex:1; text-align:left;">Sıra / Takım</div>
        <div style="width:50px;">O</div><div style="width:50px;">G</div><div style="width:50px;">M</div>
        <div style="width:70px;">AV</div><div style="width:100px; color:#22c55e;">Puan</div>
    </div>
    """, unsafe_allow_html=True)
    
    # TAKIM KARTLARI (WOW)
    for idx, r in df.reset_index(drop=True).iterrows():
        is_leader = idx == 0
        card_class = "team-card leader-card" if is_leader else "team-card"
        
        dots = "".join([f'<div class="form-icon {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        
        st.markdown(f"""
        <div class="{card_class}">
            <div class="team-info">
                <div class="team-rank">{idx+1}</div>
                <div>
                    <div class="team-title">{r['Takım']}</div>
                    <div style="display:inline-flex; margin-top:5px;">Form: {dots}</div>
                </div>
            </div>
            <div class="details-row">
                <div style="width:50px;">{r['O']}</div>
                <div style="width:50px;">{r['G']}</div>
                <div style="width:50px;">{r['M']}</div>
                <div style="width:70px; color:{'#22c55e' if r['AV'] >= 0 else '#ef4444'}">{r['AV']}</div>
                <div style="width:100px;" class="points-card">{r['P']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    stadiums = ["Filia Arena", "Velochori Arena", "Olympic Center", "City Stadium"]
    # Takvimi dün akşam (9 Nisan) oynanan maça göre ayarla
    for i in range(10):
        w = 11 + i
        if w == 11: m_date = datetime.date(2026, 3, 28)
        elif w == 12: m_date = datetime.date(2026, 4, 9) # Dün akşamki Prospor galibiyeti
        else: m_date = datetime.date(2026, 4, 19) + datetime.timedelta(weeks=i-2)
            
        res = st.session_state.matches.get(w)
        stad = stadiums[w % len(stadiums)]
        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        
        status = f'<span style="color:#22c55e;">BİTTİ' if res else f'<span style="color:#fbbf24;">🕒 18:30'
        score = f'{res["EvSkor"]} - {res["DepSkor"]}' if res else 'VS'

        st.markdown(f"""
        <div class="stadium-led-card">
            <div class="stadium-label">
                <span>{w}. HAFTA | 📍 {stad}</span>
                <span>{m_date.strftime('%d.%m.%Y')}</span>
            </div>
            <div style="padding:40px; display:flex; align-items:center; justify-content:space-between; text-align:center;">
                <div style="flex:1; font-weight:900; font-size:1.4rem; color:white; text-transform:uppercase; letter-spacing:-1px;">{t1}</div>
                <div class="led-score">{score}</div>
                <div style="flex:1; font-weight:900; font-size:1.4rem; color:white; text-transform:uppercase; letter-spacing:-1px;">{t2}</div>
            </div>
            <div style="background:#1e293b; padding:10px; text-align:center; font-size:11px; font-weight:800; border-top:1px solid #e2e8f0;">{status}</div>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div style="font-size:20px; font-weight:900; color:#fbbf24;">⚙️ SKOR YÖNETİMİ</div>', unsafe_allow_html=True)
    h_sel = st.number_input("Hafta", 11, 20, 13)
    ev_t, dep_t = ("Billispor", "Prospor") if h_sel % 2 != 0 else ("Prospor", "Billispor")
    s1 = st.number_input(f"{ev_t}", 0, 100, 0)
    s2 = st.number_input(f"{dep_t}", 0, 100, 0)
    if st.button("KAYDET VE GÜNCELLE"):
        st.session_state.matches[h_sel] = {"Ev": ev_t, "EvSkor": s1, "Dep": dep_t, "DepSkor": s2}
        st.rerun()
