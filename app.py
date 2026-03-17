import streamlit as st
import pandas as pd
import datetime

# SAYFA AYARI
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# CSS TASARIM
st.markdown("""
<style>
/* ARKA PLAN */
.stApp {
    background: #f8fafc;
}

/* GÖSTERİŞLİ BAŞLIK */
.league-title {
    font-size: 70px;
    font-weight: 900;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 40px;
    font-family: 'Arial Black', sans-serif;
    background: linear-gradient(90deg, #065f46, #10b981, #34d399, #10b981, #065f46);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

@keyframes shine {
    to { background-position: 200% center; }
}

/* TAKIM KARTI */
.team-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 15px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

.team-card:hover {
    transform: scale(1.01);
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}

.leader {
    border: 3px solid #fbbf24;
    background: linear-gradient(90deg, #fffbeb, #ffffff);
}

/* İSTATİSTİKLER (PUAN VE AVERAJ AYNI SIRADA) */
.stats-container {
    display: flex;
    gap: 40px;
    align-items: center;
}

.points-text {
    font-size: 45px;
    font-weight: 900;
    color: #059669;
}

.av-text {
    font-size: 25px;
    font-weight: 700;
    color: #64748b;
    background: #f1f5f9;
    padding: 5px 15px;
    border-radius: 10px;
}

/* FİKSTÜR */
.match-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 12px;
    border-left: 8px solid #10b981;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #1e293b;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">⚽ VELOCHORI SUPER LEAGUE ⚽</div>', unsafe_allow_html=True)

# VERİ SAKLAMA
if 'matches' not in st.session_state:
    st.session_state.matches = {}

# SIDEBAR
st.sidebar.header("🕹️ Skor Merkezi")

with st.sidebar.form("score_form"):
    week_input = st.number_input("Hafta", min_value=11, max_value=20, value=11)
    is_even = week_input % 2 == 0
    h_team, a_team = ("Prospor", "Billispor") if is_even else ("Billispor", "Prospor")
    
    st.write(f"**{week_input}. Hafta Maçı**")
    h_score = st.number_input(f"{h_team}", min_value=0, step=1)
    a_score = st.number_input(f"{a_team}", min_value=0, step=1)
    
    if st.form_submit_button("Skoru Onayla"):
        st.session_state.matches[week_input] = {"Ev": h_team, "EvSkor": h_score, "Dep": a_team, "DepSkor": a_score}
        st.success("Kaydedildi!")

# PUAN HESAPLAMA
def get_standings():
    stats = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 15, "YG": 19, "P": 18},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 19, "YG": 15, "P": 12}
    }
    for w, m in st.session_state.matches.items():
        stats[m["Ev"]]["O"] += 1; stats[m["Dep"]]["O"] += 1
        stats[m["Ev"]]["AG"] += m["EvSkor"]; stats[m["Ev"]]["YG"] += m["DepSkor"]
        stats[m["Dep"]]["AG"] += m["DepSkor"]; stats[m["Dep"]]["YG"] += m["EvSkor"]
        if m["EvSkor"] > m["DepSkor"]:
            stats[m["Ev"]]["G"] += 1; stats[m["Ev"]]["P"] += 3; stats[m["Dep"]]["M"] += 1
        elif m["EvSkor"] < m["DepSkor"]:
            stats[m["Dep"]]["G"] += 1; stats[m["Dep"]]["P"] += 3; stats[m["Ev"]]["M"] += 1
        else:
            stats[m["Ev"]]["B"] += 1; stats[m["Dep"]]["B"] += 1; stats[m["Ev"]]["P"] += 1; stats[m["Dep"]]["P"] += 1
    
    df = pd.DataFrame.from_dict(stats, orient='index').reset_index()
    df.columns = ["Takım", "O", "G", "B", "M", "AG", "YG", "P"]
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(by=["P", "Av"], ascending=[False, False])

# SEKMELER
tab1, tab2 = st.tabs(["📊 SIRALAMA", "📅 FİKSTÜR"])

with tab1:
    df = get_standings()
    for i, row in df.iterrows():
        leader_class = "leader" if i == 0 else ""
        st.markdown(f"""
        <div class="team-card {leader_class}">
            <div>
                <h2 style="margin:0; color:#1e293b;">{i+1}. {row['Takım'].upper()}</h2>
                <span style="color:#64748b;">{row['O']} Maç | {row['G']}G {row['B']}B {row['M']}M</span>
            </div>
            <div class="stats-container">
                <div class="av-text">AV: {row['Av']}</div>
                <div class="points-text">{row['P']} <small style="font-size:15px;">PUAN</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    start_date = datetime.date(2026, 3, 22)
    for i in range(10):
        w = 11 + i
        date = start_date + datetime.timedelta(days=7*i)
        h = "Prospor" if w % 2 == 0 else "Billispor"
        a = "Billispor" if h == "Prospor" else "Prospor"
        res = "vs"
        if w in st.session_state.matches:
            m = st.session_state.matches[w]
            res = f"<b>{m['EvSkor']} - {m['DepSkor']}</b>"
        
        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span><b>{w}. Hafta</b><br><small>{date.strftime('%d.%m.%Y')}</small></span>
                <span style="font-size:1.2em;">{h} {res} {a}</span>
                <span style="color:#10b981;">●</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
