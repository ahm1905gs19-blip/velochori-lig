import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- CSS: SİHİRLİ DOKUNUŞLAR ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* ANA BAŞLIK - KORUNDU */
.league-title {
    font-size: clamp(30px, 7vw, 60px);
    font-weight: 900;
    text-align: center;
    padding: 25px 0;
    background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* SIRALAMA KARTLARI - KORUNDU */
.team-card {
    display: flex; justify-content: space-between; align-items: center;
    background: white; padding: 20px; border-radius: 20px;
    margin-bottom: 15px; border: 1px solid #e2e8f0;
    flex-wrap: wrap; gap: 15px;
}
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }

.f-dot {
    width: 24px; height: 24px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 900; color: white; margin-right: 4px;
}
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

/* DETAYLI TABLO - KORUNDU */
.custom-table {
    width: 100%; border-collapse: collapse; background: white;
    border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.custom-table th { background: #1e293b; color: white; padding: 12px; font-size: 12px; }
.custom-table td { padding: 12px; text-align: center; border-bottom: 1px solid #f1f5f9; font-weight: 600; }

/* --- YENİ NESİL FİKSTÜR (ŞAŞIRTAN KISIM) --- */
.stadium-card {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    border-radius: 25px;
    padding: 20px;
    margin-bottom: 15px;
    border: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    gap: 15px;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.stadium-card:hover { transform: scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.08); }

.match-header {
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px dashed #e2e8f0; padding-bottom: 10px;
}
.week-badge {
    background: #059669; color: white; padding: 4px 12px;
    border-radius: 50px; font-size: 12px; font-weight: 900;
}

.arena-floor {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 0;
}
.team-box {
    flex: 1; text-align: center;
}
.team-name { font-size: 1.1rem; font-weight: 900; color: #1e293b; text-transform: uppercase; letter-spacing: 1px; }
.home-vibe { border-bottom: 3px solid #10b981; display: inline-block; padding: 0 5px; }

.digital-scoreboard {
    background: #0f172a;
    color: #34d399;
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem;
    padding: 10px 25px;
    border-radius: 15px;
    box-shadow: inset 0 0 10px rgba(0,255,100,0.2);
    min-width: 120px;
    text-align: center;
    border: 2px solid #1e293b;
    display: flex; justify-content: center; align-items: center;
}
.vs-glow { color: #64748b; font-size: 0.8rem; font-family: 'Inter'; font-weight: 900; }

.match-footer {
    display: flex; justify-content: center; gap: 20px;
}
.status-pill {
    font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 8px;
    display: flex; align-items: center; gap: 5px;
}
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

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏟️ MAÇ YÖNETİMİ")
    with st.form("match_admin"):
        h_no = st.number_input("Hafta Seç", 11, 20, 11)
        ev, dep = ("Prospor", "Billispor") if h_no % 2 == 0 else ("Billispor", "Prospor")
        st.success(f"📌 {ev} evinde ağırlıyor.")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev}", 0, 100, 0)
        s2 = c2.number_input(f"{dep}", 0, 100, 0)
        if st.form_submit_button("⚽ SKORU İŞLE"):
            st.session_state.matches[h_no] = {"Ev": ev, "EvSkor": s1, "Dep": dep, "DepSkor": s2}
            st.rerun()

# --- TABLAR ---
tab1, tab2 = st.tabs(["📊 LİG TABLOSU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = idx == 0
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_l else ''}">
            <div style="flex:1;">
                <span style="background:{'#fbbf24' if is_l else '#f1f5f9'}; padding:2px 10px; border-radius:8px; font-size:11px; font-weight:900;">{ '🏆 LİDER' if is_l else f'RANK {idx+1}'}</span>
                <h2 style="margin:8px 0; color:#1e293b; letter-spacing:-1px;">{r['Takım'].upper()}</h2>
                <div style="display:flex;">{f_html}</div>
            </div>
            <div style="display:flex; align-items:center; gap:35px;">
                <div style="text-align:right;">
                    <div style="font-weight:800; color:#64748b; font-size:14px;">AV: {r['Av']}</div>
                    <div style="font-size:11px; color:#94a3b8;">{r['AG']}-{r['YG']}</div>
                </div>
                <div style="font-size:45px; font-weight:900; color:#10b981;">{r['P']}<small style="font-size:14px; color:#94a3b8; margin-left:5px;">P</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📈 PERFORMANS ANALİZİ")
    t_html = f"""
    <table class="custom-table">
        <thead>
            <tr><th>TAKIM</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr>
        </thead>
        <tbody>
            {"".join([f"<tr><td>{row['Takım']}</td><td>{row['O']}</td><td>{row['G']}</td><td>{row['B']}</td><td>{row['M']}</td><td>{row['AG']}</td><td>{row['YG']}</td><td>{row['Av']}</td><td style='color:#10b981; font-weight:900;'>{row['P']}</td></tr>" for _, row in df.iterrows()])}
        </tbody>
    </table>
    """
    st.markdown(t_html, unsafe_allow_html=True)

with tab2:
    start_date = datetime.date(2026, 3, 22)
    st.markdown("<br>", unsafe_allow_html=True)
    for i in range(10):
        w = 11 + i
        m_dt = start_date + datetime.timedelta(days=7*i)
        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        res = st.session_state.matches.get(w)
        
        # Dinamik İçerik
        score_display = f'<div>{res["EvSkor"]}</div><div style="font-size:1rem; color:#475569; margin:0 10px;">-</div><div>{res["DepSkor"]}</div>' if res else '<div class="vs-glow">VS</div>'
        status_pill = f'<div class="status-pill" style="background:#dcfce7; color:#166534;">● BİTTİ</div>' if res else f'<div class="status-pill" style="background:#f1f5f9; color:#64748b;">○ BEKLEYEN MAÇ</div>'
        
        st.markdown(f"""
        <div class="stadium-card">
            <div class="match-header">
                <span class="week-badge">{w}. HAFTA</span>
                <span style="font-size:12px; font-weight:700; color:#94a3b8;">{m_dt.strftime('%d %B %Y')}</span>
            </div>
            <div class="arena-floor">
                <div class="team-box">
                    <span class="team-name home-vibe">{ev_t}</span>
                    <div style="font-size:10px; color:#10b981; font-weight:800; margin-top:5px;">EV SAHİBİ</div>
                </div>
                <div class="digital-scoreboard">
                    {score_display}
                </div>
                <div class="team-box">
                    <span class="team-name">{dep_t}</span>
                    <div style="font-size:10px; color:#94a3b8; font-weight:800; margin-top:5px;">DEPLASMAN</div>
                </div>
            </div>
            <div class="match-footer">
                {status_pill}
            </div>
        </div>
        """, unsafe_allow_html=True)
