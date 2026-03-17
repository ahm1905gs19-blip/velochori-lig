import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# --- CSS TASARIM ---
st.markdown("""
<style>
.stApp { background: #ffffff; }

/* O GÖSTERİŞLİ BAŞLIK - KORUNDU */
.league-title {
    font-size: clamp(40px, 8vw, 65px);
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

/* TAKIM KARTI (SIRALAMA SEKMESİ) - KORUNDU */
.team-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 25px 35px;
    border-radius: 24px;
    margin-bottom: 18px;
    border: 1px solid #f1f5f9;
    box-shadow: 0 10px 25px rgba(0,0,0,0.03);
}

.leader { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffdf2 0%, #ffffff 100%); }

.points-val { font-size: 42px; font-weight: 900; color: #16a34a; line-height: 1; }
.av-val { font-size: 14px; font-weight: 800; color: #64748b; background: #f1f5f9; padding: 6px 14px; border-radius: 12px; }

.form-dot {
    width: 26px; height: 26px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 900; color: white;
}
.win { background: #22c55e; }
.loss { background: #ef4444; }
.draw { background: #94a3b8; }

/* GELİŞTİRİLMİŞ FİKSTÜR TASARIMI */
.fixture-row {
    background: #ffffff;
    border-radius: 12px;
    padding: 10px 20px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #f1f5f9;
    transition: all 0.2s ease;
}

.fixture-row:nth-child(even) { background: #f8fafc; }
.fixture-row:hover { transform: scale(1.01); border-color: #16a34a; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }

.fixture-week-box {
    text-align: left;
    min-width: 100px;
}

.fixture-teams-area {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 25px;
    flex: 1;
}

.team-label {
    font-weight: 800;
    font-size: 0.95rem;
    color: #1e293b;
    width: 130px;
    text-transform: uppercase;
}

.score-pill {
    background: #1e293b;
    color: #ffffff;
    padding: 4px 18px;
    border-radius: 20px;
    font-size: 1.1rem;
    font-weight: 900;
    min-width: 80px;
    text-align: center;
    letter-spacing: 2px;
}

.vs-pill {
    background: #f1f5f9;
    color: #64748b;
    padding: 4px 15px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 900;
}

.status-badge {
    font-size: 0.7rem;
    font-weight: 800;
    width: 110px;
    text-align: right;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ YÖNETİMİ ---
if 'matches' not in st.session_state: st.session_state.matches = {}

# --- SIDEBAR (ADMIN) ---
with st.sidebar:
    st.markdown("### ⚙️ SKOR GİRİŞİ")
    with st.form("score_entry"):
        w_in = st.number_input("Hafta", 11, 20, 11)
        h, a = ("Prospor", "Billispor") if w_in % 2 == 0 else ("Billispor", "Prospor")
        st.info(f"Maç: {h} vs {a}")
        c1, c2 = st.columns(2)
        hs = c1.number_input(f"{h}", 0, 100, 0)
        as_ = c2.number_input(f"{a}", 0, 100, 0)
        if st.form_submit_button("✅ SKORU KAYDET"):
            st.session_state.matches[w_in] = {"Ev": h, "EvSkor": hs, "Dep": a, "DepSkor": as_}
            st.rerun()
    
    if st.button("🗑️ Verileri Sıfırla"):
        st.session_state.matches = {}
        st.rerun()

# --- HESAPLAMA MOTORU ---
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
t1, t2 = st.tabs(["📊 CANLI PUAN DURUMU", "🗓️ MAÇ TAKVİMİ"])

with t1:
    df = get_stats()
    for i, r in df.iterrows():
        l_css = "leader" if i == 0 else ""
        f_html = "".join([f'<div class="form-dot {"win" if x=="G" else "loss" if x=="M" else "draw"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {l_css}">
            <div>
                <span style="color:#94a3b8; font-weight:800; font-size:12px; letter-spacing:1px;">SIRALAMA: {i+1}</span>
                <h2 style="margin:0; color:#1e293b; letter-spacing:-1px; font-size:28px;">{r['Takım'].upper()}</h2>
                <div style="display:flex; gap:4px; margin-top:10px;">{f_html}</div>
            </div>
            <div style="display:flex; gap:30px; align-items:center;">
                <div style="text-align:right">
                    <div class="av-val">AVG: {r['Av']}</div>
                    <div style="color:#94a3b8; font-size:11px; margin-top:4px;">{r['AG']} AG / {r['YG']} YG</div>
                </div>
                <div class="points-val">{r['P']}<span style="font-size:14px; color:#94a3b8; margin-left:5px;">PTS</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.dataframe(df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]], use_container_width=True, hide_index=True)

with t2:
    start = datetime.date(2026, 3, 22)
    st.write("") # Boşluk
    for i in range(10):
        w = 11 + i
        dt = start + datetime.timedelta(days=7*i)
        h_t, a_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        
        done = w in st.session_state.matches
        m_data = st.session_state.matches.get(w)
        
        score_box = f'<div class="score-pill">{m_data["EvSkor"]} - {m_data["DepSkor"]}</div>' if done else '<div class="vs-pill">VS</div>'
        status = f'<span class="status-badge" style="color:#22c55e;">✅ BİTTİ</span>' if done else '<span class="status-badge" style="color:#cbd5e1;">⏳ BEKLİYOR</span>'
        
        st.markdown(f"""
        <div class="fixture-row">
            <div class="fixture-week-box">
                <b style="color:#16a34a; font-size:0.9rem;">{w}. HAFTA</b><br>
                <small style="color:#94a3b8; font-size:0.75rem;">{dt.strftime('%d.%m.%Y')}</small>
            </div>
            <div class="fixture-teams-area">
                <span class="team-label" style="text-align:right;">{h_t}</span>
                {score_box}
                <span class="team-label" style="text-align:left;">{a_t}</span>
            </div>
            {status}
        </div>
        """, unsafe_allow_html=True)
