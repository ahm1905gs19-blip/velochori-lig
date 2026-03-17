import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# --- CSS TASARIM (Taşma Sorunları Giderildi) ---
st.markdown("""
<style>
.stApp { background: #ffffff; }

.league-title {
    font-size: clamp(30px, 8vw, 60px);
    font-weight: 950;
    text-align: center;
    padding: 20px 0;
    font-family: 'Arial Black', sans-serif;
    background: linear-gradient(90deg, #16a34a, #22c55e, #4ade80, #22c55e, #16a34a);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
}

@keyframes shine { to { background-position: 200% center; } }

/* TAKIM KARTLARI - Esnek Yapı */
.team-card {
    display: flex;
    flex-wrap: wrap; /* Yazıların taşmasını engeller, gerekirse alt satıra geçer */
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 15px;
    border: 1px solid #f1f5f9;
    box-shadow: 0 5px 15px rgba(0,0,0,0.03);
    gap: 15px;
}

.leader { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffdf2 0%, #ffffff 100%); }

.points-val { font-size: clamp(30px, 5vw, 42px); font-weight: 900; color: #16a34a; }

/* FİKSTÜR ROW - Taşma Korumalı */
.fixture-row {
    background: #ffffff;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 10px;
    display: flex;
    flex-wrap: wrap; /* Mobilde VS kısmının dışarı çıkmasını engeller */
    justify-content: center;
    align-items: center;
    border: 1px solid #f1f5f9;
    gap: 10px;
}

.fixture-teams-area {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    flex: 1;
    min-width: 250px; /* Minimum sığma alanı */
}

.team-label {
    font-weight: 800;
    font-size: 0.9rem;
    color: #1e293b;
    flex: 1;
    text-align: center;
}

.score-pill {
    background: #1e293b;
    color: #ffffff;
    padding: 5px 15px;
    border-radius: 15px;
    font-weight: 900;
    min-width: 70px;
    text-align: center;
}

.vs-pill {
    background: #f1f5f9;
    color: #64748b;
    padding: 5px 12px;
    border-radius: 15px;
    font-size: 0.7rem;
    font-weight: 900;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ YÖNETİMİ ---
if 'matches' not in st.session_state: st.session_state.matches = {}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ SKOR GİRİŞİ")
    with st.form("score_entry"):
        w_in = st.number_input("Hafta", 11, 20, 11)
        h, a = ("Prospor", "Billispor") if w_in % 2 == 0 else ("Billispor", "Prospor")
        c1, c2 = st.columns(2)
        hs = c1.number_input(f"{h}", 0, 100, 0)
        as_ = c2.number_input(f"{a}", 0, 100, 0)
        if st.form_submit_button("✅ KAYDET"):
            st.session_state.matches[w_in] = {"Ev": h, "EvSkor": hs, "Dep": a, "DepSkor": as_}
            st.rerun()

# --- HESAPLAMA ---
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
        if m["EvSkor"] > m["DepSkor"]:
            data[m["Ev"]]["G"] += 1; data[m["Ev"]]["P"] += 3; data[m["Dep"]]["M"] += 1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        elif m["EvSkor"] < m["DepSkor"]:
            data[m["Dep"]]["G"] += 1; data[m["Dep"]]["P"] += 3; data[m["Ev"]]["M"] += 1
            data[m["Ev"]]["form"].append("M"); data[m["Dep"]]["form"].append("G")
        else:
            data[m["Ev"]]["B"] += 1; data[m["Dep"]]["B"] += 1; data[m["Ev"]]["P"] += 1; data[m["Dep"]]["P"] += 1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- ARAYÜZ ---
t1, t2 = st.tabs(["📊 SIRALAMA", "🗓️ FİKSTÜR"])

with t1:
    df = get_stats()
    for i, r in df.iterrows():
        l_css = "leader" if i == 0 else ""
        st.markdown(f"""
        <div class="team-card {l_css}">
            <div style="flex:1; min-width:150px;">
                <span style="color:#94a3b8; font-weight:800; font-size:12px;">#{i+1}</span>
                <h3 style="margin:0; color:#1e293b;">{r['Takım'].upper()}</h3>
            </div>
            <div style="text-align:right;">
                <div class="points-val">{r['P']} PTS</div>
                <div style="font-size:12px; color:#64748b;">AVG: {r['Av']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### 📝 Detaylı Puan Durumu")
    # INDEX NUMARALARINI GİZLEYEN KISIM:
    st.dataframe(df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]], use_container_width=True, hide_index=True)

with t2:
    start = datetime.date(2026, 3, 22)
    for i in range(10):
        w = 11 + i
        dt = start + datetime.timedelta(days=7*i)
        h_t, a_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        done = w in st.session_state.matches
        m_data = st.session_state.matches.get(w)
        
        score_box = f'<div class="score-pill">{m_data["EvSkor"]} - {m_data["DepSkor"]}</div>' if done else '<div class="vs-pill">VS</div>'
        
        st.markdown(f"""
        <div class="fixture-row">
            <div style="text-align:center; min-width:80px;">
                <b style="color:#16a34a; font-size:0.8rem;">{w}. HAFTA</b>
            </div>
            <div class="fixture-teams-area">
                <span class="team-label">{h_t}</span>
                {score_box}
                <span class="team-label">{a_t}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
