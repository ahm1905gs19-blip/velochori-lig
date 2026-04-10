import streamlit as st
import pandas as pd
import datetime

# --- 1. ULTRA MODERN & FERAH (ELITE WHITE) TASARIM ---
st.set_page_config(page_title="Velochori Pro League", page_icon="🏆", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@700&display=swap');

/* GENEL ARKA PLAN */
.stApp { 
    background: linear-gradient(135deg, #f8f9ff 0%, #f1f4f9 100%);
    font-family: 'Plus Jakarta Sans', sans-serif; 
}

/* BAŞLIK TASARIMI */
.league-title {
    font-size: 42px; font-weight: 800; text-align: center;
    color: #1e293b; padding: 40px 0 10px 0;
    letter-spacing: -1.5px;
}
.sub-title {
    text-align: center; color: #64748b; font-size: 14px; 
    margin-bottom: 40px; font-weight: 500;
}

/* PUAN DURUMU KARTLARI */
.team-row {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px 25px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    border: 1px solid rgba(255, 255, 255, 1);
    box-shadow: 0 10px 25px rgba(0,0,0,0.03);
    transition: all 0.3s ease;
}
.team-row:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }

/* LİDER VURGUSU (SOFT GOLD) */
.leader-row {
    background: white;
    border: 1.5px solid #fbbf24;
    box-shadow: 0 10px 30px rgba(251, 191, 36, 0.1);
}

.rank-circle {
    width: 40px; height: 40px; border-radius: 12px;
    background: #f1f5f9; display: flex; align-items: center; justify-content: center;
    font-weight: 800; color: #475569; margin-right: 20px;
}
.leader-circle { background: #fef3c7; color: #b45309; }

.team-name { font-size: 1.2rem; font-weight: 800; color: #1e293b; flex: 2; }

/* TABLO DEĞERLERİ */
.stat-box { flex: 1; text-align: center; }
.stat-label { font-size: 10px; color: #94a3b8; font-weight: 700; text-transform: uppercase; margin-bottom: 2px; }
.stat-value { font-size: 15px; color: #334155; font-weight: 700; }
.points-value { font-size: 22px; color: #0ea5e9; font-weight: 800; }

/* FORM NOKTALARI */
.f-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin: 0 3px; }
.W { background: #10b981; box-shadow: 0 0 8px #10b98166; }
.L { background: #ef4444; box-shadow: 0 0 8px #ef444466; }
.D { background: #94a3b8; }

/* MAÇ MERKEZİ (APPLE STYLE) */
.match-card {
    background: white; border-radius: 24px; padding: 30px;
    margin-bottom: 20px; border: 1px solid #f1f5f9;
    text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}
.score-pill {
    background: #1e293b; color: white; padding: 8px 24px;
    border-radius: 14px; font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem; display: inline-block; margin: 0 20px;
}
.vs-pill { background: #f1f5f9; color: #64748b; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ YÖNETİMİ (PROSPOR 20-19 İŞLENDİ) ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15},
        12: {"Ev": "Prospor", "EvSkor": 20, "Dep": "Billispor", "DepSkor": 19}
    }

def get_clean_data():
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
            data[m["Dep"]]["form"].append("G"); data[m["Ev"]]["form"].append("M")
        else:
            data[m["Ev"]]["P"] += 1; data[m["Dep"]]["P"] += 1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
            
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["AV"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "AV"], ascending=False)

# --- 3. ARAYÜZ ---
st.markdown('<div class="league-title">Velochori Super League</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sezon 2026 • Professional League Management</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Puan Durumu", "🗓️ Maç Merkezi"])

with tab1:
    df = get_clean_data()
    
    for idx, r in df.reset_index(drop=True).iterrows():
        is_leader = idx == 0
        leader_class = "leader-row" if is_leader else ""
        circle_class = "leader-circle" if is_leader else ""
        form_html = "".join([f'<div class="f-dot {x}"></div>' for x in r["form"][-5:]])
        
        st.markdown(f"""
        <div class="team-row {leader_class}">
            <div class="rank-circle {circle_class}">{idx+1}</div>
            <div class="team-name">
                {r['Takım']}
                <div style="margin-top:4px;">{form_html}</div>
            </div>
            <div class="stat-box"><div class="stat-label">O</div><div class="stat-value">{r['O']}</div></div>
            <div class="stat-box"><div class="stat-label">G</div><div class="stat-value">{r['G']}</div></div>
            <div class="stat-box"><div class="stat-label">M</div><div class="stat-value">{r['M']}</div></div>
            <div class="stat-box"><div class="stat-label">AV</div><div class="stat-value">{r['AV']}</div></div>
            <div class="stat-box" style="flex:1.5;"><div class="stat-label">PUAN</div><div class="points-value">{r['P']}</div></div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    stadiums = ["Filia Arena", "Velochori Arena", "Olympic Center", "City Stadium"]
    for i in range(10):
        w = 11 + i
        if w == 11: m_date = datetime.date(2026, 3, 28)
        elif w == 12: m_date = datetime.date(2026, 4, 9)
        else: m_date = datetime.date(2026, 4, 19) + datetime.timedelta(weeks=i-2)
            
        res = st.session_state.matches.get(w)
        stad = stadiums[w % len(stadiums)]
        t1, t2 = ("Billispor", "Prospor") if w % 2 != 0 else ("Prospor", "Billispor")
        
        score_html = f'<div class="score-pill">{res["EvSkor"]} - {res["DepSkor"]}</div>' if res else '<div class="score-pill vs-pill">VS</div>'
        status_text = "● BİTTİ" if res else "🕒 18:30"
        
        st.markdown(f"""
        <div class="match-card">
            <div style="font-size:11px; font-weight:700; color:#94a3b8; margin-bottom:15px; text-transform:uppercase; letter-spacing:1px;">
                {w}. Hafta • {m_date.strftime('%d.%m.%Y')} • {stad}
            </div>
            <div style="display:flex; align-items:center; justify-content:center;">
                <div style="flex:1; font-weight:700; font-size:1.1rem; text-align:right;">{t1}</div>
                {score_html}
                <div style="flex:1; font-weight:700; font-size:1.1rem; text-align:left;">{t2}</div>
            </div>
            <div style="margin-top:15px; font-size:10px; font-weight:800; color:{'#10b981' if res else '#94a3b8'}">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Yönetim")
    h_sel = st.number_input("Hafta", 11, 20, 13)
    ev_t, dep_t = ("Billispor", "Prospor") if h_sel % 2 != 0 else ("Prospor", "Billispor")
    s1 = st.number_input(f"{ev_t}", 0, 100, 0)
    s2 = st.number_input(f"{dep_t}", 0, 100, 0)
    if st.button("Kaydet"):
        st.session_state.matches[h_sel] = {"Ev": ev_t, "EvSkor": s1, "Dep": dep_t, "DepSkor": s2}
        st.rerun()
