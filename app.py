import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Pro Lig", page_icon="⚽", layout="wide")

# --- GELİŞMİŞ CSS TASARIMI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
.stApp { background: #f8fafc; font-family: 'Inter', sans-serif; }

/* EFSANE BAŞLIK */
.league-title {
    font-size: clamp(30px, 7vw, 60px);
    font-weight: 900;
    text-align: center;
    padding: 30px 0;
    background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* MODERN TAKIM KARTI */
.team-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 20px 25px;
    border-radius: 20px;
    margin-bottom: 15px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    flex-wrap: wrap;
    gap: 15px;
    transition: transform 0.2s;
}
.team-card:hover { transform: translateY(-2px); border-color: #10b981; }
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }

.rank-badge { background: #f1f5f9; color: #64748b; padding: 2px 10px; border-radius: 8px; font-size: 11px; font-weight: 900; }
.leader-badge { background: #fbbf24; color: #92400e; }

.points-text { font-size: clamp(32px, 5vw, 42px); font-weight: 900; color: #059669; line-height: 1; }

/* FORM İKONLARI */
.form-box { display: flex; gap: 5px; margin-top: 8px; }
.f-dot {
    width: 24px; height: 24px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 900; color: white;
}
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* FİKSTÜR ROW */
.f-row {
    background: white; border-radius: 12px; padding: 12px 20px;
    margin-bottom: 8px; display: flex; align-items: center;
    justify-content: space-between; border: 1px solid #f1f5f9;
    flex-wrap: wrap; gap: 10px;
}
.f-score {
    background: #1e293b; color: white; padding: 5px 15px;
    border-radius: 10px; font-weight: 900; min-width: 70px; text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA ---
if 'matches' not in st.session_state: st.session_state.matches = {}

def update_stats():
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
            data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        elif m["EvSkor"] < m["DepSkor"]:
            data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
            data[m["Ev"]]["form"].append("M"); data[m["Dep"]]["form"].append("G")
        else:
            data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 📥 SKOR MERKEZİ")
    with st.form("match_input"):
        hafta = st.number_input("Hafta", 11, 20, 11)
        ev, dep = ("Prospor", "Billispor") if hafta % 2 == 0 else ("Billispor", "Prospor")
        st.caption(f"Maç: {ev} vs {dep}")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev}", 0, 100, 0)
        s2 = c2.number_input(f"{dep}", 0, 100, 0)
        if st.form_submit_button("ONAYLA"):
            st.session_state.matches[hafta] = {"Ev": ev, "EvSkor": s1, "Dep": dep, "DepSkor": s2}
            st.rerun()
    if st.button("Sıfırla"): st.session_state.matches = {}; st.rerun()

# --- ANA EKRAN ---
tab1, tab2 = st.tabs(["📊 SIRALAMA", "🗓️ FİKSTÜR"])

with tab1:
    df = update_stats()
    for idx, row in df.reset_index(drop=True).iterrows():
        is_leader = idx == 0
        card_class = "team-card leader-card" if is_leader else "team-card"
        badge_text = "LİDER 👑" if is_leader else f"RANK {idx+1}"
        badge_class = "rank-badge leader-badge" if is_leader else "rank-badge"
        
        form_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in row["form"][-5:]])
        
        st.markdown(f"""
        <div class="{card_class}">
            <div style="flex:1; min-width:180px;">
                <span class="{badge_class}">{badge_text}</span>
                <h2 style="margin:5px 0; color:#1e293b;">{row['Takım'].upper()}</h2>
                <div class="form-box">{form_html}</div>
            </div>
            <div style="display:flex; align-items:center; gap:25px;">
                <div style="text-align:right;">
                    <div style="font-weight:800; color:#64748b; font-size:13px;">AVERAGE: {row['Av']}</div>
                    <div style="font-size:11px; color:#94a3b8;">{row['AG']} AG / {row['YG']} YG</div>
                </div>
                <div class="points-text">{row['P']}<small style="font-size:12px; color:#94a3b8; margin-left:4px;">PTS</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### 📝 Detaylı Tablo")
    st.dataframe(df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]], use_container_width=True, hide_index=True)

with tab2:
    start_date = datetime.date(2026, 3, 22)
    for i in range(10):
        w = 11 + i
        curr_date = start_date + datetime.timedelta(days=7*i)
        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        match = st.session_state.matches.get(w)
        
        score_html = f'<div class="f-score">{match["EvSkor"]} - {match["DepSkor"]}</div>' if match else '<div style="color:#cbd5e1; font-weight:900; letter-spacing:2px;">VS</div>'
        status = f'<span style="color:#10b981; font-size:11px; font-weight:700;">✓ BİTTİ</span>' if match else '<span style="color:#94a3b8; font-size:11px;">⌚ BEKLİYOR</span>'
        
        st.markdown(f"""
        <div class="f-row">
            <div style="width:90px;">
                <b style="color:#059669; font-size:13px;">{w}. HAFTA</b><br>
                <small style="color:#94a3b8;">{curr_date.strftime('%d.%m')}</small>
            </div>
            <div style="flex:1; display:flex; justify-content:center; align-items:center; gap:20px;">
                <span style="font-weight:700; color:#1e293b; width:100px; text-align:right;">{ev_t}</span>
                {score_html}
                <span style="font-weight:700; color:#1e293b; width:100px; text-align:left;">{dep_t}</span>
            </div>
            <div style="width:80px; text-align:right;">{status}</div>
        </div>
        """, unsafe_allow_html=True)
