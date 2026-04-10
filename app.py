import streamlit as st
import pandas as pd
import datetime

# --- 1. PREMIUM DASHBOARD TASARIMI ---
st.set_page_config(page_title="Velochori Pro Dashboard", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@700&display=swap');

.stApp { background: #f8fafc; font-family: 'Plus Jakarta Sans', sans-serif; }

/* HEADER */
.main-header {
    background: white; padding: 30px; border-bottom: 1px solid #e2e8f0;
    text-align: center; margin-bottom: 30px; border-radius: 0 0 30px 30px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.02);
}
.league-title { font-size: 36px; font-weight: 800; color: #1e293b; letter-spacing: -1.5px; margin: 0; }

/* PUAN DURUMU - GLASSMORPHISM TABLE */
.card-container {
    background: white; border-radius: 24px; padding: 25px;
    border: 1px solid #f1f5f9; box-shadow: 0 10px 30px rgba(0,0,0,0.03);
}
.custom-table { width: 100%; border-collapse: collapse; }
.custom-table th { 
    background: #f8fafc; color: #64748b; padding: 15px; 
    font-size: 11px; font-weight: 800; text-transform: uppercase; text-align: center;
}
.custom-table td { padding: 18px 15px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 700; color: #334155; }
.puan-cell { background: #f0fdf4; color: #10b981 !important; font-size: 1.2rem !important; border-radius: 10px; }

/* FİKSTÜR ZAMAN ÇİZGESİ */
.fixture-card {
    background: white; border-radius: 20px; padding: 20px;
    margin-bottom: 15px; border: 1px solid #f1f5f9;
    display: flex; align-items: center; transition: 0.3s;
}
.fixture-card:hover { transform: translateX(10px); border-color: #0ea5e9; }
.date-box { min-width: 60px; text-align: center; border-right: 2px solid #f1f5f9; margin-right: 20px; padding-right: 15px; }
.day-num { font-size: 20px; font-weight: 800; color: #1e293b; display: block; }
.month-txt { font-size: 10px; color: #94a3b8; font-weight: 700; text-transform: uppercase; }

.score-pill {
    background: #1e293b; color: #00ff85; padding: 6px 15px;
    border-radius: 10px; font-family: 'JetBrains Mono', monospace; font-size: 1.1rem;
}
.form-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 4px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA ENGINE (PROSPOR 20-19 DAHİL) ---
if 'matches' not in st.session_state:
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15, "Tarih": datetime.date(2026, 3, 28)},
        12: {"Ev": "Prospor", "EvSkor": 20, "Dep": "Billispor", "DepSkor": 19, "Tarih": datetime.date(2026, 4, 9)}
    }

def get_stats():
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
            data[m["Dep"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        else:
            data[m["Ev"]]["P"] += 1; data[m["Dep"]]["P"] += 1; data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["AV"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "AV"], ascending=False)

# --- 3. DASHBOARD RENDER ---
st.markdown('<div class="main-header"><div class="league-title">Velochori Super League</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("### 📊 Puan Durumu")
    df = get_stats()
    rows = ""
    for idx, r in df.reset_index(drop=True).iterrows():
        form_dots = "".join([f'<div class="form-dot {x}"></div>' for x in r["form"][-5:]])
        rows += f"""
        <tr>
            <td style="text-align:left; font-size:1.1rem;">{idx+1}. <b>{r['Takım']}</b><br><small>{form_dots}</small></td>
            <td>{r['O']}</td><td>{r['G']}</td><td>{r['B']}</td><td>{r['M']}</td>
            <td>{r['AG']}</td><td>{r['YG']}</td><td>{r['AV']}</td>
            <td class="puan-cell">{r['P']}</td>
        </tr>
        """
    st.markdown(f"""
    <div class="card-container">
        <table class="custom-table">
            <thead><tr><th style="text-align:left;">TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>PUAN</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🗓️ Fikstür & Sonuçlar")
    stadiums = ["Filia Arena", "Velochori Arena", "Olympic Center", "City Stadium"]
    
    # 1. Gelecek Maç (Sıradaki)
    next_h = 13
    m_date = datetime.date(2026, 4, 19)
    t1, t2 = ("Billispor", "Prospor")
    st.markdown(f"""
    <div class="fixture-card" style="border-left: 5px solid #0ea5e9;">
        <div class="date-box"><span class="day-num">{m_date.day}</span><span class="month-txt">NİS</span></div>
        <div style="flex:1; text-align:center;">
            <div style="font-size:10px; font-weight:800; color:#0ea5e9; margin-bottom:5px;">SIRADAKİ MAÇ • {stadiums[1]}</div>
            <div style="font-weight:800; font-size:1.1rem;">{t1} <span class="score-pill" style="background:#f1f5f9; color:#64748b;">VS</span> {t2}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Son Maç (Dün akşamki 20-19)
    last_m = st.session_state.matches[12]
    st.markdown(f"""
    <div class="fixture-card" style="border-left: 5px solid #10b981;">
        <div class="date-box"><span class="day-num">09</span><span class="month-txt">NİS</span></div>
        <div style="flex:1; text-align:center;">
            <div style="font-size:10px; font-weight:800; color:#10b981; margin-bottom:5px;">SON SONUÇ • {stadiums[0]}</div>
            <div style="font-weight:800; font-size:1.1rem;">{last_m['Ev']} <span class="score-pill">{last_m['EvSkor']} - {last_m['DepSkor']}</span> {last_m['Dep']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. ADMIN PANEL ---
with st.sidebar:
    st.markdown("## ⚙️ Hızlı Güncelle")
    h_sel = st.number_input("Hafta", 11, 20, 13)
    ev_t, dep_t = ("Billispor", "Prospor") if h_sel % 2 != 0 else ("Prospor", "Billispor")
    s1 = st.number_input(f"{ev_t}", 0, 100, 0)
    s2 = st.number_input(f"{dep_t}", 0, 100, 0)
    if st.button("KAYDET"):
        m_date = datetime.date(2026, 4, 19) + datetime.timedelta(weeks=h_sel-13) if h_sel >= 13 else datetime.date.today()
        st.session_state.matches[h_sel] = {"Ev": ev_t, "EvSkor": s1, "Dep": dep_t, "DepSkor": s2, "Tarih": m_date}
        st.rerun()
