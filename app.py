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
    transition: all 0.3s ease;
}

.leader { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffdf2 0%, #ffffff 100%); }

.points-val { font-size: 42px; font-weight: 900; color: #16a34a; line-height: 1; }
.av-val { font-size: 14px; font-weight: 800; color: #64748b; background: #f1f5f9; padding: 6px 14px; border-radius: 12px; }

.form-container { display: flex; gap: 4px; margin-top: 10px; }
.form-dot {
    width: 26px; height: 26px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 900; color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.win { background: #22c55e; }
.loss { background: #ef4444; }
.draw { background: #94a3b8; }

/* MODERN FİKSTÜR TASARIMI - YAZILAR KÜÇÜLTÜLDÜ */
.modern-fixture {
    background: #ffffff;
    border: 1px solid #f1f5f9;
    border-radius: 15px;
    padding: 12px 25px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}

.fixture-teams {
    display: flex;
    align-items: center;
    gap: 20px;
    flex-grow: 1;
    justify-content: center;
    font-weight: 700;
    font-size: 1rem; /* Küçültüldü: 1.15 -> 1 */
}

.vs-circle {
    background: #f8fafc;
    width: 38px; /* Küçültüldü: 45 -> 38 */
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 0.65rem; /* Küçültüldü: 0.75 -> 0.65 */
    font-weight: 900;
    color: #16a34a;
    border: 1px solid #e2e8f0;
}

.score-text { 
    font-size: 1.3rem; /* Küçültüldü: 1.6 -> 1.3 */
    color: #16a34a; 
    min-width: 70px; 
    text-align: center;
    font-weight: 900;
}

.fixture-date {
    font-size: 0.85rem;
    color: #94a3b8;
}

.fixture-week {
    color: #16a34a; 
    font-size: 0.95rem; /* Küçültüldü: 18px -> 0.95rem */
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ YÖNETİMİ ---
if 'matches' not in st.session_state: st.session_state.matches = {}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ SKOR PANELİ")
    with st.form("score_entry"):
        w_in = st.number_input("Hafta", 11, 20, 11)
        h, a = ("Prospor", "Billispor") if w_in % 2 == 0 else ("Billispor", "Prospor")
        st.info(f"Maç: {h} vs {a}")
        c1, c2 = st.columns(2)
        hs = c1.number_input(f"{h}", 0, 100, 0)
        as_ = c2.number_input(f"{a}", 0, 100, 0)
        if st.form_submit_button("✅ KAYDET"):
            st.session_state.matches[w_in] = {"Ev": h, "EvSkor": hs, "Dep": a, "DepSkor": as_}
            st.rerun()
    
    if st.button("🗑️ Verileri Sıfırla"):
        st.session_state.matches = {}
        st.rerun()

# --- HESAPLAMA SİSTEMİ ---
def get_stats():
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    
    sorted_weeks = sorted(st.session_state.matches.keys())
    for w in sorted_weeks:
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
t1, t2 = st.tabs(["📊 SIRALAMA", "📅 MAÇ TAKVİMİ"])

with t1:
    df = get_stats()
    for i, r in df.iterrows():
        l_css = "leader" if i == 0 else ""
        form_html = "".join([f'<div class="form-dot {"win" if x=="G" else "loss" if x=="M" else "draw"}">{x}</div>' for x in r["form"][-5:]])
        
        st.markdown(f"""
        <div class="team-card {l_css}">
            <div>
                <span style="color:#94a3b8; font-weight:800; font-size:12px; letter-spacing:1px;">LİG SIRALAMASI: {i+1}</span>
                <h2 style="margin:0; color:#1e293b; letter-spacing:-1px; font-size:28px;">{r['Takım'].upper()}</h2>
                <div class="form-container">
                    {form_html}
                </div>
            </div>
            <div class="stats-right">
                <div style="text-align:right">
                    <div class="av-val">AVERAGE: {r['Av']}</div>
                    <div style="color:#94a3b8; font-size:12px; margin-top:4px;">{r['AG']} AG / {r['YG']} YG</div>
                </div>
                <div class="points-val">{r['P']}<span style="font-size:14px; color:#94a3b8; margin-left:5px;">PTS</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.dataframe(df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]], use_container_width=True, hide_index=True)

with t2:
    start = datetime.date(2026, 3, 22)
    for i in range(10):
        w = 11 + i
        dt = start + datetime.timedelta(days=7*i)
        h_t, a_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        
        done = w in st.session_state.matches
        m_data = st.session_state.matches.get(w)
        
        score_html = f"<b class='score-text'>{m_data['EvSkor']} - {m_data['DepSkor']}</b>" if done else '<div class="vs-circle">VS</div>'
        
        st.markdown(f"""
        <div class="modern-fixture">
            <div style="width:110px; border-right:2px solid #f8fafc;">
                <b class="fixture-week">{w}. HAFTA</b><br>
                <span class="fixture-date">{dt.strftime('%d.%m.%Y')}</span>
            </div>
            <div class="fixture-teams">
                <span style="width:120px; text-align:right;">{h_t.upper()}</span>
                {score_html}
                <span style="width:120px; text-align:left;">{a_t.upper()}</span>
            </div>
            <div style="width:100px; text-align:right; font-size:0.7rem; font-weight:700;">
                <span style="color:{'#22c55e' if done else '#cbd5e1'};">{'● BİTTİ' if done else '○ BEKLİYOR'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
